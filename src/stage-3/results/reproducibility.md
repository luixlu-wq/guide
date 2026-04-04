# Reproducibility - stage-3

Status: first draft populated from real outputs on 2026-04-04.

## Run metadata
- run_id: stage3-compare-20260404
- dataset_or_eval_set: sklearn `load_breast_cancer`, fixed 80/20 stratified split
- seed_or_config_id: random_state=42 for split and model configs where applicable
- code_version: local workspace snapshot on 2026-04-04
- environment: Python 3.12, scikit-learn, pandas
- command:
  - `python topic07_fair_model_comparison.py`

## Notes
- Canonical summary files are derived directly from `topic07_fair_comparison.csv/json`.
- Use same command and seed to reproduce ranking.
