"""Stage 5 Topic 00C: PyTorch + CUDA mixed precision (advanced).

Data: synthetic regression dataset
Records/Samples: 4000
Input schema: features float[batch, 20], target float[batch, 1]
Output schema: loss trend + precision mode metadata
Split/Eval policy: fixed 85/15 split
Type: advanced device-aware training
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def build_dataset(n: int = 4000) -> tuple[torch.Tensor, torch.Tensor]:
    """Create reproducible synthetic regression data."""
    torch.manual_seed(23)
    x = torch.randn(n, 20)
    w = torch.tensor(
        [1.2, -0.7, 0.9, 0.0, -1.1, 0.3, 0.2, -0.4, 0.5, 0.0, 0.6, -0.2, 0.1, 0.8, -0.3, 0.0, 0.4, -0.5, 0.7, -0.6]
    )
    y = (x @ w + 0.1 * torch.randn(n)).unsqueeze(1)
    return x, y


# Workflow:
# 1) Build fixed synthetic data and select device.
# 2) Train with AMP on CUDA; fallback to full precision on CPU.
# 3) Compare train/validation losses.
def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x, y = build_dataset()
    split = int(0.85 * len(x))

    train_ds = TensorDataset(x[:split], y[:split])
    val_ds = TensorDataset(x[split:], y[split:])
    train_loader = DataLoader(train_ds, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=256, shuffle=False)

    model = nn.Sequential(
        nn.Linear(20, 64),
        nn.GELU(),
        nn.Linear(64, 64),
        nn.GELU(),
        nn.Linear(64, 1),
    ).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-2)
    criterion = nn.MSELoss()

    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler(device="cuda", enabled=use_amp)

    print("Data declaration")
    print("source=synthetic_regression_dataset")
    print(f"records={len(x)} train={len(train_ds)} val={len(val_ds)}")
    print("input_schema=features:float[batch,20],target:float[batch,1]")
    print("output_schema=train_loss,val_loss")
    print(f"selected_device={device.type}")
    print(f"amp_enabled={use_amp}")

    for epoch in range(1, 7):
        model.train()
        total = 0.0
        count = 0
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)

            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast(device_type="cuda", enabled=use_amp):
                pred = model(xb)
                loss = criterion(pred, yb)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total += float(loss.item()) * xb.size(0)
            count += xb.size(0)

        train_loss = total / max(1, count)

        model.eval()
        val_total = 0.0
        val_count = 0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb = xb.to(device)
                yb = yb.to(device)
                pred = model(xb)
                loss = criterion(pred, yb)
                val_total += float(loss.item()) * xb.size(0)
                val_count += xb.size(0)
        val_loss = val_total / max(1, val_count)
        print(f"epoch={epoch} train_loss={train_loss:.5f} val_loss={val_loss:.5f}")

    print("Interpretation: advanced PyTorch/CUDA workflows can use mixed precision on GPU.")


if __name__ == "__main__":
    main()
