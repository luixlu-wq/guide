"""Time-series feature engineering with pandas.

Data: synthetic close-price series generated in-script
Rows: 180
Features: date, close
Target: direction_up (classification label)
Type: feature engineering
"""

import numpy as np
import pandas as pd


def make_data():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=180, freq="D")
    close = 100 + np.cumsum(rng.normal(0, 1.0, size=180))
    return pd.DataFrame({"date": dates, "close": close})


def main():
    df = make_data().sort_values("date").reset_index(drop=True)

    df["return_1d"] = df["close"].pct_change()
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_20"] = df["close"].rolling(20).mean()
    df["volatility_5"] = df["return_1d"].rolling(5).std()
    df["direction_up"] = (df["return_1d"].shift(-1) > 0).astype(int)

    df = df.dropna().reset_index(drop=True)

    print("shape after feature engineering:", df.shape)
    print("columns:", list(df.columns))
    print("\nhead:")
    print(df.head(3))
    print("\nfeature summary:")
    print(df[["return_1d", "ma_5", "ma_20", "volatility_5"]].describe().round(4))


if __name__ == "__main__":
    main()
