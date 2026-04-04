"""Stage 7 Lab 01: PDF Q&A style RAG (offline corpus simulation).

Deliverables:
- results/lab1_outputs.jsonl
- results/lab1_retrieval_metrics.csv
- results/lab1_grounding_audit.md
"""

from __future__ import annotations

from pathlib import Path

from stage7_utils import (
    RESULTS_DIR,
    answer_metrics,
    as_csv,
    as_jsonl,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    retrieval_metrics,
)

print_data_declaration("Lab01 PDF QA RAG", "lab/retrieval+grounding")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()[:8]
vectorizer, matrix = build_tfidf_index(docs)

outputs = []
per_query = {}

for q in queries:
    retrieved = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4)
    result = grounded_answer(q.query_text, retrieved)
    latency_ms = 220 + 20 * len(retrieved)

    row = {
        "query_id": q.query_id,
        "query": q.query_text,
        "retrieved_ids": result["retrieved_ids"],
        "answer": result["answer"],
        "citations": result["citations"],
        "grounded": result["grounded"],
        "latency_ms": latency_ms,
    }
    outputs.append(row)
    per_query[q.query_id] = result["retrieved_ids"]

retr_metrics = retrieval_metrics(per_query, queries, k=4)
ans_metrics = answer_metrics(outputs)

outputs_path = Path(RESULTS_DIR) / "lab1_outputs.jsonl"
metrics_path = Path(RESULTS_DIR) / "lab1_retrieval_metrics.csv"
audit_path = Path(RESULTS_DIR) / "lab1_grounding_audit.md"

as_jsonl(outputs_path, outputs)
as_csv(metrics_path, [{"label": "lab1", **retr_metrics, **ans_metrics}])

ungrounded = [o for o in outputs if not o["grounded"]]
audit_lines = [
    "# Lab1 Grounding Audit",
    f"total_queries={len(outputs)}",
    f"ungrounded_cases={len(ungrounded)}",
    "",
    "## Ungrounded Case IDs",
] + [f"- {u['query_id']}" for u in ungrounded]

audit_path.write_text("\n".join(audit_lines), encoding="utf-8")

print("\nLab01 completed:")
print(f"- {outputs_path}")
print(f"- {metrics_path}")
print(f"- {audit_path}")
