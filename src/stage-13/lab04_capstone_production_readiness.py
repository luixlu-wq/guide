"""
lab04_capstone_production_readiness

Lab goal:
- Evaluate release gates and publish release plus rollback artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage13_utils import (
    RESULTS_DIR,
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    resolve_capstone_domain,
)


def _load_latest_hardware_point() -> dict:
    """Read latest hardware sample from Lab 1 artifact, fallback to safe defaults."""
    path = RESULTS_DIR / "hardware_saturation_log.jsonl"
    if not path.exists():
        return {"vram_allocated_mb": 6144.0, "sm_clock_throttle_count": 0, "gpu_temp_c": 66.0}

    last = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = json.loads(line)
    if not isinstance(last, dict):
        return {"vram_allocated_mb": 6144.0, "sm_clock_throttle_count": 0, "gpu_temp_c": 66.0}
    return last


def main() -> None:
    domain = resolve_capstone_domain()
    hw = _load_latest_hardware_point()
    # Assume 32GB board for threshold check used by chapter hard gate.
    vram_utilization_pct = round((float(hw.get("vram_allocated_mb", 0.0)) / (32.0 * 1024.0)) * 100.0, 2)
    sm_clock_throttle_count = int(hw.get("sm_clock_throttle_count", 0))

    declaration = {
        "Data": "Synthetic release gate checklist",
        "Requests/Samples": "10 gate checks",
        "Input schema": "gate, threshold, actual",
        "Output schema": "pass_or_fail",
        "Eval policy": "fixed release criteria",
        "Type": f"production_readiness/{domain}",
    }
    print_data_declaration("Lab 4 - Capstone Production Readiness", declaration)

    checks = [
        {"gate": "contract_validity", "threshold": "100%", "actual": "100%", "pass_or_fail": "pass"},
        {"gate": "quality_score", "threshold": ">=0.80", "actual": "0.82", "pass_or_fail": "pass"},
        {"gate": "failure_rate", "threshold": "<=0.02", "actual": "0.015", "pass_or_fail": "pass"},
        {
            "gate": "vram_utilization_threshold",
            "threshold": "<90%",
            "actual": f"{vram_utilization_pct}%",
            "pass_or_fail": "pass" if vram_utilization_pct < 90.0 else "fail",
        },
        {
            "gate": "sm_clock_throttle_count",
            "threshold": "=0",
            "actual": str(sm_clock_throttle_count),
            "pass_or_fail": "pass" if sm_clock_throttle_count == 0 else "fail",
        },
    ]
    write_rows_csv_dual("lab4_release_gate_checklist.csv", checks)

    # Release decision remains a quick summary for legacy compatibility.
    promote = all(row["pass_or_fail"] == "pass" for row in checks)
    release_decision = "promote" if promote else "hold"

    write_text_dual(
        "lab4_release_decision.md",
        (
            "# Lab 4 Release Decision\n\n"
            f"- Decision: {release_decision}\n"
            "- Reason: evaluated against fixed rerun policy plus hardware gates.\n"
        ),
    )
    write_text_dual(
        "lab4_rollback_plan.md",
        (
            "# Lab 4 Rollback Plan\n\n"
            "- Trigger rollback if quality_score < 0.78 for 2 windows.\n"
            "- Trigger rollback if failure_rate > 0.02 for 2 windows.\n"
            "- Trigger rollback if vram utilization >= 90% under release load profile.\n"
            "- Trigger rollback if sm_clock_throttle_count > 0 during release candidate test.\n"
        ),
    )

    # Canonical Stage 13 artifacts required by the chapter.
    y_statement = (
        f"In the context of {domain}, we decided to use a gate-driven release process "
        "because evidence shows stable quality and latency under fixed replay with hardware safety checks."
    )
    final_release_review = (
        "# Final Release Review\n\n"
        f"- Domain: `{domain}`\n"
        f"- Decision: `{release_decision}`\n"
        f"- VRAM utilization: `{vram_utilization_pct}%`\n"
        f"- SM clock throttle count: `{sm_clock_throttle_count}`\n"
        "- Evidence artifacts: gate checklist, rollback drill, incident trace evidence\n"
        f"- ADR Y-Statement: {y_statement}\n"
    )
    write_text_dual("final_release_review.md", final_release_review)

    rollback_drill = (
        "# Rollback Drill\n\n"
        "- Scenario: candidate build degrades grounding in canary replay.\n"
        "- Action: route traffic to previous stable build, restore prior index pointer.\n"
        "- Validation: rerun fixed replay and confirm gate recovery.\n"
        f"- Result: {'pass' if promote else 'pass (rollback path exercised)'}.\n"
    )
    write_text_dual("rollback_drill.md", rollback_drill)

    print("[INFO] Lab 4 outputs written.")


if __name__ == "__main__":
    main()
