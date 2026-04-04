"""
lab02_lora_qlora_comparison

This lab compares LoRA-like and QLoRA-like paths using the same train/test split.
Quality and memory/latency tradeoff are reported together.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import (
    RESULTS_DIR,
    evaluate_predictions,
    predict_text_model,
    print_data_declaration,
    simulate_resource_metrics,
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
        "Output schema": "trend/risk/reason JSON fields",
        "Split/Eval policy": "fixed split seed=42",
        "Type": "LoRA vs QLoRA comparison",
    }
    print_data_declaration("Lab 2 - LoRA vs QLoRA", declaration)

    rows = synthetic_finetune_dataset(n=120, seed=42)
    train, _val, test = split_dataset(rows, seed=42)

    # LoRA-like run uses larger feature budget and stronger capacity.
    lora_bundle = train_text_model(train, c_value=2.2, max_features=180)
    lora_pred = predict_text_model(lora_bundle, test)
    lora_metrics = evaluate_predictions(test, lora_pred)

    # QLoRA-like run uses tighter capacity to mimic compressed adaptation behavior.
    qlora_bundle = train_text_model(train, c_value=1.8, max_features=120)
    qlora_pred = predict_text_model(qlora_bundle, test)
    qlora_metrics = evaluate_predictions(test, qlora_pred)

    lora_rows = [{"metric": k, "value": v} for k, v in lora_metrics.items()]
    qlora_rows = [{"metric": k, "value": v} for k, v in qlora_metrics.items()]

    write_rows_csv(RESULTS_DIR / "lab2_lora_metrics.csv", lora_rows)
    write_rows_csv(RESULTS_DIR / "lab2_qlora_metrics.csv", qlora_rows)

    lora_ops = simulate_resource_metrics("lora", "intermediate")
    qlora_ops = simulate_resource_metrics("qlora", "intermediate")

    report = [
        "# Lab 2 Memory and Latency Tradeoff",
        "",
        "## Quality summary",
        f"- LoRA accuracy: {lora_metrics['accuracy']}",
        f"- QLoRA accuracy: {qlora_metrics['accuracy']}",
        f"- LoRA f1_macro: {lora_metrics['f1_macro']}",
        f"- QLoRA f1_macro: {qlora_metrics['f1_macro']}",
        "",
        "## Ops summary",
        f"- LoRA memory_mb (simulated): {lora_ops['memory_mb']}",
        f"- QLoRA memory_mb (simulated): {qlora_ops['memory_mb']}",
        f"- LoRA latency_ms (simulated): {lora_ops['latency_ms']}",
        f"- QLoRA latency_ms (simulated): {qlora_ops['latency_ms']}",
        "",
        "## Recommendation template",
        "- If quality delta is small and memory pressure is high, prefer QLoRA.",
        "- If quality gate fails under QLoRA, prefer LoRA or adjust quantization path.",
    ]

    write_text(RESULTS_DIR / "lab2_memory_latency_report.md", "\n".join(report))

    print("[INFO] Lab 2 outputs written:")
    print("- results/lab2_lora_metrics.csv")
    print("- results/lab2_qlora_metrics.csv")
    print("- results/lab2_memory_latency_report.md")


if __name__ == "__main__":
    main()
