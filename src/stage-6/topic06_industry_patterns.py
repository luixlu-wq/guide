"""Stage 6 Topic 06: Industry patterns.

This script prints concrete architecture patterns and their operational tradeoffs.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic06 Industry Patterns")

patterns = [
    {
        "name": "Support Triage Agent",
        "flow": ["classify", "route", "retrieve_policy", "draft", "optional_hitl"],
        "complexity": "intermediate",
        "key_risk": "wrong routing under ambiguous language",
    },
    {
        "name": "Finance Research Agent",
        "flow": ["retrieve", "compute", "synthesize", "grounding_check"],
        "complexity": "intermediate",
        "key_risk": "ungrounded summary claims",
    },
    {
        "name": "Ops Multi-Agent Assistant",
        "flow": ["coordinator", "specialists", "policy_gate", "incident_log"],
        "complexity": "advanced",
        "key_risk": "coordination failures and policy drift",
    },
]

print("\n=== Industry Pattern Catalog ===")
for p in patterns:
    print(f"name={p['name']}")
    print(f"complexity={p['complexity']}")
    print(f"flow={' -> '.join(p['flow'])}")
    print(f"key_risk={p['key_risk']}")
    print("---")

print("Use workflow baseline first, then add bounded agent autonomy.")
