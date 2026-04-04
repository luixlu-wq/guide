"""Stage 6 Topic 04: HITL intermediate.

This script demonstrates a simple human-in-the-loop checkpoint for risky actions.
"""

from stage6_utils import load_ticket_rows, needs_human_approval, print_data_declaration


print_data_declaration("Topic04 HITL Intermediate")
rows = load_ticket_rows()[:8]


def simulated_human_review(ticket_id: str, approved_by_default: bool = True) -> bool:
    """Offline deterministic human-review stub for teaching operational workflow."""
    # In real systems, this would call a review queue or UI workflow.
    return approved_by_default


approved_count = 0
blocked_count = 0

for row in rows:
    requires_review = needs_human_approval(row, action="send_external")
    if requires_review:
        approved = simulated_human_review(row.ticket_id, approved_by_default=True)
        if approved:
            approved_count += 1
        else:
            blocked_count += 1

print("\n=== HITL Summary ===")
print(f"reviewed_and_approved={approved_count}")
print(f"reviewed_and_blocked={blocked_count}")

print("\nOperational note:")
print("- HITL is required for high-risk external actions.")
