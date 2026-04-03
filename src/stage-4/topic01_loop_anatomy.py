"""Stage 4 Topic 01: training-loop anatomy (intermediate).

Data: synthetic regression generated in-script
Rows: 8,000
Input shape: [N, 2]
Target: y = 1.8*x1 - 0.7*x2 + 0.5 + noise, shape [N, 1]
Split: train/validation fixed by random seed
Type: regression
"""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset, random_split

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 8_000):
    generator = torch.Generator(device="cpu").manual_seed(7)
    x = torch.randn((n_rows, 2), generator=generator)
    noise = 0.15 * torch.randn((n_rows, 1), generator=generator)
    y = 1.8 * x[:, :1] - 0.7 * x[:, 1:] + 0.5 + noise
    return x, y


def evaluate(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module) -> float:
    model.eval()
    total_loss = 0.0
    total_rows = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb)
            loss = loss_fn(pred, yb)
            batch = xb.size(0)
            total_loss += float(loss.item()) * batch
            total_rows += batch
    return total_loss / total_rows


# Workflow:
# 1) Generate synthetic regression data and create fixed train/validation split.
# 2) Train a small MLP with mini-batches.
# 3) Report train/validation loss trend and learned behavior.
def main() -> None:
    torch.manual_seed(7)

    x, y = make_data(n_rows=scaled_int(8_000, quick_value=3_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic, rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    dataset = TensorDataset(x, y)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    split_gen = torch.Generator().manual_seed(7)
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=split_gen)

    train_loader = DataLoader(train_ds, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=256, shuffle=False)

    model = torch.nn.Sequential(
        torch.nn.Linear(2, 16),
        torch.nn.ReLU(),
        torch.nn.Linear(16, 1),
    )
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)

    epochs = scaled_int(25, quick_value=10)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            pred = model(xb)
            loss = loss_fn(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, 5, 10, 20, 25):
            train_loss = evaluate(model, train_loader, loss_fn)
            val_loss = evaluate(model, val_loader, loss_fn)
            print(f"epoch={epoch:02d} train_mse={train_loss:.4f} val_mse={val_loss:.4f}")

    print("Interpretation: decreasing validation loss indicates the 5-step loop is working.")


if __name__ == "__main__":
    main()
