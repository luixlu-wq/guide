"""Stage 4 Topic 03: CNN classifier (intermediate).

Data: sklearn digits dataset
Rows: 1,797
Input shape: [N, 1, 8, 8]
Target: class label 0..9, shape [N]
Split: fixed train/validation/test split
Type: multiclass image classification
"""

from __future__ import annotations

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def print_hardware_profile(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        print(f"Device: {torch.cuda.get_device_name(0)}")
        torch.backends.cudnn.benchmark = True
    else:
        print("Device: CPU fallback path")


def accuracy(model: torch.nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            yb = yb.to(device, non_blocking=(device.type == "cuda"))
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    return correct / total


# Workflow:
# 1) Use fixed train/validation/test splits.
# 2) Train CNN with mini-batch loaders and epoch-level metrics.
# 3) Monitor generalization gap (train vs validation).
def main() -> None:
    torch.manual_seed(32)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)

    data = load_digits()
    x = torch.tensor(data.images, dtype=torch.float32).unsqueeze(1) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=32, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=32, stratify=y_train_full
    )

    pin_memory = device.type == "cuda"
    train_loader = DataLoader(
        TensorDataset(x_train, y_train), batch_size=64, shuffle=True, pin_memory=pin_memory
    )
    val_loader = DataLoader(
        TensorDataset(x_val, y_val), batch_size=256, shuffle=False, pin_memory=pin_memory
    )
    test_loader = DataLoader(
        TensorDataset(x_test, y_test), batch_size=256, shuffle=False, pin_memory=pin_memory
    )

    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 16, kernel_size=3, padding=1),
        torch.nn.BatchNorm2d(16),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(kernel_size=2),
        torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.Flatten(),
        torch.nn.Linear(32 * 4 * 4, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 10),
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = torch.nn.CrossEntropyLoss()

    epochs = scaled_int(25, quick_value=10)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=pin_memory)
            yb = yb.to(device, non_blocking=pin_memory)
            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, max(2, epochs // 3), max(3, (2 * epochs) // 3), epochs):
            train_acc = accuracy(model, train_loader, device)
            val_acc = accuracy(model, val_loader, device)
            print(f"epoch={epoch:02d} train_acc={train_acc:.4f} val_acc={val_acc:.4f}")

    test_acc = accuracy(model, test_loader, device)
    print(f"final_test_accuracy={test_acc:.4f}")
    if device.type == "cuda":
        print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated(device) / 1e9:.3f} GB")
    print("Interpretation: intermediate complexity adds stable batching and validation tracking.")


if __name__ == "__main__":
    main()
