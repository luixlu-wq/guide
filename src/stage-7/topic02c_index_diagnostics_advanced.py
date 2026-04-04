"""Stage 7 Topic 02C: Index diagnostics (advanced)."""

from __future__ import annotations

from stage7_utils import build_tfidf_index, ensure_stage7_dataset, load_docs, print_data_declaration

print_data_declaration("Topic02C Index Diagnostics Advanced", "index diagnostics")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

# Compute per-document non-zero feature counts to detect sparse/weak chunks.
feature_density = matrix.getnnz(axis=1)

print("\n=== Index diagnostics ===")
print(f"matrix_shape={matrix.shape}")
print(f"min_feature_count={int(feature_density.min())}")
print(f"max_feature_count={int(feature_density.max())}")
print(f"avg_feature_count={float(feature_density.mean()):.2f}")

weak_idx = [i for i, n in enumerate(feature_density) if n < 6]
print(f"potentially_weak_chunks={len(weak_idx)}")
if weak_idx:
    for i in weak_idx[:3]:
        print({"chunk_id": docs[i].chunk_id, "text": docs[i].text})

print("\nInterpretation: very sparse chunks often underperform in retrieval and should be inspected.")
