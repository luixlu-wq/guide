"""Stage 6 Topic 02A: Tool schema simple.

This script introduces explicit tool schema declarations with required fields.
"""

from pprint import pprint

from stage6_utils import print_data_declaration


print_data_declaration("Topic02A Tool Schema Simple")

# A minimal but explicit tool contract with deterministic field names/types.
tool_schema = {
    "name": "route_queue",
    "description": "Route support ticket to a queue based on issue type.",
    "input_schema": {
        "ticket_id": "string",
        "subject": "string",
        "body": "string",
    },
    "output_schema": {
        "queue": "enum(general,billing,outage,security)",
        "reason": "string",
    },
    "errors": ["INVALID_INPUT", "TIMEOUT"],
}

print("\n=== Example Tool Schema ===")
pprint(tool_schema)

print("\nWhy this matters:")
print("- Agents need strict tool signatures to reduce malformed calls.")
print("- Output schema enables downstream validation and safer orchestration.")
