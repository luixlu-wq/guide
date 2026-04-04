"""
lab04_pattern_to_production

Lab goal:
- Move selected architecture from baseline to production decision.
- Produce release decision and rollback artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage12_utils import RESULTS_DIR, build_delta_rows, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic baseline and improved architecture KPI snapshots",
        "Requests/Samples": "fixed evaluation windows",
        "Input schema": "quality, latency, cost, failure_rate",
        "Output schema": "comparison + release decision + rollback plan",
        "Eval policy": "same gates before and after",
        "Type": "pattern to production",
    }
    print_data_declaration("Lab 4 - Pattern to Production", declaration)

    base = {"quality_score": 0.79, "latency_p95_ms": 730.0, "cost_index": 1.50, "failure_rate": 0.021}
    improved = {"quality_score": 0.86, "latency_p95_ms": 640.0, "cost_index": 1.42, "failure_rate": 0.012}

    write_rows_csv(RESULTS_DIR / "lab4_baseline_metrics.csv", [base])
    write_rows_csv(RESULTS_DIR / "lab4_improved_metrics.csv", [improved])
    write_rows_csv(RESULTS_DIR / "lab4_metrics_comparison.csv", build_delta_rows(base, improved))

    promote = improved["quality_score"] >= 0.84 and improved["failure_rate"] <= 0.015
    decision = "promote" if promote else "hold"

    decision_md = [
        "# Lab 4 Release Decision",
        "",
        f"- Decision: {decision}",
        "- Gate checks:",
        f"  - quality >= 0.84: {improved['quality_score'] >= 0.84}",
        f"  - failure_rate <= 0.015: {improved['failure_rate'] <= 0.015}",
        "- Deployment strategy: canary first, then phased rollout.",
    ]
    write_text(RESULTS_DIR / "lab4_release_decision.md", "\n".join(decision_md))

    rollback = [
        "# Lab 4 Rollback Plan",
        "",
        "- Trigger rollback if quality_score drops below 0.80 for 2 windows.",
        "- Trigger rollback if failure_rate exceeds 0.02 for 2 windows.",
        "- Revert to previous architecture profile and fixed config snapshot.",
        "- Re-run fixed regression set before re-promotion.",
    ]
    write_text(RESULTS_DIR / "lab4_rollback_plan.md", "\n".join(rollback))

    print("[INFO] Lab 4 outputs written:")
    print("- results/lab4_baseline_metrics.csv")
    print("- results/lab4_improved_metrics.csv")
    print("- results/lab4_metrics_comparison.csv")
    print("- results/lab4_release_decision.md")
    print("- results/lab4_rollback_plan.md")


if __name__ == "__main__":
    main()

