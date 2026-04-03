"""Pandas cleaning and transformation workflow.

Data: synthetic dirty table created in-script
Rows: 12
Features: Date, Close Price, Volume
Target: none
Type: tabular cleaning
"""

import numpy as np
import pandas as pd


def make_dirty_df():
    rows = [
        ["2025/01/01", 100.0, 10000],
        ["2025/01/02", 101.2, 12000],
        ["2025/01/03", None, 11000],
        ["2025/01/03", None, 11000],  # duplicate
        ["2025/01/04", 99.8, None],
        ["2025/01/05", 103.5, 13000],
        ["2025/01/06", 104.1, 12500],
        ["2025/01/07", np.nan, 12800],
        ["2025/01/08", 105.0, 14000],
        ["2025/01/09", 106.2, 15000],
        ["2025/01/10", 107.1, 16000],
        ["2025/01/11", 108.0, 17000],
    ]
    return pd.DataFrame(rows, columns=["Date", "Close Price", "Volume"])


def main():
    df = make_dirty_df()

    print("before clean")
    print("shape:", df.shape)
    print("missing:\n", df.isna().sum())

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.drop_duplicates().sort_values("date").reset_index(drop=True)

    df["close_price"] = df["close_price"].interpolate(method="linear", limit_direction="both")
    df["volume"] = df["volume"].fillna(df["volume"].median())

    print("\nafter clean")
    print("shape:", df.shape)
    print("missing:\n", df.isna().sum())
    print("\nhead:")
    print(df.head(5))


if __name__ == "__main__":
    main()
