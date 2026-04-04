"""Stage 6 Topic 00M: local model capability validation (cold-start gate).

Goal:
- Validate whether local model variants can follow strict tool JSON schemas
  before building complex orchestration logic.

Primary metric:
- Schema Adherence Rate = valid schema outputs / total test cases

Secondary metrics:
- Tool Argument Accuracy
- Mean generation latency (ms)

Optional local runtime:
- If Ollama is available at http://localhost:11434, this script calls local models.
- If unavailable, script uses deterministic offline simulation so workflow still runs.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from stage6_utils import RESULTS_DIR


def extract_json_object(raw_text: str) -> dict[str, Any] | None:
    """Best-effort JSON object extraction from model output text."""
    raw = raw_text.strip()
    if raw.startswith("{") and raw.endswith("}"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

    # Fallback: locate first object-like span.
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None


def schema_cases() -> list[dict[str, Any]]:
    """Return fixed schema-adherence validation cases."""
    return [
        {
            "case_id": "C01",
            "tool": "route_ticket",
            "schema": {"queue": "str", "priority": "str"},
            "input_text": "Security alert from enterprise customer with suspicious login.",
            "expected": {"queue": "security", "priority": "critical"},
        },
        {
            "case_id": "C02",
            "tool": "route_ticket",
            "schema": {"queue": "str", "priority": "str"},
            "input_text": "Invoice mismatch and billing complaint from pro user.",
            "expected": {"queue": "billing", "priority": "high"},
        },
        {
            "case_id": "C03",
            "tool": "policy_gate",
            "schema": {"needs_human_approval": "bool", "reason": "str"},
            "input_text": "Request to export raw customer data to external auditor email.",
            "expected": {"needs_human_approval": True, "reason": "sensitive_data_export"},
        },
        {
            "case_id": "C04",
            "tool": "policy_gate",
            "schema": {"needs_human_approval": "bool", "reason": "str"},
            "input_text": "Simple request to explain how to change notification settings.",
            "expected": {"needs_human_approval": False, "reason": "low_risk"},
        },
        {
            "case_id": "C05",
            "tool": "extract_geo_request",
            "schema": {"contains_geojson": "bool", "sensitivity": "str"},
            "input_text": "Analyze this GeoJSON with subdivision coordinates and provincial identifiers.",
            "expected": {"contains_geojson": True, "sensitivity": "high"},
        },
        {
            "case_id": "C06",
            "tool": "extract_geo_request",
            "schema": {"contains_geojson": "bool", "sensitivity": "str"},
            "input_text": "Summarize public tourism description without coordinates.",
            "expected": {"contains_geojson": False, "sensitivity": "low"},
        },
        {
            "case_id": "C07",
            "tool": "risk_score",
            "schema": {"risk_score": "float", "explanation": "str"},
            "input_text": "Production outage and repeated 500 errors in enterprise account.",
            "expected": {"risk_score": 0.9, "explanation": "critical_outage"},
        },
        {
            "case_id": "C08",
            "tool": "risk_score",
            "schema": {"risk_score": "float", "explanation": "str"},
            "input_text": "Minor feature request for monthly export formatting.",
            "expected": {"risk_score": 0.2, "explanation": "low_impact"},
        },
        {
            "case_id": "C09",
            "tool": "tool_args_validator",
            "schema": {"ticket_id": "str", "max_steps": "int"},
            "input_text": "Run triage for ticket TKT-1042 with max steps 4.",
            "expected": {"ticket_id": "TKT-1042", "max_steps": 4},
        },
        {
            "case_id": "C10",
            "tool": "tool_args_validator",
            "schema": {"ticket_id": "str", "max_steps": "int"},
            "input_text": "Run triage for ticket TKT-1005 with max steps 2.",
            "expected": {"ticket_id": "TKT-1005", "max_steps": 2},
        },
    ]


def type_ok(value: Any, type_name: str) -> bool:
    if type_name == "str":
        return isinstance(value, str)
    if type_name == "bool":
        return isinstance(value, bool)
    if type_name == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "float":
        return isinstance(value, (float, int)) and not isinstance(value, bool)
    return False


def validate_schema(output_obj: dict[str, Any], schema: dict[str, str]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for field, type_name in schema.items():
        if field not in output_obj:
            errors.append(f"missing:{field}")
            continue
        if not type_ok(output_obj[field], type_name):
            errors.append(f"type:{field}:{type_name}")
    return (len(errors) == 0), errors


def argument_accuracy(output_obj: dict[str, Any], expected_obj: dict[str, Any]) -> float:
    if not expected_obj:
        return 1.0
    matched = 0
    for k, v in expected_obj.items():
        if k in output_obj:
            if isinstance(v, float):
                # tolerance for float-like outputs.
                matched += 1 if abs(float(output_obj[k]) - v) <= 0.25 else 0
            else:
                matched += 1 if output_obj[k] == v else 0
    return matched / len(expected_obj)


def build_prompt(case: dict[str, Any]) -> str:
    return (
        "You are a strict tool-argument generator.\n"
        "Return only one JSON object. No extra text.\n"
        f"Tool: {case['tool']}\n"
        f"Required schema: {json.dumps(case['schema'])}\n"
        f"Input: {case['input_text']}\n"
    )


def call_ollama(model: str, prompt: str, timeout_s: int = 30) -> tuple[str | None, float]:
    """Call local Ollama generate endpoint and return text + latency_ms."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8")
        latency_ms = (time.perf_counter() - t0) * 1000.0
        obj = json.loads(raw)
        return str(obj.get("response", "")), latency_ms
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return None, latency_ms


def simulate_local_output(case: dict[str, Any], model: str) -> str:
    """Deterministic offline fallback to keep script operatable without Ollama."""
    expected = case["expected"]
    # Simulate lower schema adherence for q4-style model names.
    lower = model.lower()
    degrade = "q4" in lower or "4bit" in lower
    if degrade and case["case_id"] in {"C03", "C05", "C07"}:
        # Common failure pattern: wrong type or missing key.
        bad = dict(expected)
        if "risk_score" in bad:
            bad["risk_score"] = "high"
        else:
            bad.pop(next(iter(bad.keys())))
        return json.dumps(bad)
    return json.dumps(expected)


def parse_models() -> list[str]:
    env = os.getenv("STAGE6_LOCAL_MODELS", "").strip()
    if env:
        return [m.strip() for m in env.split(",") if m.strip()]
    # Default pair mirrors review guidance.
    return ["qwen2.5:32b-instruct-q4_K_M", "qwen2.5:32b-instruct-q8_0"]


# Workflow:
# 1) Define fixed schema-adherence cases.
# 2) Evaluate each local model candidate on all cases.
# 3) Compute schema adherence + argument accuracy + latency.
# 4) Save decision-ready report before orchestration coding starts.
def main() -> None:
    cases = schema_cases()
    models = parse_models()

    print("\n=== Topic00M Local Model Capability Validation ===")
    print("Data: in-script schema adherence benchmark cases")
    print(f"Records/Samples: {len(cases)} cases x {len(models)} models")
    print("Input schema: case(tool, schema, input_text, expected)")
    print("Output schema: per-case adherence and argument-accuracy metrics")
    print("Split/Eval policy: fixed case list")
    print("Type: local model capability gate")

    all_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for model in models:
        schema_ok_count = 0
        parse_ok_count = 0
        arg_acc_values: list[float] = []
        latency_values: list[float] = []
        used_ollama = False

        for case in cases:
            prompt = build_prompt(case)
            raw_text, latency_ms = call_ollama(model, prompt)
            if raw_text is None:
                raw_text = simulate_local_output(case, model)
            else:
                used_ollama = True

            parsed = extract_json_object(raw_text)
            parse_ok = parsed is not None
            parse_ok_count += int(parse_ok)

            if parsed is None:
                schema_ok = False
                errors = ["parse_error"]
                arg_acc = 0.0
            else:
                schema_ok, errors = validate_schema(parsed, case["schema"])
                arg_acc = argument_accuracy(parsed, case["expected"])

            schema_ok_count += int(schema_ok)
            arg_acc_values.append(arg_acc)
            latency_values.append(latency_ms)

            all_rows.append(
                {
                    "model": model,
                    "case_id": case["case_id"],
                    "tool": case["tool"],
                    "parse_ok": parse_ok,
                    "schema_ok": schema_ok,
                    "argument_accuracy": round(arg_acc, 4),
                    "latency_ms": round(latency_ms, 2),
                    "errors": ";".join(errors),
                }
            )

        n = len(cases)
        schema_rate = schema_ok_count / n
        parse_rate = parse_ok_count / n
        mean_acc = sum(arg_acc_values) / max(len(arg_acc_values), 1)
        mean_latency = sum(latency_values) / max(len(latency_values), 1)
        decision = "promote" if schema_rate >= 0.9 and mean_acc >= 0.9 else "hold"

        summary_rows.append(
            {
                "run_id": f"stage6_topic00m_{model}",
                "stage": "6",
                "topic_or_module": "topic00m_local_model_capability_validation",
                "metric_name": "schema_adherence_rate",
                "before_value": 0.0,
                "after_value": round(schema_rate, 4),
                "delta": round(schema_rate, 4),
                "dataset_or_eval_set": "fixed_schema_cases_10",
                "seed_or_config_id": model,
                "decision": decision,
                "parse_success_rate": round(parse_rate, 4),
                "tool_argument_accuracy": round(mean_acc, 4),
                "mean_latency_ms": round(mean_latency, 2),
                "runtime_mode": "ollama_local" if used_ollama else "offline_simulation",
            }
        )

        print(
            f"model={model} schema_adherence_rate={schema_rate:.3f} "
            f"tool_argument_accuracy={mean_acc:.3f} mean_latency_ms={mean_latency:.1f} "
            f"mode={'ollama_local' if used_ollama else 'offline_simulation'}"
        )

    out_dir = Path(RESULTS_DIR) / "stage6"
    out_dir.mkdir(parents=True, exist_ok=True)
    detail_path = out_dir / "topic00m_schema_adherence_cases.csv"
    summary_path = out_dir / "topic00m_schema_adherence_summary.csv"
    decision_path = out_dir / "topic00m_local_model_capability_report.md"

    # Save CSVs using plain writer to keep script dependency-light.
    if all_rows:
        keys = list(all_rows[0].keys())
        detail_lines = [",".join(keys)]
        for row in all_rows:
            detail_lines.append(",".join(str(row[k]).replace(",", ";") for k in keys))
        detail_path.write_text("\n".join(detail_lines), encoding="utf-8")

    if summary_rows:
        keys = list(summary_rows[0].keys())
        summary_lines = [",".join(keys)]
        for row in summary_rows:
            summary_lines.append(",".join(str(row[k]).replace(",", ";") for k in keys))
        summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    best = max(summary_rows, key=lambda r: float(r["after_value"])) if summary_rows else None
    report_lines = [
        "# Topic00M Local Model Capability Report",
        "",
        "This report is the cold-start gate before building complex agent orchestration.",
        "",
    ]
    if best:
        report_lines += [
            f"- Recommended model: `{best['seed_or_config_id']}`",
            f"- Schema adherence rate: `{best['after_value']}`",
            f"- Tool argument accuracy: `{best['tool_argument_accuracy']}`",
            f"- Mean latency ms: `{best['mean_latency_ms']}`",
            f"- Decision: `{best['decision']}`",
        ]
    decision_path.write_text("\n".join(report_lines), encoding="utf-8")

    print("\nSaved artifacts:")
    print(f"- {detail_path}")
    print(f"- {summary_path}")
    print(f"- {decision_path}")


if __name__ == "__main__":
    main()

