# Lab 1 Serving Tradeoffs

- Ollama: lowest setup complexity, weaker concurrency scaling.
- vLLM: best throughput for GPU-focused serving.
- Ray Serve: strongest orchestration and scaling flexibility.

Decision rule:
- local prototype -> Ollama
- high-throughput single service -> vLLM
- distributed production orchestration -> Ray Serve