"""Stage 4 Topic 01A: training-loop anatomy (simple).

Data: tiny synthetic regression data generated in-script
Rows: 4
Input shape: [4, 1]
Target: y = 2x + 1, shape [4, 1]
Split: no split (single mini-example)
Type: regression loop anatomy
"""

from __future__ import annotations

import torch


# Workflow:
# 1) Build tiny tensor data so each value is easy to inspect.
# 2) Run one forward pass, one loss computation, one backward pass.
# 3) Run one optimizer step and show parameter movement.
def main() -> None:
    torch.manual_seed(42)

    x = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
    y = torch.tensor([[3.0], [5.0], [7.0], [9.0]])

    print("Data declaration")
    print("rows=4, input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    model = torch.nn.Linear(1, 1)
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    w_before = float(model.weight.item())
    b_before = float(model.bias.item())

    pred = model(x)
    loss = loss_fn(pred, y)

    optimizer.zero_grad()
    loss.backward()

    grad_w = float(model.weight.grad.item())
    grad_b = float(model.bias.grad.item())

    optimizer.step()

    w_after = float(model.weight.item())
    b_after = float(model.bias.item())

    print(f"loss_before_step={loss.item():.6f}")
    print(f"grad_w={grad_w:.6f}, grad_b={grad_b:.6f}")
    print(f"weight: {w_before:.6f} -> {w_after:.6f}")
    print(f"bias  : {b_before:.6f} -> {b_after:.6f}")
    print("Interpretation: backward() computed gradients, and step() moved parameters.")


if __name__ == "__main__":
    main()
