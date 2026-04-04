"""Stage 7 Topic 02D: Local Qdrant indexing workflow.

This script demonstrates a production-style vector DB path using local Qdrant.
It is optional and will print guidance if Qdrant/client is unavailable.
"""

from __future__ import annotations

import time
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


def main() -> None:
    print_data_declaration("Topic02D Qdrant Local Index", "vector-db indexing")
    ensure_stage7_dataset()
    docs = load_docs()

    if QdrantClient is None or models is None:
        print("\nqdrant-client is not installed.")
        print("Install optional deps: pip install -r red-book/src/stage-7/requirements-optional.txt")
        return

    # Build deterministic vectors from local TF-IDF index for teaching purposes.
    vectorizer, matrix = build_tfidf_index(docs)
    vector_size = int(matrix.shape[1])

    try:
        # Expect local Qdrant service on port 6333.
        client = QdrantClient(host="localhost", port=6333, timeout=5)
        client.get_collections()
    except Exception as exc:
        print("\nCannot connect to local Qdrant at localhost:6333")
        print(f"error={exc}")
        print("Please start Qdrant, then rerun this script.")
        return

    # Recreate collection with explicit delete/create so behavior is clear to learners.
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

    query = "How often should knowledge index be refreshed?"
    q_vec = vectorizer.transform([query]).toarray()[0].astype(np.float32).tolist()

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=q_vec,
        limit=3,
        with_payload=True,
    )
    hits = response.points

    print("\n=== Qdrant indexing/search result ===")
    print(f"collection={COLLECTION_NAME}")
    print(f"vector_size={vector_size}")
    print(f"point_count={len(points)}")
    print(f"query={query}")

    for hit in hits:
        payload = hit.payload or {}
        print(
            {
                "score": round(float(hit.score), 4),
                "chunk_id": payload.get("chunk_id"),
                "source": payload.get("source"),
                "section": payload.get("section"),
            }
        )

    print("\nInterpretation: vectors are now stored in local Qdrant with metadata payload.")


if __name__ == "__main__":
    main()
