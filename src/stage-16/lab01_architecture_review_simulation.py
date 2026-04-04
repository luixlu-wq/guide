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

from stage16_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    resolve_project_profile,
    build_system_mastery_rubric,
    build_dependency_risk_map,
)


def main() -> None:
    project = resolve_project_profile()
    declaration = {
        "Data": "Synthetic architecture alternatives",
        "Requests/Samples": "4 options",
        "Input schema": "option, quality, latency, cost, risk",
        "Output schema": "weighted_score and selected_option",
        "Eval policy": "fixed weighted scorecard",
        "Type": f"architecture_review/{project}",
    }
    print_data_declaration("Lab 1 - Architecture Review Simulation", declaration)

    options = [
        {"option": "pattern_a", "quality": 0.82, "latency": 0.76, "cost": 0.81, "risk": 0.74, "weighted_score": 0.78},
        {"option": "pattern_b", "quality": 0.85, "latency": 0.68, "cost": 0.74, "risk": 0.71, "weighted_score": 0.77},
        {"option": "pattern_c", "quality": 0.79, "latency": 0.88, "cost": 0.89, "risk": 0.80, "weighted_score": 0.84},
    ]
    write_rows_csv_dual("lab1_architecture_options.csv", options)

    matrix = [
        {"criterion": "quality", "weight": 0.35},
        {"criterion": "latency", "weight": 0.25},
        {"criterion": "cost", "weight": 0.20},
        {"criterion": "risk", "weight": 0.20},
    ]
    write_rows_csv_dual("lab1_tradeoff_matrix.csv", matrix)

    write_text_dual(
        "lab1_decision_record.md",
        "# Lab 1 Decision Record\n\n- Selected architecture: pattern_c\n- Reason: best weighted score under current operational constraints.\n",
    )

    # Chapter-16 expert artifacts.
    write_text_dual("system_mastery_rubric.md", build_system_mastery_rubric(project))
    write_text_dual("dependency_risk_map.md", build_dependency_risk_map())


if __name__ == "__main__":
    main()
