# Stage 10 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 10 (final AI system integration).

---

## 1) Setup

Run inside `red-book/src/stage-10`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional richer environment:

```powershell
pip install -r requirements-optional.txt
```

---

## 2) Run Modes

Fail-fast:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10.ps1
```

Ladder (`simple -> intermediate -> advanced`):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage10.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage10.ps1 -IncludeLabs
```

---

## 3) Lab Deliverables

Lab 1:

- `results/lab1_layer_metrics.csv`
- `results/lab1_baseline_outputs.jsonl`
- `results/lab1_system_metrics.csv`

Lab 2:

- `results/lab2_contract_checks.csv`
- `results/lab2_contract_failures.md`
- `results/lab2_failure_cases.csv`
- `results/lab2_contract_fix_report.md`

Lab 3:

- `results/lab3_incident_baseline.csv`
- `results/lab3_solution_options.csv`
- `results/lab3_verification_rerun.csv`
- `results/lab3_verification_notes.md`
- `results/lab3_decision.md`

Lab 4:

- `results/lab4_baseline_outputs.jsonl`
- `results/lab4_improved_outputs.jsonl`
- `results/lab4_layer_metrics.csv`
- `results/lab4_solution_options.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_verification_report.md`
- `results/lab4_production_readiness.md`

Lab 5:

- `results/trace_sample_analysis.jsonl`
- `results/otel_trace_contract_report.md`

Lab 6:

- `results/throughput_vllm_vs_trt.csv`
- `results/hardware_saturation_log.jsonl`
- `results/hardware_quantization_report.md`

Lab 7:

- `results/production_eval_store.jsonl`
- `results/hallucination_drift_log.jsonl`
- `results/judge_alignment_report.md`

Lab 8:

- `results/circuit_breaker_incident_log.jsonl`
- `results/incident_postmortem_drill.md`

Lab 9:

- `results/drift_telemetry_report.csv`
- `results/vector_drift_analysis.md`

Lab 10:

- `results/canary_eval_windows.csv`
- `results/rollback_drill.md`
- `results/release_decision.md`
- `results/canary_eval_report.md`

---

## 4) One-Command Verification

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage10_outputs.ps1
```


---

## 5) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-10.md`
- `red-book/AI-study-handbook-10.md`

No existing file names are removed. Existing outputs remain valid.

### 5.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage10/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 5.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage10.ps1 -Lab lab01_end_to_end_baseline`
- `pwsh .\run_all_stage10.ps1 -Lab lab02_pipeline_contract_validation`
- `pwsh .\run_all_stage10.ps1 -Lab lab03_incident_diagnosis_and_fix`
- `pwsh .\run_all_stage10.ps1 -Lab lab04_baseline_to_production_integration`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 5.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- `contract_pass_rate >= 99%`
- `quality_regression <= 2%` vs baseline
- `p95_latency <= 2.5s` under declared load profile
- rollback drill completed
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 5.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- FastAPI/Pydantic
- Great Expectations
- scikit-learn
- Qdrant
- OpenTelemetry/Prometheus/Grafana
- PyTorch CUDA notes
