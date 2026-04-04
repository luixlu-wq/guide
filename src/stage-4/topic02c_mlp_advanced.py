"""Stage 4 Topic 02C: MLP classifier (advanced).

Data: sklearn digits dataset (all classes 0-9)
Rows: 1,797
Input shape: [N, 64]
Target: class label 0..9, shape [N]
Split: fixed train/validation/test split
Type: multiclass classification with baseline vs improved comparison
"""

from __future__ import annotations

import copy

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


def make_splits(seed: int = 23):
    data = load_digits()
    x = torch.tensor(data.data, dtype=torch.float32) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=seed, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=seed, stratify=y_train_full
    )
    return x_train, y_train, x_val, y_val, x_test, y_test


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


def train_model(
    model: torch.nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    *,
    epochs: int,
    lr: float,
    weight_decay: float,
    device: torch.device,
) -> tuple[torch.nn.Module, float, float]:
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    loss_fn = torch.nn.CrossEntropyLoss()
    best_state = copy.deepcopy(model.state_dict())
    best_val = -1.0

    for _ in range(epochs):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device, non_blocking=(device.type == "cuda"))
            yb = yb.to(device, non_blocking=(device.type == "cuda"))
            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        val_acc = accuracy(model, val_loader, device)
        if val_acc > best_val:
            best_val = val_acc
            best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    train_acc = accuracy(model, train_loader, device)
    return model, train_acc, best_val


# Workflow:
# 1) Keep one fixed split and compare a baseline MLP vs regularized MLP.
# 2) Apply dropout + weight decay as the controlled improvement.
# 3) Report train/validation/test deltas.
def main() -> None:
    torch.manual_seed(23)
    device = pick_device()
    print(preset_banner())
    print_hardware_profile(device)

    x_train, y_train, x_val, y_val, x_test, y_test = make_splits()

    print("Data declaration")
    print("source=sklearn.load_digits")
    print("rows=1797 input_shape=(1797,64) target_shape=(1797,)")
    print("split=train:1150, val:287, test:360")

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

    baseline = torch.nn.Sequential(
        torch.nn.Linear(64, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10),
    )

    improved = torch.nn.Sequential(
        torch.nn.Linear(64, 128),
        torch.nn.ReLU(),
        torch.nn.Dropout(p=0.25),
        torch.nn.Linear(128, 64),
        torch.nn.ReLU(),
        torch.nn.Dropout(p=0.20),
        torch.nn.Linear(64, 10),
    )

    epochs = scaled_int(30, quick_value=12)
    baseline, b_train, b_val = train_model(
        baseline, train_loader, val_loader, epochs=epochs, lr=0.004, weight_decay=0.0, device=device
    )
    improved, i_train, i_val = train_model(
        improved, train_loader, val_loader, epochs=epochs, lr=0.004, weight_decay=1e-4, device=device
    )

    b_test = accuracy(baseline, test_loader, device)
    i_test = accuracy(improved, test_loader, device)

    print(f"baseline: train={b_train:.4f} val={b_val:.4f} test={b_test:.4f}")
    print(f"improved: train={i_train:.4f} val={i_val:.4f} test={i_test:.4f}")
    print(
        f"delta_test={i_test - b_test:+.4f}, "
        f"delta_train_val_gap={(i_train - i_val) - (b_train - b_val):+.4f}"
    )
    if device.type == "cuda":
        print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated(device) / 1e9:.3f} GB")
    print("Interpretation: advanced complexity is controlled architecture/regularization tradeoff.")


if __name__ == "__main__":
    main()
