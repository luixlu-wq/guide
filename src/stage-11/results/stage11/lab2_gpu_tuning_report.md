# Lab 2 GPU Tuning Report

Applied changes:
- safer batch upper bound
- mixed precision policy
- OOM recovery and cache clearing behavior

Observed impact:
- lower p95 latency
- lower GPU memory pressure
- reduced error rate under load