"""
lab04_option_compare_and_verify

Lab goal:
- Compare two options, rerun verification, and record final decision.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage15_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic cross-domain issue options",
        "Requests/Samples": "2 options",
        "Input schema": "option, expected_quality_delta, expected_latency_delta",
        "Output schema": "verification_metrics",
        "Eval policy": "fixed rerun and gate check",
        "Type": "option_compare_verify",
    }
    print_data_declaration("Lab 4 - Option Compare and Verify", declaration)

    compare_rows = [
        {"option": "A", "expected_quality_delta": 0.06, "expected_latency_delta": 15.0, "risk": "low"},
        {"option": "B", "expected_quality_delta": 0.09, "expected_latency_delta": 34.0, "risk": "medium"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_solution_compare.csv", compare_rows)

    verification = [
        {"metric": "quality_score", "before": 0.74, "after": 0.82, "delta": 0.08},
        {"metric": "latency_p95_ms", "before": 790.0, "after": 760.0, "delta": -30.0},
        {"metric": "failure_rate", "before": 0.024, "after": 0.014, "delta": -0.010},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_verification_rerun.csv", verification)

    write_text(
        RESULTS_DIR / "lab4_decision_record.md",
        "# Lab 4 Decision Record\n\n- Selected option: B\n- Reason: higher reliability improvement with acceptable latency tradeoff.\n",
    )


if __name__ == "__main__":
    main()
