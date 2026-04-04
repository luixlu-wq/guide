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


def pick_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def print_hardware_profile(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
        print(f"Device: {torch.cuda.get_device_name(0)}")
        torch.backends.cudnn.benchmark = True
    else:
        print("Device: CPU fallback path")


# Workflow:
# 1) Load a small binary subset (digits 0 vs 1).
# 2) Train a one-hidden-layer MLP with cross-entropy loss.
# 3) Evaluate accuracy on held-out test data.
def main() -> None:
    torch.manual_seed(21)
    device = pick_device()
    print_hardware_profile(device)

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
    x_train = x_train.to(device)
    x_test = x_test.to(device)
    y_train = y_train.to(device)
    y_test = y_test.to(device)

    model = torch.nn.Sequential(
        torch.nn.Linear(64, 16),
        torch.nn.ReLU(),
        torch.nn.Linear(16, 2),
    ).to(device)
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
        acc = accuracy_score(y_test.cpu().numpy(), pred.cpu().numpy())

    print(f"test_accuracy={acc:.4f}")
    if device.type == "cuda":
        print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated(device) / 1e9:.3f} GB")
    print("Interpretation: simple MLP already solves an easy binary vision task.")


if __name__ == "__main__":
    main()
