# Lab 4 Incident Timeline

1. Alert triggered: p95 latency exceeded SLA for 3 windows.
2. Queue depth grew faster than worker drain rate.
3. Error rate increased due to timeouts and retries.
4. Root cause classified: missing backpressure policy + insufficient replicas.
5. Candidate fixes evaluated before deployment.