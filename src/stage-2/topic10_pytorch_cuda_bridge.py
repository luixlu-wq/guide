"""PyTorch/CUDA bridge for Stage 2.

Data:
- Synthetic tensor regression data generated in-script for training.
- Small pandas DataFrame for DataFrame->NumPy->Tensor bridge demo.

Rows:
- 30,000 regression samples
- 8 bridge-demo rows

Features:
- x tensor (shape [N, 1]) for regression
- close/volume columns for bridge demo

Target:
- y = 1.8*x - 0.7 + noise

Type: regression bridge demo with device/memory instrumentation
"""

from __future__ import annotations

import time

import pandas as pd
import torch


def device_pick() -> torch.device:
    """Pick CUDA when available, otherwise keep safe CPU fallback."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def vram_allocated_mb() -> float:
    """Current allocated VRAM in MB (0.0 on CPU-only runs)."""
    if not torch.cuda.is_available():
        return 0.0
    return float(torch.cuda.memory_allocated() / (1024**2))


def vram_peak_mb() -> float:
    """Peak allocated VRAM in MB since last reset (0.0 on CPU-only runs)."""
    if not torch.cuda.is_available():
        return 0.0
    return float(torch.cuda.max_memory_allocated() / (1024**2))


def dataframe_numpy_tensor_bridge(device: torch.device):
    """Show the memory path from DataFrame to NumPy to torch tensor.

    Key ideas:
    - pandas -> NumPy can avoid an extra copy with copy=False (when layout permits).
    - torch.from_numpy creates a CPU tensor view over NumPy memory (shared memory).
    - .to('cuda') performs explicit host->device transfer (not zero-copy across devices).
    """
    df = pd.DataFrame(
        {
            "close": [100.0, 100.2, 100.5, 100.4, 100.8, 101.1, 100.9, 101.3],
            "volume": [150_000, 165_000, 148_000, 172_000, 180_000, 190_000, 177_000, 205_000],
        }
    )

    # Ask pandas for float32 matrix and avoid extra copy where possible.
    arr = df[["close", "volume"]].to_numpy(dtype="float32", copy=False)

    # Build a CPU tensor view from NumPy memory.
    x_cpu = torch.from_numpy(arr)

    # Move to selected runtime device (copy for cuda path).
    x_dev = x_cpu.to(device)

    shared_ptr = int(arr.__array_interface__["data"][0]) == int(x_cpu.numpy().__array_interface__["data"][0])

    print("bridge demo:")
    print("  pandas shape:", df.shape)
    print("  numpy shape :", arr.shape, "dtype:", arr.dtype)
    print("  tensor(cpu) shape:", tuple(x_cpu.shape), "dtype:", x_cpu.dtype)
    print("  tensor(device) shape:", tuple(x_dev.shape), "device:", x_dev.device)
    print("  numpy<->tensor_cpu shared memory:", shared_ptr)


def autograd_demo(device: torch.device):
    """Simple derivative demo to verify autograd mechanics."""
    x = torch.tensor(2.0, device=device, requires_grad=True)
    y = x**3 + 2 * x
    y.backward()
    print(f"autograd demo: x={x.item():.1f}, y={y.item():.1f}, dy/dx={x.grad.item():.1f}")


def train(device: torch.device, epochs: int = 400, lr: float = 0.05):
    """Train linear regression with autograd and capture memory/timing metrics."""
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()

    before_mb = vram_allocated_mb()

    g = torch.Generator(device="cpu").manual_seed(42)
    x = torch.randn((30_000, 1), generator=g, dtype=torch.float32).to(device)
    noise = 0.15 * torch.randn((30_000, 1), generator=g, dtype=torch.float32).to(device)
    y = 1.8 * x - 0.7 + noise

    w = torch.zeros((1, 1), device=device, requires_grad=True)
    b = torch.zeros((1,), device=device, requires_grad=True)

    first_loss = None
    t0 = time.perf_counter()
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

    train_ms = (time.perf_counter() - t0) * 1000.0

    after_mb = vram_allocated_mb()
    peak_mb = vram_peak_mb()

    return {
        "w": float(w.item()),
        "b": float(b.item()),
        "first_loss": float(first_loss),
        "final_loss": float(loss.item()),
        "train_time_ms": float(train_ms),
        "vram_before_mb": float(before_mb),
        "vram_after_mb": float(after_mb),
        "vram_peak_mb": float(peak_mb),
    }


def matmul_profile(device: torch.device, size: int = 1024, iters: int = 25):
    """Benchmark one matrix multiplication workload and capture memory snapshots."""
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)

    before_mb = vram_allocated_mb() if device.type == "cuda" else 0.0

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()

    t0 = time.perf_counter()
    for _ in range(iters):
        _ = a @ b

    if device.type == "cuda":
        torch.cuda.synchronize()

    t1 = time.perf_counter()
    after_mb = vram_allocated_mb() if device.type == "cuda" else 0.0
    peak_mb = vram_peak_mb() if device.type == "cuda" else 0.0

    return {
        "avg_time_sec": float((t1 - t0) / iters),
        "vram_before_mb": float(before_mb),
        "vram_after_mb": float(after_mb),
        "vram_peak_mb": float(peak_mb),
    }


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

    dataframe_numpy_tensor_bridge(dev)
    print()

    autograd_demo(dev)
    print()

    train_metrics = train(dev)
    print(f"learned w={train_metrics['w']:.4f} (expected near 1.8)")
    print(f"learned b={train_metrics['b']:.4f} (expected near -0.7)")
    print(f"loss first={train_metrics['first_loss']:.4f} final={train_metrics['final_loss']:.4f}")
    print(f"train time={train_metrics['train_time_ms']:.2f} ms")

    if dev.type == "cuda":
        print(f"vram before train: {train_metrics['vram_before_mb']:.2f} MB")
        print(f"vram after train : {train_metrics['vram_after_mb']:.2f} MB")
        print(f"vram peak train  : {train_metrics['vram_peak_mb']:.2f} MB")
    else:
        print("vram metrics for training: skipped (CPU runtime)")

    print()
    cpu_profile = matmul_profile(torch.device("cpu"))
    print(f"cpu matmul avg: {cpu_profile['avg_time_sec']:.6f}s")

    if torch.cuda.is_available():
        gpu_profile = matmul_profile(torch.device("cuda"))
        print(f"gpu matmul avg: {gpu_profile['avg_time_sec']:.6f}s")
        print(f"cpu/gpu speedup: {cpu_profile['avg_time_sec'] / gpu_profile['avg_time_sec']:.2f}x")
        print(f"gpu vram before matmul: {gpu_profile['vram_before_mb']:.2f} MB")
        print(f"gpu vram after matmul : {gpu_profile['vram_after_mb']:.2f} MB")
        print(f"gpu vram peak matmul  : {gpu_profile['vram_peak_mb']:.2f} MB")

        # Release cached blocks from allocator pool after demo workload.
        torch.cuda.empty_cache()
        print("torch.cuda.empty_cache() called after profiling")
        print("note: empty_cache releases cached blocks; it does not delete live tensors.")
    else:
        print("gpu timing and VRAM profiling skipped because CUDA is unavailable.")


if __name__ == "__main__":
    main()
