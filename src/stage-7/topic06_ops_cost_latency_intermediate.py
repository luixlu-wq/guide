"""Stage 7 Topic 06: Ops latency/cost checks (intermediate)."""

from __future__ import annotations

from stage7_utils import (
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    latency_and_cost,
    load_docs,
    load_eval_queries,
    print_data_declaration,
)

print_data_declaration("Topic06 Ops Cost Latency Intermediate", "operations/SLO")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()[:6]
vectorizer, matrix = build_tfidf_index(docs)

rows = []
for q in queries:
    retrieved = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4)
    latency_ms, token_cost = latency_and_cost(q.query_text, top_k=4, rerank=False)

    rows.append(
        {
            "query_id": q.query_id,
            "latency_ms": latency_ms,
            "token_cost": token_cost,
            "top_chunk": retrieved[0]["chunk"].chunk_id if retrieved else "none",
        }
    )

p95_latency = sorted([r["latency_ms"] for r in rows])[int(len(rows) * 0.95) - 1]
avg_cost = sum(r["token_cost"] for r in rows) / len(rows)

print("\nrows=", rows)
print(f"p95_latency_ms={p95_latency}")
print(f"avg_token_cost={avg_cost:.2f}")
print("slo_example: p95_latency < 900ms, avg_token_cost < 400")
