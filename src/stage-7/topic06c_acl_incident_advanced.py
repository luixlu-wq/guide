"""Stage 7 Topic 06C: ACL + incident drill (advanced)."""

from __future__ import annotations

from stage7_utils import (
    acl_violation_count,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    load_docs,
    load_eval_queries,
    print_data_declaration,
    summarize_incident,
)

print_data_declaration("Topic06C ACL Incident Advanced", "security/operations")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)
queries = load_eval_queries()

docs_by_id = {d.chunk_id: d for d in docs}

# Simulate a risky role that should not access security-only chunks.
role = "employee"
outputs = []
for q in queries:
    rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=role, top_k=3)
    outputs.append({"query_id": q.query_id, "retrieved_ids": [r["chunk"].chunk_id for r in rows]})

violations = acl_violation_count(outputs, docs_by_id, role=role)
print(f"acl_violations={violations}")

if violations > 0:
    postmortem = summarize_incident(
        case_id="acl-leak-stage7",
        failure="retriever returned restricted chunk",
        fix="enforce ACL filter before ranking",
        outcome="access leak blocked after policy check",
    )
    print("\n" + postmortem)
else:
    print("No ACL violations detected. Incident drill passed.")
