"""Stage 6 Topic 07: Protocol interoperability intermediate.

This script contrasts MCP-style tool calls with A2A-style agent messages.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic07 Protocol Interop Intermediate")

# MCP-style interaction envelope (agent -> tool server).
mcp_call = {
    "protocol": "MCP",
    "target": "support-tools.route_queue",
    "payload": {"ticket_id": "TKT-1002", "subject": "Invoice mismatch", "body": "Billing total differs"},
}

# A2A-style interaction envelope (agent -> agent).
a2a_message = {
    "protocol": "A2A",
    "from_agent": "coordinator_agent",
    "to_agent": "billing_specialist_agent",
    "task": "Verify invoice discrepancy and return recommended queue + policy citation",
}

print("\n=== MCP-style Envelope ===")
print(mcp_call)

print("\n=== A2A-style Envelope ===")
print(a2a_message)

print("\nInterpretation:")
print("- MCP: interoperability for tools/resources.")
print("- A2A: interoperability for agent collaboration.")
