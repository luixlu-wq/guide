"""Stage 7 Lab 02: Policy assistant RAG.

Deliverables:
- results/lab2_outputs.jsonl
- results/lab2_policy_violations.csv
- results/lab2_fix_log.md
"""

from __future__ import annotations

from pathlib import Path

from stage7_utils import (
    RESULTS_DIR,
    as_csv,
    as_jsonl,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    load_docs,
    load_eval_queries,
    print_data_declaration,
)

print_data_declaration("Lab02 Policy Assistant RAG", "lab/policy assistant")
ensure_stage7_dataset()
docs = load_docs()
queries = load_eval_queries()
vectorizer, matrix = build_tfidf_index(docs)

outputs = []
violations = []

for q in queries:
    retrieved = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=3)
    result = grounded_answer(q.query_text, retrieved, min_score=0.09)

    # Policy rule: grounded answer must include citation.
    policy_violation = bool(result["grounded"] and not result["citations"])

    outputs.append(
        {
            "query_id": q.query_id,
            "role": q.role,
            "answer": result["answer"],
            "grounded": result["grounded"],
            "citations": result["citations"],
            "retrieved_ids": result["retrieved_ids"],
            "policy_violation": policy_violation,
        }
    )

    if policy_violation:
        violations.append({"query_id": q.query_id, "violation": "grounded_without_citation"})

outputs_path = Path(RESULTS_DIR) / "lab2_outputs.jsonl"
violations_path = Path(RESULTS_DIR) / "lab2_policy_violations.csv"
fix_log_path = Path(RESULTS_DIR) / "lab2_fix_log.md"

as_jsonl(outputs_path, outputs)
as_csv(violations_path, violations if violations else [{"query_id": "none", "violation": "none"}])

fix_log_path.write_text(
    "\n".join(
        [
            "# Lab2 Fix Log",
            "",
            "Policy enforced: grounded answers require citations.",
            f"violations={len(violations)}",
            "",
            "If violations exist, fix by blocking output and regenerating with citation guardrail.",
        ]
    ),
    encoding="utf-8",
)

print("\nLab02 completed:")
print(f"- {outputs_path}")
print(f"- {violations_path}")
print(f"- {fix_log_path}")
