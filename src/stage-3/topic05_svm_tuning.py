"""Stage 3 Topic 05: SVM with scaling and hyperparameter tuning.

Data: sklearn.datasets.load_iris
Rows: 150
Features: 4 numeric features
Target: 3-class species label
Type: Classification
"""

from __future__ import annotations

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

    print("Best params:", grid.best_params_)
    print("Best CV score:", round(grid.best_score_, 3))
    print("Test accuracy:", round(accuracy_score(y_test, y_pred), 3))
    print("Interpretation: SVM needs scaling and careful C/gamma tuning.")


if __name__ == "__main__":
    main()

