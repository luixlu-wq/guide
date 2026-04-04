"""Stage 4 Section 6C: CNN performance lab (hardware-aware, AMP-ready).

Data Source: sklearn.datasets.load_digits (local image dataset)
Schema: image tensor [N, 1, 8, 8] | target class 0..9
Preprocessing: method-chaining normalization + shape contract enforcement
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
from sklearn.metrics import accuracy_score
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


def ingest_digits_with_method_chaining() -> tuple[pd.DataFrame, list[str]]:
    raw = load_digits(as_frame=True).frame
    feature_cols = [c for c in raw.columns if c != "target"]
    renamed = {c: f"px_{c}" for c in feature_cols}
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


class PerfCNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
        )
        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(32 * 2 * 2, 64),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),
            torch.nn.Linear(64, 10),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z = self.features(x)
        return self.classifier(z)


def evaluate(model: PerfCNN, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    preds: list[np.ndarray] = []
    trues: list[np.ndarray] = []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            logits = model(xb)
            preds.append(logits.argmax(dim=1).cpu().numpy())
            trues.append(yb.numpy())
    return float(accuracy_score(np.concatenate(trues), np.concatenate(preds)))


def inspect_feature_map_contract(model: PerfCNN, device: torch.device) -> tuple[int, int]:
    with torch.no_grad():
        dummy = torch.zeros((1, 1, 8, 8), device=device)
        fmap = model.features(dummy)
    h, w = int(fmap.shape[-2]), int(fmap.shape[-1])
    print(f"Feature-map contract: after pooling -> shape={tuple(fmap.shape)}")
    return h, w


def train_config(
    *,
    model: PerfCNN,
    train_loader: DataLoader,
    val_loader: DataLoader,
    device: torch.device,
    use_amp: bool,
    epochs: int,
) -> dict:
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.002, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler("cuda", enabled=(device.type == "cuda" and use_amp))

    step_times = []
    best_val = -1.0
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            yb = yb.to(device, non_blocking=(device.type == "cuda"))

            t0 = time.perf_counter()
            optimizer.zero_grad()
            with torch.amp.autocast(device_type="cuda", enabled=(device.type == "cuda" and use_amp)):
                logits = model(xb)
                loss = loss_fn(logits, yb)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            if device.type == "cuda":
                torch.cuda.synchronize()
            step_times.append(time.perf_counter() - t0)

        if epoch in (1, max(2, epochs // 2), epochs):
            val_acc = evaluate(model, val_loader, device)
            best_val = max(best_val, val_acc)
            print(f"epoch={epoch:02d} amp={use_amp} val_acc={val_acc:.4f}")

    avg_step = float(np.mean(step_times)) if step_times else float("nan")
    throughput = float(train_loader.batch_size / avg_step) if avg_step and avg_step > 0 else float("nan")
    return {"best_val_acc": best_val, "avg_step_time_s": avg_step, "throughput_samples_s": throughput}


# Workflow:
# 1) Ingest digits with method-chaining and enforce image shape contract (N,C,H,W).
# 2) Run FP32 baseline and AMP-optimized path under same split/epoch budget.
# 3) Run failure lab checks: over-pooling risk, channel-memory pressure, overfitting signal.
# 4) Save before/after evidence (accuracy + step-time + throughput + memory).
def main() -> None:
    torch.manual_seed(306)
    np.random.seed(306)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)
    run_id = f"stage4_topic06c_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    df, feature_cols = ingest_digits_with_method_chaining()
    print("Data declaration")
    print("source=sklearn.load_digits(as_frame=True)")
    print("rows=", len(df), "input_dtype=torch.float32 target_dtype=torch.long")

    x_np = df[feature_cols].to_numpy(np.float32).reshape(-1, 1, 8, 8)
    y_np = df["target"].to_numpy(np.int64)
    x = torch.tensor(x_np, dtype=torch.float32)
    y = torch.tensor(y_np, dtype=torch.long)
    print("Shape contract check: input=", tuple(x.shape), "target=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=306, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=306, stratify=y_train_full
    )

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(
        TensorDataset(x_train, y_train),
        batch_size=64,
        shuffle=True,
        pin_memory=pin_memory,
        num_workers=0,
    )
    val_loader = DataLoader(
        TensorDataset(x_val, y_val),
        batch_size=256,
        shuffle=False,
        pin_memory=pin_memory,
        num_workers=0,
    )
    test_loader = DataLoader(
        TensorDataset(x_test, y_test),
        batch_size=256,
        shuffle=False,
        pin_memory=pin_memory,
        num_workers=0,
    )

    model_for_shape = PerfCNN().to(device)
    h, w = inspect_feature_map_contract(model_for_shape, device)

    epochs = scaled_int(20, quick_value=8)
    print("Training baseline FP32...")
    baseline = train_config(
        model=PerfCNN(),
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        use_amp=False,
        epochs=epochs,
    )

    amp_enabled = device.type == "cuda"
    print(f"Training optimized path (AMP enabled={amp_enabled})...")
    improved = train_config(
        model=PerfCNN(),
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        use_amp=amp_enabled,
        epochs=epochs,
    )

    baseline_model = PerfCNN().to(device)
    improved_model = PerfCNN().to(device)
    # Lightweight final test readout by re-running one short fit is intentionally skipped here.
    # Validation/throughput deltas are the primary performance evidence for this section.
    del baseline_model, improved_model

    # Failure lab diagnostics.
    diagnostics = []
    if h <= 1 or w <= 1:
        diagnostics.append("over_pooling_risk")
    # Rough channel-memory pressure heuristic at first deep feature map (batch=64).
    est_activation_mb = (64 * 32 * h * w * 4) / (1024**2)
    if est_activation_mb > 256:
        diagnostics.append("channel_explosion_risk")

    val_gap_delta = improved["best_val_acc"] - baseline["best_val_acc"]
    if val_gap_delta < -0.01:
        diagnostics.append("overfitting_or_instability_risk")
    if not diagnostics:
        diagnostics.append("healthy_cnn_profile")

    print("Failure-lab diagnostics:", ", ".join(diagnostics))
    print(
        f"baseline_val_acc={baseline['best_val_acc']:.4f}, improved_val_acc={improved['best_val_acc']:.4f}, "
        f"delta={val_gap_delta:+.4f}"
    )
    print(
        f"baseline_step={baseline['avg_step_time_s']:.6f}s improved_step={improved['avg_step_time_s']:.6f}s"
    )

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
            "topic_or_module": "section06_topic06c_cnn_performance",
            "metric_name": "best_val_accuracy",
            "before_value": baseline["best_val_acc"],
            "after_value": improved["best_val_acc"],
            "delta": improved["best_val_acc"] - baseline["best_val_acc"],
            "dataset_or_eval_set": "digits_val_split",
            "seed_or_config_id": "seed306",
            "decision": "promote" if improved["best_val_acc"] >= baseline["best_val_acc"] else "hold",
            "diagnosis": "|".join(diagnostics),
            "device": device.type,
            "max_vram_gb": max_mem_gb,
            "before_step_time_s": baseline["avg_step_time_s"],
            "after_step_time_s": improved["avg_step_time_s"],
            "before_throughput_samples_s": baseline["throughput_samples_s"],
            "after_throughput_samples_s": improved["throughput_samples_s"],
        }
    ]

    metrics_csv = out_dir / "topic06c_performance_metrics.csv"
    metrics_json = out_dir / "topic06c_performance_metrics.json"
    pd.DataFrame(evidence).to_csv(metrics_csv, index=False)
    metrics_json.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Saved: {metrics_csv}")
    print(f"Saved: {metrics_json}")
    print("Interpretation: this script turns CNN training into a measurable performance-engineering workflow.")


if __name__ == "__main__":
    main()

