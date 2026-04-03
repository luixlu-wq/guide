"""Stage 3 Topic 05 (Advanced): compare SVM kernels with CV and fixed holdout.

Data: sklearn.datasets.load_wine
Rows: 178
Features: 13 numeric
Target: 3 classes
Type: Classification (advanced SVM comparison)
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


# Workflow:
# 1) Compare linear/RBF/polynomial SVM kernels via grid search.
# 2) Select best configuration using CV.
# 3) Report best params, test accuracy, and top CV configs.
def main() -> None:
    data = load_wine(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    candidates = [
        {"svm__kernel": ["linear"], "svm__C": [0.1, 1, 10]},
        {"svm__kernel": ["rbf"], "svm__C": [0.1, 1, 10], "svm__gamma": [0.01, 0.1, 1]},
        {"svm__kernel": ["poly"], "svm__C": [0.1, 1, 10], "svm__degree": [2, 3]},
    ]

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(random_state=42)),
    ])

    search = GridSearchCV(pipe, candidates, cv=5, n_jobs=1)
    search.fit(X_train, y_train)

    y_pred = search.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)

    cv_results = pd.DataFrame(search.cv_results_)
    cols = ["mean_test_score", "param_svm__kernel", "param_svm__C", "param_svm__gamma", "param_svm__degree"]
    for c in cols:
        if c not in cv_results.columns:
            cv_results[c] = None

    print("Data source: load_wine")
    print("Rows: 178, Features: 13")
    print("Best params:", search.best_params_)
    print("Best CV score:", round(search.best_score_, 3))
    print("Test accuracy:", round(test_acc, 3))
    print("Top 5 CV configs:")
    print(cv_results[cols].sort_values("mean_test_score", ascending=False).head(5).to_string(index=False))


if __name__ == "__main__":
    main()

