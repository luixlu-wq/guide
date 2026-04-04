"""Stage 4 Topic 01A: neural anatomy with NumPy (simple, math-first).

Data Source: synthetic 1D regression data generated in script
Schema: 1 numeric feature (`x`) | target continuous (`y`)
Preprocessing: none required (small controlled numeric range)
Null Handling: none (generated arrays are complete)
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


def make_data():
    # Tiny data keeps every step inspectable by eye.
    x = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]], dtype=np.float64)
    y = 2.0 * x + 1.0
    return x, y


def forward(x: np.ndarray, w: float, b: float) -> np.ndarray:
    # Single-neuron linear model: y_pred = w*x + b.
    return x * w + b


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    err = y_pred - y_true
    return float(np.mean(err**2))


def gradients(x: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    # MSE derivative for one-feature linear neuron.
    # dL/dw = (2/N) * sum((y_pred - y_true) * x)
    # dL/db = (2/N) * sum(y_pred - y_true)
    err = y_pred - y_true
    n = x.shape[0]
    dw = float((2.0 / n) * np.sum(err * x))
    db = float((2.0 / n) * np.sum(err))
    return dw, db


# Workflow:
# 1) Build tiny synthetic data.
# 2) Run forward -> loss -> gradient -> update in a loop.
# 3) Print parameter movement and diagnosis.
# 4) Save evidence artifact with before/after delta.
def main() -> None:
    x, y = make_data()

    print("Data declaration")
    print("source=synthetic, rows=", x.shape[0], "input_shape=", x.shape, "target_shape=", y.shape)

    # Start from intentionally wrong parameters.
    w = 0.25
    b = -0.80
    lr = 0.05
    epochs = 80

    run_id = f"stage4_topic01a_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    loss_history: list[float] = []

    w_before, b_before = w, b
    for epoch in range(1, epochs + 1):
        y_pred = forward(x, w, b)
        loss = mse(y, y_pred)
        dw, db = gradients(x, y, y_pred)

        # Parameter update (gradient descent).
        w = w - lr * dw
        b = b - lr * db

        loss_history.append(loss)
        if epoch in (1, 2, 5, 10, 20, 40, 80):
            print(
                f"epoch={epoch:02d} loss={loss:.6f} dw={dw:.6f} db={db:.6f} "
                f"w={w:.6f} b={b:.6f}"
            )

    final_loss = loss_history[-1]
    first_loss = loss_history[0]
    print(f"final parameters: w={w:.6f} (target 2.0), b={b:.6f} (target 1.0)")
    print(f"loss: {first_loss:.6f} -> {final_loss:.6f}")

    if final_loss < first_loss * 0.05:
        diagnosis = "healthy_convergence"
        decision = "promote"
        print("DIAGNOSIS: Healthy convergence. Forward/backward/update chain is correct.")
    elif final_loss < first_loss:
        diagnosis = "slow_convergence"
        decision = "hold"
        print("DIAGNOSIS: Learning but slow. Try learning-rate tuning.")
    else:
        diagnosis = "failed_update_path"
        decision = "rollback"
        print("DIAGNOSIS: Loss not improving. Check gradient formulas and update direction.")

    out_dir = Path(__file__).parent / "results" / "stage4"
    out_dir.mkdir(parents=True, exist_ok=True)

    trace_df = pd.DataFrame(
        {
            "epoch": list(range(1, epochs + 1)),
            "loss": loss_history,
        }
    )
    trace_path = out_dir / "topic01a_numpy_loss_trace.csv"
    trace_df.to_csv(trace_path, index=False)

    evidence_df = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "stage": "4",
                "topic_or_module": "topic01a_numpy_neural_anatomy",
                "metric_name": "train_mse",
                "before_value": first_loss,
                "after_value": final_loss,
                "delta": final_loss - first_loss,
                "dataset_or_eval_set": "synthetic_1d_regression",
                "seed_or_config_id": "deterministic_handcrafted_data",
                "decision": decision,
                "failure_class": "training_or_optimization",
                "diagnosis": diagnosis,
            }
        ]
    )
    evidence_path = out_dir / "topic01a_before_after_metrics.csv"
    evidence_df.to_csv(evidence_path, index=False)

    print(f"Saved: {trace_path}")
    print(f"Saved: {evidence_path}")
    print("Interpretation: this NumPy script exposes the math behind one-neuron learning.")


if __name__ == "__main__":
    main()

