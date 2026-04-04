# Stage 9 - AI System Architecture

**Week 17-18**

---

## 0) If This Chapter Feels Hard

Use this 3-pass method:

1. Pass 1: Learn the architecture map and terminology only.
2. Pass 2: Run Stage 9 scripts and collect metrics artifacts.
3. Pass 3: Diagnose one failure, compare two fixes, and verify with rerun.

Do not try to memorize everything in one pass.

---

## 1) Stage Goal

Move from:

`"I can run a model demo"`

to:

`"I can design, operate, debug, and improve a production AI system"`

After this stage, you must be able to:

- design clear component boundaries
- operate vector retrieval with a local vector DB (Qdrant)
- serve models with measurable latency and throughput
- use PyTorch/CUDA correctly for inference paths
- troubleshoot production failures with evidence-based workflows
- make architecture decisions with explicit tradeoffs

---

## 2) Prerequisites and Environment

### Required knowledge

- Python basics
- API basics (`FastAPI` or equivalent)
- model inference basics
- retrieval basics (embeddings and top-k search)

### Environment

- OS: Windows/macOS/Linux
- Python: 3.10+
- Optional GPU: NVIDIA CUDA-capable device

### Core tooling track

- API and orchestration: `FastAPI`, `uvicorn`
- Vector DB: local `Qdrant`
- Serving options: `Ollama`, `vLLM`, `Ray Serve`
- Metrics/observability: structured logs + metrics + traces

### Data declaration standard (mandatory for all examples)

Every example must declare:

```text
Data: <name and source>
Requests/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed request set and metric policy>
Type: <serving/retrieval/scaling/observability/deployment>
```

---

## 3) AI Architecture Mental Model

Model is only one component. Production quality depends on system design.

Standard request lifecycle:

1. request ingress (`API gateway` / route)
2. validation and normalization
3. retrieval or context build (optional)
4. model inference (local or remote)
5. post-processing and schema enforcement
6. response return
7. telemetry emit (logs, metrics, traces)

If one step is weak, user quality drops even with a strong model.

---

## 4) Latency Budget and Capacity Basics

You must split end-to-end latency by component, not guess:

`total_latency = api + retrieval + model + postprocess + network`

Track at least:

- `p50`, `p95`, `p99` latency
- throughput (`req/s`)
- error rate (`5xx`, timeout, validation errors)
- queue depth
- GPU utilization and memory usage (if using CUDA)

Capacity planning baseline:

1. define SLA (example: `p95 <= 2.5s`, error rate `<1%`)
2. run baseline load
3. find bottleneck component
4. scale only bottleneck
5. rerun same test and compare before/after

---

## 5) Module 1: Component Boundaries

### What it is

Separating architecture into clear responsibilities:

- API layer
- business/orchestration layer
- retrieval layer
- model-serving layer
- observability layer

### Why it matters

Without boundaries, failures cannot be isolated quickly.

### Operatable checklist

1. API layer has no model-loading code.
2. Retrieval layer has no route or HTTP logic.
3. Model layer has no DB management logic.
4. All boundaries use explicit request/response schemas.
5. Each layer emits structured logs with request id.

### Industry pain point

- Pain point: Everything is in one file, incidents are hard to debug.
- Root causes: Fast prototype became production with no refactor.
- Resolution: Enforce module ownership + boundary tests.
- Related lab: `lab01_modular_ai_backend.py`

---

## 6) Module 2: Vector DB Architecture (Qdrant Track)

### What it is

Use embeddings + vector index to retrieve semantically relevant context.

### Why it matters

RAG quality is often limited by retrieval quality, not LLM quality.

### Data declaration example

```text
Data: internal policy snippets (local files)
Requests/Samples: 200 chunks, 30 fixed eval queries
Input schema: {query: str, top_k: int, filters: dict}
Output schema: {matches: [{id, score, text, metadata}]}
Eval policy: fixed query set + recall@k + manual relevance labels
Type: retrieval
```

### Required workflow

1. chunk documents with versioned chunk policy
2. generate embeddings with fixed model version
3. upsert to Qdrant with metadata fields
4. query with fixed eval set
5. inspect top-k quality, not only similarity score
6. tune chunking/filtering/embedding strategy
7. rerun same eval set and compare deltas

### Typical failure patterns

- high similarity but low relevance
- missing metadata filters
- stale index after source data change
- over-chunking or under-chunking

### Industry pain point

- Pain point: RAG answers sound fluent but use wrong context.
- Root causes: weak chunking strategy, missing filters, stale collection.
- Resolution: add retrieval diagnostics + ingestion/version policies.
- Related labs:
  - `topic01_qdrant_retrieval_intermediate.py`
  - `topic01c_qdrant_failure_diagnostics_advanced.py`
  - `lab02_vector_retrieval_service_qdrant.py`

---

## 7) Module 3: Model Serving Architecture

### What it is

Expose inference through stable APIs with controlled runtime behavior.

### Why it matters

A model that works in notebook can fail under concurrency and real traffic.

### Serving patterns

- local/simple: `Ollama`
- high-throughput GPU: `vLLM`
- orchestration and scaling: `Ray Serve`

### Required serving checks

1. model warm-start at service startup
2. no model reload per request
3. timeout policy
4. retry policy (with limits)
5. batch/dynamic-batch configuration
6. schema validation for both input and output

### Industry pain point

- Pain point: latency spikes during traffic bursts.
- Root causes: no queue/backpressure, bad batch settings, cold starts.
- Resolution: warm pools + queue policy + batch tuning + load testing.
- Related labs:
  - `topic02_vllm_serving_intermediate.py`
  - `topic02c_ray_serve_orchestration_advanced.py`
  - `lab03_serving_stack_comparison.py`

---

## 8) Module 4: Scaling and Backpressure

### What it is

Designing the system to stay reliable as users and requests grow.

### Scaling types

- vertical: bigger machine
- horizontal: more replicas

### Backpressure principle

If requests arrive faster than processing capacity, system must:

- queue with limits
- shed load safely when needed
- return controlled errors instead of collapsing

### Required operational thresholds (example)

- p95 latency > target for 3 windows -> scale out
- queue depth > threshold -> activate overload policy
- error rate > threshold -> hold release, investigate

### Industry pain point

- Pain point: service becomes unstable under peak load.
- Root causes: no capacity model, no autoscaling triggers, shared bottlenecks.
- Resolution: latency budget + queue policy + staged load testing.
- Related labs:
  - `topic03_queue_backpressure_intermediate.py`
  - `topic03c_autoscaling_policy_advanced.py`
  - `lab04_scaling_and_observability_incident_lab.py`

---

## 9) Module 5: PyTorch and CUDA for Inference Operations

### What it is

Using device-aware tensor execution for efficient and stable inference.

### Why it matters in architecture

Inference SLOs and cost are directly affected by device strategy.

### Core execution loop (conceptual)

1. move tensors/model to device (`cpu` or `cuda`)
2. run forward pass
3. apply post-processing
4. return structured output
5. emit device/latency/memory telemetry

### Required device safety rules

1. check `torch.cuda.is_available()` before selecting CUDA
2. keep tensors and model on same device
3. enforce CPU fallback path
4. monitor memory usage before batch/context increases
5. test OOM behavior and recovery strategy

### Ladder complexity guidance

- simple:
  - single request on CPU/CUDA with explicit device print
- intermediate:
  - mixed precision (`AMP`) and batch inference
- advanced:
  - OOM simulation, fallback, and rerun with reduced batch

### Industry pain point

- Pain point: random inference failures in production nodes.
- Root causes: mixed-device tensors, aggressive batch sizes, no fallback.
- Resolution: strict device guardrails + OOM recovery path + telemetry gates.
- Related labs:
  - `topic04_pytorch_amp_intermediate.py`
  - `topic04c_cuda_oom_recovery_advanced.py`

---

## 10) Module 6: Observability (Logs, Metrics, Traces)

### What it is

Instrumentation that makes system behavior visible and diagnosable.

### Required minimum telemetry

- structured logs:
  - request id, endpoint, model id, retrieval id, status, latency
- metrics:
  - p50/p95/p99 latency, throughput, error rate, queue depth
- traces:
  - per-component span timings

### Why it matters

Without observability, troubleshooting becomes guesswork.

### Industry pain point

- Pain point: incidents take too long to resolve.
- Root causes: missing trace correlation, inconsistent logs, weak metric coverage.
- Resolution: unified telemetry schema + incident timeline workflow.
- Related labs:
  - `topic05_metrics_tracing_intermediate.py`
  - `topic05c_incident_triage_advanced.py`
  - `lab04_scaling_and_observability_incident_lab.py`

---

## 11) Module 7: Reliability, Guardrails, and Change Control

### Reliability rules

1. use fixed regression request set
2. apply one-change-at-a-time policy
3. run before/after comparison on same test set
4. keep explicit promote/hold/rollback decision

### Guardrail examples

- strict request schema validation
- output schema validation
- max context and timeout caps
- abuse/rate limits
- safe fallback response when dependencies fail

### Industry pain point

- Pain point: quick fixes create hidden regressions.
- Root causes: no fixed eval set, no rollback protocol, untracked changes.
- Resolution: change-control workflow with hard acceptance gates.
- Related labs:
  - `topic06c_sla_slo_error_budget_advanced.py`
  - `topic07c_canary_rollback_advanced.py`
  - `lab05_architecture_project_baseline_to_production.py`

---

## 12) Example Complexity Scale (Used in All Modules)

Use this scale for every Stage 9 example:

- L1 Simple:
  - one component path
  - one metric family
  - local run
- L2 Intermediate:
  - multi-component path
  - benchmark + error handling
  - fixed comparison
- L3 Advanced:
  - load variation
  - failure injection
  - production decision (promote/hold/rollback)

Where complexity usually is:

- retrieval quality and data freshness
- serving concurrency and queue behavior
- GPU memory and device consistency
- observability completeness
- operations and incident response

---

## 13) Stage 9 Script Mapping

Target script package: `red-book/src/stage-9/`

Core topics:

- `topic00*` system flow ladders
- `topic01*` Qdrant retrieval ladders
- `topic02*` serving ladders
- `topic03*` scaling/backpressure ladders
- `topic04*` PyTorch/CUDA ladders
- `topic05*` observability ladders
- `topic06*` reliability/guardrails ladders
- `topic07*` deployment/canary/rollback ladders
- `topic08*` architecture decision ladders

Labs:

- `lab01_modular_ai_backend.py`
- `lab02_vector_retrieval_service_qdrant.py`
- `lab03_serving_stack_comparison.py`
- `lab04_scaling_and_observability_incident_lab.py`
- `lab05_architecture_project_baseline_to_production.py`

All scripts must:

- contain very detailed functional comments
- print data/schema declarations
- print metrics + interpretation text
- include explicit failure-handling paths
- support deterministic reruns

---

## 14) Practice Project Lab (Operatable Version)

## Project: Baseline to Production AI Architecture

### Fixed objective

Build and improve a retrieval + model-serving backend from baseline to production-ready.

### Fixed required workflow

1. select one fixed dataset and one fixed request eval set
2. declare full schemas (input/output/retrieval metadata)
3. implement baseline architecture (`API -> retrieval -> model`)
4. collect baseline metrics (`p50/p95/p99`, throughput, error rate)
5. identify one bottleneck from evidence
6. design at least two solution options with tradeoff table
7. apply exactly one chosen improvement
8. rerun same eval/load tests
9. report before/after deltas
10. make final decision: `promote`, `hold`, or `rollback`

### Fixed required deliverables

- `results/lab5_baseline_architecture.md`
- `results/lab5_improved_architecture.md`
- `results/lab5_metrics_comparison.csv`
- `results/lab5_solution_options.csv`
- `results/lab5_incident_or_risk_log.md`
- `results/lab5_rollback_plan.md`
- `results/lab5_production_readiness.md`

### Minimum acceptance thresholds (example)

- p95 latency improves by target percentage or meets SLA
- error rate does not regress
- retrieval relevance does not regress
- rollback plan is executable and tested

---

## 15) Troubleshooting Playbook (Identify -> Compare -> Verify)

Use this exact flow:

1. reproduce with fixed request IDs and run ID
2. classify failure:
  - retrieval quality
  - model latency
  - API/schema
  - scaling/backpressure
  - GPU/device
3. gather evidence:
  - logs, metrics, traces, failed outputs
4. generate two fix candidates
5. compare candidate tradeoffs (quality/latency/cost/risk)
6. implement one fix only
7. rerun same tests
8. verify with before/after deltas
9. publish promote/hold/rollback decision

### RAG/retrieval-specific quick diagnosis

If RAG answer quality is poor:

1. inspect retrieved chunks first (not model first)
2. check chunking policy and metadata filters
3. verify embedding model version consistency
4. check stale index and ingestion freshness
5. run query-level relevance diagnostics
6. only then adjust generation prompt/model

---

## 16) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Component boundaries | Hard to debug incidents | mixed responsibilities | enforce modular contracts | `lab01_modular_ai_backend.py` |
| Vector retrieval | Fluent but incorrect answers | poor chunking/filters/index freshness | retrieval diagnostics + governance | `lab02_vector_retrieval_service_qdrant.py` |
| Serving stack | Latency spikes | no queue controls, cold starts | warm start + backpressure + batching | `lab03_serving_stack_comparison.py` |
| Scaling | collapse under peak | no capacity planning | latency budget + autoscaling thresholds | `lab04_scaling_and_observability_incident_lab.py` |
| PyTorch/CUDA ops | OOM/device mismatch | weak device guards | fallback + memory telemetry + policy | `topic04c_cuda_oom_recovery_advanced.py` |
| Observability | slow incident triage | weak logs/metrics/traces | unified telemetry schema | `topic05c_incident_triage_advanced.py` |
| Change control | fixes cause regressions | no fixed eval gates | one-change reruns + hard gates | `lab05_architecture_project_baseline_to_production.py` |

---

## 17) Self-Test (Readiness Check)

You should be able to answer:

1. Why is a model not equal to a production AI system?
2. How do you split and analyze latency by component?
3. What retrieval checks do you run when RAG quality drops?
4. When do you choose Ollama, vLLM, or Ray Serve patterns?
5. What are your minimum PyTorch/CUDA device safety rules?
6. What metrics must be present before production promotion?
7. How do you compare two fixes and verify one safely?
8. What triggers `rollback` in your architecture policy?

If you cannot answer at least 6/8 with concrete workflows, rerun labs 2, 4, and 5.

---

## 18) Resource Library (Theory + Practical + Industry)

### Official docs

- FastAPI deployment:
  - https://fastapi.tiangolo.com/deployment/
- Qdrant documentation:
  - https://qdrant.tech/documentation/
- vLLM serving docs:
  - https://docs.vllm.ai/en/stable/serving/openai_compatible_server/
- Ray Serve docs:
  - https://docs.ray.io/en/latest/serve/
- Kubernetes autoscaling:
  - https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- PyTorch CUDA semantics:
  - https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch AMP recipe:
  - https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- CUDA programming guide:
  - https://docs.nvidia.com/cuda/cuda-programming-guide/index.html
- OpenTelemetry:
  - https://opentelemetry.io/docs/
- Prometheus:
  - https://prometheus.io/docs/

### Books and system design references

- Designing Data-Intensive Applications:
  - https://dataintensive.net/
- Building Machine Learning Powered Applications:
  - https://www.oreilly.com/library/view/building-machine-learning/9781492045106/
- Designing Machine Learning Systems:
  - https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- ML Systems Book:
  - https://www.mlsysbook.ai/

### Practical repositories

- vLLM: https://github.com/vllm-project/vllm
- Ray: https://github.com/ray-project/ray
- Qdrant: https://github.com/qdrant/qdrant
- FastAPI: https://github.com/fastapi/fastapi
- Ollama: https://github.com/ollama/ollama

---

## 19) What Comes After Stage 9

Stage 10 moves from architecture operation into advanced optimization and governance at scale.

Skills you carry forward:

- architecture boundary design
- measurable reliability workflows
- retrieval/serving/scaling operations
- evidence-based troubleshooting and rollout decisions

Readiness signal: you can improve a real architecture with measured before/after results and a safe rollback plan.

---

## 20) Merged Notes from Previous Draft (Beginner Deep-Dive)

This section merges the useful beginner-friendly content from `AI-study-handbook-9.md.bak` into the current structured chapter.

### Quick summary

A production AI system is not only a model. It is a connected system that usually includes:

- data pipeline
- API layer
- retrieval/vector search
- model serving
- monitoring and logging
- configuration and scaling

### 20.1 Architecture mental model

Think in full request flow:

`user -> API -> validation -> retrieval/tool/model -> postprocess -> response -> telemetry`

If any link is weak, user quality drops.

### 20.2 Vector database mental model

Core retrieval steps:

1. convert documents to embeddings
2. store vectors with metadata
3. convert user query to embedding
4. run nearest-neighbor retrieval
5. return top-k chunks to downstream model

Key point: retrieval quality depends on chunking, embedding model, metadata filters, and index freshness.

### 20.3 Model serving mental model

Serving turns model logic into a stable API interface. Minimum serving responsibilities:

- startup/warm model
- request validation
- inference execution
- timeout/retry policy
- structured response schema

### 20.4 GPU inference mental model

GPU inference mainly accelerates matrix/tensor operations. In production, performance depends on:

- batching policy
- memory policy
- device placement correctness
- caching strategy (for LLMs, KV cache behavior)

### 20.5 Scaling mental model

Scale bottlenecks, not everything:

1. measure
2. find bottleneck
3. apply targeted scaling
4. verify with same load profile

---

## 21) Real-World Workflow (Merged)

| Step | Action | Why it matters |
|---|---|---|
| 1 | Define product task | Prevents architecture choices without business target |
| 2 | Draw request flow | Makes boundaries and dependencies explicit |
| 3 | Separate components | Improves testing, maintainability, and scaling |
| 4 | Choose serving strategy | Aligns runtime with latency/throughput requirements |
| 5 | Add retrieval/storage when needed | Supports RAG and memory use cases |
| 6 | Add config management | Prevents hardcoded fragile systems |
| 7 | Add logging/metrics/traces | Enables incident diagnosis |
| 8 | Measure latency by component | Enables evidence-based optimization |
| 9 | Add caching/batching/scaling | Improves throughput/cost after measurement |
| 10 | Test realistic load | Reveals concurrency and saturation failures |
| 11 | Harden failure paths | Stabilizes timeout/retry/error behavior |
| 12 | Deploy with rollback policy | Keeps production changes safe |

---

## 22) Debugging Checklist (Merged)

When architecture behaves badly, check:

- [ ] Is failure in API, retrieval, model, or post-process?
- [ ] Are component boundaries clear enough to isolate failure?
- [ ] Is model loaded once, not per request?
- [ ] Are p50/p95/p99 measured by component?
- [ ] Is GPU actually used when expected?
- [ ] Are retrieval results relevant, not only high-score?
- [ ] Are logs and traces correlated by request/trace id?
- [ ] Is timeout/retry/backpressure policy correct?
- [ ] Are offline and online workloads separated?
- [ ] Are fixes verified by before/after rerun metrics?

---

## 23) Beginner Practice Walkthrough (Merged)

This complements Section 14 with a simple first implementation flow.

### Step 1: start API skeleton

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

### Step 2: add `predict` and `retrieve` endpoints

- define strict request and response schemas
- add input validation
- return structured errors

### Step 3: separate modules

Suggested structure:

```text
app/
  main.py
  api/routes.py
  services/model_service.py
  services/retrieval_service.py
  core/config.py
  core/logging.py
  schemas/request.py
  schemas/response.py
```

### Step 4: add observability

- request id
- endpoint
- latency
- failure class
- model/retrieval path

### Step 5: run negative tests

- invalid payload
- timeout simulation
- retrieval empty result
- dependency failure

---

## 24) Common Mistakes (Merged and Cleaned)

| Mistake | Why it happens | Problem | Fix |
|---|---|---|---|
| All logic in one file | fast initial prototype | hard debugging/scaling | enforce module boundaries |
| No logging/tracing | feels optional early | no incident visibility | add structured telemetry from day 1 |
| Hardcoded config/secrets | short-term convenience | unsafe and hard to deploy | environment/config management |
| Model reload per request | naive implementation | large latency waste | warm load at startup |
| No schema validation | flexible dict habits | runtime failures | strict request/response schemas |
| No load test | only single-request testing | production collapse under bursts | fixed concurrency/load tests |
| No rollback policy | optimism bias | high release risk | canary + rollback gates |

---

## 25) Extended Self-Test (Merged)

### Questions

1. Why is model quality alone not enough for production AI quality?
2. What are the minimum components of an AI system architecture?
3. How do you decide when retrieval is required?
4. What does nearest-neighbor retrieval do?
5. Why can high similarity still produce low-quality RAG answers?
6. What is model serving?
7. Why should model loading usually happen at startup?
8. What is dynamic batching and when is it useful?
9. Why are GPUs important for many inference workloads?
10. What causes CUDA device mismatch failures?
11. What is backpressure and why is it necessary?
12. What is the difference between vertical and horizontal scaling?
13. Why track p50/p95/p99 instead of only average latency?
14. What should be in minimum structured logs?
15. Why are traces useful in multi-component architecture?
16. Why should online and offline workloads be separated?
17. What is a canary rollout?
18. What should trigger rollback?
19. Why enforce one-change-at-a-time verification?
20. How do you compare two solution options fairly?
21. Why is fixed eval/load data required for verification?
22. What does a production readiness report include?
23. Why should retrieval diagnostics inspect returned chunks directly?
24. How do queue depth and error rate relate under overload?
25. Why must schema validation happen at boundaries?
26. Why can overengineering early be harmful?
27. What is an architecture decision record (ADR)?
28. What core artifacts should a Stage 9 lab generate?
29. Which signals show troubleshooting is evidence-based?
30. What is the key Stage 9 graduation capability?

### Short answer key

1. System quality depends on architecture, not only model logic.
2. API, orchestration, retrieval/storage, model serving, observability, scaling.
3. Use retrieval when task requires external/fresh knowledge grounding.
4. Finds closest vectors to a query embedding.
5. Poor chunking/filtering/freshness can return wrong context.
6. Exposing model inference via stable runtime/API.
7. Avoid repeated load latency and resource waste.
8. Groups near-time requests for better throughput.
9. Parallel tensor compute improves speed/throughput.
10. Model and tensors on different devices.
11. Prevents queue explosion and collapse under burst load.
12. Bigger machine vs more replicas.
13. Tail latency reflects user pain and SLA risk.
14. request id, endpoint, status, latency, error class, route/model info.
15. They locate slow/failing component spans.
16. Prevents batch jobs from hurting real-time inference.
17. Gradual release to a subset of traffic.
18. Sustained SLA breach or quality regression.
19. Isolates causality and avoids confounded changes.
20. Compare on same dataset/load and same metrics.
21. Enables fair before/after comparison.
22. Metrics deltas, risk log, rollback plan, decision.
23. Similarity score alone is insufficient.
24. Queue growth often precedes latency/error spikes.
25. Catch invalid inputs/outputs early and consistently.
26. Complexity before evidence slows progress and increases risk.
27. Structured record of decision, context, options, tradeoffs.
28. contracts, metrics, comparison tables, risk/rollback docs.
29. fixed reruns, measured deltas, explicit decision rationale.
30. Ability to improve architecture safely with measurable evidence.

---

## 26) Post-Stage Capability Checklist (Merged)

- [ ] I can draw and explain the full production request flow.
- [ ] I can diagnose whether failure is retrieval, serving, or scaling.
- [ ] I can run PyTorch/CUDA inference with safe fallback behavior.
- [ ] I can run a fixed before/after verification workflow.
- [ ] I can produce promote/hold/rollback decisions with evidence.
- [ ] I can translate architecture tradeoffs into implementation choices.
