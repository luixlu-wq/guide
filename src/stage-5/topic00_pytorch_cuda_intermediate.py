"""Stage 5 Topic 00: PyTorch + CUDA training loop (intermediate).

Data: synthetic binary classification dataset
Records/Samples: 1200
Input schema: features float[batch, 12], labels int[batch]
Output schema: train loss trajectory + device usage
Split/Eval policy: fixed 80/20 split
Type: device-aware training workflow
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def build_dataset(n: int = 1200) -> tuple[torch.Tensor, torch.Tensor]:
    """Create reproducible synthetic data for binary classification."""
    torch.manual_seed(11)
    x = torch.randn(n, 12)
    logits = 1.4 * x[:, 0] - 1.1 * x[:, 1] + 0.8 * x[:, 2] + 0.2 * torch.randn(n)
    y = (logits > 0).long()
    return x, y


# Workflow:
# 1) Build fixed synthetic dataset and split.
# 2) Move model and batches to selected device.
# 3) Train with standard forward/loss/backward/step loop.
def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x, y = build_dataset()

    split = int(0.8 * len(x))
    x_train, y_train = x[:split], y[:split]
    x_test, y_test = x[split:], y[split:]

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=128, shuffle=False)

    model = nn.Sequential(
        nn.Linear(12, 24),
        nn.ReLU(),
        nn.Linear(24, 2),
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-2)
    criterion = nn.CrossEntropyLoss()

    print("Data declaration")
    print("source=synthetic_binary_dataset")
    print(f"records={len(x)} train={len(x_train)} test={len(x_test)}")
    print("input_schema=features:float[batch,12],labels:int[batch]")
    print("output_schema=loss:float,accuracy:float")
    print(f"selected_device={device.type}")

    for epoch in range(1, 8):
        model.train()
        total_loss = 0.0
        total_count = 0
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)

            pred = model(xb)
            loss = criterion(pred, yb)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

            total_loss += float(loss.item()) * xb.size(0)
            total_count += xb.size(0)

        avg_loss = total_loss / max(1, total_count)
        print(f"epoch={epoch} train_loss={avg_loss:.4f}")

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for xb, yb in test_loader:
            xb = xb.to(device)
            yb = yb.to(device)
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)

    accuracy = correct / max(1, total)
    print(f"test_accuracy={accuracy:.4f}")
    print("Interpretation: same code pattern works on CPU or CUDA by switching device.")


if __name__ == "__main__":
    main()
