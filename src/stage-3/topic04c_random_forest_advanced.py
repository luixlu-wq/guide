"""Stage 3 Topic 04 (Advanced): OOB score + permutation importance.

Data: sklearn.datasets.load_breast_cancer
Rows: 569
Features: 30 numeric
Target: binary class
Type: Classification (advanced ensemble diagnostics)
"""

from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# Workflow:
# 1) Train random forest with out-of-bag validation enabled.
# 2) Evaluate test accuracy.
# 3) Compute permutation importance on holdout data.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=400,
        random_state=42,
        n_jobs=1,
        oob_score=True,
    )
    model.fit(X_train, y_train)

    test_acc = accuracy_score(y_test, model.predict(X_test))

    perm = permutation_importance(
        model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=1
    )
    importances = pd.Series(perm.importances_mean, index=X.columns)

    print("Data source: load_breast_cancer")
    print("OOB score:", round(model.oob_score_, 3))
    print("Test accuracy:", round(test_acc, 3))
    print("Top 5 permutation importances:")
    print(importances.sort_values(ascending=False).head(5))
    print("Interpretation: OOB gives extra validation signal; permutation importance is model-agnostic.")


if __name__ == "__main__":
    main()

