"""
lab03_distillation_tradeoff_lab

This lab emulates teacher-student distillation workflow and reports quality-cost tradeoffs.
It also includes a knowledge-retention gate artifact required by Stage 8.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import (
    RESULTS_DIR,
    STAGE8_RESULTS_DIR,
    as_jsonl,
    evaluate_predictions,
    predict_text_model,
    print_data_declaration,
    serialize_outputs,
    split_dataset,
    synthetic_finetune_dataset,
    train_text_model,
    write_text,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic financial instruction dataset (stage8_utils)",
        "Records": "120",
        "Input schema": "instruction:str, input:str",
        "Output schema": "trend/risk/reason JSON fields",
        "Split/Eval policy": "fixed split seed=42",
        "Type": "Distillation (teacher-student)",
    }
    print_data_declaration("Lab 3 - Distillation", declaration)

    rows = synthetic_finetune_dataset(n=120, seed=42)
    train, _val, test = split_dataset(rows, seed=42)

    # Teacher model has higher capacity and acts as supervision source.
    teacher_bundle = train_text_model(train, c_value=2.5, max_features=220)
    teacher_train_pred = predict_text_model(teacher_bundle, train)

    # Build pseudo-student training rows by replacing label with teacher label.
    distilled_train = []
    for r, teacher_label in zip(train, teacher_train_pred):
        clone = dict(r)
        clone["label"] = teacher_label
        distilled_train.append(clone)

    # Student baseline (before distillation) and distilled student use same capacity.
    student_base_bundle = train_text_model(train, c_value=1.2, max_features=90)
    student_tuned_bundle = train_text_model(distilled_train, c_value=1.2, max_features=90)

    teacher_test_pred = predict_text_model(teacher_bundle, test)
    student_base_test_pred = predict_text_model(student_base_bundle, test)
    student_tuned_test_pred = predict_text_model(student_tuned_bundle, test)

    teacher_metrics = evaluate_predictions(test, teacher_test_pred)
    student_tuned_metrics = evaluate_predictions(test, student_tuned_test_pred)

    as_jsonl(
        RESULTS_DIR / "lab3_teacher_outputs.jsonl",
        serialize_outputs(test, teacher_test_pred, model_name="teacher"),
    )
    as_jsonl(
        RESULTS_DIR / "lab3_student_outputs.jsonl",
        serialize_outputs(test, student_tuned_test_pred, model_name="student"),
    )

    # Knowledge-retention/forgetting gate on fixed "general" holdout split.
    general_rows = synthetic_finetune_dataset(n=60, seed=99)
    _g_train, _g_val, g_test = split_dataset(general_rows, seed=99)
    baseline_general_pred = predict_text_model(student_base_bundle, g_test)
    tuned_general_pred = predict_text_model(student_tuned_bundle, g_test)
    baseline_general_metrics = evaluate_predictions(g_test, baseline_general_pred)
    tuned_general_metrics = evaluate_predictions(g_test, tuned_general_pred)
    accuracy_drop = round(
        baseline_general_metrics["accuracy"] - tuned_general_metrics["accuracy"], 4
    )
    retention_gate_pass = accuracy_drop <= 0.03

    forgetting_rows = []
    for r, b_pred, t_pred in zip(g_test, baseline_general_pred, tuned_general_pred):
        forgetting_rows.append(
            {
                "case_id": r["id"],
                "input": r["input"],
                "gold_label": r["label"],
                "baseline_pred": b_pred,
                "tuned_pred": t_pred,
                "baseline_correct": b_pred == r["label"],
                "tuned_correct": t_pred == r["label"],
                "regression_flag": (b_pred == r["label"]) and (t_pred != r["label"]),
            }
        )
    as_jsonl(STAGE8_RESULTS_DIR / "forgetting_test_results.jsonl", forgetting_rows)

    report = [
        "# Lab 3 Distillation Report",
        "",
        "## Teacher metrics",
        f"- accuracy: {teacher_metrics['accuracy']}",
        f"- f1_macro: {teacher_metrics['f1_macro']}",
        "",
        "## Student metrics",
        f"- accuracy: {student_tuned_metrics['accuracy']}",
        f"- f1_macro: {student_tuned_metrics['f1_macro']}",
        "",
        "## Knowledge retention gate (general holdout)",
        f"- baseline_general_accuracy: {baseline_general_metrics['accuracy']}",
        f"- tuned_general_accuracy: {tuned_general_metrics['accuracy']}",
        f"- general_accuracy_drop: {accuracy_drop}",
        f"- retention_gate_pass: {retention_gate_pass}",
        "",
        "## Interpretation",
        "- Distillation is acceptable when student quality drop is within deployment tolerance.",
        "- Student gains are typically in cost/latency; quality must still pass gate.",
    ]

    write_text(RESULTS_DIR / "lab3_distillation_report.md", "\n".join(report))

    print("[INFO] Lab 3 outputs written:")
    print("- results/lab3_teacher_outputs.jsonl")
    print("- results/lab3_student_outputs.jsonl")
    print("- results/lab3_distillation_report.md")
    print("- results/stage8/forgetting_test_results.jsonl")


if __name__ == "__main__":
    main()
