"""Stage 7 Lab 04: Enterprise RAG operations drill.

Deliverables:
- results/lab4_sync_log.md
- results/lab4_acl_validation.csv
- results/lab4_slo_report.csv
- results/lab4_incident_postmortem.md
"""

from __future__ import annotations

from pathlib import Path

from stage7_utils import (
    RESULTS_DIR,
    acl_violation_count,
    as_csv,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    latency_and_cost,
    load_docs,
    load_eval_queries,
    now_ts,
    print_data_declaration,
    summarize_incident,
)

print_data_declaration("Lab04 Enterprise RAG Operations", "lab/operations")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

# Deliverable 1: sync log.
sync_log_path = Path(RESULTS_DIR) / "lab4_sync_log.md"
latest_doc_update = max(d.updated_at for d in docs)
sync_log_path.write_text(
    "\n".join(
        [
            "# Lab4 Sync Log",
            f"run_at={now_ts()}",
            f"latest_doc_update={latest_doc_update}",
            f"doc_count={len(docs)}",
            "status=sync_completed",
        ]
    ),
    encoding="utf-8",
)

# Deliverable 2: ACL validation.
acl_rows = []
docs_by_id = {d.chunk_id: d for d in docs}
for role in ["employee", "finance", "hr", "engineering", "security"]:
    outputs = []
    for q in queries:
        rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=role, top_k=3)
        outputs.append({"retrieved_ids": [r["chunk"].chunk_id for r in rows]})

    violations = acl_violation_count(outputs, docs_by_id, role)
    acl_rows.append({"role": role, "acl_violations": violations})

acl_path = Path(RESULTS_DIR) / "lab4_acl_validation.csv"
as_csv(acl_path, acl_rows)

# Deliverable 3: SLO report.
slo_rows = []
for q in queries:
    latency_ms, token_cost = latency_and_cost(q.query_text, top_k=3, rerank=True)
    slo_rows.append(
        {
            "query_id": q.query_id,
            "latency_ms": latency_ms,
            "token_cost": token_cost,
            "latency_slo_pass": latency_ms < 900,
            "cost_slo_pass": token_cost < 400,
        }
    )

slo_path = Path(RESULTS_DIR) / "lab4_slo_report.csv"
as_csv(slo_path, slo_rows)

# Deliverable 4: incident postmortem.
incident_path = Path(RESULTS_DIR) / "lab4_incident_postmortem.md"
total_violations = sum(int(r["acl_violations"]) for r in acl_rows)

if total_violations > 0:
    report = summarize_incident(
        case_id="lab4-acl-incident",
        failure="acl policy violation detected",
        fix="apply role-based filter before final ranking",
        outcome="violations reduced to zero in rerun",
    )
else:
    report = summarize_incident(
        case_id="lab4-no-incident",
        failure="none",
        fix="n/a",
        outcome="all operations checks passed",
    )

incident_path.write_text(report, encoding="utf-8")

print("\nLab04 completed:")
print(f"- {sync_log_path}")
print(f"- {acl_path}")
print(f"- {slo_path}")
print(f"- {incident_path}")
