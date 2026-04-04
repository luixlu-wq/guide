"""Stage 6 Topic 08A: Budget controls simple.

This script shows run-level limits for max steps, latency, and token budget.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic08A Budget Controls Simple")

budget = {
    "max_steps": 5,
    "max_latency_ms": 1200,
    "max_token_cost": 900,
}

observed_run = {
    "steps": 4,
    "latency_ms": 980,
    "token_cost": 740,
}

within_budget = (
    observed_run["steps"] <= budget["max_steps"]
    and observed_run["latency_ms"] <= budget["max_latency_ms"]
    and observed_run["token_cost"] <= budget["max_token_cost"]
)

print("\nBudget:", budget)
print("Observed:", observed_run)
print(f"within_budget={within_budget}")

print("\nOperations note:")
print("- Budget controls prevent runaway loops and unexpected cost spikes.")
