# Lab 4 Rollback Plan

- Trigger rollback if quality_score < 0.78 for 2 windows.
- Trigger rollback if failure_rate > 0.02 for 2 windows.
- Trigger rollback if vram utilization >= 90% under release load profile.
- Trigger rollback if sm_clock_throttle_count > 0 during release candidate test.
