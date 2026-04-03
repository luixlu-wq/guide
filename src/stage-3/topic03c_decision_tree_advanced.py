"""Stage 3 Topic 03 (Advanced): cost-complexity pruning selection.

Data: sklearn.datasets.load_breast_cancer
Rows: 569
Features: 30 numeric
Target: binary class
Type: Classification (advanced tree tuning)
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier


# Workflow:
# 1) Compute pruning candidates via cost-complexity path.
# 2) Select alpha with cross-validation.
# 3) Train final pruned tree and report train/test performance.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    path = DecisionTreeClassifier(random_state=42).cost_complexity_pruning_path(X_train, y_train)
    alphas = np.unique(np.round(path.ccp_alphas, 5))
    alphas = alphas[(alphas >= 0)][:8]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    best_alpha = 0.0
    best_cv = -1.0

    for alpha in alphas:
        model = DecisionTreeClassifier(random_state=42, ccp_alpha=float(alpha))
        score = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=1).mean()
        if score > best_cv:
            best_cv = score
            best_alpha = float(alpha)

    final = DecisionTreeClassifier(random_state=42, ccp_alpha=best_alpha)
    final.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, final.predict(X_train))
    test_acc = accuracy_score(y_test, final.predict(X_test))

    print("Data source: load_breast_cancer")
    print(f"Selected ccp_alpha: {best_alpha:.5f}")
    print(f"Best CV accuracy: {best_cv:.3f}")
    print(f"Train accuracy: {train_acc:.3f}")
    print(f"Test accuracy: {test_acc:.3f}")
    print("Interpretation: pruning controls overfitting while keeping tree interpretability.")


if __name__ == "__main__":
    main()

