# SFT vs QLoRA Delta Report

## Quality
- SFT accuracy: 1.0
- QLoRA accuracy: 1.0
- accuracy delta (QLoRA - SFT): 0.0
- SFT f1_macro: 1.0
- QLoRA f1_macro: 1.0
- f1_macro delta (QLoRA - SFT): 0.0

## Ops (simulated)
- SFT memory_mb: 2200.0
- QLoRA memory_mb: 620.0
- SFT latency_ms: 81.67
- QLoRA latency_ms: 55.33

## Decision template
- Prefer QLoRA when quality is within tolerance and memory pressure is high.
- Prefer SFT when QLoRA quality/regression gates fail.