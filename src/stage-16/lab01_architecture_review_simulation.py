"""
lab01_architecture_review_simulation

Lab goal:
- Run an architecture review and produce decision artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage16_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic architecture alternatives",
        "Requests/Samples": "4 options",
        "Input schema": "option, quality, latency, cost, risk",
        "Output schema": "weighted_score and selected_option",
        "Eval policy": "fixed weighted scorecard",
        "Type": "architecture_review",
    }
    print_data_declaration("Lab 1 - Architecture Review Simulation", declaration)

    options = [
        {"option": "pattern_a", "quality": 0.82, "latency": 0.76, "cost": 0.81, "risk": 0.74, "weighted_score": 0.78},
        {"option": "pattern_b", "quality": 0.85, "latency": 0.68, "cost": 0.74, "risk": 0.71, "weighted_score": 0.77},
        {"option": "pattern_c", "quality": 0.79, "latency": 0.88, "cost": 0.89, "risk": 0.80, "weighted_score": 0.84},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_architecture_options.csv", options)

    matrix = [
        {"criterion": "quality", "weight": 0.35},
        {"criterion": "latency", "weight": 0.25},
        {"criterion": "cost", "weight": 0.20},
        {"criterion": "risk", "weight": 0.20},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_tradeoff_matrix.csv", matrix)

    write_text(
        RESULTS_DIR / "lab1_decision_record.md",
        "# Lab 1 Decision Record\n\n- Selected architecture: pattern_c\n- Reason: best weighted score under current operational constraints.\n",
    )


if __name__ == "__main__":
    main()
