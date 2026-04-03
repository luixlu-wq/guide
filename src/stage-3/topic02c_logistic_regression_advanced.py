"""Stage 3 Topic 02 (Advanced): imbalanced classification and threshold tuning.

Data: sklearn.datasets.make_classification
Rows: 1200
Features: 20 numeric features
Target: binary class (imbalanced)
Type: Classification (advanced)
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def metrics_at_threshold(y_true, y_prob, th: float) -> tuple[float, float, float]:
    y_pred = (y_prob >= th).astype(int)
    return (
        precision_score(y_true, y_pred, zero_division=0),
        recall_score(y_true, y_pred, zero_division=0),
        f1_score(y_true, y_pred, zero_division=0),
    )


# Workflow:
# 1) Create imbalanced classification data.
# 2) Train class-balanced logistic model and predict probabilities.
# 3) Evaluate precision/recall/F1 at multiple decision thresholds.
def main() -> None:
    X, y = make_classification(
        n_samples=1200,
        n_features=20,
        n_informative=5,
        n_redundant=5,
        weights=[0.9, 0.1],
        flip_y=0.02,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=42)),
    ])
    model.fit(X_train, y_train)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("Data source: make_classification (imbalanced)")
    print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 3))

    for th in [0.3, 0.5, 0.7]:
        p, r, f1 = metrics_at_threshold(y_test, y_prob, th)
        print(f"threshold={th:.1f} -> precision={p:.3f}, recall={r:.3f}, f1={f1:.3f}")

    print("Interpretation: threshold tuning trades precision vs recall.")


if __name__ == "__main__":
    main()

