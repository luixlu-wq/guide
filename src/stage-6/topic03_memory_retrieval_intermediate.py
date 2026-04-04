"""Stage 6 Topic 03: Memory retrieval intermediate.

This script demonstrates a basic long-term memory retrieval strategy using
keyword overlap against persisted memory records.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic03 Memory Retrieval Intermediate")

# Simulated long-term memory store.
memory_store = [
    {"id": "M1", "text": "Enterprise outages need severity rubric and fast escalation."},
    {"id": "M2", "text": "Billing disputes require invoice evidence and contract check."},
    {"id": "M3", "text": "Security incidents require identity verification before disclosure."},
]

query = "customer reports security alert and suspicious access"
q_tokens = set(query.lower().split())

scored = []
for record in memory_store:
    tokens = set(record["text"].lower().split())
    overlap = len(q_tokens & tokens)
    scored.append((overlap, record))

# Sort descending by overlap to retrieve most relevant memory first.
scored.sort(key=lambda x: x[0], reverse=True)
top_records = [item[1] for item in scored[:2]]

print("\nQuery:")
print(query)

print("\nRetrieved memory records:")
for rec in top_records:
    print(f"- {rec['id']}: {rec['text']}")

print("\nReliability note:")
print("- Retrieval quality directly affects agent grounding quality.")
