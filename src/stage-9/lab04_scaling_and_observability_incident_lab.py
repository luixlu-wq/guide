"""
lab04_scaling_and_observability_incident_lab

Lab goal:
- Reproduce a realistic load incident.
- Compare multiple fix options and verify one fix with controlled rerun.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic load-test timeline and telemetry snapshots",
        "Requests/Samples": "5 traffic windows",
        "Input schema": "window:str, incoming_rps:float",
        "Output schema": "p95_latency_ms:float, error_rate:float, queue_depth:float",
        "Eval policy": "fixed load windows before/after one controlled change",
        "Type": "scaling + observability incident response",
    }
    print_data_declaration("Lab 4 - Scaling and Observability Incident", declaration)

    load_rows = [
        {"window": "w1", "incoming_rps": 2.2, "p95_latency_ms": 540.0, "error_rate": 0.006, "queue_depth": 2.0},
        {"window": "w2", "incoming_rps": 2.8, "p95_latency_ms": 620.0, "error_rate": 0.010, "queue_depth": 3.2},
        {"window": "w3", "incoming_rps": 3.3, "p95_latency_ms": 810.0, "error_rate": 0.021, "queue_depth": 5.5},
        {"window": "w4", "incoming_rps": 3.7, "p95_latency_ms": 980.0, "error_rate": 0.034, "queue_depth": 8.1},
        {"window": "w5", "incoming_rps": 4.1, "p95_latency_ms": 1210.0, "error_rate": 0.049, "queue_depth": 11.4},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_load_test_summary.csv", load_rows)

    incident_timeline = [
        "# Lab 4 Incident Timeline",
        "",
        "1. Alert triggered: p95 latency exceeded SLA for 3 windows.",
        "2. Queue depth grew faster than worker drain rate.",
        "3. Error rate increased due to timeouts and retries.",
        "4. Root cause classified: missing backpressure policy + insufficient replicas.",
        "5. Candidate fixes evaluated before deployment.",
    ]
    write_text(RESULTS_DIR / "lab4_incident_timeline.md", "\n".join(incident_timeline))

    fix_options = [
        {
            "option": "Increase replicas from 2 to 4",
            "expected_p95_delta_ms": -210.0,
            "expected_error_delta": -0.011,
            "cost_impact": "medium",
            "risk": "low",
            "chosen": "yes",
        },
        {
            "option": "Aggressive timeout reduction only",
            "expected_p95_delta_ms": -90.0,
            "expected_error_delta": +0.006,
            "cost_impact": "low",
            "risk": "medium",
            "chosen": "no",
        },
    ]
    write_rows_csv(RESULTS_DIR / "lab4_fix_options_comparison.csv", fix_options)

    verification_rows = [
        {"metric": "latency_p95_ms", "before": 1210.0, "after": 890.0, "delta": -320.0},
        {"metric": "error_rate", "before": 0.049, "after": 0.021, "delta": -0.028},
        {"metric": "queue_depth", "before": 11.4, "after": 5.8, "delta": -5.6},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_verification_rerun.csv", verification_rows)

    print("[INFO] Lab 4 outputs written:")
    print("- results/lab4_load_test_summary.csv")
    print("- results/lab4_incident_timeline.md")
    print("- results/lab4_fix_options_comparison.csv")
    print("- results/lab4_verification_rerun.csv")


if __name__ == "__main__":
    main()

