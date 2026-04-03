"""Stage 4 Topic 05A: transformer attention mechanics (simple).

Data: tiny synthetic token embeddings generated in-script
Rows: batch=1, sequence length=4
Input shape: [1, 4, 4]
Target: no supervised target (mechanics demo)
Split: none
Type: attention mechanics demonstration
"""

from __future__ import annotations

import math

import torch


# Workflow:
# 1) Build a tiny sequence embedding tensor.
# 2) Compute scaled dot-product attention (QK^T / sqrt(d)).
# 3) Show attention weights and mixed output vectors.
def main() -> None:
    torch.manual_seed(51)

    x = torch.tensor(
        [
            [
                [1.0, 0.0, 1.0, 0.0],
                [0.8, 0.2, 0.9, 0.1],
                [0.1, 1.0, 0.0, 1.0],
                [0.0, 0.9, 0.1, 0.8],
            ]
        ]
    )
    print("Data declaration")
    print("source=synthetic tiny embeddings")
    print("input_shape=", tuple(x.shape), "(batch, seq_len, d_model)")

    q = x
    k = x
    v = x
    d = x.size(-1)

    scores = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(d)
    weights = torch.softmax(scores, dim=-1)
    mixed = torch.matmul(weights, v)

    print("attention_weights_row0=", weights[0, 0].tolist())
    print("mixed_output_shape=", tuple(mixed.shape))
    print("Interpretation: each token becomes a weighted mix of all token values.")


if __name__ == "__main__":
    main()
