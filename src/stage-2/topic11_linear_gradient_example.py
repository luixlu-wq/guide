"""Concrete gradient example for linear regression.

Data: tiny synthetic dataset
Rows: 4
Features: x = [1, 2, 3, 4]
Target: y = [3, 5, 7, 9] (roughly y = 2x + 1)
Type: gradient demonstration

What this script shows:
1) Manual gradients for MSE:
   dL/dw = (2/n) * sum((y_hat - y) * x)
   dL/db = (2/n) * sum(y_hat - y)
2) One gradient-descent update step.
3) Comparison with PyTorch autograd (if torch is installed).
"""

from __future__ import annotations

import math

import numpy as np


def manual_gradients(x: np.ndarray, y: np.ndarray, w: float, b: float):
    n = len(x)
    y_hat = w * x + b
    err = y_hat - y
    loss = float(np.mean(err**2))
    dw = float((2.0 / n) * np.sum(err * x))
    db = float((2.0 / n) * np.sum(err))
    return loss, dw, db


def main():
    x = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y = np.array([3.0, 5.0, 7.0, 9.0], dtype=np.float64)

    w0 = 0.5
    b0 = -1.0
    lr = 0.1

    loss0, dw_manual, db_manual = manual_gradients(x, y, w0, b0)
    w1 = w0 - lr * dw_manual
    b1 = b0 - lr * db_manual
    loss1, _, _ = manual_gradients(x, y, w1, b1)

    print("manual gradient path")
    print(f"initial w={w0:.4f}, b={b0:.4f}, loss={loss0:.4f}")
    print(f"dw={dw_manual:.4f}, db={db_manual:.4f}")
    print(f"after one step (lr={lr}): w={w1:.4f}, b={b1:.4f}, loss={loss1:.4f}")

    try:
        import torch  # optional dependency (requirements-gpu.txt)
    except Exception:
        print("\nautograd comparison skipped (torch not installed).")
        print("install with: pip install -r requirements-gpu.txt")
        return

    xt = torch.tensor(x, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32)
    w = torch.tensor(w0, dtype=torch.float32, requires_grad=True)
    b = torch.tensor(b0, dtype=torch.float32, requires_grad=True)

    y_hat = w * xt + b
    loss = torch.mean((y_hat - yt) ** 2)
    loss.backward()

    dw_auto = float(w.grad.item())
    db_auto = float(b.grad.item())

    print("\nautograd comparison")
    print(f"autograd dw={dw_auto:.4f}, db={db_auto:.4f}")
    print(
        "gradient match (manual vs autograd):",
        math.isclose(dw_manual, dw_auto, rel_tol=1e-5, abs_tol=1e-5)
        and math.isclose(db_manual, db_auto, rel_tol=1e-5, abs_tol=1e-5),
    )


if __name__ == "__main__":
    main()
