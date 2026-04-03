"""Stage 3 Topic 02: Logistic Regression classification baseline.

Data: sklearn.datasets.load_breast_cancer
Rows: 569
Features: 30 numeric features
Target: binary class (0=malignant, 1=benign)
Type: Classification
"""

from __future__ import annotations

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Workflow:
# 1) Load breast cancer data and apply stratified split.
# 2) Train scaler + logistic regression pipeline.
# 3) Report accuracy, precision, recall, F1, and ROC-AUC.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_breast_cancer")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print("Target classes: 0=malignant, 1=benign")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=3000, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
    print("Precision:", round(precision_score(y_test, y_pred), 3))
    print("Recall:", round(recall_score(y_test, y_pred), 3))
    print("F1:", round(f1_score(y_test, y_pred), 3))
    print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 3))
    print("Interpretation: logistic regression is a fast, explainable baseline.")


if __name__ == "__main__":
    main()

