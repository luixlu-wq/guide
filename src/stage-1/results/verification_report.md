# Verification Report - stage-1

Status: first draft populated from real runs on 2026-04-04.

## identify
- Goal: verify Stage 1 baseline quality, leakage control, and optimization behavior.

## evidence
- `topic01_supervised_learning.py`: accuracy 0.9825, precision/recall/F1 all 0.9861.
- `topic05_gradient_descent.py`: initial loss 415.8359 -> final loss 4.1837.
- `topic06_training_vs_testing.py`: correct test R2 0.0607, leaked same-data R2 1.0.
- `topic09_validation_set.py`: best C on validation = 1.0, final test accuracy = 0.9825.
- `topic11_regularization.py`: best test accuracy at C=1.0 (0.9825).

## compare
- Compared high C overfit regime (C=1000) vs balanced C (C=1.0).
- Compared proper split evaluation vs same-data evaluation.

## change
- Selected C=1.0 and enforced fixed split + validation-first model selection.

## verify
- Re-runs remained consistent with strong test classification quality and visible leakage detection guardrails.

## decide
- Decision: promote.
- Rationale: high quality with explicit anti-leakage evidence and stable optimization trend.
