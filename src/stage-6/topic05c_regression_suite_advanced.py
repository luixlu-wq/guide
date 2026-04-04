"""Stage 6 Topic 05C: Regression suite advanced.

This script compares baseline and constrained agent configs and applies a
simple promotion gate.
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
print_data_declaration("Topic05C Regression Suite Advanced")

rows = load_ticket_rows()
eval_rows = select_eval_tickets(rows, load_eval_ids())

baseline_outputs = [run_agent_loop(row, max_steps=4) for row in eval_rows]
variant_outputs = [run_agent_loop(row, max_steps=2) for row in eval_rows]

baseline = evaluate_predictions(baseline_outputs)
variant = evaluate_predictions(variant_outputs)

# Promotion gate example: block if failure_rate worsens by more than 0.05.
delta_failure = variant["failure_rate"] - baseline["failure_rate"]
promote = delta_failure <= 0.05

print("\n=== Baseline Metrics ===")
for k, v in baseline.items():
    print(f"{k}: {v:.4f}")

print("\n=== Variant Metrics ===")
for k, v in variant.items():
    print(f"{k}: {v:.4f}")

print("\n=== Regression Gate ===")
print(f"delta_failure_rate={delta_failure:.4f}")
print(f"promotion_allowed={promote}")

print("\nAdvanced note:")
print("- Promotion gates prevent unsafe regressions from reaching production.")
