"""Matplotlib as a data-debugging tool.

Data: synthetic time-series with anomaly
Rows: 160
Features: date, close, return_1d
Target: none
Type: visualization/debugging
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")


def make_data():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=160, freq="D")
    close = 120 + np.cumsum(rng.normal(0, 1.2, size=160))
    close[90] += 18  # injected anomaly spike
    df = pd.DataFrame({"date": dates, "close": close})
    df["ma_10"] = df["close"].rolling(10).mean()
    df["return_1d"] = df["close"].pct_change()
    return df


def main():
    out_dir = Path(__file__).parent
    df = make_data()

    # line chart
    plt.figure(figsize=(10, 4))
    plt.plot(df["date"], df["close"], label="close")
    plt.plot(df["date"], df["ma_10"], label="ma_10")
    plt.title("Close vs MA10 (anomaly visible near day ~90)")
    plt.xlabel("date")
    plt.ylabel("price")
    plt.legend()
    plt.tight_layout()
    line_path = out_dir / "topic06_line.png"
    plt.savefig(line_path)
    plt.close()

    # histogram
    plt.figure(figsize=(7, 4))
    plt.hist(df["return_1d"].dropna(), bins=30)
    plt.title("Return Distribution")
    plt.xlabel("return_1d")
    plt.ylabel("count")
    plt.tight_layout()
    hist_path = out_dir / "topic06_hist.png"
    plt.savefig(hist_path)
    plt.close()

    print("saved:", line_path)
    print("saved:", hist_path)
    print("close min/max:", round(df["close"].min(), 3), round(df["close"].max(), 3))


if __name__ == "__main__":
    main()
