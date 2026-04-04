"""
lab01_capstone_baseline

Lab goal:
- Run capstone baseline and write initial evidence artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage13_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    as_jsonl_dual,
    write_text_dual,
    write_json_dual,
    resolve_capstone_domain,
    build_contract_definitions,
    collect_gpu_saturation_log,
    evaluate_wsl_boundary_performance,
    build_domain_baseline_checks,
)


def main() -> None:
    # Resolve the selected capstone domain profile. This keeps Lab 1 aligned with
    # chapter requirements that baseline checks are project-specific.
    domain = resolve_capstone_domain()

    declaration = {
        "Data": "Synthetic capstone baseline dataset",
        "Requests/Samples": "200 scenarios",
        "Input schema": "request_id, module, expected_behavior",
        "Output schema": "quality_score, latency_p95_ms, failure_rate",
        "Eval policy": "fixed seed and replay",
        "Type": f"capstone_baseline/{domain}",
    }
    print_data_declaration("Lab 1 - Capstone Baseline", declaration)

    metrics = [
        {"module": "data", "quality_score": 0.91, "latency_p95_ms": 45.0, "failure_rate": 0.005},
        {"module": "model", "quality_score": 0.78, "latency_p95_ms": 220.0, "failure_rate": 0.018},
        {"module": "reasoning", "quality_score": 0.74, "latency_p95_ms": 310.0, "failure_rate": 0.022},
    ]
    write_rows_csv_dual("lab1_capstone_baseline_metrics.csv", metrics)

    outputs = [
        {"request_id": "r001", "layer": "api", "status": "ok", "decision": "hold"},
        {"request_id": "r002", "layer": "api", "status": "ok", "decision": "promote"},
        {"request_id": "r003", "layer": "api", "status": "warn", "decision": "hold"},
    ]
    as_jsonl_dual("lab1_capstone_layer_outputs.jsonl", outputs)

    contract = [
        {"interface": "data_to_feature", "status": "pass"},
        {"interface": "feature_to_model", "status": "pass"},
        {"interface": "model_to_reasoning", "status": "warn"},
    ]
    write_rows_csv_dual("lab1_capstone_contract_status.csv", contract)

    # Code-first contract artifact used by integration boundary checks.
    write_json_dual("contract_definitions.json", build_contract_definitions(domain))

    # Hardware saturation evidence required for RTX-class release gates.
    # The helper automatically uses NVML/Torch when available and falls back safely.
    hardware_rows = collect_gpu_saturation_log(run_id="stage13_lab1_baseline", request_concurrency=4)
    as_jsonl_dual("hardware_saturation_log.jsonl", hardware_rows)

    # WSL2 boundary evidence checks whether data access from /mnt/c is unsuitable.
    write_rows_csv_dual("wsl_boundary_performance.csv", evaluate_wsl_boundary_performance())

    # Domain-specific baseline checks enforce MTG grounding or GIS projection safety.
    write_text_dual("domain_baseline_checks.md", build_domain_baseline_checks(domain))

    print("[INFO] Lab 1 outputs written.")


if __name__ == "__main__":
    main()
