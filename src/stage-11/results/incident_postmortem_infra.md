# Infrastructure Postmortem Drill

Incident class: operations_or_release
Primary symptom: p95 latency and queue depth spike with GPU pressure.
Root cause: unsafe peak traffic policy and insufficient breaker threshold handling.
Mitigation: queue backpressure + fallback path + canary probe restore.
Prevention: enforce breaker gate checks in pre-release verification.