"""Stage 3 Topic 09 (optional): PyTorch/CUDA training-loop bridge.

Data: synthetic tensor data generated in-script
Rows: 25,000
Features: x, shape [N, 1]
Target: y = 2.2*x - 0.4 + noise
Type: Regression bridge for gradient-based training
"""

from __future__ import annotations

import time

import torch


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_linear(device: torch.device, epochs: int = 400, lr: float = 0.05):
    generator = torch.Generator(device="cpu").manual_seed(42)
    x = torch.randn((25_000, 1), generator=generator).to(device)
    noise = 0.2 * torch.randn((25_000, 1), generator=generator).to(device)
    y = 2.2 * x - 0.4 + noise

    model = torch.nn.Linear(1, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    first_loss = None
    for _ in range(epochs):
        optimizer.zero_grad()
        pred = model(x)
        loss = loss_fn(pred, y)
        if first_loss is None:
            first_loss = float(loss.item())
        loss.backward()
        optimizer.step()

    return (
        float(model.weight.item()),
        float(model.bias.item()),
        first_loss,
        float(loss.item()),
    )


def matmul_timing(device: torch.device, size: int = 1024, iters: int = 20) -> float:
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)
    if device.type == "cuda":
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(iters):
        _ = a @ b
    if device.type == "cuda":
        torch.cuda.synchronize()
    t1 = time.perf_counter()
    return (t1 - t0) / iters


# Workflow:
# 1) Select CPU/GPU device and build synthetic tensor regression data.
# 2) Train a linear model with autograd and SGD.
# 3) Compare CPU/GPU matrix multiplication timing when CUDA is available.
def main() -> None:
    print("torch:", torch.__version__)
    print("cuda available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("cuda device:", torch.cuda.get_device_name(0))

    device = pick_device()
    print("selected device:", device)

    w, b, first_loss, final_loss = train_linear(device)
    print(f"learned w={w:.4f} (expected near 2.2)")
    print(f"learned b={b:.4f} (expected near -0.4)")
    print(f"loss first={first_loss:.4f}, final={final_loss:.4f}")

    cpu_time = matmul_timing(torch.device("cpu"))
    print(f"cpu matmul avg time: {cpu_time:.6f}s")

    if torch.cuda.is_available():
        gpu_time = matmul_timing(torch.device("cuda"))
        print(f"gpu matmul avg time: {gpu_time:.6f}s")
        print(f"cpu/gpu speedup: {cpu_time / gpu_time:.2f}x")
    else:
        print("gpu timing skipped because CUDA is unavailable.")


if __name__ == "__main__":
    main()

