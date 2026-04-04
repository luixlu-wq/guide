"""Stage 6 Topic 05: Eval metrics intermediate.

This script computes core agent metrics on a fixed eval set.
"""

from stage6_utils import (
    ensure_ticket_dataset,
    evaluate_predictions,
    load_eval_ids,
    load_ticket_rows,
    print_data_declaration,
    run_agent_loop,
    select_eval_tickets,
)


ensure_ticket_dataset()
print_data_declaration("Topic05 Eval Metrics Intermediate")

rows = load_ticket_rows()
eval_ids = load_eval_ids()
eval_rows = select_eval_tickets(rows, eval_ids)

outputs = [run_agent_loop(row, max_steps=4) for row in eval_rows]
metrics = evaluate_predictions(outputs)

print("\n=== Agent Evaluation Metrics ===")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")

print("\nInterpretation:")
print("- Use these metrics as baseline for future regression checks.")
print("- Never judge agent quality with only one metric.")
