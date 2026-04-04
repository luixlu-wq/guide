"""Stage 3 Topic 01: Linear Regression baseline.

Data Source: sklearn.datasets.load_diabetes
Schema: 10 numeric features | Target: continuous disease progression score
Preprocessing: StandardScaler recommended for stable coefficient-space learning
Null Handling: None (dataset is verified clean by source package)
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
    summary = (
        X.assign(target=y)
        .describe()
        .T[["mean", "std", "50%"]]
        .rename(columns={"50%": "median"})
    )
    print("\n--- Feature Summary (Method Chaining) ---")
    print(summary.to_string(float_format=lambda v: f"{v:.3f}"))

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

    train_mse = mean_squared_error(y_train, train_pred)
    test_mse = mean_squared_error(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    test_r2 = r2_score(y_test, test_pred)
    print("Train MSE:", round(train_mse, 3))
    print("Test MSE:", round(test_mse, 3))
    print("Test MAE:", round(test_mae, 3))
    print("Test R^2:", round(test_r2, 3))
    if test_r2 < 0.2:
        print("DIAGNOSIS: Underfitting risk. Improve features or consider nonlinear transforms.")
    elif (test_mse - train_mse) / max(train_mse, 1e-9) > 0.35:
        print("DIAGNOSIS: Generalization gap detected. Check overfitting or leakage.")
    else:
        print("DIAGNOSIS: Baseline is within expected range for this dataset.")
    print("Interpretation: this is a numeric-prediction baseline model.")


if __name__ == "__main__":
    main()

