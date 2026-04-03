"""Stage 3 Topic 08: Failure modes (overfitting and data leakage).

Data:
- Overfitting demo: sklearn.datasets.make_classification
- Leakage demo: synthetic random features + random labels
Type: Debugging and failure-pattern tutorial
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


def overfitting_demo() -> None:
    X, y = make_classification(
        n_samples=1200,
        n_features=25,
        n_informative=4,
        n_redundant=8,
        flip_y=0.07,
        class_sep=0.8,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    deep_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
    shallow_tree = DecisionTreeClassifier(max_depth=4, random_state=42)

    deep_tree.fit(X_train, y_train)
    shallow_tree.fit(X_train, y_train)

    deep_train = accuracy_score(y_train, deep_tree.predict(X_train))
    deep_test = accuracy_score(y_test, deep_tree.predict(X_test))
    shallow_train = accuracy_score(y_train, shallow_tree.predict(X_train))
    shallow_test = accuracy_score(y_test, shallow_tree.predict(X_test))

    print("Overfitting demo (Decision Tree):")
    print(f"  deep tree    train={deep_train:.3f}, test={deep_test:.3f}, gap={deep_train - deep_test:.3f}")
    print(f"  shallow tree train={shallow_train:.3f}, test={shallow_test:.3f}, gap={shallow_train - shallow_test:.3f}")


def leakage_demo() -> None:
    rng = np.random.default_rng(42)
    n_samples = 1200
    n_features = 600

    # Random features and random labels: no true signal.
    X = rng.normal(size=(n_samples, n_features))
    y = rng.integers(0, 2, size=n_samples)

    # Wrong workflow: feature selection on full data (leakage), then split.
    selector = SelectKBest(score_func=f_classif, k=30)
    X_selected_wrong = selector.fit_transform(X, y)

    Xw_train, Xw_test, yw_train, yw_test = train_test_split(
        X_selected_wrong, y, test_size=0.25, random_state=42, stratify=y
    )

    wrong_model = LogisticRegression(max_iter=3000, random_state=42)
    wrong_model.fit(Xw_train, yw_train)
    wrong_acc = accuracy_score(yw_test, wrong_model.predict(Xw_test))

    # Correct workflow: split first, then select features inside pipeline on train only.
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    correct_model = Pipeline(
        [
            ("select", SelectKBest(score_func=f_classif, k=30)),
            ("clf", LogisticRegression(max_iter=3000, random_state=42)),
        ]
    )
    correct_model.fit(Xc_train, yc_train)
    correct_acc = accuracy_score(yc_test, correct_model.predict(Xc_test))

    print("Leakage demo (random labels, expected near 0.5 when correct):")
    print(f"  wrong workflow (leakage) accuracy : {wrong_acc:.3f}")
    print(f"  correct workflow accuracy         : {correct_acc:.3f}")


# Workflow:
# 1) Show overfitting using deep vs shallow trees.
# 2) Show leakage using wrong-vs-correct feature selection flow.
# 3) Print diagnostics that explain suspiciously high scores.
def main() -> None:
    print("Failure Mode 1: overfitting")
    overfitting_demo()
    print()
    print("Failure Mode 2: data leakage")
    leakage_demo()
    print()
    print("Interpretation: do not trust high score without pipeline and split audit.")


if __name__ == "__main__":
    main()

