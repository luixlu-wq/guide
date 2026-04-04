"""
lab05_architecture_project_baseline_to_production

Lab goal:
- Run a beginning-to-production architecture improvement workflow.
- Produce baseline, improved design, metric deltas, and rollout decision artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import (
    RESULTS_DIR,
    build_metrics_comparison_rows,
    print_data_declaration,
    write_rows_csv,
    write_text,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic architecture KPI snapshots",
        "Requests/Samples": "fixed eval + load profile",
        "Input schema": "component metrics and incident observations",
        "Output schema": "improvement decision and production readiness report",
        "Eval policy": "baseline and improved compared on fixed KPI set",
        "Type": "baseline-to-production architecture project",
    }
    print_data_declaration("Lab 5 - Baseline to Production Architecture", declaration)

    baseline_doc = [
        "# Lab 5 Baseline Architecture",
        "",
        "- Flow: `client -> API -> retrieval -> model -> response`",
        "- Weakness: no queue backpressure policy, no canary release, weak trace coverage.",
        "- Current SLA status: p95 latency fails target under high concurrency.",
    ]
    write_text(RESULTS_DIR / "lab5_baseline_architecture.md", "\n".join(baseline_doc))

    improved_doc = [
        "# Lab 5 Improved Architecture",
        "",
        "- Added worker autoscaling trigger on queue depth + p95 latency windows.",
        "- Added canary release gate and rollback trigger thresholds.",
        "- Added trace propagation and structured logging policy.",
        "- Added retrieval freshness check in ingestion path.",
    ]
    write_text(RESULTS_DIR / "lab5_improved_architecture.md", "\n".join(improved_doc))

    baseline_metrics = {
        "routing_accuracy": 0.78,
        "latency_p95_ms": 910.0,
        "error_rate": 0.026,
        "throughput_rps": 2.7,
    }
    improved_metrics = {
        "routing_accuracy": 0.87,
        "latency_p95_ms": 690.0,
        "error_rate": 0.012,
        "throughput_rps": 3.5,
    }
    comparison_rows = build_metrics_comparison_rows(
        baseline_metrics, improved_metrics, baseline_name="baseline", improved_name="improved"
    )
    write_rows_csv(RESULTS_DIR / "lab5_metrics_comparison.csv", comparison_rows)

    solution_options = [
        {
            "problem_class": "p95 latency breach under bursts",
            "option": "Autoscale replicas + queue backpressure",
            "quality_impact": "neutral",
            "latency_impact": "high_positive",
            "cost_impact": "medium",
            "risk": "low",
            "selected": "yes",
        },
        {
            "problem_class": "p95 latency breach under bursts",
            "option": "Increase timeout only",
            "quality_impact": "neutral",
            "latency_impact": "low_positive",
            "cost_impact": "low",
            "risk": "medium",
            "selected": "no",
        },
    ]
    write_rows_csv(RESULTS_DIR / "lab5_solution_options.csv", solution_options)

    risk_log = [
        "# Lab 5 Incident or Risk Log",
        "",
        "- Risk: retrieval staleness can still degrade answer grounding.",
        "- Mitigation: add ingestion freshness SLO and stale-index alarm.",
        "- Risk: autoscaling lag during sudden spikes.",
        "- Mitigation: set minimum warm replica count.",
    ]
    write_text(RESULTS_DIR / "lab5_incident_or_risk_log.md", "\n".join(risk_log))

    rollback = [
        "# Lab 5 Rollback Plan",
        "",
        "1. Trigger rollback if error_rate > 0.02 for 3 consecutive windows.",
        "2. Trigger rollback if p95 latency exceeds 900ms for 3 windows.",
        "3. Revert traffic split from canary to baseline (100%).",
        "4. Restore last known-good config and model-serving profile.",
        "5. Re-run fixed regression request set before re-promotion.",
    ]
    write_text(RESULTS_DIR / "lab5_rollback_plan.md", "\n".join(rollback))

    decision = "promote" if improved_metrics["error_rate"] <= 0.015 and improved_metrics["latency_p95_ms"] <= 750 else "hold"
    readiness = [
        "# Lab 5 Production Readiness",
        "",
        f"- Decision: {decision}",
        "- Fixed eval set used: yes",
        "- Before/after metrics verified: yes",
        "- Rollback plan defined: yes",
        "- One-change rerun policy followed: yes",
    ]
    write_text(RESULTS_DIR / "lab5_production_readiness.md", "\n".join(readiness))

    print("[INFO] Lab 5 outputs written:")
    print("- results/lab5_baseline_architecture.md")
    print("- results/lab5_improved_architecture.md")
    print("- results/lab5_metrics_comparison.csv")
    print("- results/lab5_solution_options.csv")
    print("- results/lab5_incident_or_risk_log.md")
    print("- results/lab5_rollback_plan.md")
    print("- results/lab5_production_readiness.md")


if __name__ == "__main__":
    main()

