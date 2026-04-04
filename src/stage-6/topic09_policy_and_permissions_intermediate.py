"""Stage 6 Topic 09: Policy and permissions intermediate.

This script enforces a role-based tool permission matrix.
"""

from stage6_utils import permission_check, print_data_declaration


print_data_declaration("Topic09 Policy and Permissions Intermediate")

cases = [
    ("agent_general", "classify_priority"),
    ("agent_general", "approve_high_risk_action"),
    ("human_reviewer", "approve_high_risk_action"),
    ("agent_security", "flag_security_incident"),
]

print("\n=== Permission Matrix Checks ===")
for role, tool in cases:
    allowed = permission_check(role, tool)
    print(f"role={role} | tool={tool} | allowed={allowed}")

print("\nPolicy note:")
print("- Least privilege reduces damage when prompts or tools are compromised.")
