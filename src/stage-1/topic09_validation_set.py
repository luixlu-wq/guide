"""Validation Set — train / validation / test three-way split.

Data: Breast Cancer Wisconsin (sklearn built-in, load_breast_cancer)
Rows: 569
Features: 30 numeric cell-measurement features (mean radius, mean texture, ...)
Target: diagnosis (0 = malignant, 1 = benign)
Type: Binary Classification

Purpose:
  Show the correct three-way split: train / validation / test.

  train set      — model learns from this
  validation set — used to compare models and tune hyperparameters
  test set       — used ONCE for the final honest evaluation

  Common mistake: using the test set to pick the best model.
  That makes the test score optimistic and no longer trustworthy.

Expected output:
  train size     : ~341
  validation size: ~114
  test size      : ~114
  val  accuracy per C value: ranging ~0.93 to ~0.98
  best C on validation: 0.1 to 1.0
  final test accuracy : ~0.95 to ~0.98

  Notice that test accuracy is evaluated only once, at the very end.
"""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main():
    X, y = load_breast_cancer(return_X_y=True)

    # Step 1: Split off the test set first.
    # The test set is locked away and never used during model selection.
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    # Step 2: Split the remaining data into train and validation.
    # 0.25 of the 80% remaining = 20% of the full dataset for validation.
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42
    )

    print(f"train size     : {len(X_train)}")
    print(f"validation size: {len(X_val)}")
    print(f"test size      : {len(X_test)}")
    print()

    # Step 3: Train multiple models with different C values.
    # C is the inverse of regularization strength in LogisticRegression.
    # Use the validation score to compare — not the test score.
    results = []
    for C in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(C=C, max_iter=5000, random_state=42)),
        ])
        model.fit(X_train, y_train)
        val_acc = accuracy_score(y_val, model.predict(X_val))
        results.append((C, val_acc, model))
        print(f"  C={C:7.3f}  val_accuracy={val_acc:.4f}")

    # Step 4: Pick the best model using validation accuracy only.
    best_C, best_val_acc, best_model = max(results, key=lambda t: t[1])
    print(f"\nbest C on validation: {best_C}  val_accuracy={best_val_acc:.4f}")

    # Step 5: Evaluate the winner on the test set — exactly once.
    test_acc = accuracy_score(y_test, best_model.predict(X_test))
    print(f"final test accuracy : {test_acc:.4f}")

    print()
    print("Key lesson:")
    print("  The test set was never touched during model selection.")
    print("  If you use the test set to pick the best C,")
    print("  you are overfitting to the test set and the score is no longer honest.")


if __name__ == "__main__":
    main()
