"""Stage 3 Topic 09C (Advanced): mini-batch training with validation and optional AMP.

Data: synthetic tensor regression data generated in-script
Rows: 30,000 (train/valid split)
Features: 8 numeric features
Target: linear target with noise
Type: Regression bridge (advanced)
"""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset


def pick_device() -> torch.device:
    # Prefer CUDA if available for faster tensor operations.
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def make_data(n: int = 30_000, seed: int = 42):
    # Generate reproducible synthetic tabular tensors.
    g = torch.Generator(device="cpu").manual_seed(seed)
    X = torch.randn((n, 8), generator=g)
    true_w = torch.tensor([1.5, -2.0, 0.8, 0.0, 1.2, -0.5, 2.2, -1.1])
    y = X @ true_w + 0.3 * torch.randn((n,), generator=g)
    return X, y.unsqueeze(1)


def r2_score_torch(y_true: torch.Tensor, y_pred: torch.Tensor) -> float:
    # Compute R^2 directly in torch tensors.
    ss_res = torch.sum((y_true - y_pred) ** 2)
    ss_tot = torch.sum((y_true - torch.mean(y_true)) ** 2)
    return float(1.0 - (ss_res / ss_tot).item())


# Workflow:
# 1) Build train/validation loaders from synthetic tensors.
# 2) Move model and batch tensors to device.
# 3) Forward + loss + backward + optimizer updates per mini-batch.
# 4) Evaluate validation loss each epoch.
# 5) Report final validation metrics and device/AMP path.
def main() -> None:
    device = pick_device()
    use_amp = device.type == "cuda"

    print("selected device:", device)
    print("AMP enabled:", use_amp)

    X, y = make_data()
    split = int(0.8 * len(X))
    X_train, X_valid = X[:split], X[split:]
    y_train, y_valid = y[:split], y[split:]

    train_ds = TensorDataset(X_train, y_train)
    valid_ds = TensorDataset(X_valid, y_valid)
    train_loader = DataLoader(train_ds, batch_size=256, shuffle=True)
    valid_loader = DataLoader(valid_ds, batch_size=512, shuffle=False)

    model = torch.nn.Sequential(
        torch.nn.Linear(8, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 1),
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    first_val_loss = None
    last_val_loss = None

    for epoch in range(1, 16):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)

            optimizer.zero_grad()
            with torch.amp.autocast(device_type="cuda", enabled=use_amp):
                pred = model(xb)
                loss = loss_fn(pred, yb)

            scaler.scale(loss).backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            scaler.step(optimizer)
            scaler.update()

        # Validation pass: no gradient tracking.
        model.eval()
        total_loss = 0.0
        total_count = 0
        preds = []
        targets = []

        with torch.no_grad():
            for xb, yb in valid_loader:
                xb = xb.to(device)
                yb = yb.to(device)
                out = model(xb)
                batch_loss = loss_fn(out, yb)
                total_loss += float(batch_loss.item()) * len(xb)
                total_count += len(xb)
                preds.append(out.detach().cpu())
                targets.append(yb.detach().cpu())

        val_loss = total_loss / total_count
        if first_val_loss is None:
            first_val_loss = val_loss
        last_val_loss = val_loss

        if epoch in (1, 5, 10, 15):
            print(f"epoch={epoch:02d} val_loss={val_loss:.5f}")

    y_pred = torch.cat(preds)
    y_true = torch.cat(targets)
    r2 = r2_score_torch(y_true, y_pred)

    print(f"validation loss: {first_val_loss:.5f} -> {last_val_loss:.5f}")
    print(f"validation R^2: {r2:.3f}")
    print("Interpretation: advanced loop adds batching, validation, clipping, and optional AMP.")


if __name__ == "__main__":
    main()
