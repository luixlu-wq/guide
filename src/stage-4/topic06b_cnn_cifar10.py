"""Stage 4 Section 6B: CNN baseline (CIFAR-10 preferred, digits fallback).

Data Source: torchvision CIFAR-10 (preferred) or sklearn digits (fallback)
Schema: image tensors [N, C, H, W] | target class labels
Preprocessing: normalization + shape contract checks + split discipline
Null Handling: dataset loaders return complete tensors
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


def try_load_cifar10_local():
    try:
        import torchvision
        import torchvision.transforms as T
    except Exception:
        return None
    data_root = Path(__file__).parent / "data"
    transform = T.Compose([T.ToTensor()])
    try:
        train_ds = torchvision.datasets.CIFAR10(
            root=str(data_root), train=True, transform=transform, download=False
        )
        test_ds = torchvision.datasets.CIFAR10(
            root=str(data_root), train=False, transform=transform, download=False
        )
    except Exception:
        return None
    return train_ds, test_ds


def load_digits_fallback():
    data = load_digits(as_frame=True).frame
    feature_cols = [c for c in data.columns if c != "target"]
    df = (
        data
        .assign(**{c: data[c].astype("float32") / 16.0 for c in feature_cols})
        .loc[:, [*feature_cols, "target"]]
    )
    x = torch.tensor(df[feature_cols].to_numpy(np.float32).reshape(-1, 1, 8, 8), dtype=torch.float32)
    y = torch.tensor(df["target"].to_numpy(np.int64), dtype=torch.long)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=606, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.2, random_state=606, stratify=y_train
    )
    return {
        "name": "digits_fallback",
        "train": TensorDataset(x_train, y_train),
        "val": TensorDataset(x_val, y_val),
        "test": TensorDataset(x_test, y_test),
        "in_channels": 1,
        "image_size": 8,
        "num_classes": 10,
    }


class BaselineCNN(torch.nn.Module):
    def __init__(self, in_channels: int, image_size: int, num_classes: int):
        super().__init__()
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
        )
        final_spatial = image_size // 4
        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(32 * final_spatial * final_spatial, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def evaluate(model: BaselineCNN, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    preds = []
    trues = []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            preds.append(model(xb).argmax(dim=1).cpu().numpy())
            trues.append(yb.numpy())
    return float(accuracy_score(np.concatenate(trues), np.concatenate(preds)))


# Workflow:
# 1) Prefer local CIFAR-10 if available; fallback to digits if not.
# 2) Train baseline CNN with shape-first checks and hardware profile.
# 3) Save baseline evidence artifact for reproducible comparison.
def main() -> None:
    torch.manual_seed(606)
    np.random.seed(606)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)
    run_id = f"stage4_topic06b_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    cifar_local = try_load_cifar10_local()
    if cifar_local is not None:
        train_ds, test_ds = cifar_local
        # Build a small validation split from training set indices.
        idx = np.arange(len(train_ds))
        rng = np.random.default_rng(606)
        rng.shuffle(idx)
        val_size = int(0.1 * len(idx))
        val_idx = idx[:val_size]
        tr_idx = idx[val_size:]

        x_tr = torch.stack([train_ds[i][0] for i in tr_idx]).float()
        y_tr = torch.tensor([train_ds[i][1] for i in tr_idx], dtype=torch.long)
        x_val = torch.stack([train_ds[i][0] for i in val_idx]).float()
        y_val = torch.tensor([train_ds[i][1] for i in val_idx], dtype=torch.long)
        x_te = torch.stack([test_ds[i][0] for i in range(len(test_ds))]).float()
        y_te = torch.tensor([test_ds[i][1] for i in range(len(test_ds))], dtype=torch.long)

        data_pack = {
            "name": "cifar10_local",
            "train": TensorDataset(x_tr, y_tr),
            "val": TensorDataset(x_val, y_val),
            "test": TensorDataset(x_te, y_te),
            "in_channels": 3,
            "image_size": 32,
            "num_classes": 10,
        }
    else:
        print("CIFAR-10 not available locally; using digits fallback dataset.")
        data_pack = load_digits_fallback()

    print("Data declaration")
    print("dataset=", data_pack["name"])
    print(
        "shape_contract=(N,C,H,W) with C=", data_pack["in_channels"],
        "H=W=", data_pack["image_size"], "classes=", data_pack["num_classes"]
    )

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(data_pack["train"], batch_size=64, shuffle=True, pin_memory=pin_memory, num_workers=0)
    val_loader = DataLoader(data_pack["val"], batch_size=256, shuffle=False, pin_memory=pin_memory, num_workers=0)
    test_loader = DataLoader(data_pack["test"], batch_size=256, shuffle=False, pin_memory=pin_memory, num_workers=0)

    model = BaselineCNN(
        in_channels=int(data_pack["in_channels"]),
        image_size=int(data_pack["image_size"]),
        num_classes=int(data_pack["num_classes"]),
    ).to(device)
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

    epochs = scaled_int(12, quick_value=5)
    t0 = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=pin_memory)
            yb = yb.to(device, non_blocking=pin_memory)
            optimizer.zero_grad()
            logits = model(xb)
            loss = loss_fn(logits, yb)
            loss.backward()
            optimizer.step()
        if epoch in (1, max(2, epochs // 2), epochs):
            val_acc = evaluate(model, val_loader, device)
            print(f"epoch={epoch:02d} val_acc={val_acc:.4f}")
    elapsed = time.perf_counter() - t0

    test_acc = evaluate(model, test_loader, device)
    print(f"final_test_acc={test_acc:.4f}")
    max_mem_gb = 0.0
    if device.type == "cuda":
        max_mem_gb = torch.cuda.max_memory_allocated(device) / 1e9
        print(f"Max VRAM Allocated: {max_mem_gb:.3f} GB")

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)
    record = [
        {
            "run_id": run_id,
            "stage": "4",
            "topic_or_module": "section06_topic06b_cnn_baseline",
            "metric_name": "test_accuracy",
            "before_value": np.nan,
            "after_value": test_acc,
            "delta": np.nan,
            "dataset_or_eval_set": data_pack["name"],
            "seed_or_config_id": "seed606",
            "decision": "promote" if test_acc >= 0.85 else "hold",
            "device": device.type,
            "max_vram_gb": max_mem_gb,
            "runtime_seconds": elapsed,
        }
    ]
    csv_path = out_dir / "topic06b_cnn_baseline_metrics.csv"
    json_path = out_dir / "topic06b_cnn_baseline_metrics.json"
    pd.DataFrame(record).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print("Interpretation: baseline CNN training follows shape-first and hardware-aware practices.")


if __name__ == "__main__":
    main()

