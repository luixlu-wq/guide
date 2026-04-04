"""Stage 6 Topic 01A: Workflow-first simple baseline.

This script demonstrates why deterministic workflow should be implemented before agent loops.
The output is intentionally transparent and fully deterministic for beginner understanding.
"""

from stage6_utils import ensure_ticket_dataset, load_ticket_rows, print_data_declaration, run_workflow_baseline


# Step 1: Ensure fixed dataset exists so all learners run the same data.
ensure_ticket_dataset()

# Step 2: Print explicit schema declaration required by plan rules.
print_data_declaration("Topic01A Workflow First Simple")

# Step 3: Load sample records and run deterministic baseline pipeline.
rows = load_ticket_rows()[:5]
outputs = [run_workflow_baseline(row) for row in rows]

print("\n=== Workflow Baseline Outputs (first 5 tickets) ===")
for item in outputs:
    # Print each key result field so learners can inspect pipeline behavior.
    print(
        f"ticket={item['ticket_id']} | priority={item['predicted_priority']} | "
        f"queue={item['queue']} | human_approval={item['needs_human_approval']}"
    )

print("\nExpected interpretation:")
print("- This baseline is stable and easy to test.")
print("- We will compare agent variants against this exact workflow behavior.")
