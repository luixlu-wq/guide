"""Stage 3 Topic 01 (Simple): one-feature linear regression on synthetic data.

Data: synthetic linear data
Rows: 80
Features: 1 numeric feature
Target: continuous
Type: Regression (simple)
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# Workflow:
# 1) Generate one-feature synthetic regression data.
# 2) Fit a simple LinearRegression model.
# 3) Print learned slope/intercept and training fit quality.
def main() -> None:
    rng = np.random.default_rng(42)
    X = rng.uniform(0, 10, size=(80, 1))
    y = 3.0 * X[:, 0] + 5.0 + rng.normal(0, 1.2, size=80)

    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(X)

    print("Data source: synthetic")
    print("Rows: 80, Features: 1")
    print(f"Learned slope: {model.coef_[0]:.3f}")
    print(f"Learned intercept: {model.intercept_:.3f}")
    print(f"Train R^2: {r2_score(y, pred):.3f}")


if __name__ == "__main__":
    main()

