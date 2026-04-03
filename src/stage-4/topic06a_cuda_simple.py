"""Stage 4 Topic 06A: PyTorch device basics (simple).

Data: tiny synthetic regression data generated in-script
Rows: 4
Input shape: [4, 1]
Target: y = 2x + 1, shape [4, 1]
Split: none
Type: CPU/CUDA loop anatomy check
"""

from __future__ import annotations

import torch


# Workflow:
# 1) Pick device (cuda if available, else cpu).
# 2) Move tensors + model to same device.
# 3) Run one training step and print device checks.
def main() -> None:
    torch.manual_seed(61)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x = torch.tensor([[1.0], [2.0], [3.0], [4.0]], device=device)
    y = torch.tensor([[3.0], [5.0], [7.0], [9.0]], device=device)

    model = torch.nn.Linear(1, 1).to(device)
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    pred = model(x)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print("Data declaration")
    print("rows=4 input_shape=(4,1) target_shape=(4,1)")
    print("selected_device=", device)
    print("tensor_device=", x.device, "model_device=", next(model.parameters()).device)
    print(f"loss_after_one_step={loss.item():.6f}")
    if device.type == "cuda":
        print("CUDA path executed.")
    else:
        print("CPU fallback executed (CUDA unavailable).")


if __name__ == "__main__":
    main()
