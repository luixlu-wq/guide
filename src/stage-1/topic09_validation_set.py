"""Topic 09: Validation strategy (train/val/test + k-fold robustness check).

Data: Breast Cancer Wisconsin (scikit-learn built-in)
Rows: 569
Features: 30 numeric cell-measurement features
Target: diagnosis (0 = malignant, 1 = benign)
Type: Binary classification
"""

from __future__ import annotations

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split

from common.ml_utils import build_logreg_pipeline, load_breast_cancer_xy
from common.runtime import create_logger, write_json_artifact


def main() -> None:
    script_stem = "topic09_validation_set"
    logger = create_logger(script_stem)

    X, y = load_breast_cancer_xy()

    # Split off test first so it stays untouched during model selection.
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    # Validation set comes from the remaining non-test data.
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42
    )

    logger.info("train_size=%d validation_size=%d test_size=%d", len(X_train), len(X_val), len(X_test))

    # Hyperparameter sweep using validation set only.
    candidate_rows = []
    for c_value in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
        model = build_logreg_pipeline(C=c_value, max_iter=5000)
        model.fit(X_train, y_train)
        val_acc = float(accuracy_score(y_val, model.predict(X_val)))
        candidate_rows.append({"C": float(c_value), "val_accuracy": val_acc, "model": model})
        logger.info("C=%7.3f val_accuracy=%.4f", c_value, val_acc)

    best = max(candidate_rows, key=lambda row: row["val_accuracy"])
    best_c = float(best["C"])
    best_model = best["model"]
    best_val = float(best["val_accuracy"])

    final_test_accuracy = float(accuracy_score(y_test, best_model.predict(X_test)))
    logger.info("best_C_on_validation=%.3f val_accuracy=%.4f", best_c, best_val)
    logger.info("final_test_accuracy=%.4f", final_test_accuracy)

    # Robustness check for small datasets: k-fold CV on train+validation pool.
    tuned_model = build_logreg_pipeline(C=best_c, max_iter=5000)
    cv_scores = cross_val_score(tuned_model, X_temp, y_temp, cv=5, scoring="accuracy")
    cv_mean = float(cv_scores.mean())
    cv_std = float(cv_scores.std())
    logger.info("cross_val_accuracy_mean=%.4f std=%.4f (5-fold on train+val)", cv_mean, cv_std)

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "breast_cancer",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "final_test_accuracy",
            "quality_metric_value": final_test_accuracy,
            "metrics": {
                "split_sizes": {
                    "train": int(len(X_train)),
                    "validation": int(len(X_val)),
                    "test": int(len(X_test)),
                },
                "best_c": best_c,
                "best_validation_accuracy": best_val,
                "final_test_accuracy": final_test_accuracy,
                "cross_val_accuracy_mean": cv_mean,
                "cross_val_accuracy_std": cv_std,
            },
            "decision_note": "validation chooses hyperparameters; test is reserved for final report",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
