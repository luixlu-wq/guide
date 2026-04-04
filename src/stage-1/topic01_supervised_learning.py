"""Topic 01: Supervised learning baseline with calibration-aware outputs.

Data: Breast Cancer Wisconsin (scikit-learn built-in)
Rows: 569
Features: 30 numeric cell-measurement features
Target: diagnosis (0 = malignant, 1 = benign)
Type: Binary classification
"""

from __future__ import annotations

from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from common.ml_utils import build_logreg_pipeline, load_breast_cancer_xy, split_classification_data
from common.runtime import create_logger, get_hardware_info, write_json_artifact


def evaluate(model, X_test, y_test) -> dict:
    """Compute hard-label and probability-based metrics for production awareness."""
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    confidence = probs.copy()
    confidence[preds == 0] = 1.0 - confidence[preds == 0]
    correct_mask = preds == y_test

    mean_confidence_correct = float(confidence[correct_mask].mean()) if correct_mask.any() else 1.0
    mean_confidence_incorrect = (
        float(confidence[~correct_mask].mean()) if (~correct_mask).any() else 0.0
    )

    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds)),
        "recall": float(recall_score(y_test, preds)),
        "f1": float(f1_score(y_test, preds)),
        "brier_score": float(brier_score_loss(y_test, probs)),
        "mean_confidence": float(confidence.mean()),
        "mean_confidence_correct": mean_confidence_correct,
        "mean_confidence_incorrect": mean_confidence_incorrect,
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
    }
    return metrics


def main() -> None:
    script_stem = "topic01_supervised_learning"
    logger = create_logger(script_stem)

    X, y = load_breast_cancer_xy()
    X_train, X_test, y_train, y_test = split_classification_data(X, y)
    model = build_logreg_pipeline(C=1.0, max_iter=2000)
    model.fit(X_train, y_train)
    metrics = evaluate(model, X_test, y_test)

    logger.info("accuracy=%.4f precision=%.4f recall=%.4f f1=%.4f",
                metrics["accuracy"], metrics["precision"], metrics["recall"], metrics["f1"])
    logger.info("brier_score=%.4f mean_confidence=%.4f",
                metrics["brier_score"], metrics["mean_confidence"])
    logger.info("confusion_matrix=%s", metrics["confusion_matrix"])
    logger.info(
        "calibration_hint: confidence should align with correctness; high confidence + wrong outputs is high-risk."
    )

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "breast_cancer",
            "input_rows_or_samples": int(X.shape[0]),
            "batch_size": None,
            "quality_metric_name": "f1",
            "quality_metric_value": metrics["f1"],
            "metrics": metrics,
            "hardware": get_hardware_info(),
            "decision_note": "baseline benchmark for Stage 1 classification",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
