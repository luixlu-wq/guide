"""Leakage demo: wrong preprocessing order vs proper pipeline.

Data: synthetic high-dimensional classification data
Rows: 900
Features: 2000
Target: binary class label
Type: classification + leakage demonstration
"""

from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def wrong_workflow(X, y):
    # WRONG: feature selection fitted on full data before split (leakage risk)
    selector = SelectKBest(score_func=f_classif, k=30)
    X_selected = selector.fit_transform(X, y)
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, test_size=0.25, stratify=y, random_state=42
    )
    model = LogisticRegression(max_iter=3000, random_state=42)
    model.fit(X_train, y_train)
    return accuracy_score(y_test, model.predict(X_test))


def correct_workflow(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    pipe = Pipeline(
        [
            ("select", SelectKBest(score_func=f_classif, k=30)),
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=3000, random_state=42)),
        ]
    )
    pipe.fit(X_train, y_train)
    return accuracy_score(y_test, pipe.predict(X_test))


def main():
    X, y = make_classification(
        n_samples=900,
        n_features=2000,
        n_informative=20,
        n_redundant=20,
        class_sep=1.0,
        random_state=42,
    )
    wrong_acc = wrong_workflow(X, y)
    correct_acc = correct_workflow(X, y)

    print("wrong workflow accuracy  :", round(wrong_acc, 4))
    print("correct workflow accuracy:", round(correct_acc, 4))
    print("delta (wrong-correct)    :", round(wrong_acc - correct_acc, 4))
    print(
        "note: leakage can inflate scores; exact delta varies by dataset split."
    )


if __name__ == "__main__":
    main()
