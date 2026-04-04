"""Stage 6 Topic 04A: Guardrails simple.

This script applies a basic policy gate before returning an action-ready response.
"""

from stage6_utils import load_ticket_rows, needs_human_approval, print_data_declaration


print_data_declaration("Topic04A Guardrails Simple")
row = load_ticket_rows()[3]  # deterministic example likely security-oriented

approval_required = needs_human_approval(row, action="respond")

print("\n=== Guardrail Decision ===")
print(f"ticket={row.ticket_id}")
print(f"subject={row.subject}")
print(f"needs_human_approval={approval_required}")

print("\nWhy this matters:")
print("- Guardrails prevent unsafe autonomy on high-risk cases.")
