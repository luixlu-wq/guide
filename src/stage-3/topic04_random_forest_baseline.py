"""Stage 3 Topic 04: Random Forest baseline and feature importance.

Data Source: sklearn.datasets.load_breast_cancer
Schema: 30 numeric features | Target: binary class
Preprocessing: Scaling optional for tree ensembles
Null Handling: None (dataset is verified clean by source package)
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# Workflow:
# 1) Load breast cancer data and fit random forest baseline.
# 2) Report train/test accuracy.
# 3) Show top feature importances for interpretation.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_breast_cancer")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,  # Use all available CPU cores for local high-performance training.
    )
    model.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))

    print("Train accuracy:", round(train_acc, 3))
    print("Test accuracy:", round(test_acc, 3))
    gap = train_acc - test_acc
    if gap > 0.12:
        print(f"DIAGNOSIS: Overfitting risk detected (gap={gap:.3f}). Tune depth/min_samples.")
    else:
        print("DIAGNOSIS: Generalization gap is in a healthy range.")

    importances = pd.Series(model.feature_importances_, index=X.columns)
    print("Top 5 feature importances:")
    print(importances.sort_values(ascending=False).head(5))

    print("Interpretation: Random Forest usually improves generalization over one tree.")


if __name__ == "__main__":
    main()

