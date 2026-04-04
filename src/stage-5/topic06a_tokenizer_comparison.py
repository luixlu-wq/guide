"""Stage 5 Topic 06A: tokenizer comparison (simple -> operatable).

Data: in-script technical text samples (including GIS-like terms)
Records/Samples: 5
Input schema: raw_text:str
Output schema: tokenizer_name, token_count, tokens_preview
Split/Eval policy: fixed list
Type: tokenization and OOV-risk diagnostics
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from stage5_utils import tokenize_subword_like, tokenize_whitespace


def try_tiktoken_tokens(text: str) -> list[str] | None:
    try:
        import tiktoken  # type: ignore
    except Exception:
        return None
    enc = tiktoken.get_encoding("cl100k_base")
    ids = enc.encode(text)
    return [str(tok_id) for tok_id in ids]


def try_llama_tokens(text: str) -> list[str] | None:
    # Try a local/available HF tokenizer path; fallback to None if unavailable.
    try:
        from transformers import AutoTokenizer  # type: ignore
    except Exception:
        return None
    try:
        tok = AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer", local_files_only=True)
    except Exception:
        return None
    return tok.tokenize(text)


def oov_like_rate(tokens: list[str], vocab: set[str]) -> float:
    if not tokens:
        return 0.0
    missing = sum(1 for t in tokens if t not in vocab)
    return missing / len(tokens)


# Workflow:
# 1) Tokenize same technical text with multiple tokenizer strategies.
# 2) Compare token counts and preview token boundaries.
# 3) Simulate OOV-like behavior with a constrained vocabulary.
def main() -> None:
    texts = [
        "Ontario GIS polygon metadata includes EPSG:4326 coordinates and zoning identifiers.",
        "MapToGo integrates scenic-spot descriptions with retrieval-based grounding.",
        "The model must return valid JSON with citations and confidence_note fields.",
        "Tokenization quality impacts both context budget and retrieval chunk boundaries.",
        "Long camelCaseIdentifiersAndGeoHashes can fragment into many sub-tokens.",
    ]

    print("Data declaration")
    print("source=in_script_technical_text")
    print(f"records={len(texts)}")
    print("input_schema=raw_text:str")
    print("output_schema=tokenizer_name,token_count,tokens_preview")

    rows: list[dict[str, str | int | float]] = []
    constrained_vocab = {
        "ontario", "gis", "polygon", "metadata", "coordinates", "map", "to", "go",
        "json", "citations", "confidence", "tokenization", "quality", "retrieval",
    }

    for idx, text in enumerate(texts, start=1):
        ws = tokenize_whitespace(text)
        sw = tokenize_subword_like(text)
        tk = try_tiktoken_tokens(text)
        ll = try_llama_tokens(text)

        rows.append(
            {
                "sample_id": idx,
                "tokenizer": "whitespace",
                "token_count": len(ws),
                "tokens_preview": " | ".join(ws[:12]),
                "oov_like_rate": oov_like_rate([t.lower() for t in ws], constrained_vocab),
            }
        )
        rows.append(
            {
                "sample_id": idx,
                "tokenizer": "subword_like",
                "token_count": len(sw),
                "tokens_preview": " | ".join(sw[:12]),
                "oov_like_rate": oov_like_rate([t.replace('##', '').lower() for t in sw], constrained_vocab),
            }
        )
        if tk is not None:
            rows.append(
                {
                    "sample_id": idx,
                    "tokenizer": "tiktoken_cl100k_base",
                    "token_count": len(tk),
                    "tokens_preview": " | ".join(tk[:12]),
                    "oov_like_rate": float("nan"),
                }
            )
        if ll is not None:
            rows.append(
                {
                    "sample_id": idx,
                    "tokenizer": "llama_tokenizer",
                    "token_count": len(ll),
                    "tokens_preview": " | ".join(ll[:12]),
                    "oov_like_rate": float("nan"),
                }
            )

    df = pd.DataFrame(rows)
    print(df.groupby("tokenizer")["token_count"].mean().round(2).to_string())

    if "llama_tokenizer" not in set(df["tokenizer"]):
        print("Note: llama tokenizer not available locally; fallback comparisons still provided.")
    if "tiktoken_cl100k_base" not in set(df["tokenizer"]):
        print("Note: tiktoken not installed; install from requirements-optional for full comparison.")

    out_dir = Path(__file__).parent / "results" / "stage5"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "topic06a_tokenizer_comparison.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
    print("Interpretation: tokenizer choice changes token budget and OOV-like fragmentation behavior.")


if __name__ == "__main__":
    main()

