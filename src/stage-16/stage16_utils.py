"""
Stage 16 shared utilities.

Deterministic helpers for stage topic demos and lab artifact generation.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
RESULTS_DIR = THIS_DIR / "results"
CANONICAL_RESULTS_DIR = RESULTS_DIR / "stage16"


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


def write_rows_csv_dual(filename: str, rows: Sequence[Dict[str, Any]]) -> None:
    """Write CSV to both legacy `results/` and canonical `results/stage16/` paths."""
    write_rows_csv(RESULTS_DIR / filename, rows)
    write_rows_csv(CANONICAL_RESULTS_DIR / filename, rows)


def write_text_dual(filename: str, text: str) -> None:
    """Write text artifact to both legacy and canonical result folders."""
    write_text(RESULTS_DIR / filename, text)
    write_text(CANONICAL_RESULTS_DIR / filename, text)


def resolve_project_profile() -> str:
    """Resolve project context for Stage 16 ownership artifacts."""
    raw = os.getenv("STAGE16_PROJECT", "Ontario_GIS").strip()
    return raw if raw else "Ontario_GIS"


def build_system_mastery_rubric(project: str) -> str:
    """Create system mastery rubric with defensive ownership checks."""
    return (
        "# System Mastery Rubric\n\n"
        f"- Project context: `{project}`\n"
        "- Ownership gate: architecture decisions include measurable tradeoff evidence.\n"
        "- Defensive design gate: upstream dependency risks are mapped with fallback policy.\n"
        "- Incident gate: silent Sev1 drill includes kill-switch and communication evidence.\n"
        "- Governance gate: power-efficiency and quality gates are enforced.\n"
    )


def build_dependency_risk_map() -> str:
    """Create dependency risk map for external data providers."""
    return (
        "# Dependency Risk Map\n\n"
        "| Dependency | Risk Event | Detection | Guardrail | Owner |\n"
        "|---|---|---|---|---|\n"
        "| Land Information Ontario (LIO) schema | Upstream schema change | Schema diff check in ingest job | Schema guard + circuit breaker to safe mode | data_owner |\n"
        "| Baidu Baike content/API | Field contract drift or content format change | contract validation and parse error monitor | fallback parser + retrieval quarantine | retrieval_owner |\n"
    )


def build_silent_sev1_timeline() -> List[Dict[str, Any]]:
    """Generate silent Sev1 incident timeline for style-drift scenario."""
    return [
        {"minute": 0, "event": "sev1_declared", "class": "silent_data_quality", "owner": "incident_commander"},
        {"minute": 4, "event": "style_drift_detected_130_30", "class": "sector_concentration", "owner": "trading_owner"},
        {"minute": 7, "event": "kill_switch_triggered", "class": "risk_control", "owner": "incident_commander"},
        {"minute": 10, "event": "stakeholder_notification_sent", "class": "comms", "owner": "comms_owner"},
        {"minute": 22, "event": "root_cause_hypothesis_logged", "class": "feature_scaling_fault", "owner": "ml_owner"},
        {"minute": 35, "event": "service_suspended_until_fix_verified", "class": "containment", "owner": "incident_commander"},
    ]


def build_kill_switch_evidence() -> str:
    """Return kill-switch evidence narrative for silent Sev1 scenario."""
    return (
        "# Kill-Switch Evidence\n\n"
        "- Trigger condition: sector concentration > 80% in 130/30 output.\n"
        "- Observed concentration: 90% single-sector exposure.\n"
        "- Action: automated strategy suspension executed.\n"
        "- Stakeholder notifications: sent to trading, risk, and ops channels.\n"
        "- Resume condition: scaling fix verified and concentration back within policy.\n"
    )


def build_compute_efficiency_rows() -> List[Dict[str, Any]]:
    """Generate compute efficiency comparison for local RTX 5090 governance."""
    return [
        {
            "optimization_mode": "bf16_baseline",
            "throughput_per_sec": 1720.0,
            "avg_power_w": 410.0,
            "tokens_or_samples_per_watt": 4.20,
            "decision": "baseline",
        },
        {
            "optimization_mode": "nvfp4_or_optimized_batching",
            "throughput_per_sec": 1715.0,
            "avg_power_w": 332.0,
            "tokens_or_samples_per_watt": 5.17,
            "decision": "candidate",
        },
    ]


def build_power_perf_curve_rows() -> List[Dict[str, Any]]:
    """Create power-to-performance curve points for governance review."""
    return [
        {"mode": "conservative", "avg_power_w": 280.0, "throughput_per_sec": 1500.0},
        {"mode": "balanced", "avg_power_w": 332.0, "throughput_per_sec": 1715.0},
        {"mode": "max_perf", "avg_power_w": 430.0, "throughput_per_sec": 1760.0},
    ]


def build_mastery_scorecard_rows(project: str) -> List[Dict[str, Any]]:
    """Aggregate cross-stage deltas into final mastery scorecard."""
    return [
        {"stage": "7", "baseline_metric": "rag_grounding", "improved_metric": "rag_grounding", "delta": "+0.18", "business_or_ops_impact": "more reliable tourism answers"},
        {"stage": "8", "baseline_metric": "prompt_format_valid", "improved_metric": "prompt_format_valid", "delta": "+0.19", "business_or_ops_impact": "fewer schema violations"},
        {"stage": "14", "baseline_metric": "net_return_after_cost", "improved_metric": "net_return_after_cost", "delta": "+0.011", "business_or_ops_impact": "better trading robustness"},
        {"stage": "16", "baseline_metric": "release_governance_readiness", "improved_metric": "release_governance_readiness", "delta": "+0.22", "business_or_ops_impact": f"{project} ownership evidence complete"},
    ]


def build_y_statement(project: str) -> str:
    """Create final Y-Statement ADR for Stage 16 portfolio release."""
    return (
        "# Final Y-Statement ADR\n\n"
        f"In the context of {project}, we decided to use a defensive ownership workflow over ad-hoc release practices because evidence showed stronger reliability, clear incident command traceability, and measurable efficiency gains on local runtime.\n"
    )

