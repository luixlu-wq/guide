"""Stage 7 Lab 05: Qdrant end-to-end RAG lab (baseline vs vector DB).

Deliverables:
- results/lab5_qdrant_outputs.jsonl
- results/lab5_qdrant_metrics.csv
- results/lab5_qdrant_acl_validation.csv
- results/lab5_qdrant_runbook.md

This lab requires:
- local Qdrant service at localhost:6333
- qdrant-client installed (requirements-optional.txt)
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import numpy as np

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
    now_ts,
    print_data_declaration,
    retrieval_metrics,
)

try:
    from qdrant_client import QdrantClient  # type: ignore
    from qdrant_client.http import models  # type: ignore
except Exception:
    QdrantClient = None
    models = None


COLLECTION_NAME = "stage7_lab05_qdrant"


def _as_dense_row(matrix: Any, idx: int) -> list[float]:
    """Convert sparse vector row to dense float list for Qdrant upsert."""
    row = matrix[idx].toarray()[0].astype(np.float32)
    return row.tolist()


def _allowed_acl(role: str) -> list[str]:
    """Role-to-ACL mapping used for query filter checks."""
    if role == "security":
        return ["employee", "engineering", "finance", "hr", "security"]
    if role == "engineering":
        return ["engineering", "employee"]
    if role == "finance":
        return ["finance", "employee"]
    if role == "hr":
        return ["hr", "employee"]
    return ["employee", "engineering"]


def _ensure_collection(client: Any, docs: list[Any], matrix: Any) -> int:
    """Create deterministic lab collection and upsert all chunks with metadata payload."""
    vector_size = int(matrix.shape[1])

    if client.collection_exists(collection_name=COLLECTION_NAME):
        client.delete_collection(collection_name=COLLECTION_NAME)
        for _ in range(40):
            if not client.collection_exists(collection_name=COLLECTION_NAME):
                break
            time.sleep(0.1)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )

    points = []
    for i, doc in enumerate(docs, start=1):
        points.append(
            models.PointStruct(
                id=i,
                vector=_as_dense_row(matrix, i - 1),
                payload={
                    "chunk_id": doc.chunk_id,
                    "doc_id": doc.doc_id,
                    "source": doc.source,
                    "section": doc.section,
                    "acl_tag": doc.acl_tag,
                    "updated_at": doc.updated_at,
                    "text": doc.text,
                },
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


def _qdrant_retrieve(
    client: Any,
    query_vec: list[float],
    role: str,
    docs_by_id: dict[str, Any],
    *,
    top_k: int = 4,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Retrieve top-k points from Qdrant with ACL metadata filter.

    Returns:
    - retrieval rows compatible with `grounded_answer`
    - list of returned ACL tags (used for validation report)
    """
    allowed_acl = _allowed_acl(role)
    acl_filter = models.Filter(
        should=[
            models.FieldCondition(key="acl_tag", match=models.MatchValue(value=tag))
            for tag in allowed_acl
        ]
    )

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vec,
        query_filter=acl_filter,
        limit=top_k,
        with_payload=True,
    )

    rows: list[dict[str, Any]] = []
    acl_tags: list[str] = []
    for hit in response.points:
        payload = hit.payload or {}
        chunk_id = str(payload.get("chunk_id", ""))
        acl_tag = str(payload.get("acl_tag", ""))
        acl_tags.append(acl_tag)

        chunk_obj = docs_by_id.get(chunk_id)
        if chunk_obj is None:
            # If payload cannot map back to known docs, skip it to keep evaluation honest.
            continue

        rows.append(
            {
                "chunk": chunk_obj,
                "score": float(hit.score),
                "method": "qdrant_vector_db",
            }
        )

    return rows, acl_tags


def main() -> None:
    print_data_declaration("Lab05 Qdrant End-to-End RAG", "lab/vector-db end-to-end")
    ensure_stage7_dataset()

    outputs_path = Path(RESULTS_DIR) / "lab5_qdrant_outputs.jsonl"
    metrics_path = Path(RESULTS_DIR) / "lab5_qdrant_metrics.csv"
    acl_path = Path(RESULTS_DIR) / "lab5_qdrant_acl_validation.csv"
    runbook_path = Path(RESULTS_DIR) / "lab5_qdrant_runbook.md"

    if QdrantClient is None or models is None:
        runbook_path.write_text(
            "\n".join(
                [
                    "# Lab5 Qdrant Runbook",
                    "status=skipped",
                    "reason=qdrant-client is not installed",
                    "action=install optional dependencies and rerun",
                ]
            ),
            encoding="utf-8",
        )
        print("qdrant-client missing. Wrote skip runbook.")
        print(f"- {runbook_path}")
        return

    docs = load_docs()
    queries = load_eval_queries()
    docs_by_id = {d.chunk_id: d for d in docs}
    vectorizer, matrix = build_tfidf_index(docs)

    try:
        client = QdrantClient(host="localhost", port=6333, timeout=5)
        client.get_collections()
    except Exception as exc:
        runbook_path.write_text(
            "\n".join(
                [
                    "# Lab5 Qdrant Runbook",
                    "status=skipped",
                    "reason=cannot connect to local qdrant",
                    f"error={exc}",
                    "action=start qdrant on localhost:6333 and rerun",
                ]
            ),
            encoding="utf-8",
        )
        print("Cannot connect to local Qdrant. Wrote skip runbook.")
        print(f"- {runbook_path}")
        return

    point_count = _ensure_collection(client, docs, matrix)

    baseline_per_query = {}
    qdrant_per_query = {}
    baseline_answers = []
    qdrant_answers = []

    output_rows = []
    acl_rows = []

    for q in queries:
        # Baseline retrieval path (non-vector-DB) for comparison.
        base_rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4)
        base_result = grounded_answer(q.query_text, base_rows)
        baseline_per_query[q.query_id] = base_result["retrieved_ids"]
        baseline_answers.append(base_result)

        # Qdrant retrieval path with ACL filtering.
        q_vec = vectorizer.transform([q.query_text]).toarray()[0].astype(np.float32).tolist()
        q_rows, returned_acl_tags = _qdrant_retrieve(client, q_vec, q.role, docs_by_id, top_k=4)
        q_result = grounded_answer(q.query_text, q_rows)

        qdrant_per_query[q.query_id] = q_result["retrieved_ids"]
        qdrant_answers.append(q_result)

        allowed = set(_allowed_acl(q.role))
        violations = [tag for tag in returned_acl_tags if tag and tag not in allowed]

        acl_rows.append(
            {
                "query_id": q.query_id,
                "role": q.role,
                "allowed_acl": "|".join(sorted(allowed)),
                "returned_acl": "|".join(returned_acl_tags),
                "acl_violation_count": len(violations),
            }
        )

        output_rows.append(
            {
                "query_id": q.query_id,
                "role": q.role,
                "query": q.query_text,
                "baseline_ids": base_result["retrieved_ids"],
                "qdrant_ids": q_result["retrieved_ids"],
                "qdrant_answer": q_result["answer"],
                "qdrant_citations": q_result["citations"],
                "qdrant_grounded": q_result["grounded"],
            }
        )

    baseline_retrieval = retrieval_metrics(baseline_per_query, queries, k=4)
    qdrant_retrieval = retrieval_metrics(qdrant_per_query, queries, k=4)
    baseline_answer = answer_metrics(baseline_answers)
    qdrant_answer = answer_metrics(qdrant_answers)

    metric_rows = [
        {"variant": "baseline_dense", **baseline_retrieval, **baseline_answer},
        {"variant": "qdrant_vector_db", **qdrant_retrieval, **qdrant_answer},
    ]

    as_jsonl(outputs_path, output_rows)
    as_csv(metrics_path, metric_rows)
    as_csv(acl_path, acl_rows)

    total_acl_violations = sum(int(r["acl_violation_count"]) for r in acl_rows)

    runbook_path.write_text(
        "\n".join(
            [
                "# Lab5 Qdrant Runbook",
                f"run_at={now_ts()}",
                "status=completed",
                f"collection={COLLECTION_NAME}",
                f"point_count={point_count}",
                f"total_queries={len(queries)}",
                f"acl_violations={total_acl_violations}",
                "",
                "## Metric Summary",
                f"baseline_hit_at_k={baseline_retrieval['hit_at_k']:.4f}",
                f"qdrant_hit_at_k={qdrant_retrieval['hit_at_k']:.4f}",
                f"baseline_mrr={baseline_retrieval['mrr']:.4f}",
                f"qdrant_mrr={qdrant_retrieval['mrr']:.4f}",
                "",
                "## Interpretation",
                "Compare baseline_dense vs qdrant_vector_db rows in metrics CSV.",
                "If ACL violations are non-zero, block answer generation and fix filters.",
            ]
        ),
        encoding="utf-8",
    )

    print("\nLab05 completed:")
    print(f"- {outputs_path}")
    print(f"- {metrics_path}")
    print(f"- {acl_path}")
    print(f"- {runbook_path}")


if __name__ == "__main__":
    main()
