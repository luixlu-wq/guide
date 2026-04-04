# Stage 12 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 12 (AI system architecture patterns).

---

## 1) Setup

Run inside `red-book/src/stage-12`:

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
powershell -ExecutionPolicy Bypass -File .\run_all_stage12.ps1
```

Ladder:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage12.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage12.ps1 -IncludeLabs
```

---

## 3) Required Lab Outputs

Lab 1:

- `results/lab1_pattern_metrics.csv`
- `results/lab1_tradeoff_matrix.csv`
- `results/lab1_pattern_summary.md`

Lab 2:

- `results/lab2_failure_cases.csv`
- `results/lab2_solution_options.csv`
- `results/lab2_verification_rerun.csv`

Lab 3:

- `results/lab3_decision_scores.csv`
- `results/lab3_adr.md`
- `results/adr_scorecard_with_thresholds.csv`
- `results/architecture_decision_y_statement.md`

Lab 4:

- `results/lab4_baseline_metrics.csv`
- `results/lab4_improved_metrics.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_release_decision.md`
- `results/lab4_rollback_plan.md`
- `results/release_gate_report.md`
- `results/rollback_simulation.md`

Lab 5:

- `results/agent_card_registry.json`
- `results/a2a_handoff_trace.jsonl`
- `results/mcp_tool_contracts.md`

Lab 6:

- `results/nvfp4_throughput_quality.csv`
- `results/prefix_cache_latency_profile.csv`
- `results/agent_loop_latency_report.md`

Lab 7:

- `results/indirect_injection_case_log.jsonl`
- `results/unbounded_consumption_guard.csv`
- `results/owasp_llm_v2_redteam_report.md`

Lab 8:

- `results/geojson_schema_guard_failures.csv`
- `results/loop_breaker_events.jsonl`
- `results/coordinate_projection_validation_report.md`
- `results/mobile_latency_guard_report.md`

---

## 4) One-Command Verification

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage12_outputs.ps1
```

---

## 5) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-12.md`
- `red-book/AI-study-handbook-12.md`

No existing file names are removed. Existing outputs remain valid.

### 5.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage12/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 5.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage12.ps1 -Lab lab01_pattern_baseline_compare`
- `pwsh .\run_all_stage12.ps1 -Lab lab02_rag_vs_agent_failure_drill`
- `pwsh .\run_all_stage12.ps1 -Lab lab03_architecture_decision_record`
- `pwsh .\run_all_stage12.ps1 -Lab lab04_pattern_to_production`
- `pwsh .\run_all_stage12.ps1 -Lab lab05_a2a_mcp_interoperability`
- `pwsh .\run_all_stage12.ps1 -Lab lab06_blackwell_nvfp4_prefix_caching`
- `pwsh .\run_all_stage12.ps1 -Lab lab07_owasp_llm_v2_redteam`
- `pwsh .\run_all_stage12.ps1 -Lab lab08_gis_projection_and_loop_breaker`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 5.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- final ADR includes weighted scoring and rollback trigger
- selected pattern beats baseline on primary metric
- safety/governance gates pass before release recommendation
- fixed evaluation protocol used for all pattern comparisons
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 5.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- ADR resources
- Qdrant
- LangGraph or LlamaIndex
- OWASP LLM Top 10
- PyTorch CUDA notes
- MLflow
