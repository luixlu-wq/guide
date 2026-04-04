"""Stage 6 Topic 05: Eval metrics intermediate.

This script computes core agent metrics on a fixed eval set and adds
token-efficiency analysis:

Token Efficiency = total_tokens_used / successful_tool_calls
"""

from __future__ import annotations

from stage6_utils import (
    ensure_ticket_dataset,
    evaluate_predictions,
    load_eval_ids,
    load_ticket_rows,
    print_data_declaration,
    run_agent_loop,
    select_eval_tickets,
)


def estimate_tokens_for_output(output: dict) -> int:
    """Estimate token usage per case in a deterministic teaching-safe way."""
    # Approximate token load from:
    # 1) reply length
    # 2) tool calls (each tool call has overhead)
    reply_tokens = max(1, len(str(output.get("draft_reply", "")).split()))
    tool_calls = output.get("tool_calls", [])
    tool_overhead = 22 * len(tool_calls)
    return reply_tokens + tool_overhead


def successful_tool_calls(output: dict) -> int:
    """Count successful calls (all calls if no failure class)."""
    if output.get("failure_class"):
        return max(0, len(output.get("tool_calls", [])) - 1)
    return len(output.get("tool_calls", []))


def main() -> None:
    ensure_ticket_dataset()
    print_data_declaration("Topic05 Eval Metrics Intermediate")

    rows = load_ticket_rows()
    eval_ids = load_eval_ids()
    eval_rows = select_eval_tickets(rows, eval_ids)

    outputs = [run_agent_loop(row, max_steps=4) for row in eval_rows]
    metrics = evaluate_predictions(outputs)

    total_tokens_used = sum(estimate_tokens_for_output(out) for out in outputs)
    total_successful_tool_calls = sum(successful_tool_calls(out) for out in outputs)
    token_efficiency = (
        total_tokens_used / total_successful_tool_calls
        if total_successful_tool_calls > 0
        else float("inf")
    )

    print("\n=== Agent Evaluation Metrics ===")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
    print(f"total_tokens_used_est: {total_tokens_used}")
    print(f"successful_tool_calls: {total_successful_tool_calls}")
    print(f"token_efficiency_tokens_per_successful_tool_call: {token_efficiency:.4f}")

    print("\nInterpretation:")
    print("- Use these metrics as baseline for future regression checks.")
    print("- Never judge agent quality with only one metric.")
    print("- If token efficiency climbs over time, prompt/tool loop may be drifting.")


if __name__ == "__main__":
    main()

