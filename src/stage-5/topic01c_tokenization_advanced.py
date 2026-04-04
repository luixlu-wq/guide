"""Stage 5 Topic 01C: token budgeting and chunking (advanced).

Data: long in-script document
Records/Samples: 1 long text
Input schema: raw text
Output schema: chunk list with overlap and budget stats
Split/Eval policy: fixed chunk rules
Type: advanced tokenization/chunking for downstream RAG
"""

from __future__ import annotations

from stage5_utils import chunk_tokens, tokenize_subword_like


# Workflow:
# 1) Tokenize long text with a subword-like strategy.
# 2) Chunk tokens by fixed budget with overlap.
# 3) Report chunk stats for retrieval-friendly configuration.
def main() -> None:
    text = " ".join(
        [
            "Transformer layers rely on multi-head attention to aggregate context.",
            "Reliable LLM systems require prompt constraints and output validation.",
            "RAG quality depends heavily on chunk boundaries and retrieval ranking.",
            "Evaluation should track format validity, groundedness, and consistency.",
        ]
        * 20
    )

    tokens = tokenize_subword_like(text)
    chunks = chunk_tokens(tokens, chunk_size=120, overlap=30)

    print("Data declaration")
    print("source=in_script_long_text")
    print("records=1")
    print("input_schema=raw_text:str")
    print("output_schema=chunks:list[list[str]]")

    print(f"total_tokens={len(tokens)}")
    print(f"chunk_count={len(chunks)}")
    print("chunk_rule=chunk_size:120 overlap:30")

    for idx, ch in enumerate(chunks[:3], start=1):
        preview = " ".join(ch[:15])
        print(f"chunk_{idx}_size={len(ch)} preview={preview} ...")

    print("Interpretation: overlap preserves context continuity across chunk boundaries.")


if __name__ == "__main__":
    main()
