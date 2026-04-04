"""Stage 7 Topic 05: Evaluation metrics (intermediate).

Compares baseline dense retrieval against reranked retrieval.
"""

from __future__ import annotations

from stage7_utils import (
    answer_metrics,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    rerank_candidates,
    retrieval_metrics,
)

print_data_declaration("Topic05 Eval Metrics Intermediate", "retrieval + answer metrics")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

base_per_query = {}
rerank_per_query = {}
base_answers = []
rerank_answers = []

for q in queries:
    base_rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=5)
    rerank_rows = rerank_candidates(q.query_text, base_rows, role=q.role)

    base_per_query[q.query_id] = [r["chunk"].chunk_id for r in base_rows]
    rerank_per_query[q.query_id] = [r["chunk"].chunk_id for r in rerank_rows]

    base_answers.append(grounded_answer(q.query_text, base_rows))
    rerank_answers.append(grounded_answer(q.query_text, rerank_rows))

base_retrieval = retrieval_metrics(base_per_query, queries, k=5)
rerank_retrieval = retrieval_metrics(rerank_per_query, queries, k=5)
base_answer = answer_metrics(base_answers)
rerank_answer = answer_metrics(rerank_answers)

print("\nbaseline_retrieval=", base_retrieval)
print("rerank_retrieval=", rerank_retrieval)
print("baseline_answer=", base_answer)
print("rerank_answer=", rerank_answer)
