"""
lab01_pattern_baseline_compare

Lab goal:
- Compare architecture patterns on fixed evaluation criteria.
- Produce pattern metrics and tradeoff matrix artifacts.
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
        "Data": "Fixed synthetic architecture evaluation set",
        "Requests/Samples": "180 cases",
        "Input schema": "query, expected_pattern, complexity",
        "Output schema": "quality_score, latency_p95_ms, cost_index, failure_rate",
        "Eval policy": "same dataset and same scoring logic",
        "Type": "pattern baseline compare",
    }
    print_data_declaration("Lab 1 - Pattern Baseline Compare", declaration)

    rows = [
        {"pattern": "llm_app", "quality_score": 0.74, "latency_p95_ms": 380.0, "cost_index": 1.0, "failure_rate": 0.023},
        {"pattern": "rag", "quality_score": 0.81, "latency_p95_ms": 520.0, "cost_index": 1.4, "failure_rate": 0.019},
        {"pattern": "agent", "quality_score": 0.78, "latency_p95_ms": 690.0, "cost_index": 1.8, "failure_rate": 0.025},
        {"pattern": "multi_agent", "quality_score": 0.80, "latency_p95_ms": 820.0, "cost_index": 2.2, "failure_rate": 0.028},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_pattern_metrics.csv", rows)
    # Compatibility alias for runbook naming.
    write_rows_csv(RESULTS_DIR / "pattern_baseline_table.csv", rows)

    matrix = [
        {"criterion": "knowledge_freshness_need", "llm_app": 2, "rag": 5, "agent": 4, "multi_agent": 4},
        {"criterion": "tool_action_need", "llm_app": 1, "rag": 2, "agent": 5, "multi_agent": 5},
        {"criterion": "latency_sensitivity", "llm_app": 5, "rag": 4, "agent": 2, "multi_agent": 1},
        {"criterion": "operational_complexity_tolerance", "llm_app": 5, "rag": 4, "agent": 2, "multi_agent": 1},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_tradeoff_matrix.csv", matrix)

    summary = [
        "# Lab 1 Pattern Summary",
        "",
        "- Best simple latency path: LLM app",
        "- Best grounded knowledge path: RAG",
        "- Best dynamic action path: agent",
        "- Multi-agent only when role separation is clearly justified",
    ]
    write_text(RESULTS_DIR / "lab1_pattern_summary.md", "\n".join(summary))
    # Compatibility alias for runbook naming.
    write_text(RESULTS_DIR / "initial_decision.md", "\n".join(summary))

    print("[INFO] Lab 1 outputs written:")
    print("- results/lab1_pattern_metrics.csv")
    print("- results/lab1_tradeoff_matrix.csv")
    print("- results/lab1_pattern_summary.md")
    print("- results/pattern_baseline_table.csv")
    print("- results/initial_decision.md")


if __name__ == "__main__":
    main()
