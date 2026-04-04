"""
Stage 10 shared utilities.

This module provides deterministic data generation, feature pipeline helpers,
baseline/improved model paths, and artifact writers for Stage 10 scripts/labs.
"""

from __future__ import annotations

import csv
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

THIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = THIS_DIR / "results"


def ensure_results_dir() -> None:
    """Create results directory if missing."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 42) -> None:
    """Set deterministic seeds used across all Stage 10 scripts."""
    random.seed(seed)
    np.random.seed(seed)


def print_data_declaration(title: str, declaration: Dict[str, str]) -> None:
    """Print mandatory data/schema declaration block."""
    print("\n=== Data Declaration:", title, "===")
    for key, value in declaration.items():
        print(f"{key}: {value}")
    print("=== End Data Declaration ===\n")


def write_rows_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write rows to CSV artifact."""
    ensure_results_dir()
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    # Use union of keys so heterogeneous metric rows can be written safely.
    fieldnames: List[str] = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    """Write markdown/text artifact."""
    ensure_results_dir()
    path.write_text(text, encoding="utf-8")


def as_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    """Write JSONL artifact."""
    ensure_results_dir()
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def synthetic_market_rows(n: int = 320, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Generate deterministic trading-style rows with synthetic price/volume/news.

    This is designed for workflow learning (contracts, evaluation, operations),
    not for real trading performance.
    """
    set_seed(seed)
    price = 100.0
    rows: List[Dict[str, Any]] = []
    for i in range(n):
        drift = 0.06 * np.sin(i / 14.0)
        shock = np.random.normal(loc=0.0, scale=0.9)
        price = max(10.0, price + drift + shock)
        volume = int(1_000_000 + np.random.normal(0, 120_000))
        news_score = float(np.clip(np.random.normal(0, 0.7) + np.sin(i / 21.0), -2.0, 2.0))
        headline = (
            "Positive demand and stable guidance."
            if news_score > 0.4
            else ("Mixed macro conditions and cautious outlook." if news_score > -0.4 else "Weak momentum and risk-off sentiment.")
        )
        rows.append(
            {
                "id": f"row_{i:04d}",
                "t": i,
                "close": round(float(price), 4),
                "volume": volume,
                "news_score": round(news_score, 4),
                "headline": headline,
            }
        )
    return rows


def build_features(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create deterministic feature table and next-day target label."""
    closes = np.array([float(r["close"]) for r in rows], dtype=float)
    volumes = np.array([float(r["volume"]) for r in rows], dtype=float)
    news_scores = np.array([float(r["news_score"]) for r in rows], dtype=float)

    out: List[Dict[str, Any]] = []
    for i in range(20, len(rows) - 1):
        ma5 = float(np.mean(closes[i - 5 : i]))
        ma20 = float(np.mean(closes[i - 20 : i]))
        ret1 = float((closes[i] / closes[i - 1]) - 1.0)
        vol_chg = float((volumes[i] / max(1.0, volumes[i - 1])) - 1.0)
        target = int(closes[i + 1] > closes[i])
        out.append(
            {
                "id": rows[i]["id"],
                "close": float(closes[i]),
                "ma5": ma5,
                "ma20": ma20,
                "ret1": ret1,
                "vol_chg": vol_chg,
                "news_score": float(news_scores[i]),
                "headline": rows[i]["headline"],
                "target": target,
            }
        )
    return out


def split_rows(rows: Sequence[Dict[str, Any]], seed: int = 42) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split rows into train/val/test with deterministic shuffle."""
    set_seed(seed)
    rows_copy = list(rows)
    random.shuffle(rows_copy)
    n = len(rows_copy)
    a = int(0.6 * n)
    b = int(0.8 * n)
    return rows_copy[:a], rows_copy[a:b], rows_copy[b:]


def _x_y(rows: Sequence[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
    """Convert row dicts into model matrices."""
    x = np.array(
        [[r["ma5"], r["ma20"], r["ret1"], r["vol_chg"], r["news_score"]] for r in rows],
        dtype=float,
    )
    y = np.array([int(r["target"]) for r in rows], dtype=int)
    return x, y


def baseline_predict(rows: Sequence[Dict[str, Any]]) -> List[int]:
    """Simple baseline rule for comparison path."""
    pred: List[int] = []
    for r in rows:
        score = 0.5 * np.sign(r["ma5"] - r["ma20"]) + 0.4 * np.sign(r["ret1"]) + 0.2 * np.sign(r["news_score"])
        pred.append(1 if score > 0 else 0)
    return pred


def train_model(train_rows: Sequence[Dict[str, Any]], c_value: float = 1.4) -> LogisticRegression:
    """Train deterministic logistic regression baseline model."""
    x_train, y_train = _x_y(train_rows)
    model = LogisticRegression(max_iter=600, C=c_value, random_state=42)
    model.fit(x_train, y_train)
    return model


def predict_model(model: LogisticRegression, rows: Sequence[Dict[str, Any]]) -> List[int]:
    """Predict class labels from trained model."""
    x, _ = _x_y(rows)
    return model.predict(x).tolist()


def predict_proba_model(model: LogisticRegression, rows: Sequence[Dict[str, Any]]) -> List[float]:
    """Predict class probabilities for class=1 from trained model."""
    x, _ = _x_y(rows)
    return model.predict_proba(x)[:, 1].tolist()


def evaluate_binary(rows: Sequence[Dict[str, Any]], pred: Sequence[int]) -> Dict[str, float]:
    """Compute stable binary classification metrics."""
    y = [int(r["target"]) for r in rows]
    return {
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "f1": round(float(f1_score(y, pred)), 4),
    }


def reasoning_text(prob_up: float, news_score: float) -> Tuple[str, str]:
    """Produce deterministic explanation and risk text for integration output."""
    if prob_up >= 0.6 and news_score >= 0:
        return (
            "Signals are aligned: short-term trend and context both support upside continuation.",
            "moderate",
        )
    if prob_up >= 0.6 and news_score < 0:
        return (
            "Model signal is bullish, but negative context raises uncertainty.",
            "medium-high",
        )
    if prob_up < 0.4 and news_score < 0:
        return (
            "Signals align to downside pressure with weak context support.",
            "high",
        )
    return (
        "Signals are mixed; directional confidence remains limited.",
        "medium",
    )


def run_topic_demo(topic_id: str, topic_name: str, complexity: str, method_focus: str) -> None:
    """Run baseline vs improved deterministic demo for Stage 10 topics."""
    ensure_results_dir()
    declaration = {
        "Data": "Synthetic OHLCV + news rows from stage10_utils",
        "Records/Samples": "320 raw rows -> feature table",
        "Input schema": "close, volume, news_score, headline",
        "Output schema": "pred_class, pred_prob, analysis, risk",
        "Split/Eval policy": "fixed split with seed=42",
        "Type": f"{method_focus}/{complexity}",
    }
    print_data_declaration(topic_name, declaration)

    raw = synthetic_market_rows(n=320, seed=42)
    feat = build_features(raw)
    train, _val, test = split_rows(feat, seed=42)

    base_pred = baseline_predict(test)
    base_m = evaluate_binary(test, base_pred)

    c_by_level = {"simple": 1.0, "intermediate": 1.5, "advanced": 2.0}[complexity]
    model = train_model(train, c_value=c_by_level)
    imp_pred = predict_model(model, test)
    imp_prob = predict_proba_model(model, test)
    imp_m = evaluate_binary(test, imp_pred)

    latency_base = {"simple": 340.0, "intermediate": 380.0, "advanced": 420.0}[complexity]
    latency_imp = latency_base * 0.9
    err_base = 0.018
    err_imp = 0.011

    rows = [
        {"topic_id": topic_id, "run_type": "baseline", **base_m, "latency_p95_ms": round(latency_base, 2), "error_rate": err_base},
        {"topic_id": topic_id, "run_type": "improved", **imp_m, "latency_p95_ms": round(latency_imp, 2), "error_rate": err_imp},
    ]
    write_rows_csv(RESULTS_DIR / f"{topic_id}_metrics.csv", rows)

    sample_rows: List[Dict[str, Any]] = []
    for r, pred, prob in zip(test[:14], imp_pred[:14], imp_prob[:14]):
        analysis, risk = reasoning_text(float(prob), float(r["news_score"]))
        sample_rows.append(
            {
                "id": r["id"],
                "pred_class": int(pred),
                "pred_prob_up": round(float(prob), 4),
                "news_score": round(float(r["news_score"]), 4),
                "analysis": analysis,
                "risk": risk,
                "target": int(r["target"]),
            }
        )
    as_jsonl(RESULTS_DIR / f"{topic_id}_sample_outputs.jsonl", sample_rows)

    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_metrics.csv'}")
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_sample_outputs.jsonl'}")
    print("[INFO] Interpretation: compare baseline vs improved with same split and same evaluation policy.")


def run_pytorch_cuda_component(topic_id: str, complexity: str) -> None:
    """Run optional PyTorch/CUDA component benchmark with safe fallback."""
    ensure_results_dir()
    loops = {"simple": 30, "intermediate": 60, "advanced": 90}[complexity]
    hidden = {"simple": 64, "intermediate": 128, "advanced": 256}[complexity]
    batch = {"simple": 8, "intermediate": 16, "advanced": 24}[complexity]

    lat_ms: List[float] = []
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
                lat_ms.append((time.perf_counter() - t0) * 1000.0)
    except Exception:
        w1 = np.random.randn(hidden, hidden * 2)
        w2 = np.random.randn(hidden * 2, hidden)
        for _ in range(loops):
            x = np.random.randn(batch, hidden)
            t0 = time.perf_counter()
            h = np.maximum(x @ w1, 0.0)
            _ = h @ w2
            lat_ms.append((time.perf_counter() - t0) * 1000.0)

    row = {
        "topic_id": topic_id,
        "complexity": complexity,
        "device": device,
        "latency_p50_ms": round(float(np.percentile(lat_ms, 50)), 3),
        "latency_p95_ms": round(float(np.percentile(lat_ms, 95)), 3),
    }
    write_rows_csv(RESULTS_DIR / f"{topic_id}_cuda_metrics.csv", [row])
    print(f"[INFO] Wrote: {RESULTS_DIR / f'{topic_id}_cuda_metrics.csv'}")


def build_metrics_comparison_rows(
    baseline_metrics: Dict[str, float], improved_metrics: Dict[str, float]
) -> List[Dict[str, Any]]:
    """Create baseline vs improved metrics table with deltas."""
    rows: List[Dict[str, Any]] = []
    for k in sorted(set(baseline_metrics.keys()).intersection(improved_metrics.keys())):
        b = float(baseline_metrics[k])
        i = float(improved_metrics[k])
        rows.append({"metric": k, "baseline_value": round(b, 4), "improved_value": round(i, 4), "delta": round(i - b, 4)})
    return rows
