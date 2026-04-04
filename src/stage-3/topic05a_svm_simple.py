"""Stage 3 Topic 05 (Simple): linear-kernel SVM baseline.

Data Source: sklearn.datasets.load_iris
Schema: 4 numeric features | Target: 3 classes
Preprocessing: StandardScaler required and included in pipeline
Null Handling: None (dataset is verified clean by source package)
"""

from __future__ import annotations

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


# Workflow:
# 1) Load iris data and scale features.
# 2) Train a linear-kernel SVM.
# 3) Report holdout accuracy.
def main() -> None:
    data = load_iris(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="linear", C=1.0, random_state=42)),
    ])
    model.fit(X_train, y_train)

    print("Data source: load_iris")
    print("Rows: 150, Features: 4")
    print("Test accuracy:", round(accuracy_score(y_test, model.predict(X_test)), 3))


if __name__ == "__main__":
    main()

