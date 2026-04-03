"""Stage 4 Topic 03C: CNN classifier (advanced).

Data: sklearn digits dataset
Rows: 1,797
Input shape: [N, 1, 8, 8]
Target: class label 0..9, shape [N]
Split: fixed train/validation/test split
Type: multiclass image classification with controlled augmentation
"""

from __future__ import annotations

import copy

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def build_model() -> torch.nn.Module:
    return torch.nn.Sequential(
        torch.nn.Conv2d(1, 16, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(kernel_size=2),
        torch.nn.Dropout2d(p=0.15),
        torch.nn.Flatten(),
        torch.nn.Linear(32 * 4 * 4, 64),
        torch.nn.ReLU(),
        torch.nn.Dropout(p=0.25),
        torch.nn.Linear(64, 10),
    )


def accuracy(model: torch.nn.Module, loader: DataLoader) -> float:
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    return correct / total


def train_and_select(
    model: torch.nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    *,
    augment_noise_std: float,
) -> torch.nn.Module:
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.002, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()
    best_state = copy.deepcopy(model.state_dict())
    best_val = -1.0

    epochs = scaled_int(25, quick_value=10)
    for _ in range(epochs):
        model.train()
        for xb, yb in train_loader:
            # Controlled augmentation path for advanced comparison.
            if augment_noise_std > 0:
                xb = xb + augment_noise_std * torch.randn_like(xb)
                xb = xb.clamp(0.0, 1.0)

            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        val_acc = accuracy(model, val_loader)
        if val_acc > best_val:
            best_val = val_acc
            best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    return model


# Workflow:
# 1) Keep one fixed split.
# 2) Train baseline CNN and augmented CNN under same budget.
# 3) Compare test accuracy and train/validation gap.
def main() -> None:
    torch.manual_seed(33)
    print(preset_banner())

    data = load_digits()
    x = torch.tensor(data.images, dtype=torch.float32).unsqueeze(1) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits, rows=1797, input_shape=(1797,1,8,8), target_shape=(1797,)")

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=33, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=33, stratify=y_train_full
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    baseline = train_and_select(build_model(), train_loader, val_loader, augment_noise_std=0.0)
    improved = train_and_select(build_model(), train_loader, val_loader, augment_noise_std=0.08)

    b_train = accuracy(baseline, train_loader)
    b_val = accuracy(baseline, val_loader)
    b_test = accuracy(baseline, test_loader)

    i_train = accuracy(improved, train_loader)
    i_val = accuracy(improved, val_loader)
    i_test = accuracy(improved, test_loader)

    print(f"baseline: train={b_train:.4f} val={b_val:.4f} test={b_test:.4f}")
    print(f"improved(noise): train={i_train:.4f} val={i_val:.4f} test={i_test:.4f}")
    print(f"delta_test={i_test - b_test:+.4f}")
    print("Interpretation: advanced complexity is controlled regularization/augmentation tradeoff.")


if __name__ == "__main__":
    main()
