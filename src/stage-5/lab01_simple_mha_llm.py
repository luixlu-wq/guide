"""Stage 5 Lab 01: build a simple multi-head-attention LLM (step by step).

Data: in-script tiny text corpus (character-level language modeling)
Records/Samples: 18 short text lines -> sliding-window training samples
Input schema: x_ids[int] with shape [batch, seq_len]
Output schema: y_ids[int] with shape [batch, seq_len] (next-token targets)
Split/Eval policy: fixed 90/10 split over generated windows
Type: decoder-only language model with nn.MultiheadAttention

Lab operation steps:
1) Choose fixed corpus and task (next-token prediction).
2) Declare data source and structure.
3) Build tokenizer (char vocab) and encode text.
4) Build fixed training/validation windows.
5) Define TinyMHALLM model (MHA + FFN + residual + layernorm).
6) Run baseline evaluation before training.
7) Train with AdamW and monitor train/val loss.
8) Generate text from a prompt and inspect quality changes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass(frozen=True)
class LabConfig:
    seq_len: int = 48
    d_model: int = 96
    num_heads: int = 4
    num_layers: int = 2
    dropout: float = 0.1
    batch_size: int = 32
    train_steps: int = 240
    eval_interval: int = 40
    lr: float = 2e-3
    weight_decay: float = 1e-2
    seed: int = 123


class TinyDecoderBlock(nn.Module):
    """One decoder block with masked multi-head self-attention."""

    def __init__(self, d_model: int, num_heads: int, dropout: float) -> None:
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.ln2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor, attn_mask: torch.Tensor) -> torch.Tensor:
        # Functional role: route token information with masked self-attention.
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + attn_out

        # Functional role: position-wise nonlinear transformation.
        h = self.ln2(x)
        x = x + self.ff(h)
        return x


class TinyMHALLM(nn.Module):
    """Minimal decoder-only language model that uses multi-head attention."""

    def __init__(
        self,
        vocab_size: int,
        seq_len: int,
        d_model: int,
        num_heads: int,
        num_layers: int,
        dropout: float,
    ) -> None:
        super().__init__()
        self.seq_len = seq_len
        self.token_embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(seq_len, d_model)
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList(
            [TinyDecoderBlock(d_model, num_heads, dropout) for _ in range(num_layers)]
        )
        self.final_ln = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size)

    def _causal_mask(self, t: int, device: torch.device) -> torch.Tensor:
        # True means "blocked" for nn.MultiheadAttention bool masks.
        return torch.triu(torch.ones(t, t, device=device, dtype=torch.bool), diagonal=1)

    def forward(
        self, x_ids: torch.Tensor, y_ids: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        bsz, t = x_ids.shape
        if t > self.seq_len:
            raise ValueError(f"Sequence length {t} exceeds configured max {self.seq_len}.")

        pos = torch.arange(t, device=x_ids.device).unsqueeze(0)
        x = self.token_embed(x_ids) + self.pos_embed(pos)
        x = self.drop(x)

        mask = self._causal_mask(t, x_ids.device)
        for block in self.blocks:
            x = block(x, mask)

        logits = self.lm_head(self.final_ln(x))
        loss = None
        if y_ids is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y_ids.reshape(-1))
        return logits, loss


def build_char_vocab(text: str) -> tuple[dict[str, int], dict[int, str]]:
    chars = sorted(set(text))
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for ch, i in stoi.items()}
    return stoi, itos


def encode(text: str, stoi: dict[str, int]) -> torch.Tensor:
    return torch.tensor([stoi[c] for c in text], dtype=torch.long)


def decode(ids: torch.Tensor, itos: dict[int, str]) -> str:
    return "".join(itos[int(i)] for i in ids)


def make_windows(token_ids: torch.Tensor, seq_len: int) -> tuple[torch.Tensor, torch.Tensor]:
    xs: list[torch.Tensor] = []
    ys: list[torch.Tensor] = []
    for i in range(0, token_ids.numel() - seq_len - 1):
        xs.append(token_ids[i : i + seq_len])
        ys.append(token_ids[i + 1 : i + seq_len + 1])
    return torch.stack(xs), torch.stack(ys)


def sample_batch(
    x: torch.Tensor, y: torch.Tensor, batch_size: int, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    idx = torch.randint(0, x.size(0), (batch_size,))
    return x[idx].to(device), y[idx].to(device)


@torch.no_grad()
def estimate_loss(
    model: TinyMHALLM,
    x: torch.Tensor,
    y: torch.Tensor,
    device: torch.device,
    batch_size: int,
    batches: int = 8,
) -> float:
    model.eval()
    losses: list[float] = []
    for _ in range(batches):
        xb, yb = sample_batch(x, y, batch_size, device)
        _, loss = model(xb, yb)
        if loss is None:
            continue
        losses.append(float(loss.item()))
    model.train()
    return float(sum(losses) / max(1, len(losses)))


@torch.no_grad()
def generate_text(
    model: TinyMHALLM,
    prompt: str,
    stoi: dict[str, int],
    itos: dict[int, str],
    device: torch.device,
    max_new_tokens: int = 160,
    temperature: float = 0.9,
) -> str:
    # Functional role: autoregressive decoding loop using trained model logits.
    safe_prompt = "".join(ch for ch in prompt if ch in stoi)
    if not safe_prompt:
        safe_prompt = "model"
    ids = torch.tensor([[stoi[ch] for ch in safe_prompt]], dtype=torch.long, device=device)

    for _ in range(max_new_tokens):
        x_cond = ids[:, -model.seq_len :]
        logits, _ = model(x_cond)
        next_logits = logits[:, -1, :] / max(temperature, 1e-5)
        probs = F.softmax(next_logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        ids = torch.cat([ids, next_id], dim=1)

    return decode(ids[0].cpu(), itos)


def main() -> None:
    cfg = LabConfig()
    torch.manual_seed(cfg.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Step 1/2: fixed corpus and declared data structure.
    corpus_lines = [
        "attention maps token relations in context.",
        "multi-head attention uses several parallel heads.",
        "each head learns different interaction patterns.",
        "transformer blocks combine attention and feed-forward.",
        "layer norm and residual connections improve training.",
        "language modeling predicts the next token.",
        "causal masking blocks future tokens.",
        "embeddings map token ids to vectors.",
        "prompt clarity changes response quality.",
        "structured outputs improve reliability.",
        "retrieval adds external evidence to generation.",
        "hallucination risk requires validation checks.",
        "evaluation needs fixed data and fixed metrics.",
        "small models help understand core mechanics.",
        "training loop updates parameters by gradients.",
        "optimizer steps reduce prediction error.",
        "debugging requires controlled experiments.",
        "reproducibility needs fixed seeds and logs.",
    ]
    corpus_text = "\n".join(corpus_lines)

    stoi, itos = build_char_vocab(corpus_text)
    ids = encode(corpus_text, stoi)
    x_all, y_all = make_windows(ids, cfg.seq_len)

    split = int(0.9 * x_all.size(0))
    x_train, y_train = x_all[:split], y_all[:split]
    x_val, y_val = x_all[split:], y_all[split:]

    print("LAB DATA DECLARATION")
    print("source=in_script_tiny_llm_corpus")
    print(f"records={len(corpus_lines)} text_chars={len(corpus_text)}")
    print(f"vocab_size={len(stoi)}")
    print("input_schema=x_ids:int[batch,seq_len]")
    print("output_schema=y_ids:int[batch,seq_len] (next-token targets)")
    print(f"split_policy=fixed_90_10 windows -> train={x_train.size(0)} val={x_val.size(0)}")
    print(f"device={device.type}")
    print()

    # Step 3/4/5: define model and baseline.
    model = TinyMHALLM(
        vocab_size=len(stoi),
        seq_len=cfg.seq_len,
        d_model=cfg.d_model,
        num_heads=cfg.num_heads,
        num_layers=cfg.num_layers,
        dropout=cfg.dropout,
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)

    baseline_val = estimate_loss(model, x_val, y_val, device, cfg.batch_size)
    print("STEP 6 BASELINE")
    print(f"baseline_val_loss={baseline_val:.4f}")
    print(f"baseline_val_perplexity={math.exp(baseline_val):.2f}")
    print()

    # Step 7: train and monitor.
    print("STEP 7 TRAINING")
    for step in range(1, cfg.train_steps + 1):
        xb, yb = sample_batch(x_train, y_train, cfg.batch_size, device)
        _, loss = model(xb, yb)
        if loss is None:
            raise RuntimeError("Loss should not be None during training.")
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        if step % cfg.eval_interval == 0 or step == 1:
            train_eval = estimate_loss(model, x_train, y_train, device, cfg.batch_size, batches=4)
            val_eval = estimate_loss(model, x_val, y_val, device, cfg.batch_size, batches=4)
            print(
                f"step={step:03d} train_loss={train_eval:.4f} val_loss={val_eval:.4f} "
                f"val_ppl={math.exp(val_eval):.2f}"
            )
    print()

    # Step 8: generation after training.
    print("STEP 8 GENERATION")
    prompt = "multi-head attention "
    sample = generate_text(model, prompt, stoi, itos, device)
    final_val = estimate_loss(model, x_val, y_val, device, cfg.batch_size)
    print(f"final_val_loss={final_val:.4f}")
    print(f"final_val_perplexity={math.exp(final_val):.2f}")
    print("generated_sample:")
    print(sample)
    print()
    print("Interpretation:")
    print("- If final loss/perplexity is lower than baseline, training learned token patterns.")
    print("- Generated text should show partial grammar and topic consistency from corpus.")
    print("- This is a teaching-scale LLM, not a production-quality model.")


if __name__ == "__main__":
    main()
