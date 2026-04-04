# Lab 4 Release Decision

- Gate checks: latency improved, error rate improved, queue stabilized.
- Decision: promote with canary rollout and rollback guardrails.
- Rollback trigger: p95 > 950ms for 3 windows or error_rate > 0.025.