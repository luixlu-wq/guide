"""Stage 6 Topic 05A: Trace basics simple.

This script generates trace rows for one agent run to demonstrate minimum
observability fields.
"""

from stage6_utils import build_trace_row, print_data_declaration


print_data_declaration("Topic05A Trace Basics Simple")

run_id = "run-trace-simple-001"
query_id = "TKT-1000"

trace_rows = [
    build_trace_row(run_id, query_id, 1, "classify_priority", "ok", 42, 120),
    build_trace_row(run_id, query_id, 2, "route_queue", "ok", 31, 90),
    build_trace_row(run_id, query_id, 3, "retrieve_policy_snippets", "ok", 55, 140),
]

print("\n=== Trace Rows ===")
for row in trace_rows:
    print(row)

print("\nTrace requirement reminder:")
print("- Always log run_id, query_id, step, selected_tool, status, latency, and token cost.")
