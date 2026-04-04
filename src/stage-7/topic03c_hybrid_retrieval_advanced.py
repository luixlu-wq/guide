"""Stage 7 Topic 03C: Hybrid retrieval (advanced)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    ensure_stage7_dataset,
    grounded_answer,
    hybrid_retrieve,
    load_docs,
    print_data_declaration,
    rerank_candidates,
)

print_data_declaration("Topic03C Hybrid Retrieval Advanced", "hybrid + rerank")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "What is the API SLO and p95 latency target?"
hybrid = hybrid_retrieve(query, docs, vectorizer, matrix, role="engineering", top_k=6, alpha=0.65)
reranked = rerank_candidates(query, hybrid, role="engineering")
result = grounded_answer(query, reranked)

print("\nquery=", query)
print("\nhybrid_candidates=")
for r in hybrid:
    print(
        {
            "chunk_id": r["chunk"].chunk_id,
            "hybrid_score": round(r["score"], 4),
            "dense_component": round(r["dense_component"], 4),
            "lexical_component": round(r["lexical_component"], 4),
        }
    )

print("\nreranked_top3=")
for r in reranked[:3]:
    print({"chunk_id": r["chunk"].chunk_id, "rerank_score": round(r["rerank_score"], 4)})

print("\nanswer=", result["answer"])
print("citations=", result["citations"])
