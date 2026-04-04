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

from stage13_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, as_jsonl


def main() -> None:
    declaration = {
        "Data": "Synthetic capstone baseline dataset",
        "Requests/Samples": "200 scenarios",
        "Input schema": "request_id, module, expected_behavior",
        "Output schema": "quality_score, latency_p95_ms, failure_rate",
        "Eval policy": "fixed seed and replay",
        "Type": "capstone_baseline",
    }
    print_data_declaration("Lab 1 - Capstone Baseline", declaration)

    metrics = [
        {"module": "data", "quality_score": 0.91, "latency_p95_ms": 45.0, "failure_rate": 0.005},
        {"module": "model", "quality_score": 0.78, "latency_p95_ms": 220.0, "failure_rate": 0.018},
        {"module": "reasoning", "quality_score": 0.74, "latency_p95_ms": 310.0, "failure_rate": 0.022},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_capstone_baseline_metrics.csv", metrics)

    outputs = [
        {"request_id": "r001", "layer": "api", "status": "ok", "decision": "hold"},
        {"request_id": "r002", "layer": "api", "status": "ok", "decision": "promote"},
        {"request_id": "r003", "layer": "api", "status": "warn", "decision": "hold"},
    ]
    as_jsonl(RESULTS_DIR / "lab1_capstone_layer_outputs.jsonl", outputs)

    contract = [
        {"interface": "data_to_feature", "status": "pass"},
        {"interface": "feature_to_model", "status": "pass"},
        {"interface": "model_to_reasoning", "status": "warn"},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_capstone_contract_status.csv", contract)

    print("[INFO] Lab 1 outputs written.")


if __name__ == "__main__":
    main()
