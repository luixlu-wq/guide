"""Stage 4 Topic 04A: RNN sequence classifier (simple).

Data: synthetic sequence data generated in-script
Rows: 2,000
Input shape: [N, 6, 1]
Target: class label {0,1}, shape [N]
Split: fixed train/test split
Type: sequence classification
"""

from __future__ import annotations

import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def make_data(n_rows: int = 2_000):
    generator = torch.Generator(device="cpu").manual_seed(41)
    x = torch.randn((n_rows, 6, 1), generator=generator)
    y = (x[:, -1, 0] > x[:, 0, 0]).long()
    return x, y


class TinyRNN(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.rnn = torch.nn.RNN(input_size=1, hidden_size=12, batch_first=True)
        self.head = torch.nn.Linear(12, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.rnn(x)
        return self.head(out[:, -1, :])


# Workflow:
# 1) Build simple sequence classification data.
# 2) Train a tiny RNN using final hidden state.
# 3) Evaluate binary classification accuracy.
def main() -> None:
    torch.manual_seed(41)

    x, y = make_data()
    print("Data declaration")
    print("source=synthetic sequence rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=41, stratify=y
    )

    model = TinyRNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.CrossEntropyLoss()

    for _ in range(30):
        logits = model(x_train)
        loss = loss_fn(logits, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        pred = model(x_test).argmax(dim=1)
        acc = accuracy_score(y_test.numpy(), pred.numpy())

    print(f"test_accuracy={acc:.4f}")
    print("Interpretation: simple complexity is only sequence-to-label mapping with one RNN.")


if __name__ == "__main__":
    main()
