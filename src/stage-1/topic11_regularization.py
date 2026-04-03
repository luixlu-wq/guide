"""Regularization — controlling model complexity to prevent overfitting.

Data: Breast Cancer Wisconsin (sklearn built-in, load_breast_cancer)
Rows: 569
Features: 30 numeric cell-measurement features
Target: diagnosis (0 = malignant, 1 = benign)
Type: Binary Classification

Purpose:
  Show how the regularization strength parameter C in LogisticRegression
  affects the balance between train accuracy and test accuracy.

  In LogisticRegression, C is the INVERSE of regularization strength:
    high C (e.g. 1000) = weak regularization = model can overfit
    low  C (e.g. 0.001) = strong regularization = model may underfit
    mid  C (e.g. 0.1 to 1.0) = balanced generalization

  L2 regularization (default) adds a penalty proportional to w^2.
  This discourages any single weight from becoming very large.

Expected output:
  A table showing train_acc and test_acc for C from 0.001 to 1000.

  Very low C   (0.001): train_acc ~0.93, test_acc ~0.93 (underfit — regularization too strong)
  Balanced C   (0.1–1.0): train_acc ~0.97–0.99, test_acc ~0.97–0.98 (good generalization)
  Very high C  (1000):  train_acc ~0.99–1.00, test_acc slightly lower (overfit — no penalty)

  The gap between train and test grows as C increases beyond the balanced range.
"""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main():
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("Effect of regularization strength on train vs test accuracy")
    print("(C = inverse of regularization; higher C = weaker regularization)")
    print()
    print(f"{'C':>10} | {'train_acc':>10} | {'test_acc':>10} | {'gap (train-test)':>17} | note")
    print("-" * 75)

    best_test = 0.0
    best_C = None

    for C in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]:
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(C=C, penalty="l2", max_iter=5000, random_state=42)),
        ])
        model.fit(X_train, y_train)
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        gap = train_acc - test_acc

        if C <= 0.01:
            note = "<-- strong reg (underfit risk)"
        elif C >= 100.0:
            note = "<-- weak reg (overfit risk)"
        else:
            note = ""

        print(f"{C:>10.3f} | {train_acc:>10.4f} | {test_acc:>10.4f} | {gap:>17.4f} | {note}")

        if test_acc > best_test:
            best_test = test_acc
            best_C = C

    print()
    print(f"Best test accuracy: {best_test:.4f} at C = {best_C}")
    print()
    print("Key lessons:")
    print("  1. Very high C: near-zero regularization — model can memorize training data.")
    print("     Train accuracy climbs but test accuracy may not follow.")
    print("  2. Very low C: regularization too strong — model is forced to be too simple.")
    print("     Both train and test accuracy drop (underfitting).")
    print("  3. The best test accuracy comes from a balanced C in the middle range.")
    print("  4. Regularization is how you add a complexity penalty to the loss function:")
    print("     Total Loss = Prediction Error + lambda * sum(w^2)")
    print("     lambda = 1/C  —  larger lambda means stronger penalty.")


if __name__ == "__main__":
    main()
