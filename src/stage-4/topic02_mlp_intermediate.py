"""Stage 4 Topic 02: MLP classifier (intermediate).

Data: sklearn digits dataset (all classes 0-9)
Rows: 1,797
Input shape: [N, 64]
Target: class label 0..9, shape [N]
Split: fixed train/validation/test split
Type: multiclass classification
"""

from __future__ import annotations

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def accuracy(model: torch.nn.Module, loader: DataLoader) -> float:
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    return correct / total


def avg_loss(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module) -> float:
    model.eval()
    total = 0.0
    rows = 0
    with torch.no_grad():
        for xb, yb in loader:
            loss = loss_fn(model(xb), yb)
            total += float(loss.item()) * xb.size(0)
            rows += xb.size(0)
    return total / rows


# Workflow:
# 1) Load full digits dataset and create train/validation/test splits.
# 2) Train MLP with mini-batches and epoch-level logging.
# 3) Report train/validation/test accuracy and losses.
def main() -> None:
    torch.manual_seed(22)
    print(preset_banner())

    data = load_digits()
    x = torch.tensor(data.data, dtype=torch.float32) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=22, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=22, stratify=y_train_full
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    model = torch.nn.Sequential(
        torch.nn.Linear(64, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 10),
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    loss_fn = torch.nn.CrossEntropyLoss()

    epochs = scaled_int(30, quick_value=12)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            logits = model(xb)
            loss = loss_fn(logits, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, max(2, epochs // 3), max(3, (2 * epochs) // 3), epochs):
            train_acc = accuracy(model, train_loader)
            val_acc = accuracy(model, val_loader)
            train_loss = avg_loss(model, train_loader, loss_fn)
            val_loss = avg_loss(model, val_loader, loss_fn)
            print(
                f"epoch={epoch:02d} train_acc={train_acc:.4f} val_acc={val_acc:.4f} "
                f"train_loss={train_loss:.4f} val_loss={val_loss:.4f}"
            )

    test_acc = accuracy(model, test_loader)
    print(f"final_test_accuracy={test_acc:.4f}")
    print("Interpretation: this module adds split discipline and full metric tracking.")


if __name__ == "__main__":
    main()
