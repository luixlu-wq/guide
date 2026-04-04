# Lab 3 Operational Tradeoffs

- `ollama_local`: easiest local setup, lower throughput under concurrency.
- `vllm_server`: best throughput/latency for GPU-heavy serving path.
- `ray_serve_path`: stronger orchestration and scaling control for larger systems.

Decision rule example:
- local prototyping -> Ollama
- single-node high-throughput GPU -> vLLM
- distributed orchestration + autoscaling -> Ray Serve