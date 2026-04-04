"""Stage 7 Topic 03D: Local Qdrant ACL-filtered retrieval.

This script demonstrates role-aware retrieval with metadata filters in Qdrant.
"""

from __future__ import annotations
from typing import Any

import numpy as np

from stage7_utils import build_tfidf_index, ensure_stage7_dataset, load_docs, print_data_declaration

try:
    from qdrant_client import QdrantClient  # type: ignore
    from qdrant_client.http import models  # type: ignore
except Exception:
    QdrantClient = None
    models = None


COLLECTION_NAME = "stage7_local_qdrant_demo"


def _as_dense_row(matrix: Any, idx: int) -> list[float]:
    """Convert sparse row to dense float list for vector DB insertion."""
    row = matrix[idx].toarray()[0].astype(np.float32)
    return row.tolist()


def _allowed_acl(role: str) -> list[str]:
    """Simple role-to-ACL mapping for this educational example."""
    if role == "security":
        return ["employee", "engineering", "finance", "hr", "security"]
    if role == "engineering":
        return ["engineering", "employee"]
    if role == "finance":
        return ["finance", "employee"]
    if role == "hr":
        return ["hr", "employee"]
    return ["employee", "engineering"]


def _ensure_collection(client: Any, docs: list[Any], vectorizer: Any, matrix: Any) -> None:
    """Create or refresh collection so script is independently runnable."""
    vector_size = int(matrix.shape[1])

    # If collection already exists, reuse it to avoid conflicts with parallel demo runs.
    if client.collection_exists(collection_name=COLLECTION_NAME):
        return

    # Otherwise create and load points so this script can run independently.
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


def main() -> None:
    print_data_declaration("Topic03D Qdrant ACL Search", "vector-db retrieval + ACL")
    ensure_stage7_dataset()
    docs = load_docs()
    vectorizer, matrix = build_tfidf_index(docs)

    if QdrantClient is None or models is None:
        print("\nqdrant-client is not installed.")
        print("Install optional deps: pip install -r red-book/src/stage-7/requirements-optional.txt")
        return

    try:
        client = QdrantClient(host="localhost", port=6333, timeout=5)
        client.get_collections()
    except Exception as exc:
        print("\nCannot connect to local Qdrant at localhost:6333")
        print(f"error={exc}")
        return

    _ensure_collection(client, docs, vectorizer, matrix)

    role = "employee"
    query = "Who can access security audit logs?"
    q_vec = vectorizer.transform([query]).toarray()[0].astype(np.float32).tolist()

    allowed_acl = _allowed_acl(role)

    # ACL filter: only return points whose payload acl_tag is in role allowlist.
    acl_filter = models.Filter(
        should=[
            models.FieldCondition(key="acl_tag", match=models.MatchValue(value=tag))
            for tag in allowed_acl
        ]
    )

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=q_vec,
        query_filter=acl_filter,
        limit=5,
        with_payload=True,
    )
    hits = response.points

    print("\n=== ACL filtered search ===")
    print(f"role={role}")
    print(f"allowed_acl={allowed_acl}")
    print(f"query={query}")

    for hit in hits:
        payload = hit.payload or {}
        print(
            {
                "score": round(float(hit.score), 4),
                "chunk_id": payload.get("chunk_id"),
                "acl_tag": payload.get("acl_tag"),
                "source": payload.get("source"),
            }
        )

    returned_acl = {str((hit.payload or {}).get("acl_tag", "")) for hit in hits}
    violations = [tag for tag in returned_acl if tag not in allowed_acl]
    print(f"acl_violation_count={len(violations)}")

    if violations:
        print(f"violating_tags={violations}")
        print("ACTION: stop answer generation and investigate filter policy")
    else:
        print("ACL filter check passed.")


if __name__ == "__main__":
    main()
