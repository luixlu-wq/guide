# Lab 5 Rollback Plan

1. Trigger rollback if error_rate > 0.02 for 3 consecutive windows.
2. Trigger rollback if p95 latency exceeds 900ms for 3 windows.
3. Revert traffic split from canary to baseline (100%).
4. Restore last known-good config and model-serving profile.
5. Re-run fixed regression request set before re-promotion.