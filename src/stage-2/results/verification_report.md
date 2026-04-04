# Verification Report - stage-2

Status: first draft populated from real outputs on 2026-04-04.

## identify
- Goal: verify Stage 2 tabular pipeline gives measurable improvement over naive baseline.

## evidence
- `topic09_stage2_end_to_end_pipeline.py` metrics artifact:
  - R2 = 0.9311967064
  - MAE = 22909.2101
  - MSE = 826880013.6155
  - rows_train = 400, rows_test = 100
- Baseline comparator (DummyRegressor, same split):
  - R2 = -0.0004006896
  - MAE = 94564.0141
  - MSE = 12022845020.8085

## compare
- Option A: mean baseline predictor.
- Option B: full preprocessing + RandomForest pipeline.

## change
- Selected Option B with explicit imputation + encoding + model pipeline.

## verify
- Before/after deltas show large improvement across all tracked metrics.

## decide
- Decision: promote.
- Rationale: strong metric improvement with reproducible fixed split.
