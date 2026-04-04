"""
lab03_incident_diagnosis_and_fix

Lab goal:
- Apply the required troubleshooting workflow (identify -> compare -> verify).
- Produce option-comparison and rerun verification artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic incident telemetry windows",
        "Records/Samples": "5 windows + 2 solution options",
        "Input schema": "window, latency_p95_ms, error_rate, symptom",
        "Output schema": "option, expected_delta, chosen, verification_delta",
        "Split/Eval policy": "fixed incident replay profile",
        "Type": "incident diagnosis and fix",
    }
    print_data_declaration("Lab 3 - Incident Diagnosis and Fix", declaration)

    baseline_incident = [
        {"window": "w1", "latency_p95_ms": 610.0, "error_rate": 0.011, "symptom": "normal"},
        {"window": "w2", "latency_p95_ms": 740.0, "error_rate": 0.016, "symptom": "rising queue"},
        {"window": "w3", "latency_p95_ms": 930.0, "error_rate": 0.027, "symptom": "timeouts"},
        {"window": "w4", "latency_p95_ms": 1080.0, "error_rate": 0.034, "symptom": "retry storm"},
        {"window": "w5", "latency_p95_ms": 1220.0, "error_rate": 0.046, "symptom": "incident"},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_incident_baseline.csv", baseline_incident)

    options = [
        {"option": "add queue backpressure + worker scale", "expected_latency_delta": -250.0, "expected_error_delta": -0.02, "cost_impact": "medium", "chosen": "yes"},
        {"option": "increase timeout only", "expected_latency_delta": -80.0, "expected_error_delta": 0.004, "cost_impact": "low", "chosen": "no"},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_solution_options.csv", options)

    verification = [
        {"metric": "latency_p95_ms", "before": 1220.0, "after": 860.0, "delta": -360.0},
        {"metric": "error_rate", "before": 0.046, "after": 0.019, "delta": -0.027},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_verification_rerun.csv", verification)

    note = [
        "# Lab 3 Verification Notes",
        "",
        "- Failure classified as orchestration/ops bottleneck (not ML quality issue).",
        "- Two options compared; one controlled fix applied.",
        "- Same replay profile used before/after for fair validation.",
        "- Decision: hold until 2 additional stable windows are observed.",
    ]
    write_text(RESULTS_DIR / "lab3_verification_notes.md", "\n".join(note))

    decision = [
        "# Lab 3 Decision",
        "",
        "- Decision: hold",
        "- Reason: latency and error improved, but stability window is insufficient for promote.",
        "- Next action: rerun same profile for two additional windows before release vote.",
        "- Rollback trigger: if p95 exceeds 1000ms or error_rate exceeds 0.03.",
    ]
    write_text(RESULTS_DIR / "lab3_decision.md", "\n".join(decision))

    print("[INFO] Lab 3 outputs written:")
    print("- results/lab3_incident_baseline.csv")
    print("- results/lab3_solution_options.csv")
    print("- results/lab3_verification_rerun.csv")
    print("- results/lab3_verification_notes.md")
    print("- results/lab3_decision.md")


if __name__ == "__main__":
    main()
