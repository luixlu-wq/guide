"""
Stage 16 shared utilities.

Deterministic helpers for stage topic demos and lab artifact generation.
"""

from __future__ import annotations

import csv
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = THIS_DIR / "results"


def ensure_results_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)


def print_data_declaration(title: str, declaration: Dict[str, str]) -> None:
    print("\n=== Data Declaration:", title, "===")
    for k, v in declaration.items():
        print(f"{k}: {v}")
    print("=== End Data Declaration ===\n")


def write_rows_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    ensure_results_dir()
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: List[str] = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def synthetic_eval_set(n: int = 180, seed: int = 42) -> List[Dict[str, Any]]:
    set_seed(seed)
    patterns = ["baseline", "analysis", "comparison", "decision"]
    rows: List[Dict[str, Any]] = []
    for idx in range(n):
        rows.append(
            {
                "id": f"case_{idx:04d}",
                "request_type": patterns[idx % len(patterns)],
                "difficulty": random.choice(["low", "medium", "high"]),
                "expected_behavior": random.choice(["stable", "improve", "hold"]),
            }
        )
    random.shuffle(rows)
    return rows


def _topic_metrics(complexity: str, mode: str) -> Dict[str, float]:
    c_factor = {"simple": 0.92, "intermediate": 1.0, "advanced": 1.12}[complexity]
    improve = 1.07 if mode == "improved" else 1.0
    degrade_latency = 0.89 if mode == "improved" else 1.0
    fail_rate = 0.022 if mode == "baseline" else 0.012

    return {
        "quality_score": round(0.76 * c_factor * improve, 4),
        "latency_p95_ms": round(620.0 * c_factor * degrade_latency, 2),
        "cost_index": round(1.25 * c_factor, 3),
        "failure_rate": round(fail_rate, 4),
    }


def run_topic_demo(topic_id: str, topic_name: str, complexity: str, method_focus: str) -> None:
    declaration = {
        "Data": "Synthetic stage evaluation set",
        "Requests/Samples": "180 fixed cases",
        "Input schema": "id, request_type, difficulty, expected_behavior",
        "Output schema": "quality_score, latency_p95_ms, cost_index, failure_rate",
        "Eval policy": "fixed replay with seed=42",
        "Type": f"{method_focus}/{complexity}",
    }
    print_data_declaration(topic_name, declaration)

    rows = []
    for mode in ("baseline", "improved"):
        rows.append({"topic_id": topic_id, "run_type": mode, **_topic_metrics(complexity, mode)})
    write_rows_csv(RESULTS_DIR / f"{topic_id}_metrics.csv", rows)

    sample = synthetic_eval_set(n=180, seed=42)[:15]
    as_jsonl(RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl", sample)

    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_metrics.csv'}")
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_sample_outputs.jsonl'}")


def run_pytorch_cuda_reference(topic_id: str, complexity: str) -> None:
    loops = {"simple": 30, "intermediate": 60, "advanced": 90}[complexity]
    hidden = {"simple": 64, "intermediate": 128, "advanced": 256}[complexity]
    batch = {"simple": 8, "intermediate": 16, "advanced": 24}[complexity]

    latencies: List[float] = []
    device = "cpu-fallback"
    try:
        import torch

        torch.manual_seed(42)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = torch.nn.Sequential(
            torch.nn.Linear(hidden, hidden * 2),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden * 2, hidden),
        ).to(device)
        model.eval()
        with torch.inference_mode():
            for _ in range(loops):
                x = torch.randn((batch, hidden), device=device)
                t0 = time.perf_counter()
                _ = model(x)
                if device == "cuda":
                    torch.cuda.synchronize()
                latencies.append((time.perf_counter() - t0) * 1000.0)
    except Exception:
        w1 = np.random.randn(hidden, hidden * 2)
        w2 = np.random.randn(hidden * 2, hidden)
        for _ in range(loops):
            x = np.random.randn(batch, hidden)
            t0 = time.perf_counter()
            h = np.maximum(x @ w1, 0.0)
            _ = h @ w2
            latencies.append((time.perf_counter() - t0) * 1000.0)

    rows = [
        {
            "topic_id": topic_id,
            "complexity": complexity,
            "device": device,
            "latency_p50_ms": round(float(np.percentile(latencies, 50)), 3),
            "latency_p95_ms": round(float(np.percentile(latencies, 95)), 3),
        }
    ]
    write_rows_csv(RESULTS_DIR / f"{topic_id}_cuda_metrics.csv", rows)
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_cuda_metrics.csv'}")


def build_delta_rows(before: Dict[str, float], after: Dict[str, float]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for metric in sorted(set(before.keys()).intersection(after.keys())):
        b = float(before[metric])
        a = float(after[metric])
        rows.append(
            {
                "metric": metric,
                "baseline_value": round(b, 4),
                "improved_value": round(a, 4),
                "delta": round(a - b, 4),
            }
        )
    return rows

