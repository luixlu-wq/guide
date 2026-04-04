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
# 1) Reshape digit vectors into image tensors.
# 2) Train a minimal CNN on train split.
# 3) Evaluate holdout accuracy.
def main() -> None:
    torch.manual_seed(31)
    device = pick_device()
    print_hardware_profile(device)

    data = load_digits()
    x = torch.tensor(data.images, dtype=torch.float32).unsqueeze(1) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)

    print("Data declaration")
    print("source=sklearn.load_digits")
    print("rows=", x.shape[0], "input_shape=", tuple(x.shape), "target_shape=", tuple(y.shape))

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=31, stratify=y
    )
    x_train = x_train.to(device)
    x_test = x_test.to(device)
    y_train = y_train.to(device)
    y_test = y_test.to(device)

    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 8, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(kernel_size=2),
        torch.nn.Flatten(),
        torch.nn.Linear(8 * 4 * 4, 10),
    ).to(device)

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
        acc = accuracy_score(y_test.cpu().numpy(), pred.cpu().numpy())

    print(f"test_accuracy={acc:.4f}")
    if device.type == "cuda":
        print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated(device) / 1e9:.3f} GB")
    print("Interpretation: CNN captures local image patterns better than plain flattening.")


if __name__ == "__main__":
    main()
