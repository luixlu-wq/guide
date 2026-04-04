# Decision Log - stage-2

Status: first draft populated from real outputs on 2026-04-04.

- run_id: stage2-baseline-20260404
- scope: end-to-end tabular regression pipeline quality check
- options_compared:
  - Option A: DummyRegressor baseline
  - Option B: ColumnTransformer + RandomForestRegressor pipeline
- chosen_change: adopt full preprocessing + RF pipeline as baseline
- decision: promote
- rationale: R2 improved by +0.9316 and error metrics dropped substantially
- rollback_trigger: if rerun R2 < 0.85 or MAE > 35000 on same split/settings
