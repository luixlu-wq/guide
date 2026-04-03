"""Stage 3 Topic 07: Fair model comparison on one fixed split.

Data: sklearn.datasets.load_breast_cancer
Rows: 569
Features: 30 numeric features
Target: binary class (0=malignant, 1=benign)
Type: Fair comparison benchmark

Workflow:
1) fixed train/test split
2) model-specific preprocessing in pipelines
3) same metric set for all models
4) save results artifact
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test)[:, 1]
    else:
        # Fallback path for models without predict_proba.
        y_score = y_pred

    return {
        "model": name,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_score)),
    }


# Workflow:
# 1) Keep one fixed split for all compared models.
# 2) Train multiple models with model-appropriate pipelines.
# 3) Save comparable metrics to CSV/JSON artifacts.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_breast_cancer")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print("Fairness rule: all models use the same split and same metric set.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=3000, random_state=42)),
            ]
        ),
        "decision_tree": DecisionTreeClassifier(max_depth=4, random_state=42),
        "random_forest": RandomForestClassifier(
            n_estimators=300, random_state=42, n_jobs=1
        ),
        "svm_rbf": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", SVC(kernel="rbf", C=10, gamma=0.1, probability=True, random_state=42)),
            ]
        ),
    }

    rows = []
    for name, model in models.items():
        rows.append(evaluate_model(name, model, X_train, X_test, y_train, y_test))

    df = pd.DataFrame(rows).sort_values(by="f1", ascending=False)
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)

    csv_path = out_dir / "topic07_fair_comparison.csv"
    json_path = out_dir / "topic07_fair_comparison.json"

    df.to_csv(csv_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()

