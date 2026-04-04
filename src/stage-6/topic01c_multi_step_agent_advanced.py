"""Stage 6 Topic 01C: Multi-step agent advanced.

This advanced example demonstrates how bounded step limits affect reliability.
We intentionally run one good configuration and one constrained configuration.
"""

from stage6_utils import ensure_ticket_dataset, load_ticket_rows, print_data_declaration, run_agent_loop


ensure_ticket_dataset()
print_data_declaration("Topic01C Multi-step Agent Advanced")

rows = load_ticket_rows()[:6]

# Configuration A: sufficient max_steps, should avoid artificial step-limit failures.
safe_outputs = [run_agent_loop(row, max_steps=4) for row in rows]

# Configuration B: insufficient max_steps, intentionally triggers controlled failure class.
constrained_outputs = [run_agent_loop(row, max_steps=2) for row in rows]

safe_failures = sum(1 for row in safe_outputs if row.get("failure_class"))
constrained_failures = sum(1 for row in constrained_outputs if row.get("failure_class"))

print("\n=== Multi-step Agent Step-Budget Comparison ===")
print(f"safe_config_failures: {safe_failures}")
print(f"constrained_config_failures: {constrained_failures}")

print("\nWhere complexity is:")
print("- More steps can improve completeness but increase cost and latency.")
print("- Too few steps can create premature-stop failures.")
