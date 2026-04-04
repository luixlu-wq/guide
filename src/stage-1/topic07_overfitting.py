"""Topic 07: Overfitting demonstration using polynomial complexity sweep."""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

from common.runtime import create_logger, write_json_artifact


def make_data(n=40, seed=42):
    rng = np.random.default_rng(seed)
    X = np.sort(rng.uniform(0, 1, size=n))
    y = np.sin(2 * np.pi * X) + rng.normal(0, 0.15, size=n)
    return X.reshape(-1, 1), y


def evaluate_degree(X, y, degree):
    model = Pipeline(
        steps=[
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("linreg", LinearRegression()),
        ]
    )
    mse_scores = -cross_val_score(
        model, X, y, scoring="neg_mean_squared_error", cv=5
    )
    return float(mse_scores.mean()), float(mse_scores.std())


def main() -> None:
    script_stem = "topic07_overfitting"
    logger = create_logger(script_stem)

    X, y = make_data()
    rows = []
    for degree in [1, 4, 15]:
        mean_mse, std_mse = evaluate_degree(X, y, degree)
        rows.append({"degree": degree, "cv_mse_mean": mean_mse, "cv_mse_std": std_mse})
        logger.info("degree=%2d cv_mse_mean=%.4f cv_mse_std=%.4f", degree, mean_mse, std_mse)

    best = min(rows, key=lambda r: r["cv_mse_mean"])
    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "synthetic_sine",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "best_cv_mse",
            "quality_metric_value": float(best["cv_mse_mean"]),
            "metrics": {
                "degree_results": rows,
                "best_degree_by_cv_mse": int(best["degree"]),
            },
            "decision_note": "higher polynomial degree increases variance and overfit risk",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
