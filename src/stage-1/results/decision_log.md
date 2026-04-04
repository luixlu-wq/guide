# Decision Log - stage-1

Status: first draft populated from real runs on 2026-04-04.

- run_id: stage1-reg-20260404
- scope: logistic regularization and validation-based model selection
- options_compared:
  - Option A: C=1000 (weak regularization)
  - Option B: C=1.0 (balanced regularization)
- chosen_change: use C=1.0 with fixed split and validation-first selection
- decision: promote
- rationale: test accuracy improved from 0.9298 to 0.9825 and train-test gap reduced
- rollback_trigger: if repeated runs drop below test accuracy 0.96 or leakage checks fail
