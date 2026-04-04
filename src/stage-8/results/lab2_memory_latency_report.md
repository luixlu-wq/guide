# Lab 2 Memory and Latency Tradeoff

## Quality summary
- LoRA accuracy: 1.0
- QLoRA accuracy: 1.0
- LoRA f1_macro: 1.0
- QLoRA f1_macro: 1.0

## Ops summary
- LoRA memory_mb (simulated): 900.0
- QLoRA memory_mb (simulated): 620.0
- LoRA latency_ms (simulated): 60.0
- QLoRA latency_ms (simulated): 55.33

## Recommendation template
- If quality delta is small and memory pressure is high, prefer QLoRA.
- If quality gate fails under QLoRA, prefer LoRA or adjust quantization path.