"""Topic 04: Cost functions + vectorized-vs-loop performance benchmark."""

from __future__ import annotations

import time

import numpy as np
from sklearn.metrics import log_loss, mean_squared_error

from common.runtime import create_logger, write_json_artifact


def mse_manual(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.mean((y_true - y_pred) ** 2)


def mse_loop(y_true, y_pred):
    """Loop-based MSE for educational benchmarking (intentionally slower)."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    acc = 0.0
    for idx in range(len(y_true)):
        diff = y_true[idx] - y_pred[idx]
        acc += diff * diff
    return acc / len(y_true)


def log_loss_manual(y_true, y_prob, eps=1e-15):
    y_true = np.asarray(y_true, dtype=float)
    y_prob = np.asarray(y_prob, dtype=float)
    y_prob = np.clip(y_prob, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob))


def run_vectorization_benchmark(n: int = 700_000) -> dict:
    rng = np.random.default_rng(42)
    y_true = rng.normal(0, 1, size=n)
    y_pred = y_true + rng.normal(0, 0.2, size=n)

    t0 = time.perf_counter()
    loop_val = mse_loop(y_true, y_pred)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    vec_val = mse_manual(y_true, y_pred)
    t3 = time.perf_counter()

    loop_ms = (t1 - t0) * 1000.0
    vec_ms = (t3 - t2) * 1000.0
    return {
        "loop_mse": float(loop_val),
        "vectorized_mse": float(vec_val),
        "loop_time_ms": float(loop_ms),
        "vectorized_time_ms": float(vec_ms),
        "speedup_x": float(loop_ms / vec_ms if vec_ms > 0 else float("inf")),
    }


def main() -> None:
    script_stem = "topic04_cost_function"
    logger = create_logger(script_stem)

    y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])

    y_true_cls = np.array([1, 0, 1, 1, 0, 0])
    y_prob_cls = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.4])

    mse_man = float(mse_manual(y_true_reg, y_pred_reg))
    mse_skl = float(mean_squared_error(y_true_reg, y_pred_reg))
    ll_man = float(log_loss_manual(y_true_cls, y_prob_cls))
    ll_skl = float(log_loss(y_true_cls, y_prob_cls))

    bench = run_vectorization_benchmark()

    logger.info("mse_manual=%.6f mse_sklearn=%.6f", mse_man, mse_skl)
    logger.info("logloss_manual=%.6f logloss_sklearn=%.6f", ll_man, ll_skl)
    logger.info(
        "vectorization_benchmark loop_ms=%.2f vectorized_ms=%.2f speedup_x=%.2f",
        bench["loop_time_ms"],
        bench["vectorized_time_ms"],
        bench["speedup_x"],
    )

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "quality_metric_name": "mse_manual_vs_sklearn_abs_diff",
            "quality_metric_value": abs(mse_man - mse_skl),
            "metrics": {
                "mse_manual": mse_man,
                "mse_sklearn": mse_skl,
                "logloss_manual": ll_man,
                "logloss_sklearn": ll_skl,
                "vectorized_vs_loop": bench,
            },
            "decision_note": "vectorized linear algebra is critical for AI performance",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
