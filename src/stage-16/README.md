# Stage 16 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 16 (mastery and industry readiness).

## Setup and Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage16.ps1
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage16.ps1 -IncludeLabs
powershell -ExecutionPolicy Bypass -File .\verify_stage16_outputs.ps1
```

---

## 2) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-16.md`
- `red-book/AI-study-handbook-16.md`

No existing file names are removed. Existing outputs remain valid.

### 2.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage16/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 2.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage16.ps1 -Lab lab01_architecture_review_simulation`
- `pwsh .\run_all_stage16.ps1 -Lab lab02_incident_command_drill`
- `pwsh .\run_all_stage16.ps1 -Lab lab03_quality_governance_audit`
- `pwsh .\run_all_stage16.ps1 -Lab lab04_industry_project_portfolio_pack`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 2.3 Hard Gates (Mastery Approval)

Stage 16 completion allowed only when all pass:
- competency rubric is evidence-backed and reassessed
- architecture/incident drills complete with artifacts
- governance/security controls treated as hard gates
- portfolio shows measurable impact and decision traceability
- before/after artifacts exist

If any gate fails: mastery completion is not approved.

### 2.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- ADR references
- SRE references
- OWASP LLM Top 10
- OpenTelemetry
- Qdrant
- PyTorch CUDA notes
