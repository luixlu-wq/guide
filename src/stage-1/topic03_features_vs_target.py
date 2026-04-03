import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def make_bad_features(X, seed=42):
    rng = np.random.default_rng(seed)
    X_bad = X.copy()
    for col in range(X_bad.shape[1]):
        rng.shuffle(X_bad[:, col])
    return X_bad


def train_and_score(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)


def main():
    X, y = load_breast_cancer(return_X_y=True)
    good_acc = train_and_score(X, y)
    bad_acc = train_and_score(make_bad_features(X), y)
    print("accuracy with meaningful features:", round(good_acc, 4))
    print("accuracy with shuffled features :", round(bad_acc, 4))


if __name__ == "__main__":
    main()
