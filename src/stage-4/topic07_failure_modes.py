"""Stage 4 Topic 07: deep learning failure modes and fixes.

Data: sklearn digits dataset
Rows: 1,797
Input shape: [N, 64]
Target: class label 0..9, shape [N]
Split: fixed train/validation split
Type: diagnostics for common training failures
"""

from __future__ import annotations

import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from stage4_preset import preset_banner, scaled_int


def prepare_data(seed: int = 71):
    data = load_digits()
    x = torch.tensor(data.data, dtype=torch.float32) / 16.0
    y = torch.tensor(data.target, dtype=torch.long)
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.2, random_state=seed, stratify=y
    )
    train_loader = DataLoader(TensorDataset(x_train, y_train), batch_size=128, shuffle=True)
    val_loader = DataLoader(TensorDataset(x_val, y_val), batch_size=256, shuffle=False)
    return train_loader, val_loader


def accuracy(model: torch.nn.Module, loader: DataLoader, *, force_eval: bool = True) -> float:
    was_training = model.training
    if force_eval:
        model.eval()
    total = 0
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            pred = model(xb).argmax(dim=1)
            correct += int((pred == yb).sum().item())
            total += yb.size(0)
    if force_eval and was_training:
        model.train()
    return correct / total


def run_learning_rate_case(train_loader: DataLoader, val_loader: DataLoader, lr: float) -> float:
    torch.manual_seed(71)
    model = torch.nn.Sequential(
        torch.nn.Linear(64, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 10),
    )
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss()

    for _ in range(scaled_int(10, quick_value=5)):
        model.train()
        for xb, yb in train_loader:
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return accuracy(model, val_loader)


def run_loss_pairing_case(train_loader: DataLoader, val_loader: DataLoader) -> tuple[float, float]:
    torch.manual_seed(72)
    base = torch.nn.Sequential(torch.nn.Linear(64, 64), torch.nn.ReLU(), torch.nn.Linear(64, 10))
    wrong = torch.nn.Sequential(
        torch.nn.Linear(64, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 10),
        torch.nn.Softmax(dim=1),
    )

    good_opt = torch.optim.Adam(base.parameters(), lr=0.003)
    wrong_opt = torch.optim.Adam(wrong.parameters(), lr=0.003)
    loss_fn = torch.nn.CrossEntropyLoss()

    for _ in range(scaled_int(12, quick_value=6)):
        for xb, yb in train_loader:
            # Correct pairing: logits + CrossEntropyLoss.
            good_loss = loss_fn(base(xb), yb)
            good_opt.zero_grad()
            good_loss.backward()
            good_opt.step()

            # Wrong pairing: softmax probabilities + CrossEntropyLoss (double normalization).
            wrong_loss = loss_fn(wrong(xb), yb)
            wrong_opt.zero_grad()
            wrong_loss.backward()
            wrong_opt.step()

    return accuracy(base, val_loader), accuracy(wrong, val_loader)


def run_train_eval_case(train_loader: DataLoader, val_loader: DataLoader) -> tuple[float, float]:
    torch.manual_seed(73)
    model = torch.nn.Sequential(
        torch.nn.Linear(64, 128),
        torch.nn.ReLU(),
        torch.nn.Dropout(p=0.40),
        torch.nn.Linear(128, 10),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = torch.nn.CrossEntropyLoss()

    for _ in range(scaled_int(15, quick_value=7)):
        model.train()
        for xb, yb in train_loader:
            loss = loss_fn(model(xb), yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    eval_acc = accuracy(model, val_loader, force_eval=True)

    model.train()  # intentionally wrong mode for evaluation to show dropout-side randomness
    train_mode_scores = [accuracy(model, val_loader, force_eval=False) for _ in range(5)]
    train_mode_acc = sum(train_mode_scores) / len(train_mode_scores)
    return eval_acc, train_mode_acc


# Workflow:
# 1) Run controlled failure experiments on one fixed dataset/split.
# 2) Show metric impact of common mistakes.
# 3) Link each symptom to a concrete fix.
def main() -> None:
    print(preset_banner())
    train_loader, val_loader = prepare_data()

    print("Data declaration")
    print("source=sklearn.load_digits rows=1797 input_shape=(1797,64) target_shape=(1797,)")

    acc_high_lr = run_learning_rate_case(train_loader, val_loader, lr=3.0)
    acc_good_lr = run_learning_rate_case(train_loader, val_loader, lr=0.03)

    acc_good_pair, acc_wrong_pair = run_loss_pairing_case(train_loader, val_loader)
    acc_eval_mode, acc_train_mode_eval = run_train_eval_case(train_loader, val_loader)

    print("Failure mode: learning rate too high")
    print(f"val_acc(lr=3.00)={acc_high_lr:.4f}, val_acc(lr=0.03)={acc_good_lr:.4f}")

    print("Failure mode: wrong output-loss pairing")
    print(f"val_acc(correct logits+CE)={acc_good_pair:.4f}, val_acc(softmax+CE wrong)={acc_wrong_pair:.4f}")

    print("Failure mode: forgetting eval mode")
    print(f"val_acc(model.eval())={acc_eval_mode:.4f}, val_acc(kept model.train())={acc_train_mode_eval:.4f}")

    print("Interpretation: diagnostics show where training can fail and which fix to apply first.")


if __name__ == "__main__":
    main()
