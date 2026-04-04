# Stage 14 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 14 (hedge-fund style trading system).

## 1) Setup

Run inside `red-book/src/stage-14`:

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

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage14.ps1
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage14.ps1
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage14.ps1 -IncludeLabs
```

## 3) Required Lab Outputs

- `results/lab1_multi_asset_baseline_metrics.csv`
- `results/lab1_signal_summary.csv`
- `results/lab1_portfolio_weights.csv`
- `results/lab2_risk_before_after.csv`
- `results/lab2_constraint_changes.csv`
- `results/lab2_risk_decision.md`
- `results/lab3_execution_cost_profile.csv`
- `results/lab3_slippage_scenarios.csv`
- `results/lab3_execution_findings.md`
- `results/lab4_stress_results.csv`
- `results/lab4_recovery_actions.csv`
- `results/lab4_release_recommendation.md`

## 4) Verification

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage14_outputs.ps1
```

---

## 5) Plan Alignment Addendum (2026-04-04)

This addendum aligns this README with:
- `red-book/plan/plan-14.md`
- `red-book/AI-study-handbook-14.md`

No existing file names are removed. Existing outputs remain valid.

### 5.1 Canonical Output Compatibility

Recommended canonical output root: `results/stage14/`.

Current scripts may still write to `results/` with existing names. Keep both by using mapping:
- `artifact_name_map.md`

Canonical artifacts required by cross-plan standard:
- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

### 5.2 Command-Level Lab Operations (Normalized)

- `pwsh .\run_all_stage14.ps1 -Lab lab01_multi_asset_baseline`
- `pwsh .\run_all_stage14.ps1 -Lab lab02_risk_engine_improvement`
- `pwsh .\run_all_stage14.ps1 -Lab lab03_execution_slippage_impact`
- `pwsh .\run_all_stage14.ps1 -Lab lab04_stress_test_and_recovery`

If the runner does not accept `-Lab`, run the corresponding lab Python file directly.

### 5.3 Hard Gates (Promote/Hold/Rollback)

Promotion allowed only when all pass:
- leakage checks pass before any performance claim
- risk thresholds pass in baseline and stress scenarios
- decisions use net-of-cost metrics (not gross-only)
- strategy changes are auditable and rollback-ready
- before/after artifacts exist

If any gate fails: choose `hold` or `rollback`.

### 5.4 Resource Citation Rule

Each module/lab report must cite at least one relevant source from:
- PyPortfolioOpt / Backtrader
- pandas / scikit-learn / statsmodels
- financial ML references
- PyTorch CUDA notes
