"""
lab02_gpu_utilization_tuning

Lab goal:
- Compare baseline and tuned GPU/CUDA operation profiles.
- Produce actionable tuning report with before/after metrics.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage11_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


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

    baseline = [
        {"window": "w1", "latency_p95_ms": 680.0, "gpu_mem_mb": 5100.0, "error_rate": 0.012},
        {"window": "w2", "latency_p95_ms": 730.0, "gpu_mem_mb": 5600.0, "error_rate": 0.016},
        {"window": "w3", "latency_p95_ms": 820.0, "gpu_mem_mb": 6200.0, "error_rate": 0.021},
    ]
    improved = [
        {"window": "w1", "latency_p95_ms": 560.0, "gpu_mem_mb": 4600.0, "error_rate": 0.009},
        {"window": "w2", "latency_p95_ms": 610.0, "gpu_mem_mb": 4900.0, "error_rate": 0.011},
        {"window": "w3", "latency_p95_ms": 700.0, "gpu_mem_mb": 5300.0, "error_rate": 0.014},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_gpu_profile_baseline.csv", baseline)
    write_rows_csv(RESULTS_DIR / "lab2_gpu_profile_improved.csv", improved)

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


if __name__ == "__main__":
    main()

