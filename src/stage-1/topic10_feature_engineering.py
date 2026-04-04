"""Topic 10: Feature engineering impact, including negative/noise feature example.

Data: Synthetic tabular regression dataset generated in-script
Rows: 220
Features: area, rooms, age
Target: price
Type: Regression
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from common.runtime import create_logger, write_json_artifact


def make_data(n: int = 220, seed: int = 42):
    rng = np.random.default_rng(seed)
    area = rng.uniform(500, 3000, size=n)
    rooms = rng.integers(1, 9, size=n).astype(float)
    age = rng.uniform(1, 50, size=n)
    noise = rng.normal(0, 12000, size=n)

    # Ground-truth relationship: price depends on area, rooms, and age.
    price = 90 * area + 4000 * rooms - 700 * age + noise
    X_raw = np.column_stack([area, rooms, age])
    return X_raw, price


def add_engineered_features(X_raw):
    area = X_raw[:, 0]
    rooms = X_raw[:, 1]
    age = X_raw[:, 2]
    area_per_room = area / rooms
    log_age = np.log1p(age)
    return np.column_stack([X_raw, area_per_room, log_age])


def add_noise_feature(X):
    """Add one completely random feature to demonstrate non-useful signal."""
    rng = np.random.default_rng(2026)
    random_noise = rng.normal(0, 1, size=(X.shape[0], 1))
    return np.column_stack([X, random_noise])


def evaluate_feature_set(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return float(r2_score(y_test, pred))


def main() -> None:
    script_stem = "topic10_feature_engineering"
    logger = create_logger(script_stem)

    X_raw, y = make_data()
    X_eng = add_engineered_features(X_raw)
    X_eng_plus_noise = add_noise_feature(X_eng)

    r2_base = evaluate_feature_set(X_raw, y)
    r2_engineered = evaluate_feature_set(X_eng, y)
    r2_engineered_plus_noise = evaluate_feature_set(X_eng_plus_noise, y)

    logger.info("baseline_r2=%.4f", r2_base)
    logger.info("engineered_r2=%.4f", r2_engineered)
    logger.info("engineered_plus_noise_r2=%.4f", r2_engineered_plus_noise)
    logger.info(
        "interpretation: engineered features usually help; random noise features can hurt robustness/generalization"
    )

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "synthetic_tabular_regression",
            "input_rows_or_samples": int(X_raw.shape[0]),
            "quality_metric_name": "engineered_r2",
            "quality_metric_value": r2_engineered,
            "metrics": {
                "baseline_r2": r2_base,
                "engineered_r2": r2_engineered,
                "engineered_improvement": r2_engineered - r2_base,
                "engineered_plus_noise_r2": r2_engineered_plus_noise,
                "noise_impact_delta": r2_engineered_plus_noise - r2_engineered,
            },
            "decision_note": "feature quality matters more than adding random feature count",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
