"""
lab02_risk_engine_improvement

Lab goal:
- Improve risk profile while preserving acceptable returns.
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
    build_delta_rows,
    resolve_strategy_profile,
    build_s2_filternegative_decision_log,
    build_130_30_exposure_checks,
    build_lstm_kernel_profile,
)


def main() -> None:
    strategy = resolve_strategy_profile()
    declaration = {
        "Data": "Synthetic risk-control scenarios",
        "Requests/Samples": "2 portfolio configurations",
        "Input schema": "risk_limit, drawdown_limit, exposure_cap",
        "Output schema": "return, drawdown, volatility",
        "Eval policy": "baseline vs one-change risk control",
        "Type": f"risk_engine_improvement/{strategy}",
    }
    print_data_declaration("Lab 2 - Risk Engine Improvement", declaration)

    before = {"annual_return": 0.14, "max_drawdown": -0.12, "volatility": 0.21}
    after = {"annual_return": 0.13, "max_drawdown": -0.08, "volatility": 0.17}
    write_rows_csv_dual("lab2_risk_before_after.csv", build_delta_rows(before, after))

    changes = [
        {"control": "max_position", "before": 0.45, "after": 0.35},
        {"control": "sector_cap", "before": 0.70, "after": 0.55},
        {"control": "stop_trigger", "before": -0.12, "after": -0.08},
    ]
    write_rows_csv_dual("lab2_constraint_changes.csv", changes)

    write_text_dual(
        "lab2_risk_decision.md",
        (
            "# Lab 2 Risk Decision\n\n"
            f"- Strategy profile: `{strategy}`\n"
            "- Selected stricter risk limits to reduce drawdown.\n"
            "- Accepted moderate return decrease for better survivability.\n"
        ),
    )

    # New expert-tier artifacts for S2_FilterNegative 130/30 behavior.
    write_rows_csv_dual("s2_filternegative_decision_log.csv", build_s2_filternegative_decision_log())
    write_rows_csv_dual("lab2_130_30_exposure_checks.csv", build_130_30_exposure_checks())

    # New expert-tier runtime evidence for Blackwell-oriented LSTM path.
    write_rows_csv_dual("lstm_kernel_profile.csv", build_lstm_kernel_profile())


if __name__ == "__main__":
    main()
