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

from stage13_utils import print_data_declaration, write_rows_csv_dual, write_text_dual


def main() -> None:
    declaration = {
        "Data": "Synthetic semantic-drift incident trace",
        "Requests/Samples": "1 incident replay with fixed timeline",
        "Input schema": "timestamp, trace_id, event, owner, severity, failure_class",
        "Output schema": "action, result, verification, rollback_decision",
        "Eval policy": "fixed incident replay with same eval profile",
        "Type": "incident_response/semantic_drift",
    }
    print_data_declaration("Lab 3 - Capstone Incident Response", declaration)

    timeline = [
        {"minute": 0, "trace_id": "t-13-0001", "event": "alert_triggered", "owner": "ops", "severity": "sev2", "failure_class": "semantic_drift"},
        {"minute": 5, "trace_id": "t-13-0001", "event": "retrieval_drop_detected", "owner": "retrieval", "severity": "sev2", "failure_class": "semantic_drift"},
        {"minute": 9, "trace_id": "t-13-0001", "event": "otlp_trace_review", "owner": "ops", "severity": "sev2", "failure_class": "semantic_drift"},
        {"minute": 14, "trace_id": "t-13-0001", "event": "fix_option_selected", "owner": "ic", "severity": "sev2", "failure_class": "semantic_drift"},
        {"minute": 21, "trace_id": "t-13-0001", "event": "candidate_patch_applied", "owner": "ml", "severity": "sev2", "failure_class": "semantic_drift"},
        {"minute": 28, "trace_id": "t-13-0001", "event": "verification_passed", "owner": "ic", "severity": "sev2", "failure_class": "semantic_drift"},
    ]
    write_rows_csv_dual("lab3_incident_timeline.csv", timeline)

    rca = (
        "# Lab 3 Root Cause Analysis\n\n"
        "- Primary cause: semantic drift after boundary-data ingestion changed chunk distribution.\n"
        "- Secondary cause: retrieval chunking strategy was not validated against new schema shape.\n"
        "- Corrective actions: rebuild chunking profile, rerun fixed eval set, and tighten drift alert policy.\n"
    )
    write_text_dual("lab3_root_cause_analysis.md", rca)

    verify = [
        {"metric": "grounding_score", "before": 0.69, "after": 0.83, "delta": 0.14},
        {"metric": "failure_rate", "before": 0.031, "after": 0.014, "delta": -0.017},
        {"metric": "retrieval_hit_rate", "before": 0.61, "after": 0.79, "delta": 0.18},
    ]
    write_rows_csv_dual("lab3_verification_rerun.csv", verify)

    semantic_report = (
        "# Semantic Drift Incident Report\n\n"
        "- Incident class: `semantic_drift`\n"
        "- Trigger: new municipal boundary ingestion without chunk profile update\n"
        "- Detection evidence: OpenTelemetry retrieval spans showed context miss spike\n"
        "- Resolution: apply schema-aware chunking, rebuild index, verify on fixed replay set\n"
        "- Decision: hold release until rerun delta meets gate thresholds\n"
    )
    write_text_dual("semantic_drift_incident_report.md", semantic_report)

    trace_evidence = (
        "# Semantic Drift Trace Evidence\n\n"
        "Trace: `t-13-0001`\n\n"
        "| Span | p95 latency (ms) | Context relevance |\n"
        "|---|---:|---:|\n"
        "| retrieval_before | 148 | 0.58 |\n"
        "| retrieval_after  | 121 | 0.81 |\n"
        "| generation_after | 263 | 0.84 |\n"
    )
    write_text_dual("semantic_drift_trace_evidence.md", trace_evidence)

    print("[INFO] Lab 3 outputs written.")


if __name__ == "__main__":
    main()
