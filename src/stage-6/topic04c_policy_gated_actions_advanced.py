"""Stage 6 Topic 04C: Policy-gated actions advanced.

This script layers multiple policy checks before allowing sensitive actions.
"""

from stage6_utils import detect_prompt_injection, load_ticket_rows, needs_human_approval, print_data_declaration


print_data_declaration("Topic04C Policy-Gated Actions Advanced")
row = load_ticket_rows()[6]  # deterministic row includes data export request language

candidate_action = "export_data"
user_instruction = f"{row.subject} | {row.body}"

# Layer 1: detect prompt injection style signals.
injection_flag = detect_prompt_injection(user_instruction)

# Layer 2: risk-based approval gate.
approval_flag = needs_human_approval(row, action=candidate_action)

# Layer 3: final decision policy.
action_allowed = (not injection_flag) and (not approval_flag)

print("\n=== Policy Gate Results ===")
print(f"injection_flag={injection_flag}")
print(f"approval_required={approval_flag}")
print(f"final_action_allowed={action_allowed}")

print("\nAdvanced reliability point:")
print("- Safe systems gate actions, not only final text outputs.")
