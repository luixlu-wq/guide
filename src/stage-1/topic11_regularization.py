"""Topic 11: Regularization and C-parameter tradeoff.

Data: Breast Cancer Wisconsin (scikit-learn built-in)
Rows: 569
Features: 30 numeric cell-measurement features
Target: diagnosis (0 = malignant, 1 = benign)
Type: Binary classification
"""

from __future__ import annotations

from sklearn.metrics import accuracy_score

from common.ml_utils import build_logreg_pipeline, load_breast_cancer_xy, split_classification_data
from common.runtime import create_logger, write_json_artifact


def main() -> None:
    script_stem = "topic11_regularization"
    logger = create_logger(script_stem)

    X, y = load_breast_cancer_xy()
    X_train, X_test, y_train, y_test = split_classification_data(X, y)

    logger.info("Developer warning: in scikit-learn LogisticRegression, C = 1/lambda.")
    logger.info("smaller C => stronger regularization penalty; larger C => weaker penalty.")

    rows = []
    for c_value in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]:
        model = build_logreg_pipeline(C=c_value, max_iter=5000)
        model.fit(X_train, y_train)
        train_acc = float(accuracy_score(y_train, model.predict(X_train)))
        test_acc = float(accuracy_score(y_test, model.predict(X_test)))
        gap = train_acc - test_acc

        if c_value <= 0.01:
            note = "strong_regularization_underfit_risk"
        elif c_value >= 100.0:
            note = "weak_regularization_overfit_risk"
        else:
            note = "balanced_range_candidate"

        rows.append(
            {
                "C": float(c_value),
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "train_test_gap": float(gap),
                "note": note,
            }
        )
        logger.info(
            "C=%8.3f train_acc=%.4f test_acc=%.4f gap=%.4f note=%s",
            c_value,
            train_acc,
            test_acc,
            gap,
            note,
        )

    best = max(rows, key=lambda r: r["test_accuracy"])
    logger.info("best_test_accuracy=%.4f at C=%.3f", best["test_accuracy"], best["C"])

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "breast_cancer",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "best_test_accuracy",
            "quality_metric_value": float(best["test_accuracy"]),
            "metrics": {
                "best_c": float(best["C"]),
                "regularization_sweep": rows,
            },
            "decision_note": "pick C in the generalization sweet spot, not based on train score alone",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
