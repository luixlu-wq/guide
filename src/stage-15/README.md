# Stage 15 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 15 (systematic troubleshooting).

## Setup and Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage15.ps1
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage15.ps1 -IncludeLabs
powershell -ExecutionPolicy Bypass -File .\verify_stage15_outputs.ps1
```

---

## 2) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-15.md`
- `red-book/AI-study-handbook-15.md`

No existing file names are removed. Existing outputs remain valid.

### 2.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage15/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 2.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage15.ps1 -Lab lab01_ml_failure_diagnosis`
- `pwsh .\run_all_stage15.ps1 -Lab lab02_llm_prompt_regression`
- `pwsh .\run_all_stage15.ps1 -Lab lab03_rag_retrieval_failure`
- `pwsh .\run_all_stage15.ps1 -Lab lab04_option_compare_and_verify`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 2.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- measurable failure statement exists
- evidence bundle complete before fix selection
- at least two options compared before final decision
- verification rerun uses same data/split/eval profile
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 2.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- SRE references
- scikit-learn evaluation docs
- Great Expectations
- OpenTelemetry
- Qdrant
- PyTorch CUDA notes
