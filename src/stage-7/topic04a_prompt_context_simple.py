"""Stage 7 Topic 04A: Prompt context assembly (simple)."""

from __future__ import annotations

from stage7_utils import build_tfidf_index, dense_retrieve, ensure_stage7_dataset, load_docs, print_data_declaration


def build_prompt(query: str, retrieved_rows: list[dict]) -> str:
    """Build a grounded prompt with context and citation labels."""
    context_lines = []
    for i, row in enumerate(retrieved_rows, start=1):
        chunk = row["chunk"]
        context_lines.append(f"[{i}] source={chunk.source} text={chunk.text}")

    return (
        "Answer only from context. If evidence is missing, say insufficient evidence.\n"
        "Context:\n"
        + "\n".join(context_lines)
        + f"\nQuestion: {query}"
    )


print_data_declaration("Topic04A Prompt Context Simple", "prompt assembly")
ensure_stage7_dataset()
docs = load_docs()
vectorizer, matrix = build_tfidf_index(docs)

query = "How often should the knowledge index be refreshed?"
retrieved = dense_retrieve(query, docs, vectorizer, matrix, role="engineering", top_k=2)
prompt = build_prompt(query, retrieved)

print("\nquery=", query)
print("\nconstructed_prompt=\n")
print(prompt)
