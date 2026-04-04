"""Stage 5 Topic 01: tokenization tradeoffs (intermediate).

Data: in-script article snippets
Records/Samples: 6
Input schema: raw text strings
Output schema: token counts per tokenizer + cost estimate
Split/Eval policy: fixed list
Type: tokenization and token-budget analysis
"""

from __future__ import annotations

from stage5_utils import estimate_token_cost, token_entropy, tokenize_subword_like, tokenize_whitespace


# Workflow:
# 1) Compare token counts across tokenizer styles.
# 2) Estimate relative serving cost from token counts.
# 3) Show token diversity entropy as a rough complexity signal.
def main() -> None:
    texts = [
        "NVIDIA reported strong quarterly growth but guided cautiously on supply constraints.",
        "The regulator opened an investigation into accounting practices.",
        "The company launched a new model with improved latency.",
        "Investors reacted to margin pressure and rising debt costs.",
        "Prompt version v2 produced higher schema-valid output rates.",
        "Retrieval quality declined when chunk size became too small.",
    ]

    print("Data declaration")
    print("source=in_script_snippets")
    print(f"records={len(texts)}")
    print("input_schema=raw_text:str")
    print("output_schema=token_metrics_per_strategy")

    ws_total = 0
    sw_total = 0

    for text in texts:
        ws = tokenize_whitespace(text)
        sw = tokenize_subword_like(text)
        ws_total += len(ws)
        sw_total += len(sw)

    ws_cost = estimate_token_cost(ws_total, price_per_1k_tokens=0.002)
    sw_cost = estimate_token_cost(sw_total, price_per_1k_tokens=0.002)

    print(f"whitespace_tokens_total={ws_total}")
    print(f"subword_like_tokens_total={sw_total}")
    print(f"whitespace_estimated_cost={ws_cost:.6f}")
    print(f"subword_like_estimated_cost={sw_cost:.6f}")

    sample_tokens = tokenize_subword_like(texts[0])
    print(f"sample_subword_tokens={sample_tokens}")
    print(f"sample_subword_entropy={token_entropy(sample_tokens):.4f}")
    print("Interpretation: tokenization strategy changes both budget and context usage.")


if __name__ == "__main__":
    main()
