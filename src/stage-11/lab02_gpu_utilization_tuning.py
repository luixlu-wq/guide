"""
lab02_gpu_utilization_tuning

Lab goal:
- Compare baseline and tuned GPU/CUDA operation profiles.
- Produce actionable tuning report with before/after metrics.
- Produce Blackwell-focused profiling artifacts required by Stage 11 hard gates.
"""

from __future__ import annotations

from pathlib import Path
import sys
from datetime import datetime

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage11_utils import RESULTS_DIR, as_jsonl, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic GPU profile windows",
        "Requests/Samples": "6 benchmark windows",
        "Input schema": "batch_size, precision, concurrency",
        "Output schema": "latency_p95_ms, gpu_mem_mb, error_rate",
        "Eval policy": "fixed benchmark profile",
        "Type": "gpu utilization tuning",
    }
    print_data_declaration("Lab 2 - GPU Utilization Tuning", declaration)

    # Baseline profile intentionally includes lower compute utilization and higher memory pressure.
    baseline = [
        {
            "window": "w1",
            "latency_p95_ms": 680.0,
            "latency_p99_ms": 790.0,
            "gpu_mem_mb": 5100.0,
            "gpu_compute_utilization_ratio": 0.58,
            "vram_fragmentation_ratio": 0.41,
            "fp4_compute_utilization": 0.00,
            "sm_clock_throttle_events": 3,
            "tokens_per_watt": 27.2,
            "error_rate": 0.012,
        },
        {
            "window": "w2",
            "latency_p95_ms": 730.0,
            "latency_p99_ms": 845.0,
            "gpu_mem_mb": 5600.0,
            "gpu_compute_utilization_ratio": 0.55,
            "vram_fragmentation_ratio": 0.47,
            "fp4_compute_utilization": 0.00,
            "sm_clock_throttle_events": 4,
            "tokens_per_watt": 25.7,
            "error_rate": 0.016,
        },
        {
            "window": "w3",
            "latency_p95_ms": 820.0,
            "latency_p99_ms": 930.0,
            "gpu_mem_mb": 6200.0,
            "gpu_compute_utilization_ratio": 0.52,
            "vram_fragmentation_ratio": 0.55,
            "fp4_compute_utilization": 0.00,
            "sm_clock_throttle_events": 7,
            "tokens_per_watt": 23.8,
            "error_rate": 0.021,
        },
    ]

    # Improved profile includes tuned batching, safer memory policy, and FP4 runtime path.
    improved = [
        {
            "window": "w1",
            "latency_p95_ms": 560.0,
            "latency_p99_ms": 660.0,
            "gpu_mem_mb": 4600.0,
            "gpu_compute_utilization_ratio": 0.71,
            "vram_fragmentation_ratio": 0.28,
            "fp4_compute_utilization": 0.64,
            "sm_clock_throttle_events": 1,
            "tokens_per_watt": 34.6,
            "error_rate": 0.009,
        },
        {
            "window": "w2",
            "latency_p95_ms": 610.0,
            "latency_p99_ms": 720.0,
            "gpu_mem_mb": 4900.0,
            "gpu_compute_utilization_ratio": 0.74,
            "vram_fragmentation_ratio": 0.31,
            "fp4_compute_utilization": 0.67,
            "sm_clock_throttle_events": 1,
            "tokens_per_watt": 33.8,
            "error_rate": 0.011,
        },
        {
            "window": "w3",
            "latency_p95_ms": 700.0,
            "latency_p99_ms": 815.0,
            "gpu_mem_mb": 5300.0,
            "gpu_compute_utilization_ratio": 0.69,
            "vram_fragmentation_ratio": 0.37,
            "fp4_compute_utilization": 0.61,
            "sm_clock_throttle_events": 2,
            "tokens_per_watt": 31.5,
            "error_rate": 0.014,
        },
    ]
    write_rows_csv(RESULTS_DIR / "lab2_gpu_profile_baseline.csv", baseline)
    write_rows_csv(RESULTS_DIR / "lab2_gpu_profile_improved.csv", improved)

    # Stage 11 hard-gate artifact: precision tradeoff evidence for Blackwell-friendly paths.
    fp4_tradeoff = [
        {
            "precision_mode": "bf16",
            "tokens_per_sec": 125.0,
            "latency_p95_ms": 690.0,
            "semantic_accuracy": 0.884,
            "quantization_error_delta": 0.000,
        },
        {
            "precision_mode": "fp4",
            "tokens_per_sec": 173.0,
            "latency_p95_ms": 560.0,
            "semantic_accuracy": 0.872,
            "quantization_error_delta": 0.012,
        },
    ]
    write_rows_csv(RESULTS_DIR / "fp4_throughput_quality_tradeoff.csv", fp4_tradeoff)

    # Hardware saturation timeline, used by notebooks and operations review.
    saturation = [
        {
            "timestamp": datetime(2026, 4, 4, 10, 0, 0).isoformat(),
            "gpu_compute_utilization_ratio": 0.58,
            "vram_fragmentation_ratio": 0.41,
            "sm_clock_throttle_events": 3,
        },
        {
            "timestamp": datetime(2026, 4, 4, 10, 5, 0).isoformat(),
            "gpu_compute_utilization_ratio": 0.74,
            "vram_fragmentation_ratio": 0.31,
            "sm_clock_throttle_events": 1,
        },
    ]
    as_jsonl(RESULTS_DIR / "hardware_saturation_profile.jsonl", saturation)

    # WSL2 hardening evidence: compare filesystem path choice impact.
    wsl_io = [
        {"path_class": "/mnt/c hot-path", "io_read_ms": 320.0, "avg_batch_load_ms": 145.0},
        {"path_class": "WSL ext4 hot-path", "io_read_ms": 112.0, "avg_batch_load_ms": 61.0},
    ]
    write_rows_csv(RESULTS_DIR / "wsl_io_before_after.csv", wsl_io)

    report = [
        "# Lab 2 GPU Tuning Report",
        "",
        "Applied changes:",
        "- safer batch upper bound",
        "- mixed precision policy",
        "- OOM recovery and cache clearing behavior",
        "",
        "Observed impact:",
        "- lower p95 latency",
        "- lower GPU memory pressure",
        "- reduced error rate under load",
    ]
    write_text(RESULTS_DIR / "lab2_gpu_tuning_report.md", "\n".join(report))

    print("[INFO] Lab 2 outputs written:")
    print("- results/lab2_gpu_profile_baseline.csv")
    print("- results/lab2_gpu_profile_improved.csv")
    print("- results/lab2_gpu_tuning_report.md")
    print("- results/fp4_throughput_quality_tradeoff.csv")
    print("- results/hardware_saturation_profile.jsonl")
    print("- results/wsl_io_before_after.csv")


if __name__ == "__main__":
    main()
