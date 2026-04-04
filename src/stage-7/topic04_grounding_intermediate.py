"""Stage 7 Topic 04: Grounding policy (intermediate)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    print_data_declaration,
)

print_data_declaration("Topic04 Grounding Intermediate", "grounding policy")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

queries = [
    "How quickly must security incidents be reported?",
    "What is our Mars office parking reimbursement policy?",
]

for q in queries:
    retrieved = dense_retrieve(q, docs, vectorizer, matrix, role="employee", top_k=3)

    # A stricter threshold makes unsupported queries abstain instead of guessing.
    # This keeps the demo aligned with production grounding policy.
    result = grounded_answer(q, retrieved, min_score=0.20)

    print("\n" + "=" * 72)
    print("query=", q)
    print("retrieved_ids=", [r["chunk"].chunk_id for r in retrieved])
    print("top_score=", round(retrieved[0]["score"], 4) if retrieved else "none")
    print("answer=", result["answer"])
    print("grounded=", result["grounded"])
    print("citations=", result["citations"])

print("\nInterpretation: abstention is required when evidence is weak or missing.")
