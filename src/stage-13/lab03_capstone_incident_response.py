"""
lab03_capstone_incident_response

Lab goal:
- Execute incident timeline, root-cause summary, and verification rerun.
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
        "Data": "Synthetic incident drill timeline",
        "Requests/Samples": "1 incident with 6 timeline events",
        "Input schema": "timestamp, event, owner, severity",
        "Output schema": "action, result, verification",
        "Eval policy": "fixed incident replay",
        "Type": "incident_response",
    }
    print_data_declaration("Lab 3 - Capstone Incident Response", declaration)

    timeline = [
        {"minute": 0, "event": "alert_triggered", "owner": "ops", "severity": "sev2"},
        {"minute": 6, "event": "domain_classified", "owner": "ml", "severity": "sev2"},
        {"minute": 14, "event": "fix_option_selected", "owner": "ic", "severity": "sev2"},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_incident_timeline.csv", timeline)

    rca = "# Lab 3 Root Cause Analysis\n\n- Primary cause: retrieval freshness lag created stale context.\n- Secondary cause: alert threshold too loose for freshness drift.\n- Corrective actions: tighten freshness gate and increase index refresh cadence.\n"
    write_text(RESULTS_DIR / "lab3_root_cause_analysis.md", rca)

    verify = [
        {"metric": "grounding_score", "before": 0.69, "after": 0.82, "delta": 0.13},
        {"metric": "failure_rate", "before": 0.031, "after": 0.015, "delta": -0.016},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_verification_rerun.csv", verify)

    print("[INFO] Lab 3 outputs written.")


if __name__ == "__main__":
    main()
