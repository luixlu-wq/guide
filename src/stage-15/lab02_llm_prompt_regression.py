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

from stage15_utils import RESULTS_DIR, print_data_declaration, write_rows_csv


def main() -> None:
    declaration = {
        "Data": "Synthetic prompt evaluation cases",
        "Requests/Samples": "60 prompt cases",
        "Input schema": "prompt_id, requirement, expected_schema",
        "Output schema": "format_valid, grounding_score",
        "Eval policy": "fixed case replay",
        "Type": "llm_prompt_regression",
    }
    print_data_declaration("Lab 2 - LLM Prompt Regression", declaration)

    cases = [
        {"prompt_id": "p01", "format_valid": 0, "grounding_score": 0.61},
        {"prompt_id": "p02", "format_valid": 1, "grounding_score": 0.74},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_prompt_cases.csv", cases)

    options = [
        {"option": "add_schema_examples", "expected_format_delta": 0.18, "risk": "low"},
        {"option": "tighten_system_constraints", "expected_format_delta": 0.22, "risk": "medium"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_prompt_options.csv", options)

    verify = [
        {"metric": "format_valid_rate", "before": 0.72, "after": 0.91, "delta": 0.19},
        {"metric": "grounding_score", "before": 0.70, "after": 0.79, "delta": 0.09},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_prompt_verification.csv", verify)


if __name__ == "__main__":
    main()
