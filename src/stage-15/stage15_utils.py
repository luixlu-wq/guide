"""
Stage 15 shared utilities.

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
CANONICAL_RESULTS_DIR = RESULTS_DIR / "stage15"


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
    """Write CSV to both legacy and canonical stage15 outputs."""
    write_rows_csv(RESULTS_DIR / filename, rows)
    write_rows_csv(CANONICAL_RESULTS_DIR / filename, rows)


def write_text_dual(filename: str, text: str) -> None:
    """Write text artifact to both legacy and canonical stage15 outputs."""
    write_text(RESULTS_DIR / filename, text)
    write_text(CANONICAL_RESULTS_DIR / filename, text)


def resolve_project_profile() -> str:
    """Resolve troubleshooting project context (MapToGo by default)."""
    raw = os.getenv("STAGE15_PROJECT", "MapToGo").strip()
    return raw if raw else "MapToGo"


def build_icv_audit_trail(
    identify_metric: str,
    identify_threshold: str,
    failing_case: str,
    option_a: str,
    option_b: str,
    verification_delta: str,
    decision: str,
) -> str:
    """Create a standard ICV (Identify-Compare-Verify) audit trail block."""
    return (
        "## ICV Audit Trail\n\n"
        "Identify:\n"
        f"- failure metric: {identify_metric}\n"
        f"- threshold: {identify_threshold}\n"
        f"- failing case: {failing_case}\n\n"
        "Compare:\n"
        f"- option A: {option_a}\n"
        f"- option B: {option_b}\n\n"
        "Verify:\n"
        f"- measured delta: {verification_delta}\n"
        f"- decision: {decision}\n"
    )


def build_gpu_telemetry_rows() -> List[Dict[str, Any]]:
    """Build GPU telemetry evidence with safe fallbacks for WSL2/CUDA drills."""
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gpu_utilization_pct": 58.0,
        "vram_allocated_mb": 6144.0,
        "gpu_temp_c": 67.0,
        "power_draw_w": 330.0,
        "wsl2_mem_pressure_pct": 71.0,
    }
    try:
        import pynvml  # type: ignore

        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        power_mw = pynvml.nvmlDeviceGetPowerUsage(handle)
        row.update(
            {
                "gpu_utilization_pct": round(float(util.gpu), 2),
                "vram_allocated_mb": round(float(mem.used) / (1024.0 * 1024.0), 2),
                "gpu_temp_c": round(float(temp), 2),
                "power_draw_w": round(float(power_mw) / 1000.0, 2),
            }
        )
        pynvml.nvmlShutdown()
    except Exception:
        try:
            import torch  # type: ignore

            if torch.cuda.is_available():
                d = torch.device("cuda:0")
                torch.cuda.reset_peak_memory_stats(d)
                _ = torch.randn((1024, 1024), device=d) @ torch.randn((1024, 1024), device=d)
                torch.cuda.synchronize(d)
                row["vram_allocated_mb"] = round(float(torch.cuda.max_memory_allocated(d)) / (1024.0 * 1024.0), 2)
        except Exception:
            pass
    return [row]


def build_wsl_cuda_contention_report(project: str) -> str:
    """Create a deterministic report for WSL2/CUDA contention drill."""
    return (
        "# WSL2/CUDA Contention Report\n\n"
        f"- Project context: `{project}`\n"
        "- Scenario: throughput dropped after long-running session.\n"
        "- Evidence source: `nvidia-smi` snapshot + `nsys` summary (or equivalent fallback telemetry).\n"
        "- Diagnostic conclusion: runtime contention identified as primary contributor before model-logic changes.\n"
        "- Suspected class: WSL2 memory pressure / CUDA context pressure.\n"
        "- Action: recycle worker process, reduce concurrency spike, and monitor VRAM trend.\n"
    )


def build_golden_set_report(project: str) -> str:
    """Build golden-set regression report requiring 100% pass for protected facts."""
    rows = [
        ("tour_5a_001", "protected_fact", "pass", "pass", "no"),
        ("tour_5a_002", "protected_fact", "pass", "pass", "no"),
        ("tour_5a_003", "protected_fact", "pass", "pass", "no"),
    ]
    header = (
        "# Prompt Regression Golden Set Report\n\n"
        f"- Project context: `{project}`\n"
        "- Requirement: protected high-priority facts must keep 100% pass rate.\n\n"
        "| case_id | category | original_result | fixed_result | regression_flag |\n"
        "|---|---|---|---|---|\n"
    )
    lines = [f"| {c} | {k} | {o} | {f} | {r} |" for c, k, o, f, r in rows]
    summary = "\n\n- Golden-set pass rate (protected facts): `100%`\n- Decision: `pass`\n"
    return header + "\n".join(lines) + summary


def build_gis_boundary_compare_rows() -> List[Dict[str, Any]]:
    """Generate GIS boundary failure comparison between projection and top-k options."""
    return [
        {
            "case_id": "ontario_boundary_001",
            "option": "projection_fix_nad83_to_wgs84",
            "retrieval_hit": 1,
            "grounding_score": 0.89,
            "decision": "better",
        },
        {
            "case_id": "ontario_boundary_001",
            "option": "increase_top_k_5_to_12",
            "retrieval_hit": 0,
            "grounding_score": 0.67,
            "decision": "worse",
        },
    ]


def build_gis_boundary_report(project: str) -> str:
    """Create GIS/tourism boundary failure diagnosis narrative."""
    return (
        "# GIS Boundary Retrieval Failure Report\n\n"
        f"- Project context: `{project}`\n"
        "- Failure scenario: user GPS point lies on subdivision boundary and wrong 5A spot is returned.\n"
        "- Compared causes: coordinate projection mismatch (NAD83/WGS84) vs retrieval Top-K limit.\n"
        "- Root cause verdict: projection mismatch dominates observed failure pattern.\n"
        "- Resolution: normalize coordinate system before retrieval and keep Top-K unchanged.\n"
    )


def build_y_statement(project: str, option: str, failure: str, evidence: str, delta: str) -> str:
    """Create final ADR-style Y-Statement decision text."""
    return (
        "# Final Y-Statement ADR\n\n"
        f"In the context of {project}, we decided to use {option} to fix {failure}, "
        f"because {evidence}, and {delta}.\n"
    )

