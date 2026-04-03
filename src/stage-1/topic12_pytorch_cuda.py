"""PyTorch + CUDA fundamentals for Stage 1.

Data: synthetic linear regression tensors generated in-script with torch.randn
Rows: 20,000 training samples
Features: x (single numeric feature, shape [N, 1])
Target: y = 2.5 * x + 1.0 + noise (shape [N, 1])
Type: Regression

Purpose:
  1) Show tensor creation and device placement (CPU/GPU).
  2) Show autograd by computing a simple derivative.
  3) Train linear regression using PyTorch autograd on selected device.
  4) Compare CPU vs GPU matrix multiplication timing (if CUDA exists).
"""

from __future__ import annotations

import time

import torch


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def autograd_demo(device: torch.device) -> None:
    x = torch.tensor(3.0, device=device, requires_grad=True)
    y = x**2 + 2 * x + 1
    y.backward()
    print(f"autograd demo on {device}:")
    print(f"  x={x.item():.1f}, y={y.item():.1f}, dy/dx={x.grad.item():.1f}")


def make_data(n: int = 20_000, seed: int = 42, device: torch.device | None = None):
    if device is None:
        device = torch.device("cpu")
    g = torch.Generator(device="cpu").manual_seed(seed)
    x = torch.randn((n, 1), generator=g, dtype=torch.float32)
    noise = 0.2 * torch.randn((n, 1), generator=g, dtype=torch.float32)
    y = 2.5 * x + 1.0 + noise
    return x.to(device), y.to(device)


def train_linear_autograd(
    device: torch.device, epochs: int = 500, lr: float = 0.05
) -> tuple[float, float, float, float]:
    x, y = make_data(device=device)
    w = torch.zeros((1, 1), device=device, requires_grad=True)
    b = torch.zeros((1,), device=device, requires_grad=True)

    first_loss = None
    for _ in range(epochs):
        y_pred = x @ w + b
        loss = torch.mean((y_pred - y) ** 2)
        if first_loss is None:
            first_loss = float(loss.item())
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
            w.grad.zero_()
            b.grad.zero_()

    final_loss = float(loss.item())
    return float(w.item()), float(b.item()), float(first_loss), final_loss


def matmul_timing(device: torch.device, size: int = 1024, iters: int = 30) -> float:
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)
    if device.type == "cuda":
        torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(iters):
        _ = a @ b
    if device.type == "cuda":
        torch.cuda.synchronize()
    end = time.perf_counter()
    return (end - start) / iters


def main() -> None:
    print(f"torch version: {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"cuda device: {torch.cuda.get_device_name(0)}")
    else:
        print("cuda device: not available (running CPU path)")

    device = pick_device()
    print(f"selected device: {device}")
    print()

    autograd_demo(device)
    print()

    w, b, first_loss, final_loss = train_linear_autograd(device=device)
    print(f"linear regression autograd training on {device}:")
    print(f"  learned w: {w:.4f} (expected near 2.5)")
    print(f"  learned b: {b:.4f} (expected near 1.0)")
    print(f"  initial loss: {first_loss:.4f}")
    print(f"  final loss  : {final_loss:.4f}")
    print()

    cpu_time = matmul_timing(torch.device("cpu"))
    print(f"cpu matmul avg time: {cpu_time:.6f}s")

    if torch.cuda.is_available():
        gpu_time = matmul_timing(torch.device("cuda"))
        print(f"gpu matmul avg time: {gpu_time:.6f}s")
        speedup = cpu_time / gpu_time if gpu_time > 0 else float("inf")
        print(f"cpu/gpu speedup    : {speedup:.2f}x")
        print("note: small workloads may show limited speedup.")
    else:
        print("gpu timing skipped: CUDA unavailable.")


if __name__ == "__main__":
    main()
