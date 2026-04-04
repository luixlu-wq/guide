# Verification Report - stage-3

Status: first draft populated from real outputs on 2026-04-04.

## identify
- Goal: verify fair benchmark across classical models under the same split and metrics.

## evidence
- Source artifacts:
  - `results/topic07_fair_comparison.csv`
  - `results/topic07_fair_comparison.json`
- Ranked outcomes (F1 descending):
  - logistic_regression: accuracy 0.9825, F1 0.9861, ROC-AUC 0.9954
  - random_forest: accuracy 0.9474, F1 0.9583, ROC-AUC 0.9937
  - svm_rbf: accuracy 0.9474, F1 0.9577, ROC-AUC 0.9897
  - decision_tree: accuracy 0.9386, F1 0.9510, ROC-AUC 0.9342

## compare
- Compared decision_tree baseline vs logistic_regression winner using same split and metrics.

## change
- Chosen baseline for downstream work: logistic_regression pipeline.

## verify
- Accuracy delta: +0.0439
- F1 delta: +0.0351
- ROC-AUC delta: +0.0612

## decide
- Decision: promote.
- Rationale: logistic_regression is consistently strongest on the fixed benchmark.
