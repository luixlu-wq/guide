"""Stage 5 Topic 01A: tokenization basics (simple).

Data: small in-script text list
Records/Samples: 4
Input schema: raw text strings
Output schema: token lists + token counts
Split/Eval policy: not applicable
Type: tokenization demonstration
"""

from __future__ import annotations

from stage5_utils import tokenize_whitespace


# Workflow:
# 1) Load simple text examples.
# 2) Tokenize with whitespace split.
# 3) Print token lists and counts.
def main() -> None:
    texts = [
        "AI changes software engineering workflows.",
        "Multi-head attention helps model different relationships.",
        "Prompt clarity improves output reliability.",
        "RAG combines retrieval and generation.",
    ]

    print("Data declaration")
    print("source=in_script_texts")
    print(f"records={len(texts)}")
    print("input_schema=raw_text:str")
    print("output_schema=tokens:list[str], token_count:int")

    total = 0
    for i, text in enumerate(texts, start=1):
        toks = tokenize_whitespace(text)
        total += len(toks)
        print(f"sample={i} token_count={len(toks)} tokens={toks}")

    print(f"average_token_count={total/len(texts):.2f}")
    print("Interpretation: token count depends on tokenizer choice and text structure.")


if __name__ == "__main__":
    main()
