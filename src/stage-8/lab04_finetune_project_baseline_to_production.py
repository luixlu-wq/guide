"""
lab04_finetune_project_baseline_to_production

This lab follows beginning-to-production structure:
- baseline
- controlled improvements
- verification
- production readiness decision
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import (
    RESULTS_DIR,
    STAGE8_RESULTS_DIR,
    as_jsonl,
    baseline_predict,
    build_metrics_comparison_rows,
    evaluate_predictions,
    predict_text_model,
    print_data_declaration,
    serialize_outputs,
    split_dataset,
    synthetic_finetune_dataset,
    train_text_model,
    write_rows_csv,
    write_text,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic financial instruction dataset (stage8_utils)",
        "Records": "150",
        "Input schema": "instruction:str, input:str",
        "Output schema": "trend/risk/reason JSON fields",
        "Split/Eval policy": "fixed split seed=42",
        "Type": "Baseline to production improvement",
    }
    print_data_declaration("Lab 4 - Baseline to Production", declaration)

    rows = synthetic_finetune_dataset(n=150, seed=42)
    train, _val, test = split_dataset(rows, seed=42)

    baseline_labels = baseline_predict(test)
    baseline_metrics = evaluate_predictions(test, baseline_labels)

    # Controlled improvement: tuned model with stronger feature budget.
    improved_bundle = train_text_model(train, c_value=2.4, max_features=220)
    improved_labels = predict_text_model(improved_bundle, test)
    improved_metrics = evaluate_predictions(test, improved_labels)

    as_jsonl(
        RESULTS_DIR / "lab4_project_baseline_outputs.jsonl",
        serialize_outputs(test, baseline_labels, model_name="baseline"),
    )
    as_jsonl(
        RESULTS_DIR / "lab4_project_improved_outputs.jsonl",
        serialize_outputs(test, improved_labels, model_name="improved"),
    )

    solution_rows = [
        {
            "problem_class": "Weak format and trend consistency",
            "option_name": "Prompt-only cleanup",
            "change_scope": "low",
            "expected_quality_delta": 0.02,
            "expected_latency_delta": 0.0,
            "risk_level": "low",
            "chosen_flag": "no",
        },
        {
            "problem_class": "Weak format and trend consistency",
            "option_name": "SFT with curated dataset",
            "change_scope": "medium",
            "expected_quality_delta": 0.08,
            "expected_latency_delta": 0.01,
            "risk_level": "medium",
            "chosen_flag": "yes",
        },
    ]
    write_rows_csv(RESULTS_DIR / "lab4_solution_options.csv", solution_rows)

    metric_rows = build_metrics_comparison_rows(
        baseline_metrics,
        improved_metrics,
        baseline_name="baseline",
        tuned_name="improved",
    )
    write_rows_csv(RESULTS_DIR / "lab4_metrics_comparison.csv", metric_rows)

    # General-capability retention gate (knowledge retention check).
    general_rows = synthetic_finetune_dataset(n=60, seed=99)
    _g_train, _g_val, g_test = split_dataset(general_rows, seed=99)
    baseline_general_labels = baseline_predict(g_test)
    improved_general_labels = predict_text_model(improved_bundle, g_test)
    baseline_general_metrics = evaluate_predictions(g_test, baseline_general_labels)
    improved_general_metrics = evaluate_predictions(g_test, improved_general_labels)
    retention_drop = round(
        baseline_general_metrics["accuracy"] - improved_general_metrics["accuracy"], 4
    )

    # Simple promotion policy for teaching gate logic.
    pass_quality = improved_metrics["accuracy"] >= baseline_metrics["accuracy"]
    pass_format = (
        improved_metrics["format_validity"] >= baseline_metrics["format_validity"]
    )
    pass_retention = retention_drop <= 0.03
    decision = "promote" if (pass_quality and pass_format and pass_retention) else "hold"

    verification = [
        "# Lab 4 Verification Report",
        "",
        "## Baseline summary",
        f"- accuracy: {baseline_metrics['accuracy']}",
        f"- f1_macro: {baseline_metrics['f1_macro']}",
        "",
        "## Improved summary",
        f"- accuracy: {improved_metrics['accuracy']}",
        f"- f1_macro: {improved_metrics['f1_macro']}",
        "",
        "## Retention gate summary",
        f"- baseline_general_accuracy: {baseline_general_metrics['accuracy']}",
        f"- improved_general_accuracy: {improved_general_metrics['accuracy']}",
        f"- retention_drop: {retention_drop}",
        f"- retention_gate_pass: {pass_retention}",
        "",
        "## Regression gate checks",
        f"- quality gate pass: {pass_quality}",
        f"- format gate pass: {pass_format}",
        f"- decision: {decision}",
    ]
    write_text(RESULTS_DIR / "lab4_verification_report.md", "\n".join(verification))

    readiness = [
        "# Lab 4 Production Readiness",
        "",
        "- Fixed eval set: yes",
        "- Baseline snapshot: yes",
        "- Controlled change applied: yes",
        f"- Promotion decision: {decision}",
        "- Rollback path documented: yes (revert to baseline artifacts)",
    ]
    write_text(RESULTS_DIR / "lab4_production_readiness.md", "\n".join(readiness))

    # Mandatory Stage-8 promotion artifact.
    promotion = [
        "# Model Promotion Report",
        "",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        "stage: stage-8",
        "eval_set: fixed split seed=42 + general holdout seed=99",
        "",
        "## Side-by-side quality comparison (fixed eval set)",
        f"- baseline_accuracy: {baseline_metrics['accuracy']}",
        f"- tuned_accuracy: {improved_metrics['accuracy']}",
        f"- delta_accuracy: {round(improved_metrics['accuracy'] - baseline_metrics['accuracy'], 4)}",
        f"- baseline_f1_macro: {baseline_metrics['f1_macro']}",
        f"- tuned_f1_macro: {improved_metrics['f1_macro']}",
        f"- delta_f1_macro: {round(improved_metrics['f1_macro'] - baseline_metrics['f1_macro'], 4)}",
        "",
        "## Knowledge retention gate",
        f"- baseline_general_accuracy: {baseline_general_metrics['accuracy']}",
        f"- tuned_general_accuracy: {improved_general_metrics['accuracy']}",
        f"- retention_drop: {retention_drop}",
        f"- retention_threshold: 0.03",
        f"- retention_gate_pass: {pass_retention}",
        "",
        "## Promotion gates",
        f"- quality_gate_pass: {pass_quality}",
        f"- format_gate_pass: {pass_format}",
        f"- retention_gate_pass: {pass_retention}",
        f"- final_decision: {decision}",
        "",
        "## Rollback condition",
        "- Roll back immediately if retention gate fails or format-validity regresses.",
    ]
    write_text(STAGE8_RESULTS_DIR / "model_promotion_report.md", "\n".join(promotion))

    print("[INFO] Lab 4 outputs written:")
    print("- results/lab4_project_baseline_outputs.jsonl")
    print("- results/lab4_project_improved_outputs.jsonl")
    print("- results/lab4_solution_options.csv")
    print("- results/lab4_metrics_comparison.csv")
    print("- results/lab4_verification_report.md")
    print("- results/lab4_production_readiness.md")
    print("- results/stage8/model_promotion_report.md")


if __name__ == "__main__":
    main()
