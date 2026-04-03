"""Stage 3 Topic 03 (Simple): tiny decision tree baseline.

Data: sklearn.datasets.load_iris
Rows: 150
Features: 4 numeric features
Target: 3 classes
Type: Classification (simple tree)
"""

from __future__ import annotations

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


# Workflow:
# 1) Load iris data and train a shallow decision tree.
# 2) Print tree size characteristics (depth/leaves).
# 3) Report test accuracy for quick sanity check.
def main() -> None:
    data = load_iris(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=2, random_state=42)
    model.fit(X_train, y_train)

    print("Data source: load_iris")
    print("Rows: 150, Features: 4")
    print("Tree depth:", model.get_depth())
    print("Leaves:", model.get_n_leaves())
    print("Test accuracy:", round(accuracy_score(y_test, model.predict(X_test)), 3))


if __name__ == "__main__":
    main()

