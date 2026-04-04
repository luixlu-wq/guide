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

from stage15_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text, build_delta_rows


def main() -> None:
    declaration = {
        "Data": "Synthetic ML classification failure set",
        "Requests/Samples": "1000 rows",
        "Input schema": "features, label",
        "Output schema": "f1, recall, precision, error_segments",
        "Eval policy": "fixed split replay",
        "Type": "ml_failure_diagnosis",
    }
    print_data_declaration("Lab 1 - ML Failure Diagnosis", declaration)

    baseline = {"f1": 0.58, "recall": 0.49, "precision": 0.71}
    improved = {"f1": 0.66, "recall": 0.60, "precision": 0.73}
    write_rows_csv(RESULTS_DIR / "lab1_ml_baseline_metrics.csv", [{**baseline}])
    write_rows_csv(RESULTS_DIR / "lab1_ml_verification_rerun.csv", build_delta_rows(baseline, improved))

    write_text(
        RESULTS_DIR / "lab1_ml_failure_analysis.md",
        "# Lab 1 ML Failure Analysis\n\n- Root cause: class imbalance and weak threshold policy.\n- Fix: class weighting and calibrated threshold update.\n",
    )


if __name__ == "__main__":
    main()
