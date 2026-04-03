import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


def make_data(n=40, seed=42):
    rng = np.random.default_rng(seed)
    X = np.sort(rng.uniform(0, 1, size=n))
    y = np.sin(2 * np.pi * X) + rng.normal(0, 0.15, size=n)
    return X.reshape(-1, 1), y


def evaluate_degree(X, y, degree):
    model = Pipeline(
        steps=[
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("linreg", LinearRegression()),
        ]
    )
    mse_scores = -cross_val_score(
        model, X, y, scoring="neg_mean_squared_error", cv=5
    )
    return mse_scores.mean(), mse_scores.std()


def main():
    X, y = make_data()
    for degree in [1, 4, 15]:
        mean_mse, std_mse = evaluate_degree(X, y, degree)
        print(f"degree={degree:2d}  cv_mse_mean={mean_mse:.4f}  cv_mse_std={std_mse:.4f}")


if __name__ == "__main__":
    main()
