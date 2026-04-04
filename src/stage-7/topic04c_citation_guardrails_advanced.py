"""Stage 7 Topic 04C: Citation guardrails (advanced)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    print_data_declaration,
)


def validate_citations(result: dict) -> bool:
    """Guardrail rule: grounded answers must include at least one citation."""
    if result.get("grounded") and not result.get("citations"):
        return False
    return True


print_data_declaration("Topic04C Citation Guardrails Advanced", "grounding/citation controls")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "Can sensitive data be sent via personal email?"
retrieved = dense_retrieve(query, docs, vectorizer, matrix, role="employee", top_k=3)
result = grounded_answer(query, retrieved)

citation_ok = validate_citations(result)

print("\nquery=", query)
print("retrieved_ids=", result["retrieved_ids"])
print("answer=", result["answer"])
print("citations=", result["citations"])
print("citation_guardrail_passed=", citation_ok)

if not citation_ok:
    print("ACTION: block response and request regeneration with citations")
