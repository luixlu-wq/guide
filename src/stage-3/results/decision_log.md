# Decision Log - stage-3

Status: first draft populated from real outputs on 2026-04-04.

- run_id: stage3-compare-20260404
- scope: fair model selection for Stage 3 classical ML benchmark
- options_compared:
  - decision_tree
  - logistic_regression
  - random_forest
  - svm_rbf
- chosen_change: select logistic_regression as benchmark winner
- decision: promote
- rationale: highest accuracy/F1/ROC-AUC under fixed split and common metric set
- rollback_trigger: if re-run under same split/seed lowers logistic F1 below 0.96
