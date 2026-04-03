"""Pandas load and inspect workflow from CSV.

Data: synthetic stock-like table saved to CSV in script directory
Rows: 120
Features: date, close, volume, sector
Target: none
Type: tabular inspection
"""

from pathlib import Path

import numpy as np
import pandas as pd


def make_csv(path: Path):
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=120, freq="D")
    close = 100 + np.cumsum(rng.normal(0, 1.2, size=120))
    volume = rng.integers(50_000, 200_000, size=120)
    sector = np.where(np.arange(120) % 2 == 0, "tech", "finance")

    df = pd.DataFrame(
        {"date": dates, "close": close.round(2), "volume": volume, "sector": sector}
    )
    df.to_csv(path, index=False)


def main():
    out_csv = Path(__file__).with_name("topic03_data.csv")
    make_csv(out_csv)

    df = pd.read_csv(out_csv)
    print("loaded:", out_csv)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("\nhead:")
    print(df.head(3))
    print("\ninfo:")
    print(df.info())
    print("\nmissing values:")
    print(df.isna().sum())


if __name__ == "__main__":
    main()
