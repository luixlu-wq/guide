"""
lab03_execution_slippage_impact

Lab goal:
- Quantify execution cost and slippage impact on strategy outcomes.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage14_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    build_slippage_decomposition,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic execution profiles",
        "Requests/Samples": "3 slippage regimes",
        "Input schema": "regime, turnover, fee_bps, slip_bps",
        "Output schema": "net_return, cost_impact",
        "Eval policy": "fixed transaction model",
        "Type": "execution_slippage",
    }
    print_data_declaration("Lab 3 - Execution Slippage Impact", declaration)

    costs = [
        {"regime": "low", "fee_bps": 3, "slip_bps": 4, "cost_impact": -0.012},
        {"regime": "medium", "fee_bps": 5, "slip_bps": 8, "cost_impact": -0.027},
        {"regime": "high", "fee_bps": 8, "slip_bps": 14, "cost_impact": -0.046},
    ]
    write_rows_csv_dual("lab3_execution_cost_profile.csv", costs)

    scenarios = [
        {"scenario": "baseline_fill", "net_return": 0.136},
        {"scenario": "stressed_fill", "net_return": 0.101},
    ]
    write_rows_csv_dual("lab3_slippage_scenarios.csv", scenarios)

    write_text_dual(
        "lab3_execution_findings.md",
        (
            "# Lab 3 Execution Findings\n\n"
            "- Execution assumptions materially change realized return.\n"
            "- High-turnover paths need stricter cost controls.\n"
            "- Slippage model must separate spread and impact components.\n"
        ),
    )

    # New expert-tier artifact: volatility/ADV-aware slippage decomposition.
    write_rows_csv_dual("slippage_decomposition.csv", build_slippage_decomposition())


if __name__ == "__main__":
    main()
