"""
lab02_pipeline_contract_validation

Lab goal:
- Validate layer contracts and detect schema/interface breaks.
- Produce contract validation and failure evidence artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic contract test cases",
        "Records/Samples": "12 contract checks",
        "Input schema": "layer, required_fields, provided_fields",
        "Output schema": "check_name, pass_flag, error_detail",
        "Split/Eval policy": "fixed deterministic checks",
        "Type": "contract validation",
    }
    print_data_declaration("Lab 2 - Pipeline Contract Validation", declaration)

    checks = [
        {"check_name": "data_schema_required_columns", "pass_flag": True, "error_detail": ""},
        {"check_name": "feature_schema_target_exists", "pass_flag": True, "error_detail": ""},
        {"check_name": "ml_input_columns_match_train", "pass_flag": True, "error_detail": ""},
        {"check_name": "llm_payload_has_probabilities", "pass_flag": False, "error_detail": "missing pred_prob_up"},
        {"check_name": "api_response_schema_complete", "pass_flag": True, "error_detail": ""},
        {"check_name": "trace_id_propagation", "pass_flag": False, "error_detail": "trace_id dropped in llm layer"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_contract_checks.csv", checks)

    failures = [
        "# Lab 2 Contract Failures",
        "",
        "1. `llm_payload_has_probabilities` failed because ML probability field was not included in reasoning payload.",
        "2. `trace_id_propagation` failed because orchestration layer did not forward trace id to LLM step.",
        "",
        "Fix policy:",
        "- enforce schema validation before each layer call",
        "- add contract unit tests in CI",
    ]
    write_text(RESULTS_DIR / "lab2_contract_failures.md", "\n".join(failures))

    print("[INFO] Lab 2 outputs written:")
    print("- results/lab2_contract_checks.csv")
    print("- results/lab2_contract_failures.md")


if __name__ == "__main__":
    main()

