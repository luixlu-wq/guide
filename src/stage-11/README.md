# Stage 11 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 11 (AI infrastructure).

---

## 1) Setup

Run inside `red-book/src/stage-11`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional richer setup:

```powershell
pip install -r requirements-optional.txt
```

---

## 2) Run Modes

Fail-fast:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage11.ps1
```

Ladder:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage11.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage11.ps1 -IncludeLabs
```

---

## 3) Required Lab Outputs

Lab 1:

- `results/lab1_serving_latency_compare.csv`
- `results/lab1_serving_throughput_compare.csv`
- `results/lab1_serving_tradeoffs.md`

Lab 2:

- `results/lab2_gpu_profile_baseline.csv`
- `results/lab2_gpu_profile_improved.csv`
- `results/lab2_gpu_tuning_report.md`

Lab 3:

- `results/lab3_vector_scale_metrics.csv`
- `results/lab3_retrieval_quality.csv`
- `results/lab3_vector_ops_findings.md`

Lab 4:

- `results/lab4_incident_baseline.csv`
- `results/lab4_solution_options.csv`
- `results/lab4_verification_rerun.csv`
- `results/lab4_release_decision.md`

Expert-tier Stage 11 hard-gate outputs:

- `results/throughput_vs_latency_batch_profile.csv`
- `results/fp4_throughput_quality_tradeoff.csv`
- `results/hardware_saturation_profile.jsonl`
- `results/wsl_io_before_after.csv`
- `results/vector_recall_vs_latency_matrix.csv`
- `results/qdrant_persistence_recovery.md`
- `results/circuit_breaker_events.jsonl`
- `results/sse_ttft_metrics.csv`
- `results/sse_disconnect_recovery.md`
- `results/otel_trace_path_validation.md`
- `results/wsl_network_trace_check.md`
- `results/incident_postmortem_infra.md`
- `results/local_stack_boot_report.md`
- `results/service_health_snapshot.json`
- `results/release_readiness.json`

---

## 4) One-Command Verification

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage11_outputs.ps1
```


---

## 5) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-11.md`
- `red-book/AI-study-handbook-11.md`

No existing file names are removed. Existing outputs remain valid.

### 5.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage11/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 5.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage11.ps1 -Lab lab01_serving_benchmark`
- `pwsh .\run_all_stage11.ps1 -Lab lab02_gpu_utilization_tuning`
- `pwsh .\run_all_stage11.ps1 -Lab lab03_vector_db_scale_diagnostics`
- `pwsh .\run_all_stage11.ps1 -Lab lab04_infra_incident_recovery`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 5.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- `p95 latency improvement >= 20%`
- `gpu_utilization >= 70%` at target load with no SLO violation
- retrieval p95 and recall thresholds pass at scale
- incident drill completed with timeline and prevention actions
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 5.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- Ray Serve / vLLM / Ollama docs
- PyTorch CUDA notes (+ profiler references)
- Qdrant docs
- OpenTelemetry/Prometheus/Grafana
- Kubernetes HPA docs
