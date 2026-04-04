"""Stage 5 Topic 05C: VRAM/performance optimization demo (advanced).

Data: synthetic Q/K/V tensors
Records/Samples: configurable batch/sequence/head dimensions
Input schema: q,k,v tensors [batch, heads, seq_len, head_dim]
Output schema: timing + throughput + memory metrics
Split/Eval policy: not applicable (performance lab)
Type: hardware-aware transformer optimization
"""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import torch


def benchmark_attention(
    *,
    device: torch.device,
    dtype: torch.dtype,
    batch_size: int,
    heads: int,
    seq_len: int,
    head_dim: int,
    iters: int,
    use_flash_context: bool,
) -> dict[str, float | str]:
    q = torch.randn(batch_size, heads, seq_len, head_dim, device=device, dtype=dtype)
    k = torch.randn(batch_size, heads, seq_len, head_dim, device=device, dtype=dtype)
    v = torch.randn(batch_size, heads, seq_len, head_dim, device=device, dtype=dtype)

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        torch.cuda.synchronize()

    start = time.perf_counter()
    if use_flash_context and device.type == "cuda":
        # Prefer flash kernel path when available; safe for modern GPUs.
        with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=False):
            for _ in range(iters):
                _ = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)
    else:
        for _ in range(iters):
            _ = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)

    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    tokens_processed = batch_size * seq_len * iters
    tokens_per_s = tokens_processed / max(elapsed, 1e-9)
    peak_vram_gb = (torch.cuda.max_memory_allocated(device) / 1e9) if device.type == "cuda" else 0.0
    return {
        "elapsed_seconds": elapsed,
        "tokens_per_second": tokens_per_s,
        "peak_vram_gb": peak_vram_gb,
    }


# Workflow:
# 1) Choose runtime device and preferred precision (BF16 -> FP16 -> FP32 fallback).
# 2) Benchmark scaled dot-product attention in baseline and optimized paths.
# 3) Report throughput and memory to support configuration decisions.
def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if device.type == "cuda" and torch.cuda.is_bf16_supported():
        dtype = torch.bfloat16
        dtype_name = "bfloat16"
    elif device.type == "cuda":
        dtype = torch.float16
        dtype_name = "float16"
    else:
        dtype = torch.float32
        dtype_name = "float32"

    batch_size = 8 if device.type == "cuda" else 4
    heads = 8
    seq_len = 256
    head_dim = 64
    iters = 40

    print("Data declaration")
    print("source=synthetic_qkv_tensors")
    print(f"input_schema=qkv:[batch,heads,seq_len,head_dim]=[{batch_size},{heads},{seq_len},{head_dim}]")
    print("output_schema=timing_throughput_memory")
    print(f"device={device.type} dtype={dtype_name}")

    baseline = benchmark_attention(
        device=device,
        dtype=dtype,
        batch_size=batch_size,
        heads=heads,
        seq_len=seq_len,
        head_dim=head_dim,
        iters=iters,
        use_flash_context=False,
    )
    optimized = benchmark_attention(
        device=device,
        dtype=dtype,
        batch_size=batch_size,
        heads=heads,
        seq_len=seq_len,
        head_dim=head_dim,
        iters=iters,
        use_flash_context=True,
    )

    speedup = float(optimized["tokens_per_second"]) / max(float(baseline["tokens_per_second"]), 1e-9)
    print(f"baseline_tokens_per_s={float(baseline['tokens_per_second']):.2f}")
    print(f"optimized_tokens_per_s={float(optimized['tokens_per_second']):.2f}")
    print(f"speedup={speedup:.3f}x")
    print(f"baseline_peak_vram_gb={float(baseline['peak_vram_gb']):.3f}")
    print(f"optimized_peak_vram_gb={float(optimized['peak_vram_gb']):.3f}")

    out_dir = Path(__file__).parent / "results" / "stage5"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_df = pd.DataFrame(
        [
            {
                "run_id": "stage5_topic05c_vram_optimization",
                "stage": "5",
                "topic_or_module": "topic05c_vram_optimization",
                "metric_name": "tokens_per_second",
                "before_value": float(baseline["tokens_per_second"]),
                "after_value": float(optimized["tokens_per_second"]),
                "delta": float(optimized["tokens_per_second"]) - float(baseline["tokens_per_second"]),
                "dataset_or_eval_set": "synthetic_qkv",
                "seed_or_config_id": f"{device.type}_{dtype_name}",
                "decision": "promote" if speedup >= 1.0 else "hold",
                "before_peak_vram_gb": float(baseline["peak_vram_gb"]),
                "after_peak_vram_gb": float(optimized["peak_vram_gb"]),
            }
        ]
    )
    out_path = out_dir / "topic05c_vram_optimization_metrics.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
    print("Interpretation: this script makes hardware decisions measurable, not guess-based.")


if __name__ == "__main__":
    main()

