# Rollback Drill

- Scenario: candidate build degrades grounding in canary replay.
- Action: route traffic to previous stable build, restore prior index pointer.
- Validation: rerun fixed replay and confirm gate recovery.
- Result: pass.
