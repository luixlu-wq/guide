"""Stage 3 Topic 09A (Simple): one-step PyTorch training loop anatomy.

Data: tiny synthetic tensors (4 rows)
Rows: 4
Features: x, shape [4, 1]
Target: y = 2*x
Type: Regression bridge (simple)
"""

from __future__ import annotations

import torch


def pick_device() -> torch.device:
    # Select CUDA when available, otherwise run on CPU.
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Workflow:
# 1) Move tensors and model to selected device.
# 2) Run one forward pass.
# 3) Compute loss.
# 4) Backpropagate gradients.
# 5) Run one optimizer step and observe parameter change.
def main() -> None:
    device = pick_device()
    print("selected device:", device)

    # Step 1: create and move tensors to the same device.
    x = torch.tensor([[1.0], [2.0], [3.0], [4.0]], device=device)
    y = torch.tensor([[2.0], [4.0], [6.0], [8.0]], device=device)

    # Step 1 (model): model parameters must live on the same device.
    model = torch.nn.Linear(1, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = torch.nn.MSELoss()

    w_before = model.weight.item()
    b_before = model.bias.item()

    # Step 2: forward pass (prediction).
    pred = model(x)

    # Step 3: loss compares prediction vs target.
    loss = loss_fn(pred, y)
    print(f"loss before update: {loss.item():.6f}")

    # Step 4: backward pass computes gradients.
    optimizer.zero_grad()
    loss.backward()

    # Step 5: optimizer updates parameters.
    optimizer.step()

    w_after = model.weight.item()
    b_after = model.bias.item()

    print(f"w: {w_before:.4f} -> {w_after:.4f}")
    print(f"b: {b_before:.4f} -> {b_after:.4f}")
    print("Interpretation: one gradient step changed parameters to reduce loss.")


if __name__ == "__main__":
    main()
