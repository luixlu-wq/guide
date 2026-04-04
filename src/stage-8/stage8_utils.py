"""
Stage 8 shared utilities.

This module centralizes reusable logic so each topic and lab script can focus on
its learning objective while still being runnable, deterministic, and easy to audit.
"""

from __future__ import annotations

import csv
import json
import math
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

THIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = THIS_DIR / "results"


@dataclass
class TextModelBundle:
    """Container for vectorizer + classifier used in text-label prediction."""

    vectorizer: TfidfVectorizer
    model: LogisticRegression


def ensure_results_dir() -> None:
    """Create results directory if missing so scripts can always write artifacts."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 42) -> None:
    """Set deterministic seeds for reproducible dataset generation and model behavior."""
    random.seed(seed)
    np.random.seed(seed)


def print_data_declaration(title: str, declaration: Dict[str, str]) -> None:
    """Print a strict data/schema declaration block required by handbook policy."""
    print("\n=== Data Declaration:", title, "===")
    for key, value in declaration.items():
        print(f"{key}: {value}")
    print("=== End Data Declaration ===\n")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write rows as JSONL file for run artifacts and auditability."""
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def write_text(path: Path, text: str) -> None:
    """Write plain text/markdown artifacts used by reports and runbooks."""
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")


def write_rows_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write structured CSV outputs used by metrics and solution comparison files."""
    ensure_results_dir()
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def label_to_output(label: str) -> Dict[str, str]:
    """Map class label to a structured response object used in stage outputs."""
    if label == "bullish":
        return {
            "trend": "bullish",
            "risk": "moderate",
            "reason": "Momentum and trend signals both support upside continuation.",
        }
    if label == "bearish":
        return {
            "trend": "bearish",
            "risk": "high",
            "reason": "Trend and momentum indicate downside pressure and weaker structure.",
        }
    return {
        "trend": "neutral",
        "risk": "medium",
        "reason": "Signals are mixed, so directional confidence remains limited.",
    }


def _record_for_label(label: str, idx: int) -> Dict[str, Any]:
    """Generate one synthetic but realistic instruction-style training record."""
    bullish_patterns = [
        "MA20 > MA50, RSI=67, volume rising, price above resistance",
        "MA20 > MA50, MACD positive, breakout confirmed, volume rising",
        "Higher highs and higher lows, RSI=62, trend strength increasing",
    ]
    bearish_patterns = [
        "MA20 < MA50, RSI=33, volume rising on down days, support broken",
        "MA20 < MA50, MACD negative, failed rebound, bearish continuation",
        "Lower highs and lower lows, RSI=38, weak demand profile",
    ]
    neutral_patterns = [
        "MA20 near MA50, RSI=50, volume flat, range-bound behavior",
        "Mixed momentum signals, no clean breakout, uncertain direction",
        "Price oscillates near mean, trend strength weak, low conviction",
    ]

    if label == "bullish":
        signal = bullish_patterns[idx % len(bullish_patterns)]
    elif label == "bearish":
        signal = bearish_patterns[idx % len(bearish_patterns)]
    else:
        signal = neutral_patterns[idx % len(neutral_patterns)]

    instruction = (
        "Analyze the market setup and return JSON with trend, risk, and reason."
    )
    output = label_to_output(label)
    return {
        "id": f"case_{idx:04d}",
        "instruction": instruction,
        "input": signal,
        "label": label,
        "output": json.dumps(output, ensure_ascii=True),
    }


def synthetic_finetune_dataset(n: int = 120, seed: int = 42) -> List[Dict[str, Any]]:
    """Create deterministic dataset used across stage topics and labs."""
    set_seed(seed)
    labels = ["bullish", "neutral", "bearish"]
    rows: List[Dict[str, Any]] = []
    for i in range(n):
        rows.append(_record_for_label(labels[i % 3], i))

    random.shuffle(rows)
    return rows


def split_dataset(
    rows: Sequence[Dict[str, Any]], seed: int = 42
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split dataset into train/validation/test with deterministic shuffling."""
    set_seed(seed)
    rows_copy = list(rows)
    random.shuffle(rows_copy)

    n = len(rows_copy)
    n_train = int(0.6 * n)
    n_val = int(0.2 * n)

    train = rows_copy[:n_train]
    val = rows_copy[n_train : n_train + n_val]
    test = rows_copy[n_train + n_val :]
    return train, val, test


def _build_text(record: Dict[str, Any]) -> str:
    """Merge instruction and input to create the model text feature."""
    return f"{record['instruction']} || {record['input']}"


def heuristic_label(text: str) -> str:
    """Simple baseline heuristic to mimic prompt-only baseline behavior."""
    t = text.lower()
    if "ma20 > ma50" in t or "breakout" in t or "higher highs" in t:
        return "bullish"
    if "ma20 < ma50" in t or "support broken" in t or "lower highs" in t:
        return "bearish"
    return "neutral"


def baseline_predict(rows: Sequence[Dict[str, Any]]) -> List[str]:
    """Generate baseline predictions using deterministic heuristic logic."""
    return [heuristic_label(_build_text(r)) for r in rows]


def train_text_model(
    train_rows: Sequence[Dict[str, Any]],
    c_value: float = 2.0,
    max_features: int | None = None,
) -> TextModelBundle:
    """Train lightweight text classifier used as stand-in for tuned model behavior."""
    train_text = [_build_text(r) for r in train_rows]
    train_labels = [r["label"] for r in train_rows]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=max_features)
    x_train = vectorizer.fit_transform(train_text)

    model = LogisticRegression(
        C=c_value,
        max_iter=400,
        random_state=42,
    )
    model.fit(x_train, train_labels)
    return TextModelBundle(vectorizer=vectorizer, model=model)


def predict_text_model(bundle: TextModelBundle, rows: Sequence[Dict[str, Any]]) -> List[str]:
    """Run inference for tuned-model approximation on provided rows."""
    x = bundle.vectorizer.transform([_build_text(r) for r in rows])
    return bundle.model.predict(x).tolist()


def evaluate_predictions(rows: Sequence[Dict[str, Any]], pred_labels: Sequence[str]) -> Dict[str, float]:
    """Compute stable evaluation metrics for quality and format behavior."""
    gold = [r["label"] for r in rows]
    accuracy = float(accuracy_score(gold, pred_labels))
    f1_macro = float(f1_score(gold, pred_labels, average="macro"))

    # All generated outputs are structured from label mapping in this utility path.
    format_validity = 1.0

    return {
        "accuracy": round(accuracy, 4),
        "f1_macro": round(f1_macro, 4),
        "format_validity": round(format_validity, 4),
    }


def serialize_outputs(
    rows: Sequence[Dict[str, Any]], pred_labels: Sequence[str], model_name: str
) -> List[Dict[str, Any]]:
    """Create consistent prediction rows for JSONL artifacts and audits."""
    out: List[Dict[str, Any]] = []
    for r, label in zip(rows, pred_labels):
        out_obj = label_to_output(label)
        out.append(
            {
                "id": r["id"],
                "model": model_name,
                "input": r["input"],
                "pred_label": label,
                "gold_label": r["label"],
                "output": out_obj,
            }
        )
    return out


def simulate_resource_metrics(method_focus: str, complexity: str) -> Dict[str, float]:
    """Return deterministic synthetic ops metrics for cross-method tradeoff teaching."""
    base_memory = {
        "sft": 2200,
        "lora": 900,
        "qlora": 620,
        "distill": 480,
        "strategy": 700,
        "eval": 400,
        "ops": 500,
        "data": 300,
        "pytorch_cuda": 1100,
    }.get(method_focus, 800)

    complexity_factor = {"simple": 0.9, "intermediate": 1.0, "advanced": 1.2}[complexity]

    memory_mb = round(base_memory * complexity_factor, 2)
    latency_ms = round((45 + base_memory / 60.0) * complexity_factor, 2)
    cost_per_1k = round((base_memory / 5000.0) * complexity_factor, 4)

    return {
        "memory_mb": memory_mb,
        "latency_ms": latency_ms,
        "cost_per_1k_queries": cost_per_1k,
    }


def run_topic_demo(
    topic_id: str,
    topic_name: str,
    complexity: str,
    method_focus: str,
    seed: int = 42,
) -> None:
    """Run a full topic demonstration with baseline/tuned comparison and outputs."""
    ensure_results_dir()
    set_seed(seed)

    declaration = {
        "Data": "Synthetic financial instruction dataset (generated in stage8_utils)",
        "Records": "120",
        "Input schema": "instruction:str, input:str",
        "Output schema": "trend:str, risk:str, reason:str",
        "Split/Eval policy": "fixed train/val/test split with seed=42",
        "Type": f"{method_focus} / {complexity}",
    }
    print_data_declaration(topic_name, declaration)

    rows = synthetic_finetune_dataset(n=120, seed=seed)
    train, _val, test = split_dataset(rows, seed=seed)

    baseline_labels = baseline_predict(test)
    baseline_metrics = evaluate_predictions(test, baseline_labels)

    # Tune a lightweight text model to emulate behavior improvement path.
    c_by_complexity = {"simple": 1.0, "intermediate": 2.0, "advanced": 3.0}[complexity]
    max_features = {"simple": 80, "intermediate": 140, "advanced": 220}[complexity]
    tuned_bundle = train_text_model(train, c_value=c_by_complexity, max_features=max_features)
    tuned_labels = predict_text_model(tuned_bundle, test)
    tuned_metrics = evaluate_predictions(test, tuned_labels)

    resources = simulate_resource_metrics(method_focus=method_focus, complexity=complexity)

    metrics_rows = [
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "run_type": "baseline",
            **baseline_metrics,
            **resources,
        },
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "run_type": "tuned",
            **tuned_metrics,
            **resources,
        },
    ]

    metrics_path = RESULTS_DIR / f"{topic_id}_metrics.csv"
    outputs_path = RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl"

    write_rows_csv(metrics_path, metrics_rows)
    as_jsonl(outputs_path, serialize_outputs(test[:12], tuned_labels[:12], model_name=topic_id))

    print(f"[INFO] Wrote: {metrics_path}")
    print(f"[INFO] Wrote: {outputs_path}")
    print("[INFO] Interpretation:")
    print("- Compare baseline and tuned rows to check if adaptation actually improved quality.")
    print("- Resource metrics are included to force quality-cost tradeoff discussion.")


def run_pytorch_cuda_demo(topic_id: str, complexity: str, seed: int = 42) -> None:
    """Run PyTorch/CUDA training-loop demo with deterministic CPU fallback."""
    ensure_results_dir()
    set_seed(seed)

    declaration = {
        "Data": "Synthetic numeric regression dataset",
        "Records": "256",
        "Input schema": "x1:float, x2:float",
        "Output schema": "target:float",
        "Split/Eval policy": "fixed synthetic generation with seed=42",
        "Type": f"pytorch_cuda / {complexity}",
    }
    print_data_declaration("PyTorch/CUDA tuning demo", declaration)

    try:
        import torch

        torch.manual_seed(seed)
        device = "cuda" if torch.cuda.is_available() else "cpu"

        n = {"simple": 128, "intermediate": 256, "advanced": 512}[complexity]
        epochs = {"simple": 25, "intermediate": 50, "advanced": 80}[complexity]

        x = torch.randn(n, 2, device=device)
        noise = 0.1 * torch.randn(n, 1, device=device)
        y = 2.0 * x[:, :1] - 1.3 * x[:, 1:] + noise

        model = torch.nn.Sequential(
            torch.nn.Linear(2, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 1),
        ).to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
        loss_fn = torch.nn.MSELoss()

        start = time.perf_counter()
        for _ in range(epochs):
            optimizer.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            optimizer.step()
        duration_ms = (time.perf_counter() - start) * 1000.0

        final_loss = float(loss.detach().cpu().item())
        used_device = device

    except Exception as exc:
        # Fallback path keeps script operable even without torch/cuda package.
        used_device = "cpu-fallback"
        n = {"simple": 128, "intermediate": 256, "advanced": 512}[complexity]
        epochs = {"simple": 40, "intermediate": 60, "advanced": 90}[complexity]

        x = np.random.randn(n, 2)
        y = (2.0 * x[:, 0] - 1.3 * x[:, 1]).reshape(-1, 1)

        w = np.zeros((2, 1))
        b = 0.0
        lr = 0.05

        start = time.perf_counter()
        for _ in range(epochs):
            pred = x @ w + b
            err = pred - y
            grad_w = (2.0 / n) * (x.T @ err)
            grad_b = float((2.0 / n) * np.sum(err))
            w -= lr * grad_w
            b -= lr * grad_b
        duration_ms = (time.perf_counter() - start) * 1000.0
        final_loss = float(np.mean((x @ w + b - y) ** 2))
        print(f"[WARN] Torch/CUDA path unavailable, used fallback. Detail: {exc}")

    rows = [
        {
            "topic_id": topic_id,
            "device": used_device,
            "complexity": complexity,
            "final_loss": round(final_loss, 6),
            "duration_ms": round(duration_ms, 2),
        }
    ]

    metrics_path = RESULTS_DIR / f"{topic_id}_metrics.csv"
    write_rows_csv(metrics_path, rows)

    print(f"[INFO] Wrote: {metrics_path}")
    print("[INFO] Interpretation:")
    print("- Lower final_loss indicates the loop learned the synthetic mapping.")
    print("- Device field confirms whether CUDA or fallback path was used.")


def check_qdrant_local(timeout_sec: float = 1.0) -> Tuple[bool, str]:
    """Check whether local Qdrant endpoint is reachable for optional lab path."""
    url = "http://localhost:6333/collections"
    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
            status = getattr(resp, "status", 200)
            if status == 200:
                return True, "Qdrant reachable on localhost:6333"
            return False, f"Qdrant HTTP status {status}"
    except urllib.error.URLError as exc:
        return False, f"Qdrant unavailable: {exc}"
    except Exception as exc:
        return False, f"Qdrant check failed: {exc}"


def metric_delta(before: float, after: float) -> float:
    """Compute rounded delta helper used in reports."""
    return round(after - before, 4)


def build_metrics_comparison_rows(
    baseline_metrics: Dict[str, float], tuned_metrics: Dict[str, float],
    baseline_name: str = "baseline", tuned_name: str = "tuned"
) -> List[Dict[str, Any]]:
    """Create long-format metric rows for CSV comparison outputs."""
    rows: List[Dict[str, Any]] = []
    for metric_name in sorted(baseline_metrics.keys()):
        b = baseline_metrics[metric_name]
        t = tuned_metrics[metric_name]
        rows.append(
            {
                "metric": metric_name,
                f"{baseline_name}_value": b,
                f"{tuned_name}_value": t,
                "delta": metric_delta(b, t),
            }
        )
    return rows
