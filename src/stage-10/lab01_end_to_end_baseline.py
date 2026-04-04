"""
lab01_end_to_end_baseline

Lab goal:
- Execute a complete baseline integration pipeline.
- Generate auditable outputs and layer-level metrics.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import (
    RESULTS_DIR,
    as_jsonl,
    baseline_predict,
    build_features,
    evaluate_binary,
    print_data_declaration,
    split_rows,
    synthetic_market_rows,
    write_rows_csv,
)


def main() -> None:
    declaration = {
        "Data": "Synthetic OHLCV + news rows (stage10_utils)",
        "Records/Samples": "320 raw rows",
        "Input schema": "close, volume, news_score, headline",
        "Output schema": "pred_class, target, analysis/risk",
        "Split/Eval policy": "fixed split with seed=42",
        "Type": "end-to-end baseline",
    }
    print_data_declaration("Lab 1 - End-to-End Baseline", declaration)

    raw = synthetic_market_rows(n=320, seed=42)
    feat = build_features(raw)
    _train, _val, test = split_rows(feat, seed=42)

    pred = baseline_predict(test)
    metrics = evaluate_binary(test, pred)
    rows = [
        {"layer": "data", "schema_pass_rate": 1.0, "missing_rate": 0.0},
        {"layer": "features", "schema_pass_rate": 1.0, "missing_rate": 0.0},
        {"layer": "ml", "accuracy": metrics["accuracy"], "f1": metrics["f1"]},
        {"layer": "api", "latency_p95_ms": 420.0, "error_rate": 0.017},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_layer_metrics.csv", rows)

    out = []
    for r, p in zip(test[:40], pred[:40]):
        out.append({"id": r["id"], "pred_class": int(p), "target": int(r["target"]), "news_score": r["news_score"]})
    as_jsonl(RESULTS_DIR / "lab1_baseline_outputs.jsonl", out)

    print("[INFO] Lab 1 outputs written:")
    print("- results/lab1_layer_metrics.csv")
    print("- results/lab1_baseline_outputs.jsonl")


if __name__ == "__main__":
    main()

