"""Stage 4 Topic 02A: MLP classifier (simple).

Data: sklearn digits dataset (binary subset)
Rows: 360 (approx after filtering digits 0 and 1)
Input shape: [N, 64]
Target: class label {0,1}, shape [N]
Split: fixed train/test split with stratify
Type: binary classification
"""

from __future__ import annotations

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Workflow:
# 1) Load a small binary subset (digits 0 vs 1).
# 2) Train a one-hidden-layer MLP with cross-entropy loss.
# 3) Evaluate accuracy on held-out test data.
def main() -> None:
    torch.manual_seed(21)

    data = load_digits()
    mask = data.target <= 1
    x = torch.tensor(data.data[mask], dtype=torch.float32) / 16.0
    y = torch.tensor(data.target[mask], dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits(binary 0/1)")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=21, stratify=y
    )

    model = torch.nn.Sequential(
        torch.nn.Linear(64, 16),
        torch.nn.ReLU(),
        torch.nn.Linear(16, 2),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.CrossEntropyLoss()

    for _ in range(40):
        logits = model(x_train)
        loss = loss_fn(logits, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        pred = model(x_test).argmax(dim=1)
        acc = accuracy_score(y_test.numpy(), pred.numpy())

    print(f"test_accuracy={acc:.4f}")
    print("Interpretation: simple MLP already solves an easy binary vision task.")


if __name__ == "__main__":
    main()
