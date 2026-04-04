# Fair Comparison Checklist (Topic 07)

Run timestamp (UTC): 2026-04-04T18:02:42.202524+00:00

- [x] Same task and dataset for all models (`load_breast_cancer`)
- [x] Same split policy for all models (`test_size=0.2`, `random_state=42`, `stratify=y`)
- [x] Same metric set for all models (`accuracy`, `precision`, `recall`, `f1`, `roc_auc`)
- [x] Model-specific preprocessing is isolated inside each model pipeline
- [x] Train/test metrics are both recorded
- [x] Generalization gap is reported (`train_f1 - test_f1`)
- [x] Stability report uses 5 different split seeds (`mean` and `std`)

Primary evidence file:
- `model_compare_before_after.csv`
