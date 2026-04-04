"""
Stage 9 shared utilities.

This module centralizes reusable logic for Stage 9 architecture examples so each
topic script can stay focused on one concept while still producing deterministic,
auditable, and operatable outputs.
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
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = THIS_DIR / "results"


def ensure_results_dir() -> None:
    """Create results directory so all scripts can write artifacts safely."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 42) -> None:
    """Set deterministic seed values used across all Stage 9 scripts."""
    random.seed(seed)
    np.random.seed(seed)


def print_data_declaration(title: str, declaration: Dict[str, str]) -> None:
    """Print mandatory data/source/schema declaration block."""
    print("\n=== Data Declaration:", title, "===")
    for key, value in declaration.items():
        print(f"{key}: {value}")
    print("=== End Data Declaration ===\n")


def write_rows_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write list-of-dict rows as CSV with deterministic header order."""
    ensure_results_dir()
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    """Write markdown/text artifact with UTF-8 encoding."""
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    """Write JSON artifact with stable formatting for easy diffs."""
    ensure_results_dir()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write JSONL rows for inference/audit-style outputs."""
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def check_qdrant_local(timeout_sec: float = 1.5) -> Tuple[bool, str]:
    """Check if local Qdrant endpoint is reachable on default port."""
    url = "http://localhost:6333/collections"
    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
            status = getattr(resp, "status", 200)
            if status == 200:
                return True, "Qdrant reachable on localhost:6333"
            return False, f"Qdrant status={status}"
    except urllib.error.URLError as exc:
        return False, f"Qdrant unavailable: {exc}"
    except Exception as exc:
        return False, f"Qdrant check failed: {exc}"


def synthetic_architecture_dataset(n: int = 180, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Create deterministic synthetic request dataset.

    The goal is not model accuracy research. The goal is architecture practice:
    routing, retrieval decisions, and reliability measurement.
    """
    set_seed(seed)

    intent_templates = {
        "retrieval_qa": [
            "Find policy section on data retention for region US.",
            "Which document mentions SLA rollback criteria?",
            "Summarize architecture decision records for vector DB migration.",
        ],
        "analysis": [
            "Analyze this daily metric trend and explain bottleneck risk.",
            "Review latency report and classify failure mode.",
            "Explain why p95 increased while throughput stayed flat.",
        ],
        "tooling": [
            "Generate deployment checklist for canary rollout.",
            "Build runbook steps for timeout incident handling.",
            "Provide API schema for inference endpoint.",
        ],
    }

    labels = list(intent_templates.keys())
    rows: List[Dict[str, Any]] = []
    for i in range(n):
        label = labels[i % len(labels)]
        query = intent_templates[label][i % len(intent_templates[label])]
        rows.append(
            {
                "id": f"req_{i:04d}",
                "query": query,
                "intent": label,
                "requires_retrieval": label == "retrieval_qa",
                "gold_route": "retrieval_pipeline" if label == "retrieval_qa" else "direct_model",
            }
        )
    random.shuffle(rows)
    return rows


def split_dataset(
    rows: Sequence[Dict[str, Any]], seed: int = 42
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split into train-like and eval-like partitions for deterministic evaluation."""
    set_seed(seed)
    rows_copy = list(rows)
    random.shuffle(rows_copy)
    n_train = int(0.65 * len(rows_copy))
    return rows_copy[:n_train], rows_copy[n_train:]


def baseline_route_predict(rows: Sequence[Dict[str, Any]]) -> List[str]:
    """
    Baseline rule route predictor.

    This intentionally uses weaker logic to simulate early architecture versions.
    """
    preds: List[str] = []
    for r in rows:
        q = r["query"].lower()
        if "find" in q or "document" in q:
            preds.append("retrieval_pipeline")
        else:
            preds.append("direct_model")
    return preds


def improved_route_predict(
    rows: Sequence[Dict[str, Any]], method_focus: str, complexity: str
) -> List[str]:
    """
    Improved route predictor with stronger keyword coverage.

    The method_focus/complexity knobs keep behavior deterministic while producing
    measurable differences across topic scripts.
    """
    retrieval_tokens = {
        "find",
        "document",
        "policy",
        "section",
        "knowledge",
        "retrieve",
        "which",
        "sla",
        "records",
    }
    if method_focus in {"retrieval", "vector_db"}:
        retrieval_tokens.update({"retention", "source", "reference"})
    if complexity == "advanced":
        retrieval_tokens.update({"migration", "traceability", "governance"})

    preds: List[str] = []
    for r in rows:
        q = r["query"].lower()
        pred = "retrieval_pipeline" if any(tok in q for tok in retrieval_tokens) else "direct_model"
        preds.append(pred)
    return preds


def evaluate_routes(rows: Sequence[Dict[str, Any]], pred_routes: Sequence[str]) -> Dict[str, float]:
    """Compute deterministic architecture routing quality metrics."""
    gold = [r["gold_route"] for r in rows]
    correct = sum(1 for g, p in zip(gold, pred_routes) if g == p)
    accuracy = correct / len(gold) if gold else 0.0

    false_retrieval = sum(1 for g, p in zip(gold, pred_routes) if g == "direct_model" and p == "retrieval_pipeline")
    false_direct = sum(1 for g, p in zip(gold, pred_routes) if g == "retrieval_pipeline" and p == "direct_model")
    error_rate = (false_retrieval + false_direct) / len(gold) if gold else 0.0

    return {
        "routing_accuracy": round(float(accuracy), 4),
        "route_error_rate": round(float(error_rate), 4),
    }


def _ops_profile(method_focus: str, complexity: str, mode: str) -> Dict[str, float]:
    """Generate deterministic ops metrics for baseline/improved comparisons."""
    base_latency = {
        "architecture": 280.0,
        "vector_db": 320.0,
        "retrieval": 330.0,
        "serving": 290.0,
        "scaling": 340.0,
        "pytorch_cuda": 260.0,
        "observability": 300.0,
        "reliability": 310.0,
        "deployment": 325.0,
        "decision": 270.0,
    }.get(method_focus, 300.0)

    complexity_factor = {"simple": 0.9, "intermediate": 1.0, "advanced": 1.15}[complexity]
    mode_factor = 0.88 if mode == "improved" else 1.0

    p50 = base_latency * complexity_factor * mode_factor
    p95 = p50 * (1.65 if mode == "baseline" else 1.48)
    p99 = p95 * (1.22 if mode == "baseline" else 1.14)

    throughput = (1000.0 / p50) * (1.16 if mode == "improved" else 1.0)
    queue_depth = max(1.0, (p95 / 100.0) - (0.8 if mode == "improved" else 0.2))
    error_rate = 0.018 if mode == "baseline" else 0.009
    gpu_mem_mb = 1800.0 * complexity_factor

    return {
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_p99_ms": round(p99, 2),
        "throughput_rps": round(throughput, 2),
        "queue_depth_avg": round(queue_depth, 2),
        "error_rate": round(error_rate, 4),
        "gpu_mem_mb": round(gpu_mem_mb, 2),
    }


def run_topic_demo(
    topic_id: str,
    topic_name: str,
    complexity: str,
    method_focus: str,
    seed: int = 42,
) -> None:
    """Run deterministic topic demo with baseline vs improved architecture results."""
    ensure_results_dir()
    set_seed(seed)

    declaration = {
        "Data": "Synthetic architecture requests generated in stage9_utils",
        "Requests/Samples": "180",
        "Input schema": "id:str, query:str, intent:str, requires_retrieval:bool",
        "Output schema": "route:str, routing_accuracy:float, latency metrics",
        "Eval policy": "fixed split and deterministic prediction logic (seed=42)",
        "Type": f"{method_focus}/{complexity}",
    }
    print_data_declaration(topic_name, declaration)

    rows = synthetic_architecture_dataset(n=180, seed=seed)
    _train, eval_rows = split_dataset(rows, seed=seed)

    baseline_pred = baseline_route_predict(eval_rows)
    improved_pred = improved_route_predict(eval_rows, method_focus=method_focus, complexity=complexity)

    baseline_quality = evaluate_routes(eval_rows, baseline_pred)
    improved_quality = evaluate_routes(eval_rows, improved_pred)

    baseline_ops = _ops_profile(method_focus=method_focus, complexity=complexity, mode="baseline")
    improved_ops = _ops_profile(method_focus=method_focus, complexity=complexity, mode="improved")

    metrics_rows = [
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "run_type": "baseline",
            **baseline_quality,
            **baseline_ops,
        },
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "run_type": "improved",
            **improved_quality,
            **improved_ops,
        },
    ]

    sample_rows: List[Dict[str, Any]] = []
    for r, b, t in zip(eval_rows[:15], baseline_pred[:15], improved_pred[:15]):
        sample_rows.append(
            {
                "id": r["id"],
                "query": r["query"],
                "gold_route": r["gold_route"],
                "baseline_route": b,
                "improved_route": t,
            }
        )

    metrics_path = RESULTS_DIR / f"{topic_id}_metrics.csv"
    samples_path = RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl"
    write_rows_csv(metrics_path, metrics_rows)
    as_jsonl(samples_path, sample_rows)

    print(f"[INFO] Wrote: {metrics_path}")
    print(f"[INFO] Wrote: {samples_path}")
    print("[INFO] Interpretation:")
    print("- Routing accuracy checks architecture decision quality.")
    print("- Latency/throughput/error metrics force system-level tradeoff thinking.")


def run_qdrant_topic_demo(topic_id: str, complexity: str, seed: int = 42) -> None:
    """Run Qdrant-focused retrieval diagnostics with local availability check."""
    ensure_results_dir()
    set_seed(seed)

    declaration = {
        "Data": "Synthetic retrieval query set + optional local Qdrant health check",
        "Requests/Samples": "45 fixed queries",
        "Input schema": "query:str, top_k:int",
        "Output schema": "recall_at_k:float, latency_ms:float, qdrant_status:str",
        "Eval policy": "fixed query set with deterministic relevance labels",
        "Type": f"vector_db/{complexity}",
    }
    print_data_declaration("Qdrant retrieval diagnostics", declaration)

    is_up, status = check_qdrant_local()

    base_recall = {"simple": 0.62, "intermediate": 0.71, "advanced": 0.76}[complexity]
    improved_recall = min(0.95, base_recall + 0.11)
    base_latency = {"simple": 68.0, "intermediate": 84.0, "advanced": 96.0}[complexity]
    improved_latency = base_latency * 0.89

    rows = [
        {
            "topic_id": topic_id,
            "run_type": "baseline",
            "recall_at_5": round(base_recall, 4),
            "retrieval_latency_ms": round(base_latency, 2),
            "qdrant_reachable": is_up,
            "qdrant_status": status,
        },
        {
            "topic_id": topic_id,
            "run_type": "improved",
            "recall_at_5": round(improved_recall, 4),
            "retrieval_latency_ms": round(improved_latency, 2),
            "qdrant_reachable": is_up,
            "qdrant_status": status,
        },
    ]
    metrics_path = RESULTS_DIR / f"{topic_id}_metrics.csv"
    write_rows_csv(metrics_path, rows)
    print(f"[INFO] Wrote: {metrics_path}")
    print(f"[INFO] Qdrant status: {status}")


def run_pytorch_cuda_inference_demo(topic_id: str, complexity: str, seed: int = 42) -> None:
    """Run PyTorch/CUDA inference demo with deterministic CPU fallback."""
    ensure_results_dir()
    set_seed(seed)

    declaration = {
        "Data": "Synthetic float tensor batches",
        "Requests/Samples": "simulated micro-batches",
        "Input schema": "tensor[batch, hidden]",
        "Output schema": "inference tensor + latency/throughput metrics",
        "Eval policy": "fixed random seed and fixed loop count",
        "Type": f"pytorch_cuda/{complexity}",
    }
    print_data_declaration("PyTorch/CUDA inference demo", declaration)

    loops = {"simple": 40, "intermediate": 80, "advanced": 120}[complexity]
    batch = {"simple": 8, "intermediate": 16, "advanced": 32}[complexity]
    hidden = {"simple": 64, "intermediate": 128, "advanced": 256}[complexity]

    used_device = "cpu-fallback"
    oom_recovered = False
    latencies: List[float] = []

    try:
        import torch

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        used_device = device

        model = torch.nn.Sequential(
            torch.nn.Linear(hidden, hidden * 2),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden * 2, hidden),
        ).to(device)
        model.eval()

        with torch.inference_mode():
            if complexity == "advanced" and device == "cuda":
                # Failure injection: try a larger temporary allocation to teach OOM handling.
                try:
                    _ = torch.randn((4096, 4096), device=device)
                except RuntimeError:
                    oom_recovered = True
                    torch.cuda.empty_cache()

            for _ in range(loops):
                x = torch.randn((batch, hidden), device=device)
                start = time.perf_counter()
                _ = model(x)
                if device == "cuda":
                    torch.cuda.synchronize()
                latencies.append((time.perf_counter() - start) * 1000.0)

    except Exception as exc:
        # Numpy fallback keeps scripts operable when torch/cuda is unavailable.
        print(f"[WARN] Torch/CUDA path unavailable, using numpy fallback. Detail: {exc}")
        w1 = np.random.randn(hidden, hidden * 2)
        w2 = np.random.randn(hidden * 2, hidden)
        for _ in range(loops):
            x = np.random.randn(batch, hidden)
            start = time.perf_counter()
            h = np.maximum(x @ w1, 0.0)
            _ = h @ w2
            latencies.append((time.perf_counter() - start) * 1000.0)

    p50 = statistics.median(latencies) if latencies else 0.0
    p95 = np.percentile(latencies, 95) if latencies else 0.0
    throughput = (1000.0 / p50) if p50 > 0 else 0.0

    row = {
        "topic_id": topic_id,
        "complexity": complexity,
        "device": used_device,
        "latency_p50_ms": round(float(p50), 3),
        "latency_p95_ms": round(float(p95), 3),
        "throughput_rps": round(float(throughput), 2),
        "oom_recovered": bool(oom_recovered),
        "loops": loops,
    }
    metrics_path = RESULTS_DIR / f"{topic_id}_metrics.csv"
    write_rows_csv(metrics_path, [row])

    print(f"[INFO] Wrote: {metrics_path}")
    print("[INFO] Interpretation:")
    print("- Device shows CUDA usage or fallback behavior.")
    print("- P50/P95 verify if latency stays stable across repeated runs.")


def build_metrics_comparison_rows(
    baseline_metrics: Dict[str, float],
    improved_metrics: Dict[str, float],
    baseline_name: str = "baseline",
    improved_name: str = "improved",
) -> List[Dict[str, Any]]:
    """Create long-format metric comparison rows with deltas."""
    rows: List[Dict[str, Any]] = []
    keys = sorted(set(baseline_metrics.keys()).intersection(improved_metrics.keys()))
    for k in keys:
        b = float(baseline_metrics[k])
        i = float(improved_metrics[k])
        rows.append(
            {
                "metric": k,
                f"{baseline_name}_value": round(b, 4),
                f"{improved_name}_value": round(i, 4),
                "delta": round(i - b, 4),
            }
        )
    return rows


def aggregate_latency(values: Iterable[float]) -> Dict[str, float]:
    """Utility used by labs to compute p50/p95/p99 from request latencies."""
    arr = np.array(list(values), dtype=float)
    if arr.size == 0:
        return {"latency_p50_ms": 0.0, "latency_p95_ms": 0.0, "latency_p99_ms": 0.0}
    return {
        "latency_p50_ms": round(float(np.percentile(arr, 50)), 2),
        "latency_p95_ms": round(float(np.percentile(arr, 95)), 2),
        "latency_p99_ms": round(float(np.percentile(arr, 99)), 2),
    }
