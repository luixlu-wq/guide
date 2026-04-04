"""Stage 7 Topic 02A: Embeddings and indexing (simple)."""

from __future__ import annotations

from stage7_utils import build_tfidf_index, ensure_stage7_dataset, load_docs, print_data_declaration

print_data_declaration("Topic02A Embeddings Index Simple", "embedding/index")
ensure_stage7_dataset()
docs = load_docs()

vectorizer, matrix = build_tfidf_index(docs)

print("\n=== Index summary ===")
print(f"doc_count={len(docs)}")
print(f"matrix_shape={matrix.shape}")
print(f"vocab_size={len(vectorizer.vocabulary_)}")
print("sample_vocab_terms=", list(vectorizer.vocabulary_.keys())[:12])

print("\nInterpretation: vector index size depends on corpus and tokenizer vocabulary.")
