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

from stage16_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    resolve_project_profile,
    build_mastery_scorecard_rows,
    build_y_statement,
)


def main() -> None:
    project = resolve_project_profile()
    declaration = {
        "Data": "Synthetic portfolio evidence set",
        "Requests/Samples": "4 project evidence blocks",
        "Input schema": "artifact_type, summary, impact",
        "Output schema": "portfolio readiness index",
        "Eval policy": "fixed portfolio rubric",
        "Type": f"industry_portfolio_pack/{project}",
    }
    print_data_declaration("Lab 4 - Industry Project Portfolio Pack", declaration)

    write_text_dual(
        "lab4_portfolio_index.md",
        "# Portfolio Index\n\n1. Architecture review artifacts\n2. Incident command artifacts\n3. Governance audit artifacts\n4. Improvement loop artifacts\n",
    )

    write_text_dual(
        "lab4_case_study_summary.md",
        "# Case Study Summary\n\n- Project: AI trading assistant operations hardening.\n- Impact: lower failure rate and improved release confidence.\n",
    )

    matrix = [
        {"capability": "architecture_decision", "level": "advanced"},
        {"capability": "incident_command", "level": "advanced"},
        {"capability": "governance_audit", "level": "intermediate"},
        {"capability": "continuous_improvement", "level": "advanced"},
    ]
    write_rows_csv_dual("lab4_capability_matrix.csv", matrix)

    # Chapter-16 expert artifacts.
    write_rows_csv_dual("mastery_scorecard.csv", build_mastery_scorecard_rows(project))
    write_text_dual(
        "lab04_portfolio_evidence_pack.md",
        (
            "# Portfolio Evidence Pack\n\n"
            f"- Project context: `{project}`\n"
            "- Includes cumulative before/after deltas across staged improvements.\n"
            "- Includes architecture, incident, governance, and runtime efficiency evidence.\n"
            "- Ready for hiring/interview-level technical review.\n"
        ),
    )
    write_text_dual("lab04_final_y_statement.md", build_y_statement(project))


if __name__ == "__main__":
    main()
