"""
Stage 12 shared utilities.

Deterministic utilities for architecture-pattern comparison, failure drills,
ADR scoring artifacts, and release decision simulation.
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
CANONICAL_RESULTS_DIR = RESULTS_DIR / "stage12"


def ensure_results_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CANONICAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


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
        if path.parent == RESULTS_DIR:
            (CANONICAL_RESULTS_DIR / path.name).write_text("", encoding="utf-8")
        return
    fields: List[str] = []
    seen = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fields.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    if path.parent == RESULTS_DIR:
        alias_path = CANONICAL_RESULTS_DIR / path.name
        with alias_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)


def write_text(path: Path, text: str) -> None:
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")
    if path.parent == RESULTS_DIR:
        (CANONICAL_RESULTS_DIR / path.name).write_text(text, encoding="utf-8")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")
    if path.parent == RESULTS_DIR:
        alias_path = CANONICAL_RESULTS_DIR / path.name
        with alias_path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=True) + "\n")


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    ensure_results_dir()
    text = json.dumps(payload, ensure_ascii=True, indent=2)
    path.write_text(text + "\n", encoding="utf-8")
    if path.parent == RESULTS_DIR:
        (CANONICAL_RESULTS_DIR / path.name).write_text(text + "\n", encoding="utf-8")


def synthetic_arch_eval_set(n: int = 180, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Synthetic evaluation set for architecture-pattern comparisons.

    Labels represent which pattern is expected to handle the request best.
    """
    set_seed(seed)
    tasks = [
        ("llm_app", "Explain a concept in simple terms."),
        ("rag", "Answer policy question from internal handbook with citation."),
        ("agent", "Fetch latest price and calculate moving average."),
        ("multi_agent", "Research, critique, and summarize with role separation."),
    ]
    rows = []
    for i in range(n):
        t, q = tasks[i % len(tasks)]
        rows.append(
            {
                "id": f"case_{i:04d}",
                "query": q,
                "expected_pattern": t,
                "complexity": random.choice(["low", "medium", "high"]),
            }
        )
    random.shuffle(rows)
    return rows


def _pattern_metrics(pattern: str, complexity: str, mode: str) -> Dict[str, float]:
    base_quality = {
        "llm_app": 0.74,
        "rag": 0.81,
        "agent": 0.78,
        "multi_agent": 0.80,
    }.get(pattern, 0.75)
    base_latency = {
        "llm_app": 380.0,
        "rag": 520.0,
        "agent": 690.0,
        "multi_agent": 820.0,
    }.get(pattern, 500.0)
    base_cost = {
        "llm_app": 1.0,
        "rag": 1.4,
        "agent": 1.8,
        "multi_agent": 2.2,
    }.get(pattern, 1.2)
    c_factor = {"simple": 0.92, "intermediate": 1.0, "advanced": 1.14}[complexity]
    improve = 1.05 if mode == "improved" else 1.0
    degrade_latency = 0.9 if mode == "improved" else 1.0
    fail_rate = 0.023 if mode == "baseline" else 0.012

    return {
        "quality_score": round(base_quality * improve, 4),
        "latency_p95_ms": round(base_latency * c_factor * degrade_latency, 2),
        "cost_index": round(base_cost * c_factor, 3),
        "failure_rate": round(fail_rate, 4),
    }


def run_topic_demo(topic_id: str, topic_name: str, complexity: str, method_focus: str) -> None:
    ensure_results_dir()
    declaration = {
        "Data": "Synthetic architecture pattern evaluation set",
        "Requests/Samples": "180 fixed test cases",
        "Input schema": "query, expected_pattern, complexity",
        "Output schema": "quality/latency/cost/failure metrics",
        "Eval policy": "fixed test replay with seed=42",
        "Type": f"{method_focus}/{complexity}",
    }
    print_data_declaration(topic_name, declaration)

    # Map topic focus to one primary pattern for simple comparability.
    focus_to_pattern = {
        "architecture_decision": "llm_app",
        "llm_app_pattern": "llm_app",
        "rag_pattern": "rag",
        "agent_pattern": "agent",
        "multi_agent_pattern": "multi_agent",
        "pattern_comparison": "rag",
        "safety_governance": "agent",
        "release_rollback": "multi_agent",
    }
    pattern = focus_to_pattern.get(method_focus, "llm_app")
    rows = []
    for mode in ("baseline", "improved"):
        met = _pattern_metrics(pattern, complexity, mode)
        rows.append({"topic_id": topic_id, "pattern": pattern, "run_type": mode, **met})
    write_rows_csv(RESULTS_DIR / f"{topic_id}_metrics.csv", rows)

    sample = synthetic_arch_eval_set(n=180, seed=42)[:15]
    as_jsonl(RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl", sample)
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_metrics.csv'}")
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_sample_outputs.jsonl'}")


def run_pytorch_cuda_reference(topic_id: str, complexity: str) -> None:
    """
    Runtime reference benchmark for architecture tradeoff discussions.
    """
    ensure_results_dir()
    loops = {"simple": 30, "intermediate": 60, "advanced": 90}[complexity]
    hidden = {"simple": 64, "intermediate": 128, "advanced": 256}[complexity]
    batch = {"simple": 8, "intermediate": 16, "advanced": 24}[complexity]

    lat = []
    device = "cpu-fallback"
    try:
        import torch

        torch.manual_seed(42)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        m = torch.nn.Sequential(
            torch.nn.Linear(hidden, hidden * 2),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden * 2, hidden),
        ).to(device)
        m.eval()
        with torch.inference_mode():
            for _ in range(loops):
                x = torch.randn((batch, hidden), device=device)
                t0 = time.perf_counter()
                _ = m(x)
                if device == "cuda":
                    torch.cuda.synchronize()
                lat.append((time.perf_counter() - t0) * 1000.0)
    except Exception:
        w1 = np.random.randn(hidden, hidden * 2)
        w2 = np.random.randn(hidden * 2, hidden)
        for _ in range(loops):
            x = np.random.randn(batch, hidden)
            t0 = time.perf_counter()
            h = np.maximum(x @ w1, 0.0)
            _ = h @ w2
            lat.append((time.perf_counter() - t0) * 1000.0)

    rows = [
        {
            "topic_id": topic_id,
            "complexity": complexity,
            "device": device,
            "latency_p50_ms": round(float(np.percentile(lat, 50)), 3),
            "latency_p95_ms": round(float(np.percentile(lat, 95)), 3),
        }
    ]
    write_rows_csv(RESULTS_DIR / f"{topic_id}_cuda_metrics.csv", rows)
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_cuda_metrics.csv'}")


def build_delta_rows(before: Dict[str, float], after: Dict[str, float]) -> List[Dict[str, Any]]:
    rows = []
    for k in sorted(set(before.keys()).intersection(after.keys())):
        b = float(before[k])
        a = float(after[k])
        rows.append({"metric": k, "baseline_value": round(b, 4), "improved_value": round(a, 4), "delta": round(a - b, 4)})
    return rows
