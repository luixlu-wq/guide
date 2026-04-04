"""Stage 7 Lab 03: Hybrid retrieval benchmark.

Deliverables:
- results/lab3_retrieval_comparison.csv
- results/lab3_error_cases.md
- results/lab3_before_after_summary.md
"""

from __future__ import annotations

from pathlib import Path

from stage7_utils import (
    RESULTS_DIR,
    as_csv,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    hybrid_retrieve,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    retrieval_metrics,
)

print_data_declaration("Lab03 Hybrid Retrieval Benchmark", "lab/retrieval benchmark")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

base_per_query = {}
hybrid_per_query = {}

for q in queries:
    base = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4)
    hyb = hybrid_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4, alpha=0.65)

    base_per_query[q.query_id] = [r["chunk"].chunk_id for r in base]
    hybrid_per_query[q.query_id] = [r["chunk"].chunk_id for r in hyb]

base_metrics = retrieval_metrics(base_per_query, queries, k=4)
hybrid_metrics = retrieval_metrics(hybrid_per_query, queries, k=4)

comparison_rows = [
    {"variant": "dense_baseline", **base_metrics},
    {"variant": "hybrid", **hybrid_metrics},
]

comparison_path = Path(RESULTS_DIR) / "lab3_retrieval_comparison.csv"
error_path = Path(RESULTS_DIR) / "lab3_error_cases.md"
summary_path = Path(RESULTS_DIR) / "lab3_before_after_summary.md"

as_csv(comparison_path, comparison_rows)

error_cases = []
for q in queries:
    gold = set(q.gold_chunk_ids)
    base_hit = any(cid in gold for cid in base_per_query[q.query_id][:4])
    hyb_hit = any(cid in gold for cid in hybrid_per_query[q.query_id][:4])
    if base_hit and not hyb_hit:
        error_cases.append(f"- {q.query_id}: hybrid missed while baseline hit")

error_lines = ["# Lab3 Error Cases", ""] + (error_cases or ["- none"])
error_path.write_text("\n".join(error_lines), encoding="utf-8")

summary_path.write_text(
    "\n".join(
        [
            "# Lab3 Before/After Summary",
            "",
            f"dense_hit@k={base_metrics['hit_at_k']:.3f}",
            f"hybrid_hit@k={hybrid_metrics['hit_at_k']:.3f}",
            f"dense_recall@k={base_metrics['recall_at_k']:.3f}",
            f"hybrid_recall@k={hybrid_metrics['recall_at_k']:.3f}",
            "",
            "Controlled change: enabled dense+lexical hybrid retrieval with alpha=0.65.",
        ]
    ),
    encoding="utf-8",
)

print("\nLab03 completed:")
print(f"- {comparison_path}")
print(f"- {error_path}")
print(f"- {summary_path}")
