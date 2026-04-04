"""Stage 7 Topic 03: Retrieval + reranking (intermediate)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    print_data_declaration,
    rerank_candidates,
)

print_data_declaration("Topic03 Retrieval Rerank Intermediate", "dense + rerank")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "What pattern indicates prompt injection and how should we respond?"
base = dense_retrieve(query, docs, vectorizer, matrix, role="security", top_k=5)
reranked = rerank_candidates(query, base, role="security")
result = grounded_answer(query, reranked)

print("\nquery=", query)
print("\nbase_ranking=")
for r in base:
    print({"chunk_id": r["chunk"].chunk_id, "score": round(r["score"], 4), "section": r["chunk"].section})

print("\nreranked=")
for r in reranked[:5]:
    print({"chunk_id": r["chunk"].chunk_id, "rerank_score": round(r["rerank_score"], 4), "section": r["chunk"].section})

print("\nanswer=", result["answer"])
print("citations=", result["citations"])
