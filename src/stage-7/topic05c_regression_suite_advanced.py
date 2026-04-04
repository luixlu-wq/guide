"""Stage 7 Topic 05C: Regression suite (advanced)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    hybrid_retrieve,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    retrieval_metrics,
)

print_data_declaration("Topic05C Regression Suite Advanced", "regression gates")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

base_per_query = {}
hybrid_per_query = {}
for q in queries:
    base_rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4)
    hyb_rows = hybrid_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4, alpha=0.6)
    base_per_query[q.query_id] = [r["chunk"].chunk_id for r in base_rows]
    hybrid_per_query[q.query_id] = [r["chunk"].chunk_id for r in hyb_rows]

base_metrics = retrieval_metrics(base_per_query, queries, k=4)
hybrid_metrics = retrieval_metrics(hybrid_per_query, queries, k=4)

hit_drop = base_metrics["hit_at_k"] - hybrid_metrics["hit_at_k"]
recall_drop = base_metrics["recall_at_k"] - hybrid_metrics["recall_at_k"]

pass_gate = not (hit_drop > 0.03 or recall_drop > 0.03)

print("\nbase_metrics=", base_metrics)
print("hybrid_metrics=", hybrid_metrics)
print(f"gate_passed={pass_gate}")
print("gate_rule=block if hit@k or recall@k drops by more than 3%")
