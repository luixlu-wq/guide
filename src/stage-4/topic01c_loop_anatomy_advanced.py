"""Stage 4 Topic 01C: training-loop anatomy (advanced).

Data: synthetic regression generated in-script
Rows: 12,000
Input shape: [N, 6]
Target: nonlinear regression target, shape [N, 1]
Split: fixed train/validation split by random seed
Type: regression with gradient diagnostics
"""

from __future__ import annotations

import math

import torch
from torch.utils.data import DataLoader, TensorDataset, random_split

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 12_000):
    generator = torch.Generator(device="cpu").manual_seed(17)
    x = torch.randn((n_rows, 6), generator=generator)
    y = (
        1.2 * x[:, 0:1]
        - 0.8 * x[:, 1:2]
        + 0.6 * x[:, 2:3] * x[:, 3:4]
        + 0.3 * torch.sin(x[:, 4:5])
        - 0.2 * x[:, 5:6] ** 2
    )
    y += 0.12 * torch.randn((n_rows, 1), generator=generator)
    return x, y


def mse(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module) -> float:
    model.eval()
    total = 0.0
    rows = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb)
            batch = xb.size(0)
            total += float(loss_fn(pred, yb).item()) * batch
            rows += batch
    return total / rows


def gradient_l2_norm(model: torch.nn.Module) -> float:
    sq_sum = 0.0
    for p in model.parameters():
        if p.grad is not None:
            sq_sum += float(torch.sum(p.grad.detach() ** 2).item())
    return math.sqrt(sq_sum)


# Workflow:
# 1) Build harder synthetic regression data with nonlinear interactions.
# 2) Train deeper network while measuring gradient norms.
# 3) Apply gradient clipping + LR scheduler and report train/validation behavior.
def main() -> None:
    torch.manual_seed(17)

    x, y = make_data(n_rows=scaled_int(12_000, quick_value=4_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic, rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    dataset = TensorDataset(x, y)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    split_gen = torch.Generator().manual_seed(17)
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=split_gen)

    train_loader = DataLoader(train_ds, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=256, shuffle=False)

    model = torch.nn.Sequential(
        torch.nn.Linear(6, 48),
        torch.nn.ReLU(),
        torch.nn.Linear(48, 48),
        torch.nn.ReLU(),
        torch.nn.Linear(48, 1),
    )
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.5)

    epochs = scaled_int(35, quick_value=14)
    for epoch in range(1, epochs + 1):
        model.train()
        grad_norm_last = 0.0
        for xb, yb in train_loader:
            pred = model(xb)
            loss = loss_fn(pred, yb)
            optimizer.zero_grad()
            loss.backward()

            # Clip gradients to avoid unstable updates on harder objectives.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
            grad_norm_last = gradient_l2_norm(model)
            optimizer.step()

        scheduler.step()

        if epoch in (1, 5, 10, 20, 30, 35):
            train_loss = mse(model, train_loader, loss_fn)
            val_loss = mse(model, val_loader, loss_fn)
            lr = optimizer.param_groups[0]["lr"]
            print(
                f"epoch={epoch:02d} lr={lr:.5f} train_mse={train_loss:.4f} "
                f"val_mse={val_loss:.4f} grad_l2_last={grad_norm_last:.4f}"
            )

    print("Interpretation: clipping + scheduler stabilize the loop on harder data.")


if __name__ == "__main__":
    main()
