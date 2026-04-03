"""Stage 4 Topic 06C: CUDA + AMP training path (advanced).

Data: sklearn digits dataset
Rows: 1,797
Input shape: [N, 64]
Target: class label 0..9, shape [N]
Split: fixed train/validation split
Type: multiclass classification with optional mixed precision
"""

from __future__ import annotations

import time

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def accuracy(model: torch.nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    return correct / total


# Workflow:
# 1) Select device and load digits dataset.
# 2) Train MLP with AMP enabled only on CUDA.
# 3) Report accuracy and runtime, with explicit CPU fallback messaging.
def main() -> None:
    torch.manual_seed(63)
    print(preset_banner())

    data = load_digits()
    x = torch.tensor(data.data, dtype=torch.float32) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits rows=1797 input_shape=(1797,64) target_shape=(1797,)")

    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.2, random_state=63, stratify=y
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=128, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.nn.Sequential(
        torch.nn.Linear(64, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 10),
    ).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()

    use_amp = device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    start = time.perf_counter()
    epochs = scaled_int(20, quick_value=8)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)
            optimizer.zero_grad()

            if use_amp:
                # Mixed precision forward/backward path for CUDA.
                with torch.amp.autocast(device_type="cuda", dtype=torch.float16):
                    logits = model(xb)
                    loss = loss_fn(logits, yb)
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                logits = model(xb)
                loss = loss_fn(logits, yb)
                loss.backward()
                optimizer.step()

        if epoch in (1, max(2, epochs // 2), epochs):
            val_acc = accuracy(model, val_loader, device)
            print(f"epoch={epoch:02d} val_acc={val_acc:.4f}")

    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    final_acc = accuracy(model, val_loader, device)
    print("selected_device=", device)
    print("amp_enabled=", use_amp)
    print(f"final_val_accuracy={final_acc:.4f}")
    print(f"elapsed_seconds={elapsed:.2f}")

    if not use_amp:
        print("CPU fallback path used. AMP was skipped because CUDA is unavailable.")


if __name__ == "__main__":
    main()
