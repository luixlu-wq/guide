"""Stage 5 Topic 05A: manual attention math (simple).

Data: in-script 3-token sequence embeddings
Records/Samples: 1 sequence of length 3
Input schema: token embedding matrix X, shape [seq_len, d_model]
Output schema: attention scores, attention weights, context vectors
Split/Eval policy: not applicable (mechanism demo)
Type: transformer attention mechanics
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd


def softmax_rows(x: np.ndarray) -> np.ndarray:
    """Numerically stable row-wise softmax."""
    shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


# Workflow:
# 1) Build a tiny token-embedding matrix for a 3-token sentence.
# 2) Project embeddings into Q/K/V spaces.
# 3) Compute scaled dot-product attention by hand.
# 4) Save scores/weights/context as artifacts so learners can inspect every stage.
def main() -> None:
    # Small educational sequence: ["the", "river", "bank"].
    # Each row is one token vector in d_model=4.
    x = np.array(
        [
            [1.0, 0.2, 0.0, 0.1],  # "the"
            [0.1, 0.9, 0.3, 0.2],  # "river"
            [0.2, 0.3, 0.8, 0.7],  # "bank"
        ],
        dtype=np.float64,
    )
    tokens = ["the", "river", "bank"]
    seq_len, d_model = x.shape

    # Fixed linear projections for deterministic reproducibility.
    w_q = np.array(
        [
            [0.8, 0.1, 0.0, 0.0],
            [0.0, 0.7, 0.2, 0.0],
            [0.1, 0.0, 0.6, 0.1],
            [0.0, 0.2, 0.1, 0.7],
        ]
    )
    w_k = np.array(
        [
            [0.7, 0.0, 0.1, 0.1],
            [0.1, 0.8, 0.0, 0.1],
            [0.0, 0.2, 0.7, 0.0],
            [0.0, 0.1, 0.1, 0.8],
        ]
    )
    w_v = np.array(
        [
            [0.9, 0.0, 0.0, 0.1],
            [0.0, 0.9, 0.1, 0.0],
            [0.1, 0.0, 0.9, 0.0],
            [0.0, 0.1, 0.0, 0.9],
        ]
    )

    q = x @ w_q
    k = x @ w_k
    v = x @ w_v

    # Core attention equation: softmax(QK^T / sqrt(d_k)) V
    scale = math.sqrt(d_model)
    scores = (q @ k.T) / scale
    weights = softmax_rows(scores)
    context = weights @ v

    print("Data declaration")
    print("source=in_script_tokens")
    print(f"records=1 sequence | seq_len={seq_len} | d_model={d_model}")
    print("input_schema=X:[seq_len,d_model]")
    print("output_schema=scores:[seq_len,seq_len], weights:[seq_len,seq_len], context:[seq_len,d_model]")
    print()
    print("Tokens:", tokens)
    print("scores_shape:", scores.shape)
    print("weights_shape:", weights.shape)
    print("context_shape:", context.shape)
    print("Attention weights for token 'bank' attending to all tokens:")
    print(weights[2].round(4).tolist())

    out_dir = Path(__file__).parent / "results" / "stage5"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save a combined table so students can inspect intermediate mechanics.
    rows: list[dict[str, float | str]] = []
    for i, qtok in enumerate(tokens):
        for j, ktok in enumerate(tokens):
            rows.append(
                {
                    "query_token": qtok,
                    "key_token": ktok,
                    "score": float(scores[i, j]),
                    "weight": float(weights[i, j]),
                }
            )
    pd.DataFrame(rows).to_csv(out_dir / "topic05a_attention_math_scores.csv", index=False)
    pd.DataFrame(context, columns=[f"ctx_{i}" for i in range(d_model)]).assign(token=tokens).to_csv(
        out_dir / "topic05a_attention_math_context.csv", index=False
    )

    print("Saved: results/stage5/topic05a_attention_math_scores.csv")
    print("Saved: results/stage5/topic05a_attention_math_context.csv")
    print("Interpretation: this script exposes attention mechanics before framework abstractions.")


if __name__ == "__main__":
    main()

