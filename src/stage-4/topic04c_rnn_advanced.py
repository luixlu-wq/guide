"""Stage 4 Topic 04C: RNN/GRU/LSTM comparison (advanced).

Data: synthetic sequence data generated in-script
Rows: 7,000
Input shape: [N, 20, 4]
Target: class label {0,1}, shape [N]
Split: fixed train/validation/test split
Type: sequence classification with architecture comparison
"""

from __future__ import annotations

import copy

import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 7_000):
    generator = torch.Generator(device="cpu").manual_seed(43)
    x = torch.randn((n_rows, 20, 4), generator=generator)
    long_term = x[:, :10, 0].mean(dim=1)
    short_term = x[:, 10:, 1].sum(dim=1)
    y = (long_term + 0.35 * short_term > 0.0).long()
    return x, y


class SequenceClassifier(torch.nn.Module):
    def __init__(self, kind: str) -> None:
        super().__init__()
        hidden = 32
        if kind == "rnn":
            self.core = torch.nn.RNN(input_size=4, hidden_size=hidden, batch_first=True)
        elif kind == "gru":
            self.core = torch.nn.GRU(input_size=4, hidden_size=hidden, batch_first=True)
        elif kind == "lstm":
            self.core = torch.nn.LSTM(input_size=4, hidden_size=hidden, batch_first=True)
        else:
            raise ValueError(f"Unsupported kind: {kind}")
        self.head = torch.nn.Linear(hidden, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.core(x)
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


def fit_and_select(kind: str, train_loader: DataLoader, val_loader: DataLoader) -> tuple[torch.nn.Module, float, float]:
    model = SequenceClassifier(kind)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()
    best_state = copy.deepcopy(model.state_dict())
    best_val = -1.0

    epochs = scaled_int(18, quick_value=8)
    for _ in range(epochs):
        model.train()
        for xb, yb in train_loader:
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()

            # Gradient clipping is added to stabilize recurrent training.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.5)
            optimizer.step()

        val_acc = accuracy(model, val_loader)
        if val_acc > best_val:
            best_val = val_acc
            best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    train_acc = accuracy(model, train_loader)
    return model, train_acc, best_val


# Workflow:
# 1) Keep one fixed dataset and split.
# 2) Train RNN, GRU, and LSTM under the same budget.
# 3) Compare architecture behavior using identical evaluation conditions.
def main() -> None:
    torch.manual_seed(43)

    x, y = make_data(n_rows=scaled_int(7_000, quick_value=2_500))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic sequence rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=43, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=43, stratify=y_train_full
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    for kind in ("rnn", "gru", "lstm"):
        model, train_acc, val_acc = fit_and_select(kind, train_loader, val_loader)
        test_acc = accuracy(model, test_loader)
        gap = train_acc - val_acc
        print(f"{kind.upper():4s} train={train_acc:.4f} val={val_acc:.4f} test={test_acc:.4f} train_val_gap={gap:.4f}")

    print("Interpretation: advanced complexity is architecture tradeoff + recurrent stability control.")


if __name__ == "__main__":
    main()
