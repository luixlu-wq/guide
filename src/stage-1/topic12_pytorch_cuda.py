"""Topic 12: PyTorch + CUDA fundamentals with VRAM instrumentation.

Data: Synthetic linear regression tensors generated in-script
Rows: 20,000
Features: x (shape [N, 1])
Target: y = 2.5 * x + 1.0 + noise
Type: Regression
"""

from __future__ import annotations

import time

import torch

from common.runtime import create_logger, write_json_artifact


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def vram_allocated_mb() -> float:
    if not torch.cuda.is_available():
        return 0.0
    return float(torch.cuda.memory_allocated() / (1024**2))


def vram_peak_mb() -> float:
    if not torch.cuda.is_available():
        return 0.0
    return float(torch.cuda.max_memory_allocated() / (1024**2))


def autograd_demo(device: torch.device) -> dict:
    x = torch.tensor(3.0, device=device, requires_grad=True)
    y = x**2 + 2 * x + 1
    y.backward()
    return {
        "x": float(x.item()),
        "y": float(y.item()),
        "dy_dx": float(x.grad.item()),
    }


def make_data(n: int = 20_000, seed: int = 42, device: torch.device | None = None):
    if device is None:
        device = torch.device("cpu")
    g = torch.Generator(device="cpu").manual_seed(seed)
    x = torch.randn((n, 1), generator=g, dtype=torch.float32)
    noise = 0.2 * torch.randn((n, 1), generator=g, dtype=torch.float32)
    y = 2.5 * x + 1.0 + noise
    return x.to(device), y.to(device)


def train_linear_autograd(
    device: torch.device,
    epochs: int = 500,
    lr: float = 0.05,
) -> tuple[float, float, float, float, float]:
    x, y = make_data(device=device)
    w = torch.zeros((1, 1), device=device, requires_grad=True)
    b = torch.zeros((1,), device=device, requires_grad=True)

    start = time.perf_counter()
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
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    return float(w.item()), float(b.item()), float(first_loss), float(loss.item()), float(elapsed_ms)


def matmul_timing(device: torch.device, size: int = 1024, iters: int = 30) -> dict:
    a = torch.randn((size, size), device=device)
    b = torch.randn((size, size), device=device)

    before_mb = vram_allocated_mb() if device.type == "cuda" else 0.0
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()

    start = time.perf_counter()
    for _ in range(iters):
        _ = a @ b

    if device.type == "cuda":
        torch.cuda.synchronize()

    elapsed_s = (time.perf_counter() - start) / iters
    after_mb = vram_allocated_mb() if device.type == "cuda" else 0.0
    peak_mb = vram_peak_mb() if device.type == "cuda" else 0.0

    return {
        "avg_time_sec": float(elapsed_s),
        "memory_before_mb": float(before_mb),
        "memory_after_mb": float(after_mb),
        "memory_peak_mb": float(peak_mb),
    }


def main() -> None:
    script_stem = "topic12_pytorch_cuda"
    logger = create_logger(script_stem)

    logger.info("torch_version=%s", torch.__version__)
    logger.info("cuda_available=%s", torch.cuda.is_available())
    if torch.cuda.is_available():
        logger.info("cuda_device=%s", torch.cuda.get_device_name(0))

    logger.info(
        "concept_note: torch.tensor is the tensor abstraction used by PyTorch kernels; numpy.array is CPU-only by default."
    )

    device = pick_device()
    logger.info("selected_device=%s", device)

    auto = autograd_demo(device)
    logger.info("autograd_demo x=%.1f y=%.1f dy_dx=%.1f", auto["x"], auto["y"], auto["dy_dx"])

    w, b, first_loss, final_loss, train_time_ms = train_linear_autograd(device=device)
    logger.info("training_result w=%.4f b=%.4f", w, b)
    logger.info("loss_initial=%.4f loss_final=%.4f train_time_ms=%.2f", first_loss, final_loss, train_time_ms)

    cpu_perf = matmul_timing(torch.device("cpu"))
    logger.info("cpu_matmul_avg_time_sec=%.6f", cpu_perf["avg_time_sec"])

    gpu_perf = None
    speedup_x = None
    if torch.cuda.is_available():
        gpu_perf = matmul_timing(torch.device("cuda"))
        speedup_x = cpu_perf["avg_time_sec"] / gpu_perf["avg_time_sec"] if gpu_perf["avg_time_sec"] > 0 else None
        logger.info("gpu_matmul_avg_time_sec=%.6f", gpu_perf["avg_time_sec"])
        logger.info(
            "gpu_vram_before_mb=%.2f after_mb=%.2f peak_mb=%.2f",
            gpu_perf["memory_before_mb"],
            gpu_perf["memory_after_mb"],
            gpu_perf["memory_peak_mb"],
        )
        if speedup_x is not None:
            logger.info("cpu_gpu_speedup_x=%.2f", speedup_x)
    else:
        logger.info("gpu_path_skipped: CUDA unavailable")

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "quality_metric_name": "final_training_loss",
            "quality_metric_value": final_loss,
            "hardware": {
                "cuda_available": bool(torch.cuda.is_available()),
                "device": str(device),
                "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            },
            "metrics": {
                "autograd_demo": auto,
                "training": {
                    "learned_w": w,
                    "learned_b": b,
                    "initial_loss": first_loss,
                    "final_loss": final_loss,
                    "train_time_ms": train_time_ms,
                },
                "cpu_matmul": cpu_perf,
                "gpu_matmul": gpu_perf,
                "cpu_gpu_speedup_x": speedup_x,
            },
            "decision_note": "use VRAM and timing metrics to verify CUDA path and estimate scaling headroom",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
