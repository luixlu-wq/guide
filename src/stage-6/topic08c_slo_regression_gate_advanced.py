"""Stage 6 Topic 08C: SLO regression gate advanced.

This script demonstrates service-level objective checks before promotion.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic08C SLO Regression Gate Advanced")

slo = {
    "task_success_rate_min": 0.90,
    "failure_rate_max": 0.08,
    "p95_latency_ms_max": 1500,
    "cost_per_task_max": 0.035,
}

candidate_metrics = {
    "task_success_rate": 0.93,
    "failure_rate": 0.05,
    "p95_latency_ms": 1400,
    "cost_per_task": 0.031,
}

passes = (
    candidate_metrics["task_success_rate"] >= slo["task_success_rate_min"]
    and candidate_metrics["failure_rate"] <= slo["failure_rate_max"]
    and candidate_metrics["p95_latency_ms"] <= slo["p95_latency_ms_max"]
    and candidate_metrics["cost_per_task"] <= slo["cost_per_task_max"]
)

print("\nSLO targets:")
print(slo)

print("\nCandidate metrics:")
print(candidate_metrics)

print(f"\nrelease_gate_passed={passes}")

print("\nAdvanced note:")
print("- Release gates convert reliability requirements into enforceable checks.")
