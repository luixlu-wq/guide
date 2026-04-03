"""scikit-learn split + preprocessing baseline.

Data: Breast Cancer Wisconsin (sklearn built-in)
Rows: 569
Features: 30 numeric features
Target: diagnosis (0 malignant, 1 benign)
Type: binary classification
"""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main():
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=5000, random_state=42)),
        ]
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    print("train shape:", X_train.shape, "test shape:", X_test.shape)
    print("test accuracy:", round(acc, 4))
    print("test f1      :", round(f1, 4))


if __name__ == "__main__":
    main()
