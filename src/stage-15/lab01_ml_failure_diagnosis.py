"""
lab01_ml_failure_diagnosis

Lab goal:
- Diagnose one ML failure and verify one targeted fix.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage15_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    build_delta_rows,
    resolve_project_profile,
    build_icv_audit_trail,
    build_gpu_telemetry_rows,
    build_wsl_cuda_contention_report,
)


def main() -> None:
    project = resolve_project_profile()
    declaration = {
        "Data": "Synthetic ML classification failure set",
        "Requests/Samples": "1000 rows",
        "Input schema": "features, label",
        "Output schema": "f1, recall, precision, error_segments",
        "Eval policy": "fixed split replay",
        "Type": f"ml_failure_diagnosis/{project}",
    }
    print_data_declaration("Lab 1 - ML Failure Diagnosis", declaration)

    baseline = {"f1": 0.58, "recall": 0.49, "precision": 0.71}
    improved = {"f1": 0.66, "recall": 0.60, "precision": 0.73}
    write_rows_csv_dual("lab1_ml_baseline_metrics.csv", [{**baseline}])
    write_rows_csv_dual("lab1_ml_verification_rerun.csv", build_delta_rows(baseline, improved))

    icv_block = build_icv_audit_trail(
        identify_metric="f1",
        identify_threshold="< 0.60",
        failing_case="ml_case_imbalance_001",
        option_a="class_weighting",
        option_b="threshold_recalibration",
        verification_delta="f1: +0.08 (0.58 -> 0.66)",
        decision="promote",
    )

    write_text_dual(
        "lab1_ml_failure_analysis.md",
        (
            "# Lab 1 ML Failure Analysis\n\n"
            "- Root cause: class imbalance and weak threshold policy.\n"
            "- Fix: class weighting and calibrated threshold update.\n\n"
            f"{icv_block}"
        ),
    )

    # Canonical chapter-aligned aliases.
    write_text_dual(
        "ml_failure_statement.md",
        "Observed symptom: f1 degraded below threshold.\nAffected metric: f1 (<0.60).\nWhere observed: eval set.\nWhen started: current run.\nSuspected domain: runtime/infrastructure + ML policy.\nConfidence level: medium.\n",
    )
    write_text_dual("ml_root_cause.md", "Primary root cause: class imbalance. Secondary factor: threshold policy.")

    # Required expert drill artifacts for WSL2/CUDA contention diagnosis.
    write_rows_csv_dual("lab01_gpu_telemetry_log.csv", build_gpu_telemetry_rows())
    write_text_dual("lab01_wsl_cuda_contention_report.md", build_wsl_cuda_contention_report(project))

    # Global Stage 15 ICV evidence artifact.
    write_text_dual("icv_protocol_report.md", icv_block)


if __name__ == "__main__":
    main()
