"""Stage 7 Topic 05A: Evaluation basics (simple)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    retrieval_metrics,
)

print_data_declaration("Topic05A Eval Basics Simple", "retrieval metrics")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

per_query = {}
for q in queries:
    rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=3)
    per_query[q.query_id] = [r["chunk"].chunk_id for r in rows]

metrics = retrieval_metrics(per_query, queries, k=3)
print("\nretrieval_metrics=", metrics)
print("Interpretation: hit@k and recall@k must be tracked before prompt tuning.")
