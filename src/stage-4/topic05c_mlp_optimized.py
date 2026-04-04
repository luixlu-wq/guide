"""Stage 4 Section 5C: MLP optimized (BatchNorm + Dropout + Scheduler + AMP).

Data Source: sklearn.datasets.load_digits (local digits dataset)
Schema: 64 numeric features | target class 0..9
Preprocessing: method-chaining normalization + split discipline + dtype/device contract
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


def load_digits_df() -> tuple[pd.DataFrame, list[str]]:
    raw = load_digits(as_frame=True).frame
    feat = [c for c in raw.columns if c != "target"]
    ren = {c: f"px_{c}" for c in feat}
    df = (
        raw.rename(columns=ren)
        .pipe(
            lambda d: d.assign(
                **{c: d[c].astype("float32") / 16.0 for c in d.columns if c != "target"}
            )
        )
        .loc[:, [*ren.values(), "target"]]
    )
    return df, list(ren.values())


class OptimizedMLP(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(64, 256),
            torch.nn.BatchNorm1d(256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.25),
            torch.nn.Linear(256, 128),
            torch.nn.BatchNorm1d(128),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.20),
            torch.nn.Linear(128, 10),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def evaluate(model: OptimizedMLP, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    model.eval()
    preds = []
    trues = []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            out = model(xb).argmax(dim=1).cpu().numpy()
            preds.append(out)
            trues.append(yb.numpy())
    y_true = np.concatenate(trues)
    y_pred = np.concatenate(preds)
    return float(accuracy_score(y_true, y_pred)), float(f1_score(y_true, y_pred, average="macro"))


def hidden_dead_ratio(model: OptimizedMLP, loader: DataLoader, device: torch.device) -> float:
    # Approximate dead-neuron ratio by inspecting activations after first ReLU.
    model.eval()
    total = 0
    zeros = 0
    with torch.no_grad():
        for xb, _ in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            x = model.net[0](xb)
            x = model.net[1](x)
            x = model.net[2](x)  # first ReLU output
            zeros += int((x <= 0).sum().item())
            total += int(x.numel())
    return zeros / total if total else 0.0


# Workflow:
# 1) Build method-chained tabular ingestion and shape contract.
# 2) Train optimized MLP with BN + Dropout + StepLR.
# 3) Enable AMP on CUDA for throughput/memory efficiency.
# 4) Track failure-lab diagnostics and evidence schema metrics.
def main() -> None:
    torch.manual_seed(503)
    np.random.seed(503)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)
    run_id = f"stage4_topic05c_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    df, cols = load_digits_df()
    x = torch.tensor(df[cols].to_numpy(np.float32), dtype=torch.float32)
    y = torch.tensor(df["target"].to_numpy(np.int64), dtype=torch.long)
    print("Data declaration")
    print("source=sklearn.load_digits(as_frame=True)")
    print("rows=", len(df), "input_shape=(N,64) target_shape=(N,)")
    print("input_dtype=torch.float32 target_dtype=torch.long")

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=503, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=503, stratify=y_train_full
    )

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True, pin_memory=pin_memory)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False, pin_memory=pin_memory)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False, pin_memory=pin_memory)

    model = OptimizedMLP().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(4, scaled_int(12, quick_value=4) // 2), gamma=0.5)
    loss_fn = torch.nn.CrossEntropyLoss()
    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    epochs = scaled_int(30, quick_value=12)
    first_val_f1 = None
    last_val_f1 = None
    t0 = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=pin_memory)
            yb = yb.to(device, non_blocking=pin_memory)

            optimizer.zero_grad()
            with torch.amp.autocast(device_type="cuda", enabled=use_amp):
                logits = model(xb)
                loss = loss_fn(logits, yb)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

        scheduler.step()

        if epoch in (1, max(2, epochs // 3), max(3, (2 * epochs) // 3), epochs):
            train_acc, train_f1 = evaluate(model, train_loader, device)
            val_acc, val_f1 = evaluate(model, val_loader, device)
            if first_val_f1 is None:
                first_val_f1 = val_f1
            last_val_f1 = val_f1
            print(
                f"epoch={epoch:02d} lr={optimizer.param_groups[0]['lr']:.5f} "
                f"train_acc={train_acc:.4f} val_acc={val_acc:.4f} train_f1={train_f1:.4f} val_f1={val_f1:.4f}"
            )
    elapsed = time.perf_counter() - t0

    test_acc, test_f1 = evaluate(model, test_loader, device)
    dead_ratio = hidden_dead_ratio(model, val_loader, device)
    print(f"final_test_acc={test_acc:.4f} final_test_f1={test_f1:.4f} dead_relu_ratio={dead_ratio:.4f}")

    diagnosis = []
    if dead_ratio > 0.85:
        diagnosis.append("dying_relu_risk")
    if first_val_f1 is not None and last_val_f1 is not None and (last_val_f1 - first_val_f1) < 0.01:
        diagnosis.append("slow_convergence_or_vanishing_risk")
    if not diagnosis:
        diagnosis.append("healthy_optimized_training")
    print("Diagnosis:", ", ".join(diagnosis))

    max_mem_gb = 0.0
    if device.type == "cuda":
        max_mem_gb = torch.cuda.max_memory_allocated(device) / 1e9
        print(f"Max VRAM Allocated: {max_mem_gb:.3f} GB")

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)
    evidence = [
        {
            "run_id": run_id,
            "stage": "4",
            "topic_or_module": "section05_topic05c_mlp_optimized",
            "metric_name": "val_f1_macro",
            "before_value": float(first_val_f1 if first_val_f1 is not None else np.nan),
            "after_value": float(last_val_f1 if last_val_f1 is not None else np.nan),
            "delta": float(
                (last_val_f1 - first_val_f1)
                if (first_val_f1 is not None and last_val_f1 is not None)
                else np.nan
            ),
            "dataset_or_eval_set": "digits_val_split",
            "seed_or_config_id": "seed503",
            "decision": "promote" if test_f1 >= 0.95 else "hold",
            "diagnosis": "|".join(diagnosis),
            "device": device.type,
            "use_amp": use_amp,
            "max_vram_gb": max_mem_gb,
            "runtime_seconds": elapsed,
        }
    ]
    csv_path = out_dir / "topic05c_optimized_metrics.csv"
    json_path = out_dir / "topic05c_optimized_metrics.json"
    pd.DataFrame(evidence).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print("Interpretation: optimized MLP combines regularization + scheduling + hardware-aware execution.")


if __name__ == "__main__":
    main()

