"""Stage 4 Topic 04: GRU sequence classifier (intermediate).

Data: synthetic sequence data generated in-script
Rows: 5,000
Input shape: [N, 12, 3]
Target: class label {0,1}, shape [N]
Split: fixed train/validation/test split
Type: sequence classification
"""

from __future__ import annotations

import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 5_000):
    generator = torch.Generator(device="cpu").manual_seed(42)
    x = torch.randn((n_rows, 12, 3), generator=generator)
    signal = x[:, :, 0].sum(dim=1) + 0.5 * x[:, :, 1].mean(dim=1)
    y = (signal > 0.0).long()
    return x, y


class GRUClassifier(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.gru = torch.nn.GRU(input_size=3, hidden_size=24, batch_first=True)
        self.head = torch.nn.Linear(24, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.gru(x)
        return self.head(out[:, -1, :])


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


# Workflow:
# 1) Generate a harder sequence dataset with 3 features per time step.
# 2) Train GRU with mini-batches and validation checks.
# 3) Report train/validation/test accuracy.
def main() -> None:
    torch.manual_seed(42)

    x, y = make_data(n_rows=scaled_int(5_000, quick_value=2_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic sequence rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=42, stratify=y_train_full
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    model = GRUClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.004)
    loss_fn = torch.nn.CrossEntropyLoss()

    epochs = scaled_int(20, quick_value=8)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, max(2, epochs // 2), epochs):
            train_acc = accuracy(model, train_loader)
            val_acc = accuracy(model, val_loader)
            print(f"epoch={epoch:02d} train_acc={train_acc:.4f} val_acc={val_acc:.4f}")

    test_acc = accuracy(model, test_loader)
    print(f"final_test_accuracy={test_acc:.4f}")
    print("Interpretation: intermediate complexity adds stronger sequence features and validation discipline.")


if __name__ == "__main__":
    main()
