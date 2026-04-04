"""Stage 5 Topic 01: Multi-Head Attention deep understanding demo.

Data: synthetic token embedding tensors generated in-script
Rows/Samples: batch_size=2 sequences
Input schema: x tensor, shape [batch, seq_len, d_model]
Output schema: attention outputs and attention-weight tensors
Split/Eval policy: not applicable (mechanism demo)
Type: transformer mechanism understanding
"""

from __future__ import annotations

import math

import torch


def manual_scaled_dot_product_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    mask: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Compute one-head scaled dot-product attention.

    q, k, v shapes: [batch, seq_len, d_k]
    Returns:
        output: [batch, seq_len, d_k]
        weights: [batch, seq_len, seq_len]
    """
    d_k = q.size(-1)
    scores = q @ k.transpose(-1, -2) / math.sqrt(d_k)

    if mask is not None:
        scores = scores + mask

    weights = torch.softmax(scores, dim=-1)
    output = weights @ v
    return output, weights


# Workflow:
# 1) Build synthetic token embeddings and inspect single-head attention.
# 2) Run nn.MultiheadAttention and inspect per-head attention maps.
# 3) Show how a TransformerEncoderLayer uses multi-head attention inside a larger block.
def main() -> None:
    torch.manual_seed(5)

    batch_size = 2
    seq_len = 6
    d_model = 16
    num_heads = 4
    d_head = d_model // num_heads

    x = torch.randn(batch_size, seq_len, d_model)

    print("Data declaration")
    print(f"source=synthetic token embeddings")
    print(f"rows/samples=batch_size={batch_size}")
    print(f"input_shape={tuple(x.shape)} (batch, seq_len, d_model)")
    print(f"d_model={d_model}, num_heads={num_heads}, d_head={d_head}")

    # ----- Part A: one-head attention (manual math path) -----
    q1 = x[:, :, :d_head]
    k1 = x[:, :, :d_head]
    v1 = x[:, :, :d_head]

    one_head_out, one_head_weights = manual_scaled_dot_product_attention(q1, k1, v1)

    print("\nPart A - Single-head self-attention (manual)")
    print("one_head_qkv_shape:", tuple(q1.shape))
    print("one_head_output_shape:", tuple(one_head_out.shape))
    print("one_head_weights_shape:", tuple(one_head_weights.shape))
    print("example weights (batch0, token0 -> all tokens):")
    print(one_head_weights[0, 0].tolist())

    # ----- Part B: multi-head attention (framework path) -----
    mha = torch.nn.MultiheadAttention(
        embed_dim=d_model,
        num_heads=num_heads,
        batch_first=True,
    )

    mha_out, mha_weights = mha(
        x,
        x,
        x,
        need_weights=True,
        average_attn_weights=False,
    )

    print("\nPart B - Multi-head self-attention (PyTorch)")
    print("mha_output_shape:", tuple(mha_out.shape))
    print("mha_weights_shape:", tuple(mha_weights.shape), "(batch, num_heads, tgt_len, src_len)")
    print("example weights (batch0, head0, token0 -> all tokens):")
    print(mha_weights[0, 0, 0].tolist())

    # Show that different heads can attend differently.
    head0 = mha_weights[0, 0, 0]
    head1 = mha_weights[0, 1, 0]
    mean_abs_diff = torch.mean(torch.abs(head0 - head1)).item()
    print(f"head0_vs_head1_mean_abs_diff={mean_abs_diff:.6f}")

    # ----- Part C: Transformer block context -----
    encoder_layer = torch.nn.TransformerEncoderLayer(
        d_model=d_model,
        nhead=num_heads,
        dim_feedforward=64,
        batch_first=True,
    )
    transformer_out = encoder_layer(x)

    print("\nPart C - TransformerEncoderLayer context")
    print("transformer_output_shape:", tuple(transformer_out.shape))

    print("\nConcept summary")
    print("- Self-attention: one attention mechanism over a sequence.")
    print("- Multi-head attention: multiple attention heads in parallel + concat + projection.")
    print("- Transformer layer: multi-head attention + feed-forward + residual + layer norm.")


if __name__ == "__main__":
    main()
