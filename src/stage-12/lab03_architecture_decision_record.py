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
    # Compatibility alias for runbook naming.
    write_rows_csv(RESULTS_DIR / "scorecard.csv", scores)

    # Expert-tier threshold-aware scorecard for release governance.
    threshold_scorecard = [
        {"option": "llm_app", "weighted_score": 0.80, "pass_threshold_0_80": True, "rollback_trigger_defined": True},
        {"option": "rag", "weighted_score": 0.82, "pass_threshold_0_80": True, "rollback_trigger_defined": True},
        {"option": "agent", "weighted_score": 0.73, "pass_threshold_0_80": False, "rollback_trigger_defined": True},
        {"option": "multi_agent", "weighted_score": 0.69, "pass_threshold_0_80": False, "rollback_trigger_defined": True},
    ]
    write_rows_csv(RESULTS_DIR / "adr_scorecard_with_thresholds.csv", threshold_scorecard)

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
    # Compatibility alias for runbook naming.
    write_text(RESULTS_DIR / "final_adr.md", "\n".join(adr))

    y_statement = [
        "# Architecture Decision Y-Statement",
        "",
        "In the context of MapToGo + Ontario GIS support workflows,",
        "we decided to use RAG to handle grounded, freshness-sensitive knowledge requests,",
        "because it outperformed alternatives on weighted quality-risk score and remains operationally simpler than full multi-agent routing,",
        "and measured p95 latency stayed within the defined release budget.",
    ]
    write_text(RESULTS_DIR / "architecture_decision_y_statement.md", "\n".join(y_statement))

    print("[INFO] Lab 3 outputs written:")
    print("- results/lab3_decision_scores.csv")
    print("- results/lab3_adr.md")
    print("- results/scorecard.csv")
    print("- results/final_adr.md")
    print("- results/adr_scorecard_with_thresholds.csv")
    print("- results/architecture_decision_y_statement.md")


if __name__ == "__main__":
    main()
