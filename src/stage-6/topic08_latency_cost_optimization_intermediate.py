"""Stage 6 Topic 08: Latency and cost optimization intermediate.

This script compares before/after operation settings and prints practical deltas.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic08 Latency/Cost Optimization Intermediate")

before = {
    "avg_steps": 6.2,
    "p95_latency_ms": 1800,
    "cost_per_task": 0.042,
}

after = {
    "avg_steps": 4.1,
    "p95_latency_ms": 1210,
    "cost_per_task": 0.027,
}

print("\n=== Before ===")
for k, v in before.items():
    print(f"{k}: {v}")

print("\n=== After ===")
for k, v in after.items():
    print(f"{k}: {v}")

print("\n=== Delta (after - before) ===")
for key in before:
    print(f"{key}: {after[key] - before[key]:.4f}")

print("\nInterpretation:")
print("- Fewer steps often improves both latency and cost.")
print("- Keep safety metrics stable while optimizing performance.")
