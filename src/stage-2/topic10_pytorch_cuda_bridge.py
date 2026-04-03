"""Optional PyTorch/CUDA bridge for Stage 2.

Data: synthetic tensor data generated with torch.randn
Rows: 30,000
Features: x (shape [N, 1])
Target: y = 1.8*x - 0.7 + noise
Type: regression bridge demo
"""

from __future__ import annotations

import time

import torch


def device_pick() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def autograd_demo(device: torch.device):
    x = torch.tensor(2.0, device=device, requires_grad=True)
    y = x**3 + 2 * x
    y.backward()
    print(f"autograd demo: x={x.item():.1f}, y={y.item():.1f}, dy/dx={x.grad.item():.1f}")


def train(device: torch.device, epochs=400, lr=0.05):
    g = torch.Generator(device="cpu").manual_seed(42)
    x = torch.randn((30_000, 1), generator=g).to(device)
    noise = 0.15 * torch.randn((30_000, 1), generator=g).to(device)
    y = 1.8 * x - 0.7 + noise

    w = torch.zeros((1, 1), device=device, requires_grad=True)
    b = torch.zeros((1,), device=device, requires_grad=True)

    first_loss = None
    for _ in range(epochs):
        pred = x @ w + b
        loss = torch.mean((pred - y) ** 2)
        if first_loss is None:
            first_loss = float(loss.item())
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
            w.grad.zero_()
            b.grad.zero_()

    return float(w.item()), float(b.item()), float(first_loss), float(loss.item())


def matmul_time(device: torch.device, size=1024, iters=25):
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


def main():
    print("torch version:", torch.__version__)
    print("cuda available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("cuda device:", torch.cuda.get_device_name(0))
    else:
        print("cuda device: unavailable (CPU path)")

    dev = device_pick()
    print("selected device:", dev)
    print()

    autograd_demo(dev)
    w, b, first_loss, final_loss = train(dev)
    print()
    print(f"learned w={w:.4f} (expected near 1.8)")
    print(f"learned b={b:.4f} (expected near -0.7)")
    print(f"loss first={first_loss:.4f} final={final_loss:.4f}")
    print()

    cpu_t = matmul_time(torch.device("cpu"))
    print(f"cpu matmul avg: {cpu_t:.6f}s")
    if torch.cuda.is_available():
        gpu_t = matmul_time(torch.device("cuda"))
        print(f"gpu matmul avg: {gpu_t:.6f}s")
        print(f"cpu/gpu speedup: {cpu_t / gpu_t:.2f}x")
        print("note: speedup depends on workload size.")
    else:
        print("gpu timing skipped because CUDA is unavailable.")


if __name__ == "__main__":
    main()
