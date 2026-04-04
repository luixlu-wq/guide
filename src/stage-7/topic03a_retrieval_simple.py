"""Stage 7 Topic 03A: Retrieval baseline (simple)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    print_data_declaration,
)

print_data_declaration("Topic03A Retrieval Simple", "dense retrieval")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "How do we report a security incident?"
retrieved = dense_retrieve(query, docs, vectorizer, matrix, role="employee", top_k=3)
result = grounded_answer(query, retrieved)

print("\nquery=", query)
print("retrieved=")
for r in retrieved:
    print({"chunk_id": r["chunk"].chunk_id, "score": round(r["score"], 4), "source": r["chunk"].source})

print("\nanswer=", result["answer"])
print("citations=", result["citations"])
print("grounded=", result["grounded"])
