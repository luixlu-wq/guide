"""
Stage 11 shared utilities.

Utilities for deterministic infrastructure benchmarking simulations across
serving, GPU/CUDA operations, vector DB diagnostics, and incident handling.
"""

from __future__ import annotations

import csv
import json
import random
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

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
    fieldnames: List[str] = []
    seen = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_text(path: Path, text: str) -> None:
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")


def check_qdrant_local(timeout_sec: float = 1.5) -> Tuple[bool, str]:
    url = "http://localhost:6333/collections"
    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
            if getattr(resp, "status", 200) == 200:
                return True, "Qdrant reachable on localhost:6333"
            return False, f"Qdrant HTTP status={getattr(resp, 'status', 'unknown')}"
    except urllib.error.URLError as exc:
        return False, f"Qdrant unavailable: {exc}"
    except Exception as exc:
        return False, f"Qdrant check failed: {exc}"


def synthetic_workload(n: int = 260, seed: int = 42) -> List[Dict[str, Any]]:
    set_seed(seed)
    out: List[Dict[str, Any]] = []
    for i in range(n):
        prompt_len = random.choice([64, 128, 256, 512, 768])
        output_len = random.choice([64, 96, 128, 160])
        conc = random.choice([1, 2, 4, 6, 8])
        out.append(
            {
                "req_id": f"req_{i:04d}",
                "prompt_len": prompt_len,
                "output_len": output_len,
                "concurrency": conc,
            }
        )
    return out


def _simulate_serving_metrics(method_focus: str, complexity: str, mode: str) -> Dict[str, float]:
    base = {
        "infra_basics": 360.0,
        "serving_patterns": 420.0,
        "gpu_cuda_ops": 310.0,
        "vector_db_ops": 390.0,
        "distributed_decisions": 370.0,
        "monitoring_alerting": 355.0,
        "capacity_cost": 380.0,
        "incident_response": 430.0,
    }.get(method_focus, 370.0)
    c = {"simple": 0.92, "intermediate": 1.0, "advanced": 1.15}[complexity]
    m = 1.0 if mode == "baseline" else 0.86
    p50 = base * c * m
    p95 = p50 * (1.62 if mode == "baseline" else 1.45)
    p99 = p95 * (1.2 if mode == "baseline" else 1.12)
    throughput = (1000.0 / p50) * (1.14 if mode == "improved" else 1.0)
    err = 0.021 if mode == "baseline" else 0.011
    gpu_mem = 2200.0 * c
    return {
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_p99_ms": round(p99, 2),
        "throughput_rps": round(throughput, 2),
        "error_rate": round(err, 4),
        "gpu_mem_mb": round(gpu_mem, 2),
    }


def run_topic_demo(topic_id: str, topic_name: str, complexity: str, method_focus: str) -> None:
    ensure_results_dir()
    declaration = {
        "Data": "Synthetic infrastructure workload profiles",
        "Requests/Samples": "260 fixed synthetic requests",
        "Input schema": "req_id, prompt_len, output_len, concurrency",
        "Output schema": "latency/throughput/error/resource metrics",
        "Eval policy": "fixed seed workload replay",
        "Type": f"{method_focus}/{complexity}",
    }
    print_data_declaration(topic_name, declaration)

    wl = synthetic_workload(n=260, seed=42)
    rows = []
    for mode in ("baseline", "improved"):
        met = _simulate_serving_metrics(method_focus, complexity, mode)
        rows.append({"topic_id": topic_id, "run_type": mode, **met})
    write_rows_csv(RESULTS_DIR / f"{topic_id}_metrics.csv", rows)

    # Sample outputs keep traceability for troubleshooting drills.
    sample = []
    for r in wl[:15]:
        sample.append(
            {
                "req_id": r["req_id"],
                "prompt_len": r["prompt_len"],
                "output_len": r["output_len"],
                "concurrency": r["concurrency"],
                "route": "gpu_fast_path" if r["prompt_len"] <= 512 else "gpu_safe_path",
            }
        )
    as_jsonl(RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl", sample)
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_metrics.csv'}")
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_sample_outputs.jsonl'}")


def run_gpu_demo(topic_id: str, complexity: str) -> None:
    ensure_results_dir()
    loops = {"simple": 30, "intermediate": 60, "advanced": 100}[complexity]
    hidden = {"simple": 64, "intermediate": 128, "advanced": 256}[complexity]
    batch = {"simple": 8, "intermediate": 16, "advanced": 24}[complexity]
    device = "cpu-fallback"
    lat: List[float] = []
    oom_recovered = False
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
            if complexity == "advanced" and device == "cuda":
                try:
                    _ = torch.randn((4096, 4096), device=device)
                except RuntimeError:
                    oom_recovered = True
                    torch.cuda.empty_cache()
            for _ in range(loops):
                x = torch.randn((batch, hidden), device=device)
                t0 = time.perf_counter()
                _ = model(x)
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
            "oom_recovered": bool(oom_recovered),
        }
    ]
    write_rows_csv(RESULTS_DIR / f"{topic_id}_cuda_metrics.csv", rows)
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_cuda_metrics.csv'}")


def build_comparison_rows(before: Dict[str, float], after: Dict[str, float]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for k in sorted(set(before.keys()).intersection(after.keys())):
        b = float(before[k])
        a = float(after[k])
        rows.append({"metric": k, "baseline_value": round(b, 4), "improved_value": round(a, 4), "delta": round(a - b, 4)})
    return rows


def summarize_latency(samples: Sequence[float]) -> Dict[str, float]:
    if not samples:
        return {"latency_p50_ms": 0.0, "latency_p95_ms": 0.0, "latency_p99_ms": 0.0}
    return {
        "latency_p50_ms": round(float(np.percentile(samples, 50)), 2),
        "latency_p95_ms": round(float(np.percentile(samples, 95)), 2),
        "latency_p99_ms": round(float(np.percentile(samples, 99)), 2),
    }

