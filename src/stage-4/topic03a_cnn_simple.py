"""Stage 4 Topic 03A: CNN classifier (simple).

Data: sklearn digits dataset
Rows: 1,797
Input shape: [N, 1, 8, 8]
Target: class label 0..9, shape [N]
Split: fixed train/test split
Type: multiclass image classification
"""

from __future__ import annotations

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Workflow:
# 1) Reshape digit vectors into image tensors.
# 2) Train a minimal CNN on train split.
# 3) Evaluate holdout accuracy.
def main() -> None:
    torch.manual_seed(31)

    data = load_digits()
    x = torch.tensor(data.images, dtype=torch.float32).unsqueeze(1) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=31, stratify=y
    )

    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 8, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(kernel_size=2),
        torch.nn.Flatten(),
        torch.nn.Linear(8 * 4 * 4, 10),
    )

    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

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
    print("Interpretation: CNN captures local image patterns better than plain flattening.")


if __name__ == "__main__":
    main()
