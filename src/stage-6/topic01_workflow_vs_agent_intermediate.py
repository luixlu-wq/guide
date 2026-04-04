"""Stage 6 Topic 01: Workflow vs Agent (intermediate).

This script compares two execution styles on the same fixed evaluation subset:
1) deterministic workflow baseline
2) bounded agent loop

The goal is to show measurable tradeoffs, not only conceptual differences.
"""

from stage6_utils import (
    ensure_ticket_dataset,
    evaluate_predictions,
    load_eval_ids,
    load_ticket_rows,
    print_data_declaration,
    run_agent_loop,
    run_workflow_baseline,
    select_eval_tickets,
)


# Create deterministic dataset/eval IDs for reproducible comparisons.
_, _ = ensure_ticket_dataset()
print_data_declaration("Topic01 Workflow vs Agent Intermediate")

# Load fixed evaluation subset.
rows = load_ticket_rows()
eval_ids = load_eval_ids()
eval_rows = select_eval_tickets(rows, eval_ids)

# Run both systems on identical inputs.
workflow_outputs = [run_workflow_baseline(row) for row in eval_rows]
agent_outputs = [run_agent_loop(row, max_steps=4) for row in eval_rows]

# Evaluate both systems with the same metric function.
workflow_metrics = evaluate_predictions(workflow_outputs)
agent_metrics = evaluate_predictions(agent_outputs)

print("\n=== Workflow Metrics ===")
for k, v in workflow_metrics.items():
    print(f"{k}: {v:.4f}")

print("\n=== Agent Metrics ===")
for k, v in agent_metrics.items():
    print(f"{k}: {v:.4f}")

print("\nInterpretation guide:")
print("- Workflow usually has lower orchestration complexity.")
print("- Agent loops may increase steps and flexibility.")
print("- Use fixed metrics to justify architecture choice.")
