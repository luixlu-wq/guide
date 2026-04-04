# Reproducibility - stage-1

Status: first draft populated from real runs on 2026-04-04.

## Run metadata
- run_id: stage1-batch-20260404
- dataset_or_eval_set: sklearn `load_breast_cancer`, `load_diabetes`, and synthetic data from scripts
- seed_or_config_id: random_state=42 (split/model), gradient descent lr=0.001 epochs=3000
- code_version: local workspace snapshot on 2026-04-04
- environment: Python 3.12 (local), scikit-learn + numpy + matplotlib
- commands:
  - `python topic01_supervised_learning.py`
  - `python topic05_gradient_descent.py`
  - `python topic06_training_vs_testing.py`
  - `python topic09_validation_set.py`
  - `python topic11_regularization.py`

## Notes
- `topic05_loss_curve.png` regenerated during run.
- FutureWarning in sklearn logistic `penalty` noted; results unaffected for this run.
