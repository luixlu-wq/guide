"""Topic 03: Feature quality impact + feature-importance visualization."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np
from sklearn.metrics import accuracy_score

from common.ml_utils import build_logreg_pipeline, load_breast_cancer_xy, split_classification_data
from common.runtime import create_logger, write_json_artifact

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def make_bad_features(X, seed: int = 42):
    """Break feature-target relationship by shuffling each column independently."""
    rng = np.random.default_rng(seed)
    X_bad = X.copy()
    for col in range(X_bad.shape[1]):
        rng.shuffle(X_bad[:, col])
    return X_bad


def train_and_score(X, y):
    X_train, X_test, y_train, y_test = split_classification_data(X, y)
    model = build_logreg_pipeline(C=1.0, max_iter=2000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return float(accuracy_score(y_test, preds)), model


def save_feature_importance_plot(model, feature_names, out_path: Path, top_k: int = 12) -> list[dict]:
    """Use abs(logistic coefficients) as a simple feature-importance proxy."""
    coefs = np.abs(model.named_steps["clf"].coef_[0])
    order = np.argsort(coefs)[::-1][:top_k]
    selected_names = [str(feature_names[i]) for i in order]
    selected_vals = [float(coefs[i]) for i in order]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(selected_names)), selected_vals)
    plt.xticks(range(len(selected_names)), selected_names, rotation=60, ha="right")
    plt.ylabel("abs(coefficient)")
    plt.title("Topic03 Feature Importance (Logistic Regression Coefficients)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return [
        {"feature": feature, "abs_coefficient": value}
        for feature, value in zip(selected_names, selected_vals)
    ]


def main() -> None:
    script_stem = "topic03_features_vs_target"
    logger = create_logger(script_stem)

    X, y, feature_names = load_breast_cancer_xy(with_feature_names=True)
    good_acc, good_model = train_and_score(X, y)
    bad_acc, _ = train_and_score(make_bad_features(X), y)

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    fig_path = results_dir / "topic03_feature_importance.png"
    top_features = save_feature_importance_plot(good_model, feature_names, fig_path)

    logger.info("accuracy_meaningful_features=%.4f", good_acc)
    logger.info("accuracy_shuffled_features=%.4f", bad_acc)
    logger.info("feature_importance_plot=%s", fig_path)

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "breast_cancer",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "accuracy",
            "quality_metric_value": good_acc,
            "metrics": {
                "accuracy_meaningful_features": good_acc,
                "accuracy_shuffled_features": bad_acc,
                "accuracy_drop": good_acc - bad_acc,
                "top_features": top_features,
            },
            "figure_paths": [str(fig_path)],
            "decision_note": "feature quality dominates downstream model performance",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
