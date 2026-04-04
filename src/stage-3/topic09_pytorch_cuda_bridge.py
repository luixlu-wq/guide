"""Stage 3 Topic 09: PyTorch/CUDA training-loop bridge with CPU/GPU benchmark artifacts.

Data Source: synthetic tensor data generated in script
Schema: 1 numeric feature tensor | Target: continuous tensor regression
Preprocessing: device transfer and dtype consistency required (`cpu`/`cuda`)
Null Handling: None (synthetic tensor generator produces complete arrays)
"""

from __future__ import annotations

import json
from pathlib import Path
import time

import pandas as pd
import torch


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def make_regression_tensors(n_rows: int = 25_000):
    generator = torch.Generator(device="cpu").manual_seed(42)
    x_cpu = torch.randn((n_rows, 1), generator=generator)
    noise_cpu = 0.2 * torch.randn((n_rows, 1), generator=generator)
    y_cpu = 2.2 * x_cpu - 0.4 + noise_cpu
    return x_cpu, y_cpu


def train_linear(
    device: torch.device,
    x_cpu: torch.Tensor,
    y_cpu: torch.Tensor,
    epochs: int = 250,
    lr: float = 0.05,
):
    start_total = time.perf_counter()

    transfer_time_s = 0.0
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        t_transfer_start = time.perf_counter()
        x = x_cpu.to(device)
        y = y_cpu.to(device)
        torch.cuda.synchronize()
        transfer_time_s = time.perf_counter() - t_transfer_start
    else:
        x = x_cpu
        y = y_cpu

    model = torch.nn.Linear(1, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    first_loss = None
    start_compute = time.perf_counter()
    for _ in range(epochs):
        optimizer.zero_grad()
        pred = model(x)
        loss = loss_fn(pred, y)
        if first_loss is None:
            first_loss = float(loss.item())
        loss.backward()
        optimizer.step()

    if device.type == "cuda":
        torch.cuda.synchronize()
        peak_memory_mb = float(torch.cuda.max_memory_allocated(device) / (1024 * 1024))
    else:
        peak_memory_mb = 0.0

    compute_time_s = time.perf_counter() - start_compute
    total_time_s = time.perf_counter() - start_total

    return {
        "device": device.type,
        "rows": int(x_cpu.shape[0]),
        "epochs": epochs,
        "transfer_time_s": float(transfer_time_s),
        "compute_time_s": float(compute_time_s),
        "total_time_s": float(total_time_s),
        "first_loss": float(first_loss) if first_loss is not None else float("nan"),
        "final_loss": float(loss.item()),
        "learned_w": float(model.weight.item()),
        "learned_b": float(model.bias.item()),
        "peak_memory_mb": peak_memory_mb,
    }


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


def write_stage3_artifacts(cpu_stats: dict, gpu_stats: dict | None) -> None:
    out_dir = Path(__file__).parent / "results" / "stage3"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [cpu_stats]
    if gpu_stats is not None:
        rows.append(gpu_stats)

    df = pd.DataFrame(rows)
    csv_path = out_dir / "cpu_gpu_latency_transfer.csv"
    json_path = out_dir / "cpu_gpu_latency_transfer.json"
    df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    if gpu_stats is None:
        decision = (
            "CUDA unavailable. Use CPU path and keep this benchmark as the fallback baseline."
        )
        risk_note = "No GPU benchmark yet; transfer/compute tradeoff cannot be evaluated."
    else:
        if gpu_stats["total_time_s"] < cpu_stats["total_time_s"]:
            decision = "GPU wins for this workload and should be preferred for repeated training."
        else:
            decision = "CPU is faster for this workload due to transfer/overhead effects."
        risk_note = (
            "Monitor CUDA memory pressure and rerun benchmark when batch size or row count changes."
        )

    decision_path = out_dir / "decision_and_risk.md"
    decision_text = f"""# CPU vs GPU Decision And Risk Note (Topic 09)

## Summary
- CPU total time: {cpu_stats["total_time_s"]:.6f}s
- GPU total time: {gpu_stats["total_time_s"]:.6f}s
""" if gpu_stats is not None else f"""# CPU vs GPU Decision And Risk Note (Topic 09)

## Summary
- CPU total time: {cpu_stats["total_time_s"]:.6f}s
- GPU total time: not available (CUDA unavailable)
"""
    decision_text += f"""
## Decision
{decision}

## Risks
- {risk_note}
- CUDA OOM risk can increase when batch/model size grows.
- Transfer cost can dominate when tensors are small.

## Evidence Files
- `cpu_gpu_latency_transfer.csv`
- `cpu_gpu_latency_transfer.json`
"""
    decision_path.write_text(decision_text, encoding="utf-8")

    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print(f"Saved: {decision_path}")


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
    x_cpu, y_cpu = make_regression_tensors()

    cpu_stats = train_linear(torch.device("cpu"), x_cpu, y_cpu)
    print(
        "cpu train:",
        f"loss {cpu_stats['first_loss']:.4f}->{cpu_stats['final_loss']:.4f},",
        f"total {cpu_stats['total_time_s']:.6f}s",
    )

    cpu_time = matmul_timing(torch.device("cpu"))
    print(f"cpu matmul avg time: {cpu_time:.6f}s")

    gpu_stats = None
    if torch.cuda.is_available():
        gpu_stats = train_linear(torch.device("cuda"), x_cpu, y_cpu)
        print(
            "gpu train:",
            f"loss {gpu_stats['first_loss']:.4f}->{gpu_stats['final_loss']:.4f},",
            f"transfer {gpu_stats['transfer_time_s']:.6f}s,",
            f"compute {gpu_stats['compute_time_s']:.6f}s,",
            f"total {gpu_stats['total_time_s']:.6f}s",
        )
        print(
            f"learned gpu w={gpu_stats['learned_w']:.4f} (expected near 2.2), "
            f"b={gpu_stats['learned_b']:.4f} (expected near -0.4)"
        )
        print(f"gpu peak memory: {gpu_stats['peak_memory_mb']:.2f} MB")
        gpu_time = matmul_timing(torch.device("cuda"))
        print(f"gpu matmul avg time: {gpu_time:.6f}s")
        print(f"cpu/gpu speedup: {cpu_time / gpu_time:.2f}x")
    else:
        print("gpu timing skipped because CUDA is unavailable.")

    write_stage3_artifacts(cpu_stats, gpu_stats)


if __name__ == "__main__":
    main()


