"""
lab06_blackwell_nvfp4_prefix_caching

Lab goal:
- Compare BF16 vs NVFP4 throughput/quality tradeoff.
- Measure prefix-caching and prompt-reordering impact on loop latency.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage12_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic Blackwell runtime benchmark windows",
        "Requests/Samples": "6 benchmark points",
        "Input schema": "precision_mode, caching_strategy, loop_steps",
        "Output schema": "latency_ms, throughput_tps, quality_score",
        "Eval policy": "fixed workload and fixed judge rubric",
        "Type": "nvfp4 + prefix caching",
    }
    print_data_declaration("Lab 6 - Blackwell NVFP4 Prefix Caching", declaration)

    nvfp4_rows = [
        {"precision_mode": "bf16", "throughput_tps": 132.0, "latency_p95_ms": 640.0, "quality_score": 0.884},
        {"precision_mode": "nvfp4", "throughput_tps": 212.0, "latency_p95_ms": 470.0, "quality_score": 0.872},
    ]
    write_rows_csv(RESULTS_DIR / "nvfp4_throughput_quality.csv", nvfp4_rows)

    cache_rows = [
        {"strategy": "no_prefix_cache", "avg_loop_latency_ms": 980.0, "ttft_ms": 320.0},
        {"strategy": "prefix_cache_static_first", "avg_loop_latency_ms": 410.0, "ttft_ms": 138.0},
    ]
    write_rows_csv(RESULTS_DIR / "prefix_cache_latency_profile.csv", cache_rows)

    report = [
        "# Agent Loop Latency Report",
        "",
        "- NVFP4 improved throughput while quality delta stayed within tolerance.",
        "- Prefix caching + prompt reordering reduced loop latency substantially.",
        "- Recommendation: keep dynamic tool outputs at prompt tail for cache reuse.",
    ]
    write_text(RESULTS_DIR / "agent_loop_latency_report.md", "\n".join(report))

    print("[INFO] Lab 6 outputs written:")
    print("- results/nvfp4_throughput_quality.csv")
    print("- results/prefix_cache_latency_profile.csv")
    print("- results/agent_loop_latency_report.md")


if __name__ == "__main__":
    main()

