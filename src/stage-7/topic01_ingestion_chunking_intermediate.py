"""Stage 7 Topic 01: Ingestion and chunking (intermediate).

Focus: compare naive sentence split vs metadata-preserving chunking summary.
"""

from __future__ import annotations

from stage7_utils import ensure_stage7_dataset, load_docs, print_data_declaration


def naive_split(text: str, max_len: int = 55) -> list[str]:
    """Naive character-window split used to show boundary problems."""
    out = []
    for start in range(0, len(text), max_len):
        out.append(text[start : start + max_len])
    return out


print_data_declaration("Topic01 Ingestion Chunking Intermediate", "chunk quality comparison")
ensure_stage7_dataset()
docs = load_docs()

sample = docs[0]
naive_chunks = naive_split(sample.text, max_len=40)

print("\n=== Comparison ===")
print("original_text=", sample.text)
print("\nnaive_chunks=")
for idx, c in enumerate(naive_chunks, start=1):
    print(f"  {idx}. {c}")

print("\nmetadata_preserving_chunk=")
print(
    {
        "chunk_id": sample.chunk_id,
        "section": sample.section,
        "source": sample.source,
        "text": sample.text,
    }
)

print("\nInterpretation: naive chunks can split critical facts; semantic chunks keep meaning intact.")
