# Lab 4 Rollback Plan

- Trigger rollback if quality_score drops below 0.80 for 2 windows.
- Trigger rollback if failure_rate exceeds 0.02 for 2 windows.
- Revert to previous architecture profile and fixed config snapshot.
- Re-run fixed regression set before re-promotion.