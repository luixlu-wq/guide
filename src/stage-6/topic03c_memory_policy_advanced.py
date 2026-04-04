"""Stage 6 Topic 03C: Memory policy advanced.

This script demonstrates memory write policy + TTL expiration to prevent
stale or speculative information from polluting long-term state.
"""

from datetime import datetime, timedelta

from stage6_utils import print_data_declaration


print_data_declaration("Topic03C Memory Policy Advanced")

now = datetime(2026, 4, 4, 10, 0, 0)

memory_records = [
    {"id": "R1", "text": "verified billing policy", "confidence": 0.95, "expires_at": now + timedelta(days=10)},
    {"id": "R2", "text": "model guess without evidence", "confidence": 0.30, "expires_at": now + timedelta(days=5)},
    {"id": "R3", "text": "old outage workaround", "confidence": 0.80, "expires_at": now - timedelta(days=1)},
]


def memory_write_allowed(confidence: float, has_evidence: bool) -> bool:
    """Policy: only high-confidence, evidence-backed facts can be persisted."""
    return confidence >= 0.7 and has_evidence


# Filter records by policy and TTL.
usable = [
    rec
    for rec in memory_records
    if rec["expires_at"] > now and memory_write_allowed(rec["confidence"], "verified" in rec["text"])
]

print("\n=== Memory Records After Policy + TTL ===")
for rec in usable:
    print(f"id={rec['id']} | confidence={rec['confidence']} | text={rec['text']}")

print("\nComplexity note:")
print("- Memory policy increases reliability but requires disciplined state management.")
