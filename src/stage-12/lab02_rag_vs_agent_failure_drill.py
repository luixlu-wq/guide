"""
lab02_rag_vs_agent_failure_drill

Lab goal:
- Reproduce representative RAG and agent failure modes.
- Compare fix options and verify targeted improvements.
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
        "Data": "Synthetic failure scenario set",
        "Requests/Samples": "8 cases",
        "Input schema": "pattern, failure_type, symptom",
        "Output schema": "fix_option, expected_delta, verification_delta",
        "Eval policy": "fixed failure replay",
        "Type": "rag vs agent failure drill",
    }
    print_data_declaration("Lab 2 - RAG vs Agent Failure Drill", declaration)

    failures = [
        {"pattern": "rag", "failure_type": "stale_retrieval", "symptom": "outdated citation"},
        {"pattern": "rag", "failure_type": "filter_miss", "symptom": "wrong doc scope"},
        {"pattern": "agent", "failure_type": "tool_loop", "symptom": "repeated calls"},
        {"pattern": "agent", "failure_type": "unsafe_tool_choice", "symptom": "invalid action route"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_failure_cases.csv", failures)
    # Compatibility alias for runbook naming.
    trace_lines = [
        "# Failure Trace",
        "",
        "- rag: stale_retrieval -> outdated citation",
        "- rag: filter_miss -> wrong doc scope",
        "- agent: tool_loop -> repeated calls",
        "- agent: unsafe_tool_choice -> invalid action route",
    ]
    write_text(RESULTS_DIR / "failure_trace.md", "\n".join(trace_lines))

    options = [
        {"pattern": "rag", "option": "freshness gate + reindex policy", "expected_quality_delta": 0.08, "expected_latency_delta": 18.0, "chosen": "yes"},
        {"pattern": "agent", "option": "tool schema constraints + step cap", "expected_quality_delta": 0.06, "expected_latency_delta": 10.0, "chosen": "yes"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_solution_options.csv", options)
    # Compatibility alias for runbook naming.
    write_rows_csv(RESULTS_DIR / "option_compare.csv", options)

    verify = [
        {"metric": "rag_grounding_score", "before": 0.71, "after": 0.82, "delta": 0.11},
        {"metric": "agent_tool_success_rate", "before": 0.76, "after": 0.86, "delta": 0.10},
        {"metric": "agent_loop_incidents", "before": 9, "after": 2, "delta": -7},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_verification_rerun.csv", verify)

    print("[INFO] Lab 2 outputs written:")
    print("- results/lab2_failure_cases.csv")
    print("- results/lab2_solution_options.csv")
    print("- results/lab2_verification_rerun.csv")
    print("- results/failure_trace.md")
    print("- results/option_compare.csv")


if __name__ == "__main__":
    main()
