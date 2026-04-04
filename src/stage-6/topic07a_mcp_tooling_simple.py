"""Stage 6 Topic 07A: MCP tooling simple.

This script demonstrates an MCP-style resource/tool declaration as a conceptual
shape-level example (offline and framework-independent).
"""

from pprint import pprint

from stage6_utils import print_data_declaration


print_data_declaration("Topic07A MCP Tooling Simple")

mcp_like_definition = {
    "server": "support-tools",
    "resources": [
        {"uri": "db://tickets", "description": "ticket records"},
        {"uri": "doc://policies", "description": "policy documents"},
    ],
    "tools": [
        {
            "name": "route_queue",
            "description": "Route ticket to queue",
            "input_schema": {"ticket_id": "string", "subject": "string", "body": "string"},
            "output_schema": {"queue": "string", "reason": "string"},
        }
    ],
}

print("\n=== MCP-like Tool/Resource Definition ===")
pprint(mcp_like_definition)

print("\nConcept reminder:")
print("- MCP standardizes how agents discover and use tools/resources.")
