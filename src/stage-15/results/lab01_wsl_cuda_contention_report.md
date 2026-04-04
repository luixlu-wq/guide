# WSL2/CUDA Contention Report

- Project context: `MapToGo`
- Scenario: throughput dropped after long-running session.
- Evidence source: `nvidia-smi` snapshot + `nsys` summary (or equivalent fallback telemetry).
- Diagnostic conclusion: runtime contention identified as primary contributor before model-logic changes.
- Suspected class: WSL2 memory pressure / CUDA context pressure.
- Action: recycle worker process, reduce concurrency spike, and monitor VRAM trend.
