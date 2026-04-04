"""
lab01_instruction_tuning_baseline

This lab compares a prompt-like baseline against a tuned model using the same
fixed test set. The goal is to teach fair evaluation, not one-off demos.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import (
    RESULTS_DIR,
    as_jsonl,
    baseline_predict,
    build_metrics_comparison_rows,
    evaluate_predictions,
    print_data_declaration,
    predict_text_model,
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
        "Records": "120",
        "Input schema": "instruction:str, input:str",
        "Output schema": "trend:str, risk:str, reason:str",
        "Split/Eval policy": "fixed split seed=42",
        "Type": "SFT baseline comparison",
    }
    print_data_declaration("Lab 1 - Instruction Tuning Baseline", declaration)

    rows = synthetic_finetune_dataset(n=120, seed=42)
    train, _val, test = split_dataset(rows, seed=42)

    base_labels = baseline_predict(test)
    base_metrics = evaluate_predictions(test, base_labels)

    tuned_bundle = train_text_model(train, c_value=2.0, max_features=180)
    tuned_labels = predict_text_model(tuned_bundle, test)
    tuned_metrics = evaluate_predictions(test, tuned_labels)

    base_outputs = serialize_outputs(test, base_labels, model_name="baseline_prompt")
    tuned_outputs = serialize_outputs(test, tuned_labels, model_name="tuned_sft")

    as_jsonl(RESULTS_DIR / "lab1_base_outputs.jsonl", base_outputs)
    as_jsonl(RESULTS_DIR / "lab1_tuned_outputs.jsonl", tuned_outputs)

    comparison_rows = build_metrics_comparison_rows(
        base_metrics,
        tuned_metrics,
        baseline_name="base",
        tuned_name="tuned",
    )
    write_rows_csv(RESULTS_DIR / "lab1_metrics_comparison.csv", comparison_rows)

    mismatches = []
    for b, t in zip(base_outputs, tuned_outputs):
        if b["pred_label"] != b["gold_label"] or t["pred_label"] != t["gold_label"]:
            mismatches.append((b, t))
        if len(mismatches) >= 8:
            break

    lines = [
        "# Lab 1 Error Cases",
        "",
        "This file lists representative mistakes for baseline and tuned models.",
        "",
    ]
    if not mismatches:
        lines.append("No mismatches found in sampled outputs. Use harder test set in next iteration.")
    else:
        for i, (b, t) in enumerate(mismatches, start=1):
            lines.extend(
                [
                    f"## Case {i}",
                    f"Input: {b['input']}",
                    f"Gold: {b['gold_label']}",
                    f"Baseline: {b['pred_label']}",
                    f"Tuned: {t['pred_label']}",
                    "",
                ]
            )

    write_text(RESULTS_DIR / "lab1_error_cases.md", "\n".join(lines))

    print("[INFO] Lab 1 outputs written:")
    print("- results/lab1_base_outputs.jsonl")
    print("- results/lab1_tuned_outputs.jsonl")
    print("- results/lab1_metrics_comparison.csv")
    print("- results/lab1_error_cases.md")


if __name__ == "__main__":
    main()
