"""Stage 7 Topic 02: Embeddings and indexing (intermediate).

Focus: inspect nearest chunks for one query and understand index behavior.
"""

from __future__ import annotations

from stage7_utils import build_tfidf_index, dense_retrieve, ensure_stage7_dataset, load_docs, print_data_declaration

print_data_declaration("Topic02 Embeddings Index Intermediate", "embedding diagnostics")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "What are API reliability targets and latency limits?"
rows = dense_retrieve(query, docs, vectorizer, matrix, role="engineering", top_k=4)

print("\nquery=", query)
print("top_k_results=")
for r in rows:
    print(
        {
            "chunk_id": r["chunk"].chunk_id,
            "section": r["chunk"].section,
            "score": round(r["score"], 4),
            "source": r["chunk"].source,
        }
    )

print("\nInterpretation: nearest neighbors in embedding space drive downstream answer quality.")
