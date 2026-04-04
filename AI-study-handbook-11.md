# Stage 11 - AI Infrastructure

**Week 21**

---

## 0) If This Chapter Feels Hard

Use this order:

1. Understand the request lifecycle and SLO vocabulary.
2. Run baseline benchmarks first, before any tuning.
3. Diagnose one failure domain at a time (`serving`, `gpu`, `retrieval`, `network`).
4. Apply one change only, then rerun the same workload.

This chapter is intentionally operations-first. The goal is to make systems stable, not just "working once".

---

## 1) Stage Goal

Move from:

`"model runs in notebook"`

to:

`"service is measurable, reliable, scalable, and recoverable"`

You must be able to:

- define measurable SLO/SLA targets
- build baseline latency/throughput/error profiles
- run PyTorch/CUDA inference safely with fallback
- operate vector DB retrieval with quality and freshness controls
- diagnose incidents quickly with evidence
- make promote/hold/rollback decisions from rerun data

---

## 2) Infrastructure Mental Model (Concept + Theory)

Request path:

`ingress -> validation -> queue/batching -> model runtime -> postprocess -> response -> telemetry -> alerting`

### Why this model matters

- `ingress/validation` protects system boundaries.
- `queue/batching` controls load and GPU efficiency.
- `runtime` determines latency and memory behavior.
- `telemetry` enables fast diagnosis and safe release decisions.

### Infrastructure failure taxonomy

- `boundary failures`: malformed input, schema mismatch
- `capacity failures`: queue growth, timeout spikes
- `runtime failures`: OOM, mixed-device tensors, kernel stalls
- `retrieval failures`: stale index, high query latency, poor relevance
- `operations failures`: missing alerts, unclear runbook, slow rollback

If you cannot map a failure to one of these categories, your diagnosis is not complete.

---

## 3) SLO/SLA and Measurement Baseline

### Required metrics

- latency: `p50`, `p95`, `p99`
- throughput: requests per second
- error rate: validation/timeout/5xx
- queue metrics: depth, wait time
- resources: CPU, GPU utilization, GPU memory
- retrieval metrics (if RAG): retrieval latency, relevance@k, freshness age

### Minimum SLO template

- `p95_latency <= 900ms`
- `error_rate < 1.5%`
- `availability >= 99.5%`

### Baseline workflow (mandatory)

1. Freeze workload profile (request mix + concurrency + duration).
2. Run baseline with fixed seed and fixed model settings.
3. Save artifacts in `results/`.
4. Identify top bottleneck from metrics.
5. Propose two fix options with expected tradeoffs.
6. Apply one option only.
7. Rerun identical workload and compare deltas.
8. Decide `promote`, `hold`, or `rollback`.

---

## 4) Module A - Serving Patterns (Ollama, vLLM, Ray)

### Conceptual explanation

- **Ollama**: simple local serving, low setup overhead, good for controlled local environments.
- **vLLM**: optimized high-throughput serving with advanced runtime scheduling.
- **Ray Serve**: distributed serving and orchestration when multi-service scaling is required.

### How to choose

- choose **Ollama** when simplicity and local iteration speed matter most
- choose **vLLM** when GPU throughput and token latency are primary constraints
- choose **Ray Serve** when distributed routing, autoscaling, and service composition are required

### Industry pain point

- Pain point: p95 spikes during load bursts.
- Root causes: no queue policy, weak warmup, cold-start penalties.
- Resolution: warmup strategy + queue/backpressure + benchmark-driven tuning.
- Related lab: `lab01_serving_benchmark.py`

### Operatable walkthrough

1. Run `lab01_serving_benchmark.py`.
2. Compare `lab1_serving_latency_compare.csv`.
3. Compare `lab1_serving_throughput_compare.csv`.
4. Read bottleneck notes in `lab1_serving_tradeoffs.md`.
5. Pick a serving profile and document why.

---

## 5) Module B - GPU Inference Operations (PyTorch/CUDA)

### Conceptual explanation

PyTorch executes tensor operators on devices (`cpu` or `cuda`). CUDA gives acceleration but adds memory and scheduling constraints.

### Runtime theory in practice

Inference loop:

1. detect device
2. place model and tensors on the same device
3. run forward pass
4. record latency and memory usage
5. handle OOM and fallback logic

### Critical operational rules

- never mix CPU and CUDA tensors in one operation path
- batch size must fit memory headroom, not only average memory
- define OOM behavior before production rollout
- keep fallback behavior explicit (`cuda` to `cpu`)

### Industry pain point

- Pain point: random crashes after traffic spikes.
- Root causes: unsafe batch/context settings, missing memory guardrails.
- Resolution: device checks + memory headroom policy + adaptive batch limits.
- Related lab: `lab02_gpu_utilization_tuning.py`

### Operatable walkthrough

1. Run baseline profile in `lab02_gpu_utilization_tuning.py`.
2. Inspect `lab2_gpu_profile_baseline.csv`.
3. Apply one tuning change (for example batch or precision policy).
4. Rerun and inspect `lab2_gpu_profile_improved.csv`.
5. Write decision and risks in `lab2_gpu_tuning_report.md`.

---

## 6) Module C - Vector DB Production Operations

### Conceptual explanation

RAG quality depends on retrieval quality and freshness. Poor retrieval often appears as "LLM hallucination" but root cause is index/data operations.

### Required operating controls

- ingestion freshness window
- index health checks
- query latency by filter type
- relevance@k tracking by query class
- reindex policy and rollback snapshot

### Industry pain point

- Pain point: quality degrades as data volume grows.
- Root causes: stale index, poor chunking, weak metadata filters.
- Resolution: retrieval diagnostics + freshness SLO + scheduled maintenance.
- Related lab: `lab03_vector_db_scale_diagnostics.py`

### Operatable walkthrough

1. Run `lab03_vector_db_scale_diagnostics.py`.
2. Review scale behavior in `lab3_vector_scale_metrics.csv`.
3. Review retrieval quality in `lab3_retrieval_quality.csv`.
4. Document root causes and fixes in `lab3_vector_ops_findings.md`.

---

## 7) Module D - Distributed Decisions (When to Scale Out)

### Conceptual explanation

Distributed infrastructure adds failure modes and operational cost. Scale out only when single-node limits are proven by data.

### Decision checklist

Scale out is justified when at least two are true:

- p95 SLO is repeatedly missed on optimized single-node profile
- queue depth grows persistently under expected traffic
- GPU memory constraints block required throughput
- availability targets cannot be met with single-zone/single-node controls

### Anti-pattern

Do not use distributed architecture to hide missing profiling discipline.

---

## 8) Module E - Observability and On-Call Runbook

### Required observability contract

- logs: `request_id`, route, model id, latency, error class, status code
- metrics: p50/p95/p99, throughput, error rate, queue depth, GPU memory
- traces: per-stage timings for ingress/retrieval/runtime/postprocess

### On-call incident workflow

1. detect alert and identify breached SLO
2. classify domain (`serving`, `gpu`, `retrieval`, `network`)
3. gather evidence (logs + metrics + traces)
4. compare at least two fix options
5. apply one controlled change
6. rerun fixed test profile
7. decide `promote`, `hold`, or `rollback`

---

## 9) Module F - Capacity Planning and Cost Controls

### Conceptual explanation

Capacity planning balances latency target, concurrency, and hardware cost.

### Required planning inputs

- request rate profile by hour/day
- prompt/context length distribution
- output token distribution
- model runtime profile by hardware
- target SLO and failure budget

### Cost-control techniques

- right-size model/runtime by endpoint class
- use batching where latency budget allows
- use caching for repeatable requests
- apply timeout/circuit-breaker guardrails
- avoid autoscaling without metric gates

---

## 10) Data Declaration Standard (Mandatory)

Every example must declare:

```text
Data: <name and source>
Requests/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed workload/eval set>
Type: <serving/gpu/vector_db/distributed/ops>
```

---

## 11) Example Complexity Scale

- L1 Simple: one component, one metric family
- L2 Intermediate: component comparison with fixed workload
- L3 Advanced: failure injection + incident workflow + release gate

Where complexity is:

- concurrency behavior and queue dynamics
- GPU memory/runtime stability
- vector DB freshness and scaling
- alert quality and diagnosis speed
- release governance and rollback confidence

---

## 12) Stage 11 Script Mapping

Target package: `red-book/src/stage-11/`

Topics:

- `topic00*_infra_basics_*`
- `topic01*_serving_patterns_*`
- `topic02*_gpu_cuda_ops_*`
- `topic03*_vector_db_ops_*`
- `topic04*_distributed_decisions_*`
- `topic05*_monitoring_alerting_*`
- `topic06*_capacity_cost_*`
- `topic07*_incident_response_*`

Labs:

- `lab01_serving_benchmark.py`
- `lab02_gpu_utilization_tuning.py`
- `lab03_vector_db_scale_diagnostics.py`
- `lab04_infra_incident_recovery.py`

All scripts must:

- print data/schema declarations
- run deterministically
- generate `results/` artifacts
- include clear functional comments
- include interpretation notes for operational decisions

---

## 13) Practice Labs (Detailed, Operatable)

## Lab 1: Serving Benchmark

Goal:

- compare serving behavior under fixed request profile

Required workflow:

1. freeze request profile and concurrency
2. run baseline benchmark
3. record p50/p95/p99 and throughput
4. compare serving options
5. write tradeoff decision

Required outputs:

- `results/lab1_serving_latency_compare.csv`
- `results/lab1_serving_throughput_compare.csv`
- `results/lab1_serving_tradeoffs.md`

Success criteria:

- selected serving path has explicit latency-throughput justification

## Lab 2: GPU Utilization and CUDA Tuning

Goal:

- improve runtime profile without violating safety

Required workflow:

1. run baseline profile
2. identify dominant bottleneck (`memory` or `latency`)
3. compare two tuning options
4. apply one option and rerun
5. verify improvement and risk

Required outputs:

- `results/lab2_gpu_profile_baseline.csv`
- `results/lab2_gpu_profile_improved.csv`
- `results/lab2_gpu_tuning_report.md`

Success criteria:

- improvement is measured; tradeoff is documented

## Lab 3: Vector DB Scale Diagnostics

Goal:

- diagnose retrieval behavior as data scale increases

Required workflow:

1. run baseline retrieval profile
2. measure latency and relevance@k
3. apply one retrieval/indexing fix
4. rerun same query set
5. verify change impact

Required outputs:

- `results/lab3_vector_scale_metrics.csv`
- `results/lab3_retrieval_quality.csv`
- `results/lab3_vector_ops_findings.md`

Success criteria:

- root cause and fix are evidence-backed

## Lab 4: Infrastructure Incident Recovery

Goal:

- execute realistic incident diagnosis and controlled recovery

Required workflow:

1. reproduce incident baseline
2. classify failure domain
3. compare fix options
4. apply one fix only
5. rerun and verify
6. decide release action

Required outputs:

- `results/lab4_incident_baseline.csv`
- `results/lab4_solution_options.csv`
- `results/lab4_verification_rerun.csv`
- `results/lab4_release_decision.md`

Success criteria:

- decision is supported by rerun evidence, not intuition

---

## 14) Troubleshooting Decision Tree (Identify -> Compare -> Verify)

1. **Symptom appears** (latency spike, error increase, quality drop)
2. **Locate primary signal**
   - queue depth high -> serving/capacity branch
   - GPU memory spike -> runtime branch
   - retrieval latency/relevance drop -> vector branch
3. **Form two candidate fixes**
4. **Choose one controlled change**
5. **Rerun fixed profile**
6. **Verify deltas**
   - if gates pass -> `promote`
   - if mixed -> `hold`
   - if regression -> `rollback`

---

## 15) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Serving | unstable p95 under load | weak batching/queue/warmup | benchmark + backpressure tuning | `lab01_serving_benchmark.py` |
| GPU runtime | OOM and crash loops | unsafe batch/context settings | memory guardrails + fallback path | `lab02_gpu_utilization_tuning.py` |
| Vector DB | retrieval degrades at scale | stale index/filters/chunking | diagnostics + freshness policy | `lab03_vector_db_scale_diagnostics.py` |
| Incident ops | slow and repeated incidents | weak telemetry/runbook discipline | standardized diagnosis workflow | `lab04_infra_incident_recovery.py` |

---

## 16) Self-Test (Readiness)

You should answer with operational detail:

1. How do you define and validate SLO/SLA targets?
2. How do you choose between Ollama, vLLM, and Ray Serve?
3. What are minimum CUDA safety checks before rollout?
4. How do you detect and quantify vector DB freshness issues?
5. How do you classify incidents quickly by failure domain?
6. What evidence is required before scaling out?
7. Which metrics must pass before promotion?
8. What exact conditions trigger rollback?

If fewer than 6/8 are answerable with concrete steps, rerun labs 1-4.

---

## 17) Resource Library

- Ray docs: https://docs.ray.io/
- vLLM docs: https://docs.vllm.ai/
- Ollama docs: https://docs.ollama.com/
- Kubernetes HPA: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- PyTorch CUDA semantics: https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch AMP recipe: https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- OpenTelemetry docs: https://opentelemetry.io/docs/

---

## 18) What Comes After Stage 11

Stage 12 moves from infrastructure operations to architecture-pattern decisions (LLM app, RAG, agent, multi-agent) using explicit tradeoff evidence and ADR discipline.

You carry forward:

- metric-driven operation mindset
- incident diagnosis and rerun verification
- release-gate and rollback discipline

## 19) Missing-Item Gap Closure (Stage 11 Addendum)

This section closes remaining gaps and makes Stage 11 infrastructure work operational.

Mandatory additions for this chapter:
- deeper module-level infra theory for serving/GPU/vector DB/scale decisions
- command-level benchmark and incident run instructions
- explicit infrastructure failure signatures and first diagnostics
- mandatory telemetry artifacts for each lab
- stricter performance/cost/reliability gate criteria

## 20) Stage 11 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Serving Patterns | Runtime tradeoffs: startup, throughput, memory, batching behavior | Benchmark Ollama/vLLM/Ray on identical load profile | Throughput collapse when concurrency rises | `results/stage11/serving_benchmark.csv` | `topic01_serving_patterns` + `lab01_serving_benchmark.py` |
| GPU/CUDA Ops | Host-device transfer cost, batch-size effect, kernel utilization | Run batch ladder and concurrency ladder with fixed request mix | GPU allocated but util low, queue time high | `results/stage11/gpu_profile_before_after.csv` | `topic02_gpu_cuda_ops` + `lab02_gpu_utilization_tuning.py` |
| Vector DB Ops | Index/filter/shard tradeoffs and recall-latency balance | Tune one retrieval parameter per run on fixed query set | Recall drops or p95 retrieval spikes after scale-up | `results/stage11/vector_latency_recall.csv` | `topic03_vector_db_ops` + `lab03_vector_db_scale_diagnostics.py` |
| Distributed Decisions | Bottleneck-first scaling theory | Diagnose bottleneck before adding replicas/GPUs | Higher cost with negligible latency/QPS gains | `results/stage11/cost_throughput_delta.csv` | `topic04_distributed_decisions` + `lab01_serving_benchmark.py` |
| Observability/On-Call | SLO, error budget, alert quality and escalation model | Build golden-signal dashboard and severity routing policy | Late detection, noisy alerts, unclear escalation owner | `results/stage11/incident_timeline.md` | `topic05_monitoring_alerting` + `lab04_infra_incident_recovery.py` |
| Capacity/Cost | Capacity forecasting with budget guardrails | Add demand model + budget threshold alerts + scale policy | Budget spikes and saturation events | `results/stage11/capacity_cost_report.md` | `topic06_capacity_cost` + `lab02_gpu_utilization_tuning.py` |

## 21) Stage 11 Lab Operation Runbook (Command-Level)

### Lab 1: Serving Benchmark
- Command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab01_serving_benchmark`
- Required outputs:
  - `results/stage11/serving_benchmark.csv`
  - `results/stage11/runtime_decision.md`
- Pass criteria:
  - Selected runtime is justified by throughput/latency/error evidence.
- First troubleshooting action:
  - Lock warmup count and request profile before rerunning.

### Lab 2: GPU Utilization and CUDA Tuning
- Command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab02_gpu_utilization_tuning`
- Required outputs:
  - `results/stage11/gpu_profile_before_after.csv`
  - `results/stage11/tuning_notes.md`
- Pass criteria:
  - GPU utilization improves without SLO violation.
- First troubleshooting action:
  - Check CPU preprocessing and copy overhead before kernel-level tuning.

### Lab 3: Vector DB Scale Diagnostics
- Command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab03_vector_db_scale_diagnostics`
- Required outputs:
  - `results/stage11/vector_latency_recall.csv`
  - `results/stage11/index_tuning_log.md`
- Pass criteria:
  - Recall and p95 retrieval latency both meet thresholds.
- First troubleshooting action:
  - Validate chunking/filter strategy before index parameter sweeps.

### Lab 4: Infrastructure Incident Recovery
- Command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab04_infra_incident_recovery`
- Required outputs:
  - `results/stage11/incident_timeline.md`
  - `results/stage11/postmortem.md`
- Pass criteria:
  - Response workflow is complete and prevention actions are assigned.
- First troubleshooting action:
  - Re-run incident drill with explicit role assignment if ownership was unclear.

## 22) Stage 11 Resource-to-Module Mapping (Must Cite in Chapter Text)

- Serving: Ray Serve docs, vLLM docs, Ollama docs
- GPU/CUDA: PyTorch CUDA notes, NVIDIA profiling docs
- Vector DB: Qdrant documentation
- Observability: OpenTelemetry, Prometheus, Grafana
- Autoscaling: Kubernetes HPA docs

Requirement: each Stage 11 module must cite at least one source from this list.

## 23) Stage 11 Production Review Rubric (Hard Gates)

- `p95 latency improvement >= 20%` for chosen serving path
- `gpu_utilization >= 70%` at target load with no SLO breach
- retrieval p95 and recall thresholds both pass at target scale
- incident drill completed with complete timeline and CAPA
- all improvements include before/after evidence artifacts

If any hard gate fails: decision cannot be `promote`.
