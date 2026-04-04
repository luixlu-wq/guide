## ICV Audit Trail

Identify:
- failure metric: f1
- threshold: < 0.60
- failing case: ml_case_imbalance_001

Compare:
- option A: class_weighting
- option B: threshold_recalibration

Verify:
- measured delta: f1: +0.08 (0.58 -> 0.66)
- decision: promote
