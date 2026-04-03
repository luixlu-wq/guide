"""Stage 3 Topic 02 (Simple): basic logistic regression on easy synthetic data.

Data: sklearn.datasets.make_classification
Rows: 240
Features: 2 numeric features
Target: binary class
Type: Classification (simple)
"""

from __future__ import annotations

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# Workflow:
# 1) Generate easy binary classification data.
# 2) Train baseline logistic regression.
# 3) Print test accuracy as a simple classification check.
def main() -> None:
    X, y = make_classification(
        n_samples=240,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        class_sep=1.5,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Data source: make_classification")
    print("Rows: 240, Features: 2")
    print("Test accuracy:", round(accuracy_score(y_test, y_pred), 3))


if __name__ == "__main__":
    main()

