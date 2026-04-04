"""
lab04_industry_project_portfolio_pack

Lab goal:
- Build hiring-ready portfolio evidence artifacts.
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
        "Data": "Synthetic portfolio evidence set",
        "Requests/Samples": "4 project evidence blocks",
        "Input schema": "artifact_type, summary, impact",
        "Output schema": "portfolio readiness index",
        "Eval policy": "fixed portfolio rubric",
        "Type": "industry_portfolio_pack",
    }
    print_data_declaration("Lab 4 - Industry Project Portfolio Pack", declaration)

    write_text(
        RESULTS_DIR / "lab4_portfolio_index.md",
        "# Portfolio Index\n\n1. Architecture review artifacts\n2. Incident command artifacts\n3. Governance audit artifacts\n4. Improvement loop artifacts\n",
    )

    write_text(
        RESULTS_DIR / "lab4_case_study_summary.md",
        "# Case Study Summary\n\n- Project: AI trading assistant operations hardening.\n- Impact: lower failure rate and improved release confidence.\n",
    )

    matrix = [
        {"capability": "architecture_decision", "level": "advanced"},
        {"capability": "incident_command", "level": "advanced"},
        {"capability": "governance_audit", "level": "intermediate"},
        {"capability": "continuous_improvement", "level": "advanced"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_capability_matrix.csv", matrix)


if __name__ == "__main__":
    main()
