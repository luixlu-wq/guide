"""Stage 4 Topic 05: transformer encoder classifier (intermediate).

Data: synthetic token sequences generated in-script
Rows: 6,000
Input shape: [N, 12] token ids
Target: class label {0,1}, shape [N]
Split: fixed train/validation/test split
Type: sequence classification with transformer encoder
"""

from __future__ import annotations

import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def make_data(n_rows: int = 6_000, seq_len: int = 12, vocab_size: int = 32):
    generator = torch.Generator(device="cpu").manual_seed(52)
    tokens = torch.randint(0, vocab_size, (n_rows, seq_len), generator=generator)
    high_count = (tokens >= (vocab_size // 2)).sum(dim=1)
    y = (high_count > (seq_len // 2)).long()
    return tokens, y


class TransformerClassifier(torch.nn.Module):
    def __init__(self, vocab_size: int = 32, seq_len: int = 12) -> None:
        super().__init__()
        d_model = 32
        self.token_emb = torch.nn.Embedding(vocab_size, d_model)
        self.pos_emb = torch.nn.Embedding(seq_len, d_model)
        layer = torch.nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=4,
            dim_feedforward=64,
            dropout=0.1,
            batch_first=True,
        )
        self.encoder = torch.nn.TransformerEncoder(layer, num_layers=2)
        self.head = torch.nn.Linear(d_model, 2)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        bsz, seq_len = tokens.shape
        positions = torch.arange(seq_len, device=tokens.device).unsqueeze(0).expand(bsz, -1)
        x = self.token_emb(tokens) + self.pos_emb(positions)
        h = self.encoder(x)
        pooled = h.mean(dim=1)
        return self.head(pooled)


def accuracy(model: torch.nn.Module, loader: DataLoader) -> float:
    model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    return correct / total


# Workflow:
# 1) Create token sequences and binary labels.
# 2) Train transformer encoder classifier.
# 3) Evaluate train/validation/test accuracy under fixed split.
def main() -> None:
    torch.manual_seed(52)

    x, y = make_data(n_rows=scaled_int(6_000, quick_value=2_500))
    print(preset_banner())
    print("Data declaration")
    print("source=synthetic token sequences")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=52, stratify=y
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full, y_train_full, test_size=0.2, random_state=52, stratify=y_train_full
    )

    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=256, shuffle=False)

    model = TransformerClassifier()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)

    epochs = scaled_int(15, quick_value=7)
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in train_loader:
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch in (1, max(2, epochs // 2), epochs):
            train_acc = accuracy(model, train_loader)
            val_acc = accuracy(model, val_loader)
            print(f"epoch={epoch:02d} train_acc={train_acc:.4f} val_acc={val_acc:.4f}")

    test_acc = accuracy(model, test_loader)
    print(f"final_test_accuracy={test_acc:.4f}")
    print("Interpretation: transformer complexity starts from attention + positional encoding.")


if __name__ == "__main__":
    main()
