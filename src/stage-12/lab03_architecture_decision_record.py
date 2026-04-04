"""
lab03_architecture_decision_record

Lab goal:
- Generate an ADR with scored alternatives and explicit decision criteria.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage12_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic architecture scorecard inputs",
        "Requests/Samples": "4 architecture options",
        "Input schema": "option, quality, latency, cost, risk",
        "Output schema": "weighted_score and selected option",
        "Eval policy": "fixed weighting policy",
        "Type": "architecture decision record",
    }
    print_data_declaration("Lab 3 - Architecture Decision Record", declaration)

    scores = [
        {"option": "llm_app", "quality": 0.74, "latency": 0.90, "cost": 0.92, "risk": 0.70, "weighted_score": 0.80},
        {"option": "rag", "quality": 0.86, "latency": 0.76, "cost": 0.80, "risk": 0.78, "weighted_score": 0.82},
        {"option": "agent", "quality": 0.83, "latency": 0.62, "cost": 0.68, "risk": 0.64, "weighted_score": 0.73},
        {"option": "multi_agent", "quality": 0.84, "latency": 0.54, "cost": 0.58, "risk": 0.60, "weighted_score": 0.69},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_decision_scores.csv", scores)

    adr = [
        "# ADR-001: Pattern Choice for Knowledge Assistant",
        "",
        "## Context",
        "- Need grounded answers over changing internal documentation.",
        "- Must keep p95 latency under 700ms where possible.",
        "",
        "## Options",
        "- llm_app",
        "- rag",
        "- agent",
        "- multi_agent",
        "",
        "## Decision",
        "- Selected: rag",
        "- Reason: best weighted score under quality + operational constraints.",
        "",
        "## Risks",
        "- retrieval freshness drift",
        "- index maintenance overhead",
        "",
        "## Rollback trigger",
        "- grounding score < 0.75 for 3 windows",
        "",
        "## Validation plan",
        "- fixed eval replay weekly",
        "- incident drill monthly",
    ]
    write_text(RESULTS_DIR / "lab3_adr.md", "\n".join(adr))

    print("[INFO] Lab 3 outputs written:")
    print("- results/lab3_decision_scores.csv")
    print("- results/lab3_adr.md")


if __name__ == "__main__":
    main()

