"""Stage 3 Topic 01: Linear Regression baseline.

Data: sklearn.datasets.load_diabetes
Rows: 442
Features: 10 numeric features
Target: disease progression score (continuous)
Type: Regression
"""

from __future__ import annotations

from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Workflow:
# 1) Load diabetes regression data and split train/test.
# 2) Train a scaler + linear regression pipeline.
# 3) Report train/test regression metrics.
def main() -> None:
    data = load_diabetes(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_diabetes")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print(f"Target: continuous (mean={y.mean():.3f}, std={y.std():.3f})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("reg", LinearRegression()),
        ]
    )

    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    print("Train MSE:", round(mean_squared_error(y_train, train_pred), 3))
    print("Test MSE:", round(mean_squared_error(y_test, test_pred), 3))
    print("Test MAE:", round(mean_absolute_error(y_test, test_pred), 3))
    print("Test R^2:", round(r2_score(y_test, test_pred), 3))
    print("Interpretation: this is a numeric-prediction baseline model.")


if __name__ == "__main__":
    main()

