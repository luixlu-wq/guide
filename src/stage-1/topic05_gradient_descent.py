from __future__ import annotations

import matplotlib
import numpy as np
from pathlib import Path

from common.runtime import create_logger, write_json_artifact

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def make_data(n: int = 200, seed: int = 42):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 10, size=n)
    y = 3.0 * X + 5.0 + rng.normal(0, 2, size=n)
    return X, y


def predict(X, w, b):
    return w * X + b


def mse(X, y, w, b):
    y_pred = predict(X, w, b)
    return np.mean((y_pred - y) ** 2)


def gradients(X, y, w, b):
    n = len(X)
    err = predict(X, w, b) - y
    dw = (2 / n) * np.sum(err * X)
    db = (2 / n) * np.sum(err)
    return dw, db


def train_gradient_descent(X, y, lr: float = 0.001, epochs: int = 3000):
    """Train linear regression and capture line snapshots for visualization."""
    w, b = 0.0, 0.0
    history = []
    snapshots = {}
    tracked_epochs = {1, 100, 1000, epochs}

    for epoch in range(1, epochs + 1):
        dw, db = gradients(X, y, w, b)
        w -= lr * dw
        b -= lr * db
        history.append(mse(X, y, w, b))
        if epoch in tracked_epochs:
            snapshots[epoch] = {"w": float(w), "b": float(b)}

    return float(w), float(b), history, snapshots


def plot_loss_curve(loss_history, out_path: Path):
    plt.figure(figsize=(8, 4))
    plt.plot(loss_history)
    plt.title("Gradient Descent Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_line_evolution(X, y, snapshots, out_path: Path):
    """Plot model line at selected epochs to make learning progression visible."""
    x_grid = np.linspace(X.min(), X.max(), 200)
    plt.figure(figsize=(8, 5))
    plt.scatter(X, y, alpha=0.35, label="data points")

    for epoch in sorted(snapshots):
        w = snapshots[epoch]["w"]
        b = snapshots[epoch]["b"]
        plt.plot(x_grid, predict(x_grid, w, b), label=f"epoch {epoch}")

    plt.title("Regression Line Evolution During Gradient Descent")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    script_stem = "topic05_gradient_descent"
    logger = create_logger(script_stem)

    X, y = make_data()
    w, b, loss_history, snapshots = train_gradient_descent(X, y, lr=0.001, epochs=3000)

    logger.info("learned_w=%.4f learned_b=%.4f", w, b)
    logger.info("initial_loss=%.4f final_loss=%.4f", loss_history[0], loss_history[-1])

    root_plot = Path(__file__).with_name("topic05_loss_curve.png")
    plot_loss_curve(loss_history, root_plot)

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    evolution_plot = results_dir / "topic05_regression_line_evolution.png"
    plot_line_evolution(X, y, snapshots, evolution_plot)

    logger.info("saved_plot_loss=%s", root_plot)
    logger.info("saved_plot_line_evolution=%s", evolution_plot)

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "final_mse",
            "quality_metric_value": float(loss_history[-1]),
            "metrics": {
                "learned_w": w,
                "learned_b": b,
                "initial_mse": float(loss_history[0]),
                "final_mse": float(loss_history[-1]),
                "snapshots": snapshots,
            },
            "figure_paths": [str(root_plot), str(evolution_plot)],
            "decision_note": "visualize both loss reduction and line convergence",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
