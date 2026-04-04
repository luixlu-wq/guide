"""Stage 3 Topic 05: SVM with scaling and hyperparameter tuning.

Data Source: sklearn.datasets.load_iris
Schema: 4 numeric features | Target: 3-class species label
Preprocessing: StandardScaler required for distance/margin stability
Null Handling: None (dataset is verified clean by source package)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


# Workflow:
# 1) Build scaler + RBF SVM pipeline.
# 2) Tune C and gamma with cross-validation.
# 3) Evaluate tuned model on test split.
def main() -> None:
    data = load_iris(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_iris")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print(f"Classes: {sorted(y.unique().tolist())}")
    print("Scaling check: SVM is distance-based; running without StandardScaler is a common failure mode.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svm", SVC(kernel="rbf", random_state=42)),
        ]
    )

    grid = GridSearchCV(
        estimator=pipeline,
        param_grid={
            "svm__C": [0.1, 1, 10, 100],
            "svm__gamma": [0.01, 0.1, 1],
        },
        cv=5,
        n_jobs=1,
    )

    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)

    test_acc = accuracy_score(y_test, y_pred)
    print("Best params:", grid.best_params_)
    print("Best CV score:", round(grid.best_score_, 3))
    print("Test accuracy:", round(test_acc, 3))
    if test_acc < 0.8:
        print("DIAGNOSIS: Underfitting/parameter mismatch. Expand C/gamma search space.")
    else:
        print("DIAGNOSIS: Tuned SVM is performing within expected range.")

    out_dir = Path(__file__).parent / "results" / "stage3"
    out_dir.mkdir(parents=True, exist_ok=True)
    row = {
        "model": "svm_rbf_tuned",
        "cv_score": float(grid.best_score_),
        "test_accuracy": float(test_acc),
        "best_params": str(grid.best_params_),
    }
    pd.DataFrame([row]).to_csv(out_dir / "topic05_svm_summary.csv", index=False)
    (out_dir / "topic05_svm_summary.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
    print(f"Saved: {out_dir / 'topic05_svm_summary.csv'}")
    print(f"Saved: {out_dir / 'topic05_svm_summary.json'}")
    print("Interpretation: SVM needs scaling and careful C/gamma tuning.")


if __name__ == "__main__":
    main()

