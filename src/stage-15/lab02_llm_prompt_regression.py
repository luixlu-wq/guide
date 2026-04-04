"""
lab02_llm_prompt_regression

Lab goal:
- Detect prompt regression and verify improved prompt policy.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage15_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    resolve_project_profile,
    build_golden_set_report,
    build_icv_audit_trail,
)


def main() -> None:
    project = resolve_project_profile()
    declaration = {
        "Data": "Synthetic prompt evaluation cases",
        "Requests/Samples": "60 prompt cases",
        "Input schema": "prompt_id, requirement, expected_schema",
        "Output schema": "format_valid, grounding_score",
        "Eval policy": "fixed case replay",
        "Type": f"llm_prompt_regression/{project}",
    }
    print_data_declaration("Lab 2 - LLM Prompt Regression", declaration)

    cases = [
        {"prompt_id": "p01", "format_valid": 0, "grounding_score": 0.61},
        {"prompt_id": "p02", "format_valid": 1, "grounding_score": 0.74},
    ]
    write_rows_csv_dual("lab2_prompt_cases.csv", cases)

    options = [
        {"option": "add_schema_examples", "expected_format_delta": 0.18, "risk": "low"},
        {"option": "tighten_system_constraints", "expected_format_delta": 0.22, "risk": "medium"},
    ]
    write_rows_csv_dual("lab2_prompt_options.csv", options)

    verify = [
        {"metric": "format_valid_rate", "before": 0.72, "after": 0.91, "delta": 0.19},
        {"metric": "grounding_score", "before": 0.70, "after": 0.79, "delta": 0.09},
    ]
    write_rows_csv_dual("lab2_prompt_verification.csv", verify)

    icv_block = build_icv_audit_trail(
        identify_metric="format_valid_rate",
        identify_threshold="< 0.85",
        failing_case="prompt_case_p01",
        option_a="add_schema_examples",
        option_b="tighten_system_constraints",
        verification_delta="format_valid_rate: +0.19 (0.72 -> 0.91)",
        decision="promote",
    )

    # Canonical Stage-15 outputs used by chapter gates.
    write_rows_csv_dual("prompt_regression_table.csv", verify)
    write_text_dual("prompt_fix_note.md", "Selected option: tighten_system_constraints for stronger schema compliance.")
    write_text_dual("lab02_prompt_regression.md", build_golden_set_report(project) + "\n\n" + icv_block)


if __name__ == "__main__":
    main()
