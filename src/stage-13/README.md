# Stage 13 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 13 (capstone delivery).

## 1) Setup

Run inside `red-book/src/stage-13`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional richer setup:

```powershell
pip install -r requirements-optional.txt
```

## 2) Run Modes

Fail-fast:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage13.ps1
```

Ladder:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage13.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage13.ps1 -IncludeLabs
```

## 3) Required Lab Outputs

- `results/lab1_capstone_baseline_metrics.csv`
- `results/lab1_capstone_layer_outputs.jsonl`
- `results/lab1_capstone_contract_status.csv`
- `results/lab2_solution_options.csv`
- `results/lab2_before_after_delta.csv`
- `results/lab2_improvement_decision.md`
- `results/lab3_incident_timeline.csv`
- `results/lab3_root_cause_analysis.md`
- `results/lab3_verification_rerun.csv`
- `results/lab4_release_gate_checklist.csv`
- `results/lab4_release_decision.md`
- `results/lab4_rollback_plan.md`

## 4) One-Command Verification

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage13_outputs.ps1
```

---

## 5) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-13.md`
- `red-book/AI-study-handbook-13.md`

No existing file names are removed. Existing outputs remain valid.

### 5.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage13/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 5.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage13.ps1 -Lab lab01_capstone_baseline`
- `pwsh .\run_all_stage13.ps1 -Lab lab02_capstone_improvement_cycle`
- `pwsh .\run_all_stage13.ps1 -Lab lab03_capstone_incident_response`
- `pwsh .\run_all_stage13.ps1 -Lab lab04_capstone_production_readiness`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 5.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- milestone gates complete with required evidence
- one full improvement cycle with measurable delta
- one full incident drill with quality postmortem
- signed go/no-go with rollback proof
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 5.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- DORA/SRE references
- DVC and/or MLflow
- FastAPI
- Qdrant
- PyTorch CUDA notes
