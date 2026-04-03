"""End-to-end Stage 2 pipeline: load -> clean -> feature -> split -> train -> evaluate.

Data: synthetic house table generated in-script
Rows: 500
Features:
  - area (numeric)
  - rooms (numeric)
  - age (numeric)
  - zone (categorical: A/B/C)
Target: price (numeric, regression)
Type: end-to-end tabular regression
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_data(n=500, seed=42):
    rng = np.random.default_rng(seed)
    area = rng.uniform(600, 3200, size=n)
    rooms = rng.integers(1, 8, size=n).astype(float)
    age = rng.uniform(1, 60, size=n)
    zone = rng.choice(["A", "B", "C"], size=n, p=[0.4, 0.35, 0.25])

    zone_boost = np.where(zone == "A", 45000, np.where(zone == "B", 15000, -5000))
    noise = rng.normal(0, 25000, size=n)
    price = 120 * area + 7000 * rooms - 900 * age + zone_boost + noise

    df = pd.DataFrame(
        {"area": area, "rooms": rooms, "age": age, "zone": zone, "price": price}
    )

    # Inject a small amount of missing values for realistic cleaning.
    miss_idx = rng.choice(df.index, size=20, replace=False)
    df.loc[miss_idx[:10], "rooms"] = np.nan
    df.loc[miss_idx[10:], "zone"] = np.nan
    return df


def main():
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)

    df = make_data()
    X = df.drop(columns=["price"])
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric = ["area", "rooms", "age"]
    categorical = ["zone"]

    num_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    cat_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    pre = ColumnTransformer(
        [
            ("num", num_pipe, numeric),
            ("cat", cat_pipe, categorical),
        ]
    )

    model = Pipeline(
        [
            ("preprocess", pre),
            ("rf", RandomForestRegressor(n_estimators=250, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    metrics = {
        "r2": float(r2_score(y_test, preds)),
        "mae": float(mean_absolute_error(y_test, preds)),
        "mse": float(mean_squared_error(y_test, preds)),
        "rows_train": int(len(X_train)),
        "rows_test": int(len(X_test)),
    }

    metrics_path = out_dir / "topic09_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("metrics:", {k: round(v, 4) if isinstance(v, float) else v for k, v in metrics.items()})
    print("saved:", metrics_path)


if __name__ == "__main__":
    main()
