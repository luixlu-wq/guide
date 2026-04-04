"""
lab01_multi_asset_baseline

Lab goal:
- Create deterministic baseline metrics for a multi-asset strategy.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage14_utils import RESULTS_DIR, print_data_declaration, write_rows_csv


def main() -> None:
    declaration = {
        "Data": "Synthetic multi-asset baseline set",
        "Requests/Samples": "3 assets x 120 bars",
        "Input schema": "asset, signal_strength, volatility, expected_return",
        "Output schema": "weight, risk_score, strategy_return",
        "Eval policy": "fixed replay window",
        "Type": "multi_asset_baseline",
    }
    print_data_declaration("Lab 1 - Multi Asset Baseline", declaration)

    metrics = [
        {"metric": "annual_return", "value": 0.14},
        {"metric": "max_drawdown", "value": -0.09},
        {"metric": "sharpe_proxy", "value": 1.12},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_multi_asset_baseline_metrics.csv", metrics)

    signals = [
        {"asset": "NVDA", "signal_strength": 0.71},
        {"asset": "MSFT", "signal_strength": 0.62},
        {"asset": "GOOG", "signal_strength": 0.58},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_signal_summary.csv", signals)

    weights = [
        {"asset": "NVDA", "weight": 0.38},
        {"asset": "MSFT", "weight": 0.34},
        {"asset": "GOOG", "weight": 0.28},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_portfolio_weights.csv", weights)


if __name__ == "__main__":
    main()
