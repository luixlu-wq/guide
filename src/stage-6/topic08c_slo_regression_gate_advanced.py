"""Stage 6 Topic 08C: SLO regression gate advanced.

This script demonstrates:
1) classical SLO pass/fail gate
2) orchestration-divergence detection ("ghost in the loop")
3) max-self-correction and backoff prompt policy trigger
"""

from __future__ import annotations

from stage6_utils import print_data_declaration


def detect_repeated_tool_signatures(signatures: list[str], repeat_threshold: int = 3) -> bool:
    """Detect repeated bad-loop pattern from tool-call signatures."""
    if len(signatures) < repeat_threshold:
        return False
    last = signatures[-1]
    streak = 1
    for i in range(len(signatures) - 2, -1, -1):
        if signatures[i] == last:
            streak += 1
        else:
            break
    return streak >= repeat_threshold


def main() -> None:
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

    base_gate_passed = (
        candidate_metrics["task_success_rate"] >= slo["task_success_rate_min"]
        and candidate_metrics["failure_rate"] <= slo["failure_rate_max"]
        and candidate_metrics["p95_latency_ms"] <= slo["p95_latency_ms_max"]
        and candidate_metrics["cost_per_task"] <= slo["cost_per_task_max"]
    )

    # Simulated agent loop trace signatures:
    # "tool_name|normalized_arg_fingerprint"
    tool_call_signatures = [
        "retrieve_policy|ticket=TKT-1001",
        "retrieve_policy|ticket=TKT-1001",
        "retrieve_policy|ticket=TKT-1001",
        "retrieve_policy|ticket=TKT-1001",
    ]

    max_self_correction = 3
    repeated_loop = detect_repeated_tool_signatures(tool_call_signatures, repeat_threshold=max_self_correction)
    backoff_prompt_triggered = repeated_loop
    final_gate_passed = base_gate_passed and (not repeated_loop)

    print("\nSLO targets:")
    print(slo)

    print("\nCandidate metrics:")
    print(candidate_metrics)

    print("\nLoop-divergence checks:")
    print(f"tool_call_signatures={tool_call_signatures}")
    print(f"max_self_correction={max_self_correction}")
    print(f"repeated_loop_detected={repeated_loop}")
    print(f"backoff_prompt_triggered={backoff_prompt_triggered}")

    print(f"\nbase_release_gate_passed={base_gate_passed}")
    print(f"final_release_gate_passed={final_gate_passed}")

    if backoff_prompt_triggered:
        print("\nBackoff prompt example:")
        print(
            "Re-read system instructions. Stop repeating the same tool call. "
            "Either choose a different tool or ask for clarification."
        )

    print("\nAdvanced note:")
    print("- Release gates should include loop-divergence controls, not only quality/cost thresholds.")


if __name__ == "__main__":
    main()

