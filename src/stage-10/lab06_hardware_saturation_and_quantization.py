"""
lab06_hardware_saturation_and_quantization

Lab goal:
- Compare serving throughput across runtime/precision paths.
- Produce hardware saturation evidence for Blackwell-aware operations.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import RESULTS_DIR, as_jsonl, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic runtime benchmark windows",
        "Records/Samples": "4 benchmark points",
        "Input schema": "runtime, precision, concurrency",
        "Output schema": "ttft_ms, throughput_tps, quality_delta",
        "Split/Eval policy": "fixed request mix and fixed token budget",
        "Type": "hardware telemetry + quantization",
    }
    print_data_declaration("Lab 6 - Hardware Saturation and Quantization", declaration)

    throughput_rows = [
        {"runtime": "vllm", "precision": "bf16", "concurrency": 6, "ttft_ms": 290.0, "tokens_per_sec": 128.0},
        {"runtime": "vllm", "precision": "nvfp4", "concurrency": 6, "ttft_ms": 220.0, "tokens_per_sec": 182.0},
        {"runtime": "tensorrt_llm", "precision": "bf16", "concurrency": 6, "ttft_ms": 250.0, "tokens_per_sec": 156.0},
        {"runtime": "tensorrt_llm", "precision": "nvfp4", "concurrency": 6, "ttft_ms": 195.0, "tokens_per_sec": 214.0},
    ]
    write_rows_csv(RESULTS_DIR / "throughput_vllm_vs_trt.csv", throughput_rows)

    saturation = [
        {
            "timestamp": datetime(2026, 4, 4, 14, 30, 0).isoformat(),
            "gpu_compute_utilization_ratio": 0.73,
            "vram_used_gb": 21.6,
            "vram_fragmentation_ratio": 0.34,
            "quantization_mode": "bf16",
            "quantization_error_delta": 0.0,
            "sm_clock_throttle_events": 2,
        },
        {
            "timestamp": datetime(2026, 4, 4, 14, 40, 0).isoformat(),
            "gpu_compute_utilization_ratio": 0.84,
            "vram_used_gb": 16.2,
            "vram_fragmentation_ratio": 0.28,
            "quantization_mode": "nvfp4",
            "quantization_error_delta": 0.011,
            "sm_clock_throttle_events": 1,
        },
    ]
    as_jsonl(RESULTS_DIR / "hardware_saturation_log.jsonl", saturation)

    report = [
        "# Hardware Saturation Summary",
        "",
        "- NVFP4 path improved TTFT and tokens/sec in fixed workload.",
        "- Quality delta remained within configured tolerance.",
        "- Recommendation: use NVFP4 for high-load serving with guardrail monitoring.",
    ]
    write_text(RESULTS_DIR / "hardware_quantization_report.md", "\n".join(report))

    print("[INFO] Lab 6 outputs written:")
    print("- results/throughput_vllm_vs_trt.csv")
    print("- results/hardware_saturation_log.jsonl")
    print("- results/hardware_quantization_report.md")


if __name__ == "__main__":
    main()

