"""Topic 08: Bias-variance trade-off via tree-depth sweep."""

from __future__ import annotations

from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from common.runtime import create_logger, write_json_artifact


def main() -> None:
    script_stem = "topic08_bias_variance"
    logger = create_logger(script_stem)

    X, y = make_classification(
        n_samples=1500,
        n_features=20,
        n_informative=6,
        n_redundant=4,
        flip_y=0.05,
        class_sep=1.0,
        random_state=42,
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    results = []
    for depth in range(1, 21):
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        train_err = 1 - accuracy_score(y_train, model.predict(X_train))
        val_err = 1 - accuracy_score(y_val, model.predict(X_val))
        results.append(
            {
                "depth": depth,
                "train_error": float(train_err),
                "val_error": float(val_err),
            }
        )

    best = min(results, key=lambda row: row["val_error"])
    logger.info("best_depth_by_val_error=%d", best["depth"])
    logger.info("sample_rows=%s", results[::3])

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "make_classification(n=1500,d=20)",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "best_validation_error",
            "quality_metric_value": float(best["val_error"]),
            "metrics": {
                "best_depth_by_val_error": int(best["depth"]),
                "depth_sweep": results,
            },
            "decision_note": "choose capacity where validation error is minimized, not training error",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
