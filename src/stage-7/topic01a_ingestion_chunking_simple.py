"""Stage 7 Topic 01A: Ingestion and chunking (simple)."""

from __future__ import annotations

from stage7_utils import ensure_stage7_dataset, load_docs, print_data_declaration

print_data_declaration("Topic01A Ingestion Chunking Simple", "ingestion/chunking")
docs_path, eval_path = ensure_stage7_dataset()

docs = load_docs(docs_path)

print("\n=== Workflow ===")
print("1) ensure dataset exists")
print("2) inspect first chunks and metadata")
print("3) verify chunk ids are traceable")

print(f"docs_path={docs_path}")
print(f"eval_path={eval_path}")
print(f"doc_count={len(docs)}")

for row in docs[:3]:
    print(
        {
            "chunk_id": row.chunk_id,
            "source": row.source,
            "section": row.section,
            "acl_tag": row.acl_tag,
            "text": row.text,
        }
    )

print("\nInterpretation: ingestion quality starts with clear metadata and traceable chunk IDs.")
