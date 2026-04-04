# Stage 16 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 16 (mastery and industry readiness).

## Setup and Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# fail-fast path (intermediate topics + lab01)
powershell -ExecutionPolicy Bypass -File .\run_all_stage16.ps1

# run one specific lab
powershell -ExecutionPolicy Bypass -File .\run_all_stage16.ps1 -Lab lab02_incident_command_drill
powershell -ExecutionPolicy Bypass -File .\run_all_stage16.ps1 -Lab lab03_quality_governance_audit
powershell -ExecutionPolicy Bypass -File .\run_all_stage16.ps1 -Lab lab04_industry_project_portfolio_pack

# full ladder
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage16.ps1 -IncludeLabs

# output verification
powershell -ExecutionPolicy Bypass -File .\verify_stage16_outputs.ps1
```

## Optional Environment Inputs

```powershell
# project profile used in chapter-16 ownership artifacts
$env:STAGE16_PROJECT = "Ontario_GIS"  # or MapToGo or LSTM_Trading
```

## 2) Plan Alignment Addendum (2026-04-04)

This README aligns with:
- `red-book/plan/plan-16.md`
- `red-book/AI-study-handbook-16.md`

No existing file names are removed. Existing outputs remain valid.

### 2.1 Canonical Output Compatibility

Canonical output root: `results/stage16/`.

Current scripts also write legacy artifacts to `results/` for backward compatibility.

Reference mapping:
- `artifact_name_map.md`

### 2.2 Required Expert Artifacts

Legacy compatibility artifacts in `results/`:
- `lab1_architecture_options.csv`
- `lab1_tradeoff_matrix.csv`
- `lab1_decision_record.md`
- `lab2_incident_timeline.csv`
- `lab2_actions_and_owners.csv`
- `lab2_postmortem.md`
- `lab3_audit_checklist.csv`
- `lab3_risk_register.csv`
- `lab3_audit_recommendation.md`
- `lab4_portfolio_index.md`
- `lab4_case_study_summary.md`
- `lab4_capability_matrix.csv`

Canonical chapter-16 ownership artifacts in `results/stage16/`:
- `system_mastery_rubric.md`
- `dependency_risk_map.md`
- `lab02_silent_sev1_timeline.csv`
- `lab02_kill_switch_evidence.md`
- `compute_efficiency_report.csv`
- `power_perf_curve.csv`
- `mastery_scorecard.csv`
- `lab04_portfolio_evidence_pack.md`
- `lab04_final_y_statement.md`

### 2.3 Hard Gates (Mastery Approval)

Stage 16 completion is approved only when all pass:
- ownership rubric and dependency risk map are complete and evidence-backed
- silent Sev1 timeline and kill-switch evidence are present
- compute-efficiency and power-performance evidence are present
- portfolio pack includes cumulative delta scorecard
- final release decision is signed via Y-Statement

If any gate fails: mastery completion is not approved.

### 2.4 Resource Citation Rule

Each module/lab report should cite at least one relevant source from:
- ADR references
- SRE references
- OWASP LLM Top 10
- OpenTelemetry
- Qdrant
- PyTorch CUDA notes
