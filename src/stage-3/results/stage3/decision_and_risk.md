# CPU vs GPU Decision And Risk Note (Topic 09)

## Summary
- CPU total time: 0.798970s
- GPU total time: not available (CUDA unavailable)

## Decision
CUDA unavailable. Use CPU path and keep this benchmark as the fallback baseline.

## Risks
- No GPU benchmark yet; transfer/compute tradeoff cannot be evaluated.
- CUDA OOM risk can increase when batch/model size grows.
- Transfer cost can dominate when tensors are small.

## Evidence Files
- `cpu_gpu_latency_transfer.csv`
- `cpu_gpu_latency_transfer.json`
