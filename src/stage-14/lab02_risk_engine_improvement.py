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

from stage14_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text, build_delta_rows


def main() -> None:
    declaration = {
        "Data": "Synthetic risk-control scenarios",
        "Requests/Samples": "2 portfolio configurations",
        "Input schema": "risk_limit, drawdown_limit, exposure_cap",
        "Output schema": "return, drawdown, volatility",
        "Eval policy": "baseline vs one-change risk control",
        "Type": "risk_engine_improvement",
    }
    print_data_declaration("Lab 2 - Risk Engine Improvement", declaration)

    before = {"annual_return": 0.14, "max_drawdown": -0.12, "volatility": 0.21}
    after = {"annual_return": 0.13, "max_drawdown": -0.08, "volatility": 0.17}
    write_rows_csv(RESULTS_DIR / "lab2_risk_before_after.csv", build_delta_rows(before, after))

    changes = [
        {"control": "max_position", "before": 0.45, "after": 0.35},
        {"control": "sector_cap", "before": 0.70, "after": 0.55},
        {"control": "stop_trigger", "before": -0.12, "after": -0.08},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_constraint_changes.csv", changes)

    write_text(
        RESULTS_DIR / "lab2_risk_decision.md",
        "# Lab 2 Risk Decision\n\n- Selected stricter risk limits to reduce drawdown.\n- Accepted moderate return decrease for better survivability.\n",
    )


if __name__ == "__main__":
    main()
