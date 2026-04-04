# Model Promotion Report

generated_at: 2026-04-04T19:50:28.133724+00:00
stage: stage-8
eval_set: fixed split seed=42 + general holdout seed=99

## Side-by-side quality comparison (fixed eval set)
- baseline_accuracy: 0.6333
- tuned_accuracy: 1.0
- delta_accuracy: 0.3667
- baseline_f1_macro: 0.5484
- tuned_f1_macro: 1.0
- delta_f1_macro: 0.4516

## Knowledge retention gate
- baseline_general_accuracy: 0.5833
- tuned_general_accuracy: 1.0
- retention_drop: -0.4167
- retention_threshold: 0.03
- retention_gate_pass: True

## Promotion gates
- quality_gate_pass: True
- format_gate_pass: True
- retention_gate_pass: True
- final_decision: promote

## Rollback condition
- Roll back immediately if retention gate fails or format-validity regresses.