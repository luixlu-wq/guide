"""Stage 5 Topic 05B: minimal transformer block (baseline).

Data: in-script tiny character corpus
Records/Samples: generated sliding windows from corpus
Input schema: x_ids:[batch, seq_len], y_ids:[batch, seq_len]
Output schema: logits:[batch, seq_len, vocab_size], loss
Split/Eval policy: fixed 90/10 train/validation split
Type: decoder-only next-token training baseline
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class MinimalDecoderBlock(nn.Module):
    """Single decoder-style block with causal self-attention + FFN."""

    def __init__(self, d_model: int, nhead: int, ff_dim: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.ln2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, ff_dim),
            nn.ReLU(),
            nn.Linear(ff_dim, d_model),
        )

    def forward(self, x: torch.Tensor, attn_mask: torch.Tensor) -> torch.Tensor:
        # Pre-norm attention.
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + attn_out

        # Pre-norm feed-forward.
        h2 = self.ln2(x)
        x = x + self.ff(h2)
        return x


class MiniTransformerLM(nn.Module):
    """Tiny decoder-only LM for educational baseline training."""

    def __init__(self, vocab_size: int, seq_len: int, d_model: int = 64, nhead: int = 4, ff_dim: int = 128):
        super().__init__()
        self.seq_len = seq_len
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(seq_len, d_model)
        self.block = MinimalDecoderBlock(d_model, nhead, ff_dim)
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, x_ids: torch.Tensor) -> torch.Tensor:
        bsz, t = x_ids.shape
        device = x_ids.device
        pos = torch.arange(t, device=device).unsqueeze(0).expand(bsz, t)

        x = self.token_emb(x_ids) + self.pos_emb(pos)

        # Strict causal mask: token i cannot attend to j>i.
        causal_mask = torch.full((t, t), float("-inf"), device=device).triu(diagonal=1)
        x = self.block(x, causal_mask)
        x = self.ln_f(x)
        return self.lm_head(x)


def build_char_dataset(text: str, seq_len: int) -> tuple[torch.Tensor, torch.Tensor, dict[str, int], list[str]]:
    chars = sorted(set(text))
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = chars
    ids = [stoi[ch] for ch in text]

    x_rows: list[list[int]] = []
    y_rows: list[list[int]] = []
    for i in range(0, len(ids) - seq_len - 1):
        x_rows.append(ids[i : i + seq_len])
        y_rows.append(ids[i + 1 : i + seq_len + 1])

    x = torch.tensor(x_rows, dtype=torch.long)
    y = torch.tensor(y_rows, dtype=torch.long)
    return x, y, stoi, itos


def eval_loss(model: nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    ce = nn.CrossEntropyLoss()
    losses = []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            logits = model(xb)
            loss = ce(logits.reshape(-1, logits.size(-1)), yb.reshape(-1))
            losses.append(float(loss.item()))
    return float(np.mean(losses)) if losses else float("nan")


# Workflow:
# 1) Build a tiny character-level dataset and fixed split.
# 2) Train a single-block decoder transformer with causal mask.
# 3) Compare baseline vs final validation loss/perplexity.
# 4) Save before/after evidence.
def main() -> None:
    torch.manual_seed(505)
    np.random.seed(505)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    text = (
        "attention helps models focus on relevant tokens. "
        "multi head attention captures different relationships in parallel. "
        "transformers use causal masks for next token prediction. "
    )
    seq_len = 24
    batch_size = 32

    x, y, stoi, _ = build_char_dataset(text, seq_len=seq_len)
    n = len(x)
    n_train = int(0.9 * n)
    x_train, y_train = x[:n_train], y[:n_train]
    x_val, y_val = x[n_train:], y[n_train:]

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=batch_size, shuffle=False)

    model = MiniTransformerLM(vocab_size=len(stoi), seq_len=seq_len).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    ce = nn.CrossEntropyLoss()

    baseline_val_loss = eval_loss(model, val_loader, device)
    epochs = 30
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)
            logits = model(xb)
            loss = ce(logits.reshape(-1, logits.size(-1)), yb.reshape(-1))
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            opt.step()

        if epoch in (1, 10, 20, epochs):
            val_loss = eval_loss(model, val_loader, device)
            print(f"epoch={epoch:02d} val_loss={val_loss:.4f} val_ppl={math.exp(min(20.0, val_loss)):.2f}")

    final_val_loss = eval_loss(model, val_loader, device)

    print("Data declaration")
    print("source=in_script_tiny_corpus")
    print(f"records={n} windows | vocab_size={len(stoi)} | seq_len={seq_len}")
    print("input_schema=x_ids:[batch,seq_len]")
    print("output_schema=next_token_logits:[batch,seq_len,vocab_size]")
    print(f"device={device.type}")
    print(f"baseline_val_loss={baseline_val_loss:.4f} final_val_loss={final_val_loss:.4f}")
    print(f"baseline_val_ppl={math.exp(min(20.0, baseline_val_loss)):.2f}")
    print(f"final_val_ppl={math.exp(min(20.0, final_val_loss)):.2f}")

    out_dir = Path(__file__).parent / "results" / "stage5"
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        [
            {
                "run_id": "stage5_topic05b_min_transformer",
                "stage": "5",
                "topic_or_module": "topic05b_min_transformer",
                "metric_name": "val_loss",
                "before_value": baseline_val_loss,
                "after_value": final_val_loss,
                "delta": final_val_loss - baseline_val_loss,
                "dataset_or_eval_set": "tiny_char_val",
                "seed_or_config_id": "seed505",
                "decision": "promote" if final_val_loss < baseline_val_loss else "hold",
            }
        ]
    )
    out_path = out_dir / "topic05b_min_transformer_metrics.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
    print("Interpretation: this script maps transformer mechanics to a runnable next-token baseline.")


if __name__ == "__main__":
    main()

