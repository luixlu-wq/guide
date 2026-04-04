"""
lab04_stress_test_and_recovery

Lab goal:
- Simulate stress events and define recovery plus release recommendation.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage14_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic stress scenarios",
        "Requests/Samples": "4 adverse scenarios",
        "Input schema": "scenario, volatility_shock, liquidity_shock",
        "Output schema": "drawdown, recovery_days, pass_fail",
        "Eval policy": "fixed stress playbook",
        "Type": "stress_recovery",
    }
    print_data_declaration("Lab 4 - Stress Test and Recovery", declaration)

    stress = [
        {"scenario": "vol_spike", "drawdown": -0.11, "recovery_days": 19, "pass_fail": "pass"},
        {"scenario": "corr_spike", "drawdown": -0.14, "recovery_days": 27, "pass_fail": "warn"},
        {"scenario": "liquidity_shock", "drawdown": -0.17, "recovery_days": 33, "pass_fail": "warn"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_stress_results.csv", stress)

    actions = [
        {"action": "reduce_leverage", "priority": "high"},
        {"action": "tighten_position_caps", "priority": "high"},
        {"action": "slow_rebalance", "priority": "medium"},
    ]
    write_rows_csv(RESULTS_DIR / "lab4_recovery_actions.csv", actions)

    write_text(
        RESULTS_DIR / "lab4_release_recommendation.md",
        "# Lab 4 Release Recommendation\n\n- Decision: hold\n- Reason: liquidity shock scenario exceeds drawdown tolerance and requires mitigation before promote.\n",
    )


if __name__ == "__main__":
    main()
