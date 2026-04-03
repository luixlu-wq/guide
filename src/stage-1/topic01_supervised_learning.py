from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def load_data():
    X, y = load_breast_cancer(return_X_y=True)
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


def build_model():
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    print("accuracy :", round(accuracy_score(y_test, preds), 4))
    print("precision:", round(precision_score(y_test, preds), 4))
    print("recall   :", round(recall_score(y_test, preds), 4))
    print("f1       :", round(f1_score(y_test, preds), 4))
    print("confusion matrix:\n", confusion_matrix(y_test, preds))


def main():
    X_train, X_test, y_train, y_test = load_data()
    model = build_model()
    model.fit(X_train, y_train)
    evaluate(model, X_test, y_test)


if __name__ == "__main__":
    main()
