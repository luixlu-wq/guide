"""
lab04_capstone_production_readiness

Lab goal:
- Evaluate release gates and publish release plus rollback artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage13_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic release gate checklist",
        "Requests/Samples": "8 gate checks",
        "Input schema": "gate, threshold, actual",
        "Output schema": "pass_or_fail",
        "Eval policy": "fixed release criteria",
        "Type": "production_readiness",
    }
    print_data_declaration("Lab 4 - Capstone Production Readiness", declaration)

    checks = [
        {"gate": "contract_validity", "threshold": "100%", "actual": "100%", "pass_or_fail": "pass"},
        {"gate": "quality_score", "threshold": ">=0.80", "actual": "0.82", "pass_or_fail": "pass"},
        {"gate": "failure_rate", "threshold": "<=0.02", "actual": "0.015", "pass_or_fail": "pass"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_release_gate_checklist.csv", checks)

    write_text(
        RESULTS_DIR / "lab4_release_decision.md",
        "# Lab 4 Release Decision\n\n- Decision: promote\n- Reason: all critical gates passed under fixed rerun policy.\n",
    )
    write_text(
        RESULTS_DIR / "lab4_rollback_plan.md",
        "# Lab 4 Rollback Plan\n\n- Trigger rollback if quality_score < 0.78 for 2 windows.\n- Trigger rollback if failure_rate > 0.02 for 2 windows.\n",
    )

    print("[INFO] Lab 4 outputs written.")


if __name__ == "__main__":
    main()
