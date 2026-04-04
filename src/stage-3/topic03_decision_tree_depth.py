"""Stage 3 Topic 03: Decision Tree depth and overfitting behavior.

Data Source: sklearn.datasets.load_breast_cancer
Schema: 30 numeric features | Target: binary class
Preprocessing: Scaling optional for trees (split rules are scale-insensitive)
Null Handling: None (dataset is verified clean by source package)
"""

from __future__ import annotations

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def evaluate_depth(max_depth: int | None) -> tuple[float, float]:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    return train_acc, test_acc


# Workflow:
# 1) Train decision trees with multiple depth settings.
# 2) Compare train/test accuracy at each depth.
# 3) Use score gaps to demonstrate overfitting.
def main() -> None:
    print("Data source: sklearn.datasets.load_breast_cancer")
    print("Rows: 569")
    print("Features: 30")

    best_depth = None
    best_test_acc = -1.0
    for depth in [2, 4, 8, None]:
        train_acc, test_acc = evaluate_depth(depth)
        gap = train_acc - test_acc
        print(
            f"max_depth={depth}, train_acc={train_acc:.3f}, test_acc={test_acc:.3f}, gap={gap:.3f}"
        )
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            best_depth = depth
        if gap > 0.15:
            print(f"  DIAGNOSIS: Overfitting detected (gap={gap:.3f}). Suggest reducing max_depth.")
        elif test_acc < 0.6:
            print("  DIAGNOSIS: Underfitting detected. Model may be too simple.")
        else:
            print("  DIAGNOSIS: Fit-quality is acceptable for this depth.")

    print(f"Best test depth candidate: {best_depth} (test_acc={best_test_acc:.3f})")

    print("Interpretation: deep trees can overfit; compare train/test gap.")


if __name__ == "__main__":
    main()

