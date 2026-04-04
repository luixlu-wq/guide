"""Stage 4 Section 5A: NumPy MLP simple (math-first, no autograd).

Data Source: synthetic XOR-style classification points
Schema: 2 numeric features | target binary class {0,1}
Preprocessing: none (small controlled numeric dataset)
Null Handling: none (arrays generated in script)
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


def make_xor_data() -> tuple[np.ndarray, np.ndarray]:
    # Duplicate XOR points with tiny noise so optimization is less brittle.
    base_x = np.array(
        [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
        ],
        dtype=np.float64,
    )
    base_y = np.array([[0.0], [1.0], [1.0], [0.0]], dtype=np.float64)
    rng = np.random.default_rng(501)
    x = np.repeat(base_x, repeats=12, axis=0) + 0.03 * rng.normal(size=(48, 2))
    y = np.repeat(base_y, repeats=12, axis=0)
    return x, y


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, z)


def relu_grad(z: np.ndarray) -> np.ndarray:
    return (z > 0).astype(np.float64)


def bce_loss(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    eps = 1e-8
    y_prob = np.clip(y_prob, eps, 1.0 - eps)
    return float(-np.mean(y_true * np.log(y_prob) + (1.0 - y_true) * np.log(1.0 - y_prob)))


# Workflow:
# 1) Build XOR data.
# 2) Define one-hidden-layer MLP with manual forward/backward.
# 3) Train using gradient descent and inspect loss + gradient norms.
# 4) Run failure checks (shape mismatch guard, dying ReLU ratio).
def main() -> None:
    run_id = f"stage4_topic05a_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    x, y = make_xor_data()
    n, d = x.shape
    hidden_dim = 8

    print("Data declaration")
    print("source=synthetic_xor rows=", n, "input_shape=", x.shape, "target_shape=", y.shape)

    # Shape-first contract.
    # X: [B,2] -> hidden: [B,8] -> output_prob: [B,1]
    rng = np.random.default_rng(502)
    w1 = 0.5 * rng.normal(size=(d, hidden_dim))
    b1 = np.zeros((1, hidden_dim))
    w2 = 0.5 * rng.normal(size=(hidden_dim, 1))
    b2 = np.zeros((1, 1))

    lr = 0.08
    epochs = 1000
    loss_trace = []
    grad_trace = []

    for epoch in range(1, epochs + 1):
        # Forward.
        z1 = x @ w1 + b1
        h = relu(z1)
        z2 = h @ w2 + b2
        y_prob = sigmoid(z2)

        # Loss.
        loss = bce_loss(y, y_prob)

        # Backward (manual).
        dz2 = (y_prob - y) / n
        dw2 = h.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        dh = dz2 @ w2.T
        dz1 = dh * relu_grad(z1)
        dw1 = x.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Update.
        w2 -= lr * dw2
        b2 -= lr * db2
        w1 -= lr * dw1
        b1 -= lr * db1

        grad_norm = float(np.sqrt(np.sum(dw1**2) + np.sum(dw2**2)))
        loss_trace.append(loss)
        grad_trace.append(grad_norm)

        if epoch in (1, 2, 5, 20, 100, 300, 600, 1000):
            print(f"epoch={epoch:04d} loss={loss:.6f} grad_norm={grad_norm:.6f}")

    # Inference diagnostics.
    z1 = x @ w1 + b1
    h = relu(z1)
    y_pred = (sigmoid(h @ w2 + b2) >= 0.5).astype(np.float64)
    acc = float((y_pred == y).mean())
    dead_ratio = float((h <= 0).sum() / h.size)
    mean_grad = float(np.mean(grad_trace))

    diagnosis = []
    if mean_grad < 1e-5:
        diagnosis.append("vanishing_gradient_risk")
    if dead_ratio > 0.85:
        diagnosis.append("dying_relu_risk")
    if not diagnosis:
        diagnosis.append("healthy_signal")

    print(f"final_accuracy={acc:.4f}")
    print(f"dead_relu_ratio={dead_ratio:.4f} mean_grad_norm={mean_grad:.6f}")
    print("Diagnosis:", ", ".join(diagnosis))

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({"epoch": np.arange(1, epochs + 1), "loss": loss_trace, "grad_norm": grad_trace}).to_csv(
        out_dir / "topic05a_numpy_trace.csv", index=False
    )
    pd.DataFrame(
        [
            {
                "run_id": run_id,
                "stage": "4",
                "topic_or_module": "section05_topic05a_mlp_simple",
                "metric_name": "train_bce",
                "before_value": float(loss_trace[0]),
                "after_value": float(loss_trace[-1]),
                "delta": float(loss_trace[-1] - loss_trace[0]),
                "dataset_or_eval_set": "synthetic_xor",
                "seed_or_config_id": "seed501_502",
                "decision": "promote" if acc >= 0.90 else "hold",
                "diagnosis": "|".join(diagnosis),
                "accuracy": acc,
            }
        ]
    ).to_csv(out_dir / "topic05a_before_after_metrics.csv", index=False)

    print(f"Saved: {out_dir / 'topic05a_numpy_trace.csv'}")
    print(f"Saved: {out_dir / 'topic05a_before_after_metrics.csv'}")
    print("Interpretation: manual forward/backward exposes MLP math without autograd.")


if __name__ == "__main__":
    main()

