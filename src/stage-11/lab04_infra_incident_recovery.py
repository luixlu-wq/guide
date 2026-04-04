"""
lab04_infra_incident_recovery

Lab goal:
- Execute incident diagnosis and controlled fix verification.
- Produce release decision artifact with promote/hold/rollback logic.
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
        "Data": "Synthetic infrastructure incident timeline",
        "Requests/Samples": "5 windows + 2 fix options",
        "Input schema": "window, p95_latency, error_rate, queue_depth",
        "Output schema": "option comparison + rerun deltas + decision",
        "Eval policy": "fixed replay and same acceptance gates",
        "Type": "incident recovery",
    }
    print_data_declaration("Lab 4 - Infrastructure Incident Recovery", declaration)

    base = [
        {"window": "w1", "latency_p95_ms": 620.0, "error_rate": 0.012, "queue_depth": 2.1},
        {"window": "w2", "latency_p95_ms": 770.0, "error_rate": 0.017, "queue_depth": 3.8},
        {"window": "w3", "latency_p95_ms": 940.0, "error_rate": 0.026, "queue_depth": 5.7},
        {"window": "w4", "latency_p95_ms": 1110.0, "error_rate": 0.035, "queue_depth": 8.6},
        {"window": "w5", "latency_p95_ms": 1280.0, "error_rate": 0.048, "queue_depth": 11.3},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_incident_baseline.csv", base)

    options = [
        {"option": "queue backpressure + min replica increase", "expected_latency_delta": -290.0, "expected_error_delta": -0.022, "cost_impact": "medium", "chosen": "yes"},
        {"option": "timeout increase only", "expected_latency_delta": -70.0, "expected_error_delta": 0.005, "cost_impact": "low", "chosen": "no"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_solution_options.csv", options)

    rerun = [
        {"metric": "latency_p95_ms", "before": 1280.0, "after": 860.0, "delta": -420.0},
        {"metric": "error_rate", "before": 0.048, "after": 0.018, "delta": -0.03},
        {"metric": "queue_depth", "before": 11.3, "after": 4.9, "delta": -6.4},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_verification_rerun.csv", rerun)

    decision = [
        "# Lab 4 Release Decision",
        "",
        "- Gate checks: latency improved, error rate improved, queue stabilized.",
        "- Decision: promote with canary rollout and rollback guardrails.",
        "- Rollback trigger: p95 > 950ms for 3 windows or error_rate > 0.025.",
    ]
    write_text(RESULTS_DIR / "lab4_release_decision.md", "\n".join(decision))

    print("[INFO] Lab 4 outputs written:")
    print("- results/lab4_incident_baseline.csv")
    print("- results/lab4_solution_options.csv")
    print("- results/lab4_verification_rerun.csv")
    print("- results/lab4_release_decision.md")


if __name__ == "__main__":
    main()

