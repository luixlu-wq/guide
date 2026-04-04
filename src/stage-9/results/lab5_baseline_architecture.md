# Lab 5 Baseline Architecture

- Flow: `client -> API -> retrieval -> model -> response`
- Weakness: no queue backpressure policy, no canary release, weak trace coverage.
- Current SLA status: p95 latency fails target under high concurrency.