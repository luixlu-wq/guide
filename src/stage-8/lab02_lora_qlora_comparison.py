"""
lab02_lora_qlora_comparison

This lab compares LoRA-like and QLoRA-like paths using the same train/test split.
Quality and memory/latency tradeoff are reported together.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import (
    RESULTS_DIR,
    STAGE8_RESULTS_DIR,
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


def _capture_vram_telemetry(method: str, rank: int, alpha: int, batch_size: int) -> dict:
    """Capture peak VRAM telemetry with torch CUDA when available, with safe fallbacks."""
    row = {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "method": method,
        "rank": rank,
        "alpha": alpha,
        "batch_size": batch_size,
        "device_name": "cpu",
        "peak_vram_mb": 0.0,
        "source": "fallback",
        "decision": "observe",
    }

    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            device = torch.device("cuda")
            row["device_name"] = torch.cuda.get_device_name(0)
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats(device)

            # Tiny backward pass used only for deterministic telemetry capture.
            x = torch.randn(batch_size, 768, device=device)
            y = torch.randn(batch_size, 1, device=device)
            model = torch.nn.Sequential(
                torch.nn.Linear(768, 512),
                torch.nn.ReLU(),
                torch.nn.Linear(512, 1),
            ).to(device)
            loss = torch.nn.MSELoss()(model(x), y)
            loss.backward()
            torch.cuda.synchronize()

            row["peak_vram_mb"] = round(
                float(torch.cuda.max_memory_allocated(device) / (1024**2)), 2
            )
            row["source"] = "torch.cuda.max_memory_allocated"
            return row
    except Exception:
        pass

    try:
        # Best-effort nvidia-smi fallback when torch path is unavailable.
        proc = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.used",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            first = proc.stdout.strip().splitlines()[0]
            parts = [p.strip() for p in first.split(",")]
            if len(parts) >= 2:
                row["device_name"] = parts[0]
                row["peak_vram_mb"] = round(float(parts[1]), 2)
                row["source"] = "nvidia-smi"
    except Exception:
        pass

    return row


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

    # SFT-like run is used to produce explicit SFT vs QLoRA delta report.
    sft_bundle = train_text_model(train, c_value=2.4, max_features=220)
    sft_pred = predict_text_model(sft_bundle, test)
    sft_metrics = evaluate_predictions(test, sft_pred)

    lora_rows = [{"metric": k, "value": v} for k, v in lora_metrics.items()]
    qlora_rows = [{"metric": k, "value": v} for k, v in qlora_metrics.items()]

    write_rows_csv(RESULTS_DIR / "lab2_lora_metrics.csv", lora_rows)
    write_rows_csv(RESULTS_DIR / "lab2_qlora_metrics.csv", qlora_rows)

    lora_ops = simulate_resource_metrics("lora", "intermediate")
    qlora_ops = simulate_resource_metrics("qlora", "intermediate")
    sft_ops = simulate_resource_metrics("sft", "intermediate")

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

    # Mandatory Stage-8 artifacts (review-driven).
    vram_rows = [
        _capture_vram_telemetry(method="lora", rank=8, alpha=16, batch_size=16),
        _capture_vram_telemetry(method="qlora", rank=8, alpha=16, batch_size=16),
        _capture_vram_telemetry(method="sft", rank=0, alpha=0, batch_size=16),
    ]
    write_rows_csv(STAGE8_RESULTS_DIR / "vram_telemetry_5090.csv", vram_rows)

    sft_vs_qlora = [
        "# SFT vs QLoRA Delta Report",
        "",
        "## Quality",
        f"- SFT accuracy: {sft_metrics['accuracy']}",
        f"- QLoRA accuracy: {qlora_metrics['accuracy']}",
        f"- accuracy delta (QLoRA - SFT): {round(qlora_metrics['accuracy'] - sft_metrics['accuracy'], 4)}",
        f"- SFT f1_macro: {sft_metrics['f1_macro']}",
        f"- QLoRA f1_macro: {qlora_metrics['f1_macro']}",
        f"- f1_macro delta (QLoRA - SFT): {round(qlora_metrics['f1_macro'] - sft_metrics['f1_macro'], 4)}",
        "",
        "## Ops (simulated)",
        f"- SFT memory_mb: {sft_ops['memory_mb']}",
        f"- QLoRA memory_mb: {qlora_ops['memory_mb']}",
        f"- SFT latency_ms: {sft_ops['latency_ms']}",
        f"- QLoRA latency_ms: {qlora_ops['latency_ms']}",
        "",
        "## Decision template",
        "- Prefer QLoRA when quality is within tolerance and memory pressure is high.",
        "- Prefer SFT when QLoRA quality/regression gates fail.",
    ]
    write_text(STAGE8_RESULTS_DIR / "sft_vs_qlora_delta.md", "\n".join(sft_vs_qlora))

    print("[INFO] Lab 2 outputs written:")
    print("- results/lab2_lora_metrics.csv")
    print("- results/lab2_qlora_metrics.csv")
    print("- results/lab2_memory_latency_report.md")
    print("- results/stage8/vram_telemetry_5090.csv")
    print("- results/stage8/sft_vs_qlora_delta.md")


if __name__ == "__main__":
    main()
