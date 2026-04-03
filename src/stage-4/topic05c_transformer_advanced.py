"""Stage 4 Topic 05C: transformer next-token modeling (advanced).

Data: synthetic token sequences generated in-script
Rows: 8,000 sequences
Input shape: [N, 18] token ids
Target: next-token ids, shape [N, 18]
Split: fixed train/validation/test split
Type: autoregressive next-token prediction
"""

from __future__ import annotations

import math

import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 8_000, seq_len: int = 19, vocab_size: int = 40):
    generator = torch.Generator(device="cpu").manual_seed(53)
    starts = torch.randint(0, vocab_size, (n_rows, 1), generator=generator)
    steps = torch.randint(1, 4, (n_rows, 1), generator=generator)

    idx = torch.arange(seq_len).unsqueeze(0)
    tokens = (starts + idx * steps) % vocab_size
    tokens = tokens.long()

    x = tokens[:, :-1]
    y = tokens[:, 1:]
    return x, y


class TinyCausalTransformer(torch.nn.Module):
    def __init__(self, vocab_size: int = 40, seq_len: int = 18) -> None:
        super().__init__()
        d_model = 48
        self.token_emb = torch.nn.Embedding(vocab_size, d_model)
        self.pos_emb = torch.nn.Embedding(seq_len, d_model)

        layer = torch.nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=4,
            dim_feedforward=96,
            dropout=0.1,
            batch_first=True,
        )
        self.encoder = torch.nn.TransformerEncoder(layer, num_layers=2)
        self.head = torch.nn.Linear(d_model, vocab_size)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        bsz, seq_len = tokens.shape
        positions = torch.arange(seq_len, device=tokens.device).unsqueeze(0).expand(bsz, -1)
        x = self.token_emb(tokens) + self.pos_emb(positions)

        # Causal mask prevents token t from seeing future tokens > t.
        mask = torch.nn.Transformer.generate_square_subsequent_mask(seq_len, device=tokens.device)
        h = self.encoder(x, mask=mask)
        return self.head(h)


def evaluate(model: torch.nn.Module, loader: DataLoader, loss_fn: torch.nn.Module):
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    total_correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            logits = model(xb)
            loss = loss_fn(logits.reshape(-1, logits.size(-1)), yb.reshape(-1))
            total_loss += float(loss.item()) * yb.numel()
            pred = logits.argmax(dim=-1)
            total_correct += int((pred == yb).sum().item())
            total_tokens += yb.numel()
    mean_loss = total_loss / total_tokens
    token_acc = total_correct / total_tokens
    ppl = math.exp(mean_loss)
    return mean_loss, token_acc, ppl


# Workflow:
# 1) Build synthetic autoregressive sequences with predictable token transitions.
# 2) Train causal transformer to predict next token at each step.
# 3) Evaluate token accuracy and perplexity on fixed validation/test splits.
def main() -> None:
    torch.manual_seed(53)

    x, y = make_data(n_rows=scaled_int(8_000, quick_value=3_000))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic arithmetic token sequences")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=53
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=53
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    model = TinyCausalTransformer()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.002, weight_decay=1e-4)

    epochs = scaled_int(12, quick_value=6)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            logits = model(xb)
            loss = loss_fn(logits.reshape(-1, logits.size(-1)), yb.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

        if epoch in (1, max(2, epochs // 2), epochs):
            val_loss, val_acc, val_ppl = evaluate(model, val_loader, loss_fn)
            print(
                f"epoch={epoch:02d} val_loss={val_loss:.4f} "
                f"val_token_acc={val_acc:.4f} val_ppl={val_ppl:.2f}"
            )

    test_loss, test_acc, test_ppl = evaluate(model, test_loader, loss_fn)
    print(f"test_loss={test_loss:.4f} test_token_acc={test_acc:.4f} test_ppl={test_ppl:.2f}")
    print("Interpretation: advanced complexity is causal masking + sequence-level token prediction.")


if __name__ == "__main__":
    main()
