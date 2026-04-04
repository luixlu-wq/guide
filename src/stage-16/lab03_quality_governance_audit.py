"""
lab03_quality_governance_audit

Lab goal:
- Audit system quality and governance controls.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage16_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    build_compute_efficiency_rows,
    build_power_perf_curve_rows,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic governance checklist",
        "Requests/Samples": "12 controls",
        "Input schema": "control, target, observed",
        "Output schema": "pass_or_fail",
        "Eval policy": "fixed audit procedure",
        "Type": "quality_governance_audit",
    }
    print_data_declaration("Lab 3 - Quality Governance Audit", declaration)

    checklist = [
        {"control": "input_schema_validation", "target": "enabled", "observed": "enabled", "pass_or_fail": "pass"},
        {"control": "output_policy_check", "target": "enabled", "observed": "enabled", "pass_or_fail": "pass"},
        {"control": "run_id_traceability", "target": "100%", "observed": "96%", "pass_or_fail": "warn"},
    ]
    write_rows_csv_dual("lab3_audit_checklist.csv", checklist)

    risks = [
        {"risk": "trace_gap", "severity": "medium", "mitigation": "enforce correlation-id middleware"},
        {"risk": "stale_index_window", "severity": "high", "mitigation": "tighten reindex policy"},
    ]
    write_rows_csv_dual("lab3_risk_register.csv", risks)

    write_text_dual(
        "lab3_audit_recommendation.md",
        "# Lab 3 Audit Recommendation\n\n- Decision: hold until traceability reaches 99% and freshness controls are tightened.\n",
    )

    # Chapter-16 compute governance artifacts.
    write_rows_csv_dual("compute_efficiency_report.csv", build_compute_efficiency_rows())
    write_rows_csv_dual("power_perf_curve.csv", build_power_perf_curve_rows())


if __name__ == "__main__":
    main()
