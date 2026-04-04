from __future__ import annotations

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def load_breast_cancer_xy(with_feature_names: bool = False):
    data = load_breast_cancer()
    if with_feature_names:
        return data.data, data.target, data.feature_names
    return data.data, data.target


def split_classification_data(X, y, test_size: float = 0.2, random_state: int = 42):
    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )


def build_logreg_pipeline(
    C: float = 1.0,
    max_iter: int = 2000,
    random_state: int = 42,
    penalty: str | None = None,
    solver: str | None = None,
) -> Pipeline:
    clf_kwargs = {
        "C": C,
        "max_iter": max_iter,
        "random_state": random_state,
    }
    if penalty is not None:
        clf_kwargs["penalty"] = penalty
    if solver is not None:
        clf_kwargs["solver"] = solver

    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(**clf_kwargs),
            ),
        ]
    )
