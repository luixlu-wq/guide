"""Stage 4 Section 5B: PyTorch MLP baseline (industry-style, shape-first).

Data Source: sklearn.datasets.load_digits (MNIST-style local digits dataset)
Schema: 64 numeric pixel features (0..16) | target class 0..9
Preprocessing: method-chaining normalization + dtype contract + train/val/test split
Null Handling: none (source dataset is complete)
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import time

import numpy as np
import pandas as pd
import torch
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def print_hardware_profile(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        torch.backends.cudnn.benchmark = True
        print(f"Device: {torch.cuda.get_device_name(0)}")
    else:
        print("Device: CPU fallback path")


def load_digits_with_method_chaining() -> tuple[pd.DataFrame, list[str]]:
    raw = load_digits(as_frame=True).frame
    feature_cols = [c for c in raw.columns if c != "target"]
    renamed = {c: f"px_{c}" for c in feature_cols}

    # Method-chaining ingestion (McKinney/Harrison style):
    # rename -> normalize -> select stable schema.
    df = (
        raw.rename(columns=renamed)
        .pipe(
            lambda d: d.assign(
                **{c: d[c].astype("float32") / 16.0 for c in d.columns if c != "target"}
            )
        )
        .loc[:, [*renamed.values(), "target"]]
    )
    return df, list(renamed.values())


class MLPBaseline(torch.nn.Module):
    def __init__(self, in_dim: int = 64, hidden_dim: int = 128, out_dim: int = 10):
        super().__init__()
        self.fc1 = torch.nn.Linear(in_dim, hidden_dim)
        self.act1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(hidden_dim, out_dim)

    def forward(self, x: torch.Tensor, return_hidden: bool = False):
        h = self.act1(self.fc1(x))
        out = self.fc2(h)
        if return_hidden:
            return out, h
        return out


def evaluate(model: MLPBaseline, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    model.eval()
    y_true: list[np.ndarray] = []
    y_pred: list[np.ndarray] = []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            logits = model(xb)
            pred = logits.argmax(dim=1).cpu().numpy()
            y_pred.append(pred)
            y_true.append(yb.numpy())
    y_true_np = np.concatenate(y_true)
    y_pred_np = np.concatenate(y_pred)
    return float(accuracy_score(y_true_np, y_pred_np)), float(
        f1_score(y_true_np, y_pred_np, average="macro")
    )


def mean_grad_norm(model: MLPBaseline) -> float:
    vals = []
    for p in model.parameters():
        if p.grad is not None:
            vals.append(float(torch.linalg.norm(p.grad.detach()).item()))
    return float(np.mean(vals)) if vals else 0.0


def relu_dead_ratio(model: MLPBaseline, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    total = 0
    zeros = 0
    with torch.no_grad():
        for xb, _ in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            _, hidden = model(xb, return_hidden=True)
            zeros += int((hidden <= 0).sum().item())
            total += int(hidden.numel())
    return zeros / total if total else 0.0


# Workflow:
# 1) Ingest local digits data with method chaining and explicit dtype contract.
# 2) Enforce shape-first checks: X:[B,64] -> hidden:[B,H] -> logits:[B,10].
# 3) Train MLP and track accuracy/F1 + gradient norms.
# 4) Run failure lab checks (vanishing gradient, dying ReLU, shape mismatch guard).
# 5) Save evidence artifact with run_id, before/after, delta.
def main() -> None:
    torch.manual_seed(205)
    np.random.seed(205)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)

    run_id = f"stage4_topic05b_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    df, feature_cols = load_digits_with_method_chaining()
    feature_summary = (
        df[feature_cols]
        .describe()
        .T[["mean", "std", "min", "max"]]
        .head(8)
    )
    print("Data declaration")
    print("source=sklearn.load_digits(as_frame=True) | rows=", len(df))
    print("input_dtype=torch.float32 target_dtype=torch.long")
    print("input_shape=(N,64) target_shape=(N,)")
    print("--- Method-Chaining Summary (first 8 features) ---")
    print(feature_summary.to_string(float_format=lambda x: f"{x:.3f}"))

    x = torch.tensor(df[feature_cols].to_numpy(np.float32), dtype=torch.float32)
    y = torch.tensor(df["target"].to_numpy(np.int64), dtype=torch.long)

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=205, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=205, stratify=y_train_full
    )

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(
        TensorDataset(x_train, y_train),
        batch_size=64,
        shuffle=True,
        pin_memory=pin_memory,
    )
    val_loader = DataLoader(
        TensorDataset(x_val, y_val),
        batch_size=256,
        shuffle=False,
        pin_memory=pin_memory,
    )
    test_loader = DataLoader(
        TensorDataset(x_test, y_test),
        batch_size=256,
        shuffle=False,
        pin_memory=pin_memory,
    )

    model = MLPBaseline().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()

    # Shape-first contract verification on first batch.
    xb0, yb0 = next(iter(train_loader))
    xb0 = xb0.to(device, non_blocking=pin_memory)
    logits0, hidden0 = model(xb0, return_hidden=True)
    print("Shape contract check")
    print(
        f"X={tuple(xb0.shape)} hidden={tuple(hidden0.shape)} logits={tuple(logits0.shape)} "
        f"target={tuple(yb0.shape)}"
    )

    epochs = scaled_int(30, quick_value=12)
    first_val_f1 = None
    last_val_f1 = None
    grad_trace: list[float] = []
    t0 = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=pin_memory)
            yb = yb.to(device, non_blocking=pin_memory)

            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            grad_trace.append(mean_grad_norm(model))
            optimizer.step()

        if epoch in (1, max(2, epochs // 3), max(3, (2 * epochs) // 3), epochs):
            train_acc, train_f1 = evaluate(model, train_loader, device)
            val_acc, val_f1 = evaluate(model, val_loader, device)
            if first_val_f1 is None:
                first_val_f1 = val_f1
            last_val_f1 = val_f1
            print(
                f"epoch={epoch:02d} train_acc={train_acc:.4f} val_acc={val_acc:.4f} "
                f"train_f1={train_f1:.4f} val_f1={val_f1:.4f}"
            )
    elapsed = time.perf_counter() - t0

    test_acc, test_f1 = evaluate(model, test_loader, device)
    print(f"final_test_acc={test_acc:.4f} final_test_f1={test_f1:.4f}")

    # Failure lab diagnostics.
    dead_ratio = relu_dead_ratio(model, val_loader, device)
    mean_grad = float(np.mean(grad_trace)) if grad_trace else 0.0
    diagnosis = []
    if mean_grad < 1e-4:
        diagnosis.append("vanishing_gradient_risk")
    if dead_ratio > 0.80:
        diagnosis.append("dying_relu_risk")
    if not diagnosis:
        diagnosis.append("healthy_training_signal")
    print(f"Failure-lab diagnostics: mean_grad_norm={mean_grad:.6f} dead_relu_ratio={dead_ratio:.4f}")
    print("Diagnosis:", ", ".join(diagnosis))

    if device.type == "cuda":
        print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated(device) / 1e9:.3f} GB")

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)

    evidence = [
        {
            "run_id": run_id,
            "stage": "4",
            "topic_or_module": "section05_topic05b_mlp_pytorch",
            "metric_name": "val_f1_macro",
            "before_value": float(first_val_f1 if first_val_f1 is not None else np.nan),
            "after_value": float(last_val_f1 if last_val_f1 is not None else np.nan),
            "delta": float(
                (last_val_f1 - first_val_f1)
                if (first_val_f1 is not None and last_val_f1 is not None)
                else np.nan
            ),
            "dataset_or_eval_set": "digits_val_split",
            "seed_or_config_id": "seed205",
            "decision": "promote" if test_f1 >= 0.92 else "hold",
            "diagnosis": "|".join(diagnosis),
            "runtime_seconds": elapsed,
            "device": device.type,
        }
    ]
    evidence_csv = out_dir / "topic05b_before_after_metrics.csv"
    evidence_json = out_dir / "topic05b_before_after_metrics.json"
    pd.DataFrame(evidence).to_csv(evidence_csv, index=False)
    evidence_json.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Saved: {evidence_csv}")
    print(f"Saved: {evidence_json}")
    print("Interpretation: this is a shape-first PyTorch MLP baseline with industry diagnostics.")


if __name__ == "__main__":
    main()

