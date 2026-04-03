"""Stage 3 Topic 04 (Simple): small Random Forest baseline.

Data: sklearn.datasets.load_iris
Rows: 150
Features: 4 numeric
Target: 3 classes
Type: Classification (simple ensemble)
"""

from __future__ import annotations

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# Workflow:
# 1) Load iris data and train a small random forest.
# 2) Predict on holdout set.
# 3) Print test accuracy baseline.
def main() -> None:
    data = load_iris(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=1)
    model.fit(X_train, y_train)

    print("Data source: load_iris")
    print("Rows: 150, Features: 4")
    print("Test accuracy:", round(accuracy_score(y_test, model.predict(X_test)), 3))


if __name__ == "__main__":
    main()

