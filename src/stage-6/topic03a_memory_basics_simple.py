"""Stage 6 Topic 03A: Memory basics simple.

This script shows short-term memory as a compact per-session dictionary.
"""

from stage6_utils import load_ticket_rows, print_data_declaration


print_data_declaration("Topic03A Memory Basics Simple")
rows = load_ticket_rows()[:3]

# Short-term memory for one conversation/session.
session_memory: dict[str, str] = {}

for row in rows:
    # Keep only minimal useful facts to avoid memory overload.
    session_memory["last_ticket_id"] = row.ticket_id
    session_memory["last_subject"] = row.subject
    print(f"updated_memory_for={row.ticket_id}")

print("\n=== Session Memory Snapshot ===")
print(session_memory)

print("\nInterpretation:")
print("- Short-term memory should stay small and purpose-driven.")
