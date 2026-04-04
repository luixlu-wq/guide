"""
lab02_capstone_improvement_cycle

Lab goal:
- Compare solution options and verify one controlled improvement.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage13_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text, build_delta_rows


def main() -> None:
    declaration = {
        "Data": "Synthetic improvement scenarios",
        "Requests/Samples": "120 scenarios",
        "Input schema": "scenario_id, bottleneck, option",
        "Output schema": "quality_delta, latency_delta, cost_delta",
        "Eval policy": "baseline vs one-change rerun",
        "Type": "improvement_cycle",
    }
    print_data_declaration("Lab 2 - Capstone Improvement Cycle", declaration)

    options = [
        {"option": "prompt_constraints", "expected_quality_delta": 0.05, "expected_latency_delta": 12.0, "risk": "low"},
        {"option": "retrieval_rerank", "expected_quality_delta": 0.07, "expected_latency_delta": 28.0, "risk": "medium"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_solution_options.csv", options)

    before = {"quality_score": 0.74, "latency_p95_ms": 820.0, "cost_index": 1.55, "failure_rate": 0.026}
    after = {"quality_score": 0.81, "latency_p95_ms": 760.0, "cost_index": 1.58, "failure_rate": 0.017}
    write_rows_csv(RESULTS_DIR / "lab2_before_after_delta.csv", build_delta_rows(before, after))

    decision = "# Lab 2 Improvement Decision\n\n- Selected option: retrieval_rerank\n- Reason: best reliability gain with acceptable latency tradeoff.\n"
    write_text(RESULTS_DIR / "lab2_improvement_decision.md", decision)

    print("[INFO] Lab 2 outputs written.")


if __name__ == "__main__":
    main()
