"""Stage 3 Topic 01 (Advanced): polynomial + regularized regression comparison.

Data Source: synthetic nonlinear regression data (generated in script)
Schema: 1 numeric base feature expanded by PolynomialFeatures | Target: continuous
Preprocessing: StandardScaler required for high-degree regularized branch
Null Handling: None (synthetic generator produces complete tensors)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


# Workflow:
# 1) Build nonlinear synthetic data.
# 2) Compare linear, polynomial, and regularized polynomial models.
# 3) Print train/test metrics to show bias/variance tradeoffs.
def main() -> None:
    rng = np.random.default_rng(42)
    X = rng.uniform(-3, 3, size=(500, 1))
    y = 0.8 * X[:, 0] ** 3 - 1.2 * X[:, 0] ** 2 + 2.0 * X[:, 0] + rng.normal(0, 1.2, size=500)
    X_df = pd.DataFrame(X, columns=["x"])
    summary = (
        X_df.assign(target=y)
        .describe()
        .T[["mean", "std", "50%"]]
        .rename(columns={"50%": "median"})
    )
    print("\n--- Feature Summary (Method Chaining) ---")
    print(summary.to_string(float_format=lambda v: f"{v:.3f}"))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "linear": Pipeline([
            ("lin", LinearRegression()),
        ]),
        "poly3_linear": Pipeline([
            ("poly", PolynomialFeatures(degree=3, include_bias=False)),
            ("lin", LinearRegression()),
        ]),
        "poly8_ridge": Pipeline([
            ("poly", PolynomialFeatures(degree=8, include_bias=False)),
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=3.0, random_state=42)),
        ]),
    }

    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        rows.append(
            {
                "model": name,
                "train_mse": mean_squared_error(y_train, train_pred),
                "test_mse": mean_squared_error(y_test, test_pred),
                "test_r2": r2_score(y_test, test_pred),
            }
        )

    df = pd.DataFrame(rows).sort_values("test_mse")
    print("Data source: synthetic nonlinear")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    best = df.iloc[0]
    if float(best["test_r2"]) < 0.5:
        print("DIAGNOSIS: Feature representation still weak for this nonlinear target.")
    else:
        print("DIAGNOSIS: Nonlinear feature + regularization strategy is working.")
    print("Interpretation: polynomial features help nonlinear signal; regularization controls overfit.")


if __name__ == "__main__":
    main()

