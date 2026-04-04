# Stage 11 Handbook Improvement Plan (v1)

Target file: red-book/AI-study-handbook-11.md  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve AI-study-handbook-11.md to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Keep chapter content implementation-first, not concept-only.
- Add clear and complete examples for each key topic.
- Examples must be complete and operatable with data, functions, workflow, and expected outputs.
- Declare data source and data structure used in all examples.
- Add detailed explanation and demonstration for concepts.
- Add clearer instruction on learning targets.
- Add detailed tutorials for key topics.
- Add practical labs with fixed deliverables.
- Add troubleshooting guidance for realistic failures and fixes.
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.
- Mandatory request: include PyTorch and CUDA conceptual/tutorial content in the chapter.
- Mandatory request: include runnable PyTorch/CUDA example code (simple -> intermediate -> advanced).
- Key request: emphasize industry standard instruction, operation, issue identification, troubleshooting, result evaluation, solution improvement in chapter content, scripts, labs, and acceptance criteria.

Carry-over key requirements from prior plans (must remain active):

- collect high-quality resources (official docs, books, videos, practical repos, industry guides)
- teach both theory and realistic project operations
- teach troubleshooting as a core skill: identify -> compare -> verify
- include beginning-to-production lab with fixed deliverables and rollout gates
- include topic-level industry pain points, root causes, practical resolution strategies, and mapped lab drills

Stage-11-specific locked requirements:

- Make infrastructure chapter operational with measurable SLO/SLA criteria.
- Add serving stack comparisons with strict benchmark workflow.
- Add GPU utilization/memory diagnostics and failure-recovery procedures.
- Add vector DB scaling and reliability checks with evidence artifacts.

---

## 1) Review Summary (Current Chapter State)

### What is already strong

- Infrastructure topics are identified: serving, GPU, vector DB, distributed systems.
- Good beginner motivation for moving from features to operations.

### What still needs improvement

- Needs concrete infrastructure runbooks and SLO metrics.
- Needs stronger capacity, autoscaling, and cost controls.
- Needs operatable incident response drills.

---

## 2) Target Outcomes (Measurable)

Stage 11 rewrite is complete only when:

- every core module includes implementation workflow, not concept-only explanation
- each module maps to runnable scripts with simple/intermediate/advanced progression
- each script prints data/schema declarations and key metrics
- labs produce fixed artifacts in results/
- troubleshooting section uses the required flow: identify -> compare -> verify
- chapter includes explicit production decision logic: promote / hold / rollback

---

## 3) Resource Upgrade (High-Quality Catalog)

Link verification status:

- Last verified: 2026-04-04
- Policy: replace/remove links after 2 failed checks
- Resource quality rule: prioritize infra/vendor primary docs and profiling tooling references.

### 3.1 Official Documentation (Primary)

- Ray docs (distributed runtime and serve): https://docs.ray.io/en/latest/
- RayService quickstart on Kubernetes: https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayservice-quick-start.html
- vLLM docs (high-throughput LLM serving): https://docs.vllm.ai/en/latest/
- Ollama docs (local model runtime ops): https://docs.ollama.com/
- Kubernetes HPA docs (autoscaling control): https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- PyTorch CUDA semantics: https://docs.pytorch.org/docs/stable/notes/cuda.html
- NVIDIA Nsight Systems user guide (GPU profiling): https://docs.nvidia.com/nsight-systems/UserGuide/index.html
- CUDA Toolkit docs (runtime/compiler fundamentals): https://developer.nvidia.com/cuda/toolkit
- OpenTelemetry collector docs: https://opentelemetry.io/docs/collector/
- Prometheus docs (infra telemetry): https://prometheus.io/docs/introduction/overview/

### 3.2 Books (Infra + Reliability)

- Designing Data-Intensive Applications: https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
- Practical MLOps: https://www.oreilly.com/library/view/practical-mlops/9781098103002/
- Site Reliability Engineering Workbook: https://sre.google/workbook/table-of-contents/

### 3.3 Tutorials / Courses / Videos

- Full Stack Deep Learning (LLMOps + deployment labs): https://fullstackdeeplearning.com/
- PyTorch tutorials (profiling and distributed basics): https://docs.pytorch.org/tutorials/
- NVIDIA CUDA optimization blog (transfer bottlenecks): https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/

### 3.4 Practical Repos / Reference Implementations

- Ray project: https://github.com/ray-project/ray
- vLLM project: https://github.com/vllm-project/vllm
- Ollama project: https://github.com/ollama/ollama
- OpenTelemetry Python: https://github.com/open-telemetry/opentelemetry-python

### 3.5 Resource-to-Chapter Mapping Rule (Mandatory)

- Every infra module must include one baseline benchmark run and one profiling run.
- Each benchmark/profiling run must cite one source from 3.1 and one practical implementation source from 3.4.

---

## 4) Required Chapter Structure

1. Infrastructure mental model and boundaries
2. Model serving patterns (Ollama/vLLM/Ray)
3. GPU inference operations (PyTorch/CUDA)
4. Vector DB production behaviors
5. Distributed training/inference decision rules
6. Observability and on-call runbooks
7. Capacity planning and cost governance
8. Labs and incident drills

---

## 5) Concept Module Template (Mandatory)

Every module must include:

- what it is
- why it matters
- data declaration block
- input/output schema block
- worked example
- assumptions and limits
- beginner mistake + fix
- quick check
- failure injection case
- observability hooks
- cost/latency note
- script mapping and expected artifacts

Hard requirement: no module ships with missing fields.

---

## 6) Example Complexity Scale (Use in All Modules)

- Simple: single-path run, small scope, one metric family
- Intermediate: comparison run, fixed evaluation set, error analysis
- Advanced: failure injection, tradeoff analysis, production decision

Each module must explicitly state where complexity lives:

- data/schema complexity
- modeling/reasoning complexity
- compute/memory complexity
- evaluation complexity
- operations complexity

---

## 7) Stage 11 Script Package Plan (red-book/src/stage-11/)

Required files:

- README.md
- requirements.txt
- requirements-optional.txt
- run_all_stage11.ps1
- run_ladder_stage11.ps1
- verify_stage.ps1
- stage11_utils.py

Topic ladders:

- topic00*_infra_basics_*
- topic01*_serving_patterns_*
- topic02*_gpu_cuda_ops_*
- topic03*_vector_db_ops_*
- topic04*_distributed_decisions_*
- topic05*_monitoring_alerting_*
- topic06*_capacity_cost_*
- topic07*_incident_response_*

Labs:

- lab01_serving_benchmark.py
- lab02_gpu_utilization_tuning.py
- lab03_vector_db_scale_diagnostics.py
- lab04_infra_incident_recovery.py

Script requirements:

- very detailed and clear functional comments
- deterministic reruns
- explicit failure handling paths
- metrics and interpretation output

---

## 8) Industry Pain-Point Matrix Requirement

### 8.1 Stage-Specific Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped lab |
|---|---|---|---|---|---|
| Serving patterns | Throughput drops under real concurrency | Wrong batching policy, model/runtime mismatch | Benchmark Ollama/vLLM/Ray with same workload and pick by evidence | QPS, latency, error rate comparison report | lab01_serving_benchmark.py |
| GPU/CUDA ops | GPU is allocated but utilization is low | CPU bottleneck, tiny batches, host-device copy overhead | Increase batch/window, optimize transfer path, profile with Nsight | GPU util %, mem %, kernel timeline | lab02_gpu_utilization_tuning.py |
| Vector DB ops | Retrieval latency increases after data growth | Bad index params, oversized payloads, no shard strategy | Tune index/hnsw/filter fields and shard policy with fixed dataset | Recall@k + p95 retrieval latency | lab03_vector_db_scale_diagnostics.py |
| Distributed decisions | Scale-out increases cost with little gain | Horizontal scaling without bottleneck analysis | Run bottleneck-first decision checklist before scaling | Cost per 1k requests + latency delta | lab01_serving_benchmark.py |
| Monitoring/alerting | Incidents detected too late | Missing SLOs, noisy alerts, no golden signals | Define SLOs + severity policy + alert routing | MTTD, false alert rate, SLO burn chart | lab04_infra_incident_recovery.py |
| Capacity/cost | Infra spend spikes unexpectedly | No quota policy, over-provisioned GPU pool | Add capacity model + budget guardrails + auto scale limits | Monthly cost trend + utilization report | lab02_gpu_utilization_tuning.py |
| Incident response | Recovery is inconsistent across engineers | No runbook, unclear ownership/escalation | Implement incident roles, timeline template, standard mitigation playbook | MTTR and incident postmortem completeness | lab04_infra_incident_recovery.py |

### 8.2 Required Matrix Usage Workflow

1. Reproduce each failure mode under fixed load profile.
2. Capture profiler + telemetry evidence before tuning.
3. Apply one infra change at a time.
4. Rerun identical load profile and compare deltas.
5. Log operational decision and rollback condition.

### 8.3 Mandatory Artifacts

- `results/stage11/benchmark_matrix.csv`
- `results/stage11/gpu_profile_summary.md`
- `results/stage11/incident_postmortem.md`

---

## 9) Troubleshooting and Verification Standard

Required workflow:

1. reproduce with fixed run ID and fixed eval/load set
2. classify failure type from evidence
3. compare at least two solution options with tradeoffs
4. apply one targeted change only
5. rerun same eval/load set
6. report before/after deltas
7. make promote/hold/rollback decision

Required logs per run:

- run id, config versions, data version
- latency/quality/cost metrics
- failure class and chosen fix
- verification result and final decision

---

## 10) Acceptance Criteria (Definition of Done)

Stage 11 is accepted only if:

- chapter is actionable without extra interpretation
- modules are complete under the mandatory template
- scripts and labs are runnable and artifact-based
- industry-standard operation and troubleshooting guidance is explicit
- result evaluation and solution-improvement workflow is measurable
- chapter passes UTF-8 quality check

---

## 11) Priority Breakdown

P0 (must do):

- chapter restructure to operatable format
- script/lab package and runners
- troubleshooting and verification workflow
- industry pain-point mapping and resolution drills

P1 (should do):

- richer benchmark comparisons
- deeper operations and governance playbooks

P2 (nice to have):

- optional advanced infrastructure/distributed extensions

---

## 12) Operable Roadmap (Week 21-22)

### Week 21 (Foundation and Baseline)

Day 1:
- align learning targets with measurable outputs and acceptance gates

Day 2:
- run simple topic ladder scripts and capture baseline artifacts

Day 3:
- run intermediate topic ladder scripts and classify early failure patterns

Day 4:
- run advanced topic ladder scripts with one controlled stress/failure condition

Day 5:
- execute Lab 1 (lab01_serving_benchmark.py) and publish baseline evidence

Day 6:
- execute Lab 2 (lab02_gpu_utilization_tuning.py) and produce before/after comparison draft

Day 7:
- checkpoint review: identify gaps, prioritize fixes, and define rerun scope

### Week 22 (Verification and Release Readiness)

Day 8:
- execute Lab 3 (lab03_vector_db_scale_diagnostics.py) and complete incident/failure diagnosis notes

Day 9:
- compare at least two solution options with explicit tradeoffs

Day 10:
- apply one targeted change and rerun fixed test/eval/load set

Day 11:
- execute Lab 4 (lab04_infra_incident_recovery.py) and generate release-readiness artifacts

Day 12:
- complete regression and gate checks; document residual risks

Day 13:
- finalize decision log (promote / hold / rollback)

Day 14:
- publish stage completion report and transition readiness note

---

## 13) Notebook and Visuals Plan

Notebook track (mandatory):

- stage11_notebook01_baseline.ipynb
- stage11_notebook02_intermediate_analysis.ipynb
- stage11_notebook03_advanced_failure_drill.ipynb
- stage11_notebook04_lab_walkthrough.ipynb

Visual requirements (mandatory):

- one end-to-end workflow diagram
- one pain-point matrix table snapshot
- one before/after metric comparison chart
- one decision flowchart (identify -> compare -> verify -> decide)
- one release/rollback readiness summary figure

Readout requirements:

- each notebook must state data source/schema at the top
- each notebook must include exact rerun command and expected outputs
- each notebook must include one explicit troubleshooting note

---

## 14) Practice Labs (Real, Operatable)

Lab 1: lab01_serving_benchmark.py

Goal:
- produce a reproducible baseline run with declared data, schema, and metrics.

Required outputs:
- one baseline metrics artifact (.csv or .json)
- one baseline narrative artifact (.md)

Lab 2: lab02_gpu_utilization_tuning.py

Goal:
- apply one controlled improvement and compare against the baseline.

Required outputs:
- one option-comparison artifact (solution_options/tradeoff)
- one before/after metric artifact

Lab 3: lab03_vector_db_scale_diagnostics.py

Goal:
- perform realistic failure diagnosis and produce verification rerun evidence.

Required outputs:
- one failure-class artifact
- one verification rerun artifact

Lab 4: lab04_infra_incident_recovery.py

Goal:
- complete production-readiness decision with promote/hold/rollback logic.

Required outputs:
- one readiness/report artifact
- one decision artifact
- one rollback-condition artifact

Lab rules (non-negotiable):

1. fixed run ID, fixed eval/load profile, and fixed config per comparison run
2. one-change-at-a-time for improvement validation
3. all artifacts written under stage-local results
4. no release decision without before/after evidence

---

## 15) Debugging and Quality Gates

Required debugging flow:

1. identify failure class from evidence
2. capture baseline metrics and traces
3. compare at least 2 solution paths
4. apply one targeted change
5. rerun identical test/eval/load set
6. evaluate gate thresholds
7. decide (promote / hold / rollback)

Mandatory gate thresholds for Stage 11:

- p95_latency <= 1.5s
- error_rate <= 1%
- gpu_utilization >= 60% at target load
- incident_mttr trend improving

Hard-stop conditions:

- missing data/schema declaration in any lab output
- missing before/after artifact for improvement claims
- uncontrolled multi-change rerun
- missing decision log

---

## 16) Infrastructure Reliability Spec

Required controls:

- explicit owner for each module/topic/lab output
- fixed acceptance gate checklist tied to measurable metrics
- standardized incident/failure taxonomy for this stage
- rollback trigger definitions before promotion
- artifact traceability from script -> result -> decision

Mandatory evidence pack:

- pain_point_matrix.md
- before_after_metrics.csv
- verification_report.md
- decision_log.md
- reproducibility.md

Release decision policy:

- promote only when all mandatory gates pass
- hold when evidence is partial or conflicting
- rollback when regression/risk exceeds threshold

---

## 17) Data and Schema Declaration Standard

Every topic script and lab must declare:

- data source and ownership
- row/object volume and feature/field definitions
- target/output schema and type expectations
- split/eval/load profile definitions
- version IDs for data/config/model/prompt (as applicable)

Canonical metrics table columns (required for comparisons):

- run_id
- stage
- topic_or_module
- metric_name
- before_value
- after_value
- delta
- dataset_or_eval_set
- seed_or_config_id
- decision

---

## 18) Implementation Plan (Execution Order)

1. align chapter narrative to script/lab package order
2. enforce module template completeness checks
3. add/verify data-schema declaration blocks in all examples
4. execute simple/intermediate/advanced ladders
5. execute all four labs and collect outputs
6. fill pain-point matrix with evidence links
7. run troubleshooting workflow on at least one failure case
8. generate before/after metric table with deltas
9. produce verification report and decision log
10. validate canonical artifact mapping (artifact_name_map.md)
11. run final readability/encoding pass
12. publish transition readiness note

---

## 19) Additional Improvement Items

- add stage-specific common mistakes table (top 10)
- add one checklist for first-time learner run order
- add one checklist for reviewer/mentor validation
- add one quick reference map from topic -> lab -> artifact
- add one command index for all stage runners/verifiers
- add one known-issues section with expected failure signatures

---

## 20) Chapter Simplification Blueprint (Mandatory)

Pass 1 (orientation):
- read stage goal, architecture/module map, and required outputs

Pass 2 (execution):
- run simple -> intermediate -> advanced ladder scripts

Pass 3 (operations):
- run labs and complete troubleshooting + verification cycle

Pass 4 (decision):
- finalize evidence pack and produce release decision

Simplification rule:
- if a section cannot be mapped to a runnable script or artifact, revise it until operatable.

---

## 21) Stage Transition Requirement

Before Stage 12, learner must prove benchmark-based serving selection, GPU tuning evidence, and one completed incident recovery drill.

Transition checklist:

- all mandatory artifacts exist and are mapped
- gate thresholds are evaluated and recorded
- one complete troubleshooting loop is documented
- final decision log includes rollback trigger
- stage README links to notebooks, labs, and artifacts

---

## 22) Global Key Request Addendum (2026-04-04)

- Key request: emphasize industry standard instruction, operation, issue identification, troubleshooting, result evaluation, solution improvement in chapter content, scripts, labs, and acceptance criteria.

## Cross-Plan Consistency Addendum (2026-04-04, Additive-Only)

This addendum is additive and does not remove or override existing content. Existing file names, workflows, and section details remain valid.

### A) Canonical Decision Labels (Use Across All Stages)

- `promote`: change passes all required gates and can move forward
- `hold`: change is promising but evidence is incomplete or mixed
- `rollback`: change increases risk/regression and must be reverted to prior baseline

### B) Canonical Troubleshooting Flow Labels

Use these labels in reports for consistency (even if stage-specific wording differs):

1. `identify` (problem statement + failure class)
2. `evidence` (logs/metrics/traces/schema snapshots)
3. `compare` (>=2 options and tradeoffs)
4. `change` (one targeted change only)
5. `verify` (same dataset/split/eval/load profile)
6. `decide` (`promote` / `hold` / `rollback`)

### C) Canonical Artifact Naming Convention (Recommended)

Keep all existing stage-specific filenames. In addition, produce or map to these canonical artifact names:

- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

If a stage already uses different names, add one of the following without deleting existing files:

- a short mapping file: `artifact_name_map.md`
- or duplicate/export canonical alias files that point to existing outputs

### D) Evidence Schema (Minimum Fields for Any Metric Table)

Every before/after metric table should include these columns (additive requirement):

- `run_id`
- `stage`
- `topic_or_module`
- `metric_name`
- `before_value`
- `after_value`
- `delta`
- `dataset_or_eval_set`
- `seed_or_config_id`
- `decision`

### E) Failure Class Taxonomy (Cross-Stage)

Use common labels for easier comparison across plans:

- `data_schema`
- `data_quality`
- `feature_or_representation`
- `training_or_optimization`
- `retrieval_or_context`
- `generation_or_reasoning`
- `tool_or_api`
- `latency_or_cost`
- `security_or_policy`
- `operations_or_release`

### F) Stage Folder and Result Folder Convention

Recommended unified pattern:

- scripts: `red-book/src/stage-<N>/`
- outputs: `results/stage<N>/`

If a plan already uses another path, keep it and add a path mapping note in stage README.

### G) No-Delete Compatibility Rule

- Do not delete prior deliverable names from existing plan text.
- Add normalization as aliases/mappings only.

---

## 22.1) Stage 11 Expert-Tier Hard-Gate Addendum (Mirror of Chapter 11 Section 24)

This section is additive-only and mandatory for Stage 11 acceptance.  
It mirrors the Chapter 11 infrastructure addendum and must be applied in scripts, labs, notebooks, and release decisions.

### 22.1.1) Blackwell Precision and Throughput Gate (RTX 5090)

Mandatory requirements:

- benchmark baseline precision path (`bf16` or `fp16`) versus Blackwell path (`fp4` where supported)
- compare both performance and quality on the same fixed query/eval workload
- include VRAM fragmentation tracking, not only allocated memory

Required artifact:

- `results/stage11/fp4_throughput_quality_tradeoff.csv`

Hard gate:

- no promotion if precision decision is based on throughput only without quality delta evidence

### 22.1.2) WSL2 Production Hardening Gate

Mandatory requirements:

- keep model weights and active vector indexes inside WSL filesystem (no hot-path `/mnt/c/...`)
- validate telemetry/trace transport with WSL networking configuration
- run before/after I/O comparison after hardening

Required artifacts:

- `results/stage11/wsl_io_before_after.csv`
- `results/stage11/wsl_network_trace_check.md`

Hard gate:

- no promotion if storage path or trace transport is unverified

### 22.1.3) High-Availability and Circuit-Breaker Gate

Mandatory requirements:

- define infra circuit breaker thresholds:
  - `gpu_temp_c > 85`
  - `vram_used_ratio > 0.95`
- define fallback behavior (`cpu fallback` or controlled `503`)
- validate Qdrant durability with persistence/WAL recovery drill

Required artifacts:

- `results/stage11/circuit_breaker_events.jsonl`
- `results/stage11/qdrant_persistence_recovery.md`

Hard gate:

- no promotion if breaker behavior is undefined or fallback is not verified by drill evidence

### 22.1.4) Streaming Infrastructure (SSE) and TTFT Gate

Mandatory requirements:

- provide SSE streaming endpoint behavior for user-facing responses
- measure and report `TTFT` plus end-to-end latency
- verify client-disconnect cancellation to reclaim compute/VRAM

Required artifacts:

- `results/stage11/sse_ttft_metrics.csv`
- `results/stage11/sse_disconnect_recovery.md`

Hard gate:

- no promotion if streaming path cannot prove cancellation/recovery behavior

### 22.1.5) Infrastructure-as-Code Reproducibility Gate

Mandatory requirements:

- one-command local stack startup using `docker compose`
- stack includes:
  - model runtime (`ollama` or `vllm`)
  - vector DB (`qdrant`)
  - telemetry collector (`opentelemetry-collector`)
- include service health checks and shutdown procedure

Required artifacts:

- `results/stage11/local_stack_boot_report.md`
- `results/stage11/service_health_snapshot.json`

Hard gate:

- no promotion if environment bootstrap is not reproducible from documented one-command startup

### 22.1.6) Go/No-Go Unified Evidence Schema Gate

Mandatory release decision file:

- `results/stage11/release_readiness.json`

Required fields:

- `p95_latency_ms`
- `token_throughput_per_sec`
- `error_rate_by_class` (boundary/hardware/model/retrieval/operations)
- `decision`
- `evidence_refs`

Hard gate:

- decision must default to `hold` if any required field is missing

### 22.1.7) Module-Level Missing Item Closure (Required Deliverables)

Add these as explicit required outcomes:

- Module 3 High-Performance Serving:
  - include in-flight/continuous batching benchmark
  - output: `results/stage11/throughput_vs_latency_batch_profile.csv`
- Module 5 Observability with OTel:
  - trace one GIS request end-to-end (`API -> retrieval -> generation`)
  - output: `results/stage11/otel_trace_path_validation.md`
- Module 7 Failure Recovery Drill:
  - simulate VRAM leak symptoms and verify controlled recovery
  - output: `results/stage11/incident_postmortem_infra.md`

### 22.1.8) Stage 11 Promotion Rule Update (Strict)

For Stage 11, promotion is allowed only if all are true:

1. existing Stage 11 hard gates pass
2. all Section 22.1 artifacts exist with valid evidence
3. release decision file is complete and internally consistent
4. at least one failure drill proves safe recovery under stress

If any item fails, final decision must be `hold` or `rollback`.
- When old and canonical names both exist, the stage README must state the mapping.




## 23) Missing-Item Gap Closure (Detailed)

Additive-only section to close remaining depth gaps for Stage 11.

Missing items that are now mandatory:
- topic-level infrastructure theory depth per module
- command-level benchmarking and incident run instructions
- explicit infra failure signatures and first diagnostic actions
- required telemetry artifacts per lab
- stronger mapping between runtime choice and evidence
- stage-specific resource map for serving, GPU, vector DB, and scaling

## 24) Stage 11 Module Deepening Backlog (Topic by Topic)

| Module | Theory to Add | Operatable Tutorial to Add | Typical Failure Signature | Required Evidence | Script/Lab Mapping |
|---|---|---|---|---|---|
| Serving patterns | runtime tradeoff theory (startup/throughput/cost) | identical-load benchmark across Ollama/vLLM/Ray | high latency under concurrency | benchmark_matrix.csv | topic01_serving_patterns + lab01_serving_benchmark.py |
| GPU/CUDA ops | host-device transfer and batching theory | profile batch ladder and concurrency ladder | low GPU util with queue growth | gpu_profile_before_after.csv | topic02_gpu_cuda_ops + lab02_gpu_utilization_tuning.py |
| Vector DB ops | index/filter/shard theory | fixed-query retrieval tuning sequence | latency/recall degradation after scale-up | vector_latency_recall.csv | topic03_vector_db_ops + lab03_vector_db_scale_diagnostics.py |
| Distributed decisions | bottleneck-first scaling theory | cost vs latency what-if comparison | cost increases without throughput gains | cost_throughput_delta table | topic04_distributed_decisions + lab01_serving_benchmark.py |
| Observability/on-call | SLO, burn-rate, alert routing theory | alert policy and escalation drill | late detection and noisy alerts | MTTD + false-alert report | topic05_monitoring_alerting + lab04_infra_incident_recovery.py |
| Capacity/cost controls | capacity forecasting and guardrail theory | budget threshold + autoscaling policy simulation | budget spike and saturation events | capacity_cost_report.md | topic06_capacity_cost + lab02_gpu_utilization_tuning.py |

Rule: every row above must be reflected in chapter tutorial text and stage scripts.

## 25) Stage 11 Lab Operability Contract (Command-Level)

- `lab01_serving_benchmark.py`
  - command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab01_serving_benchmark`
  - outputs: runtime benchmark table + runtime decision note
  - pass: runtime choice is justified by throughput/latency/error evidence
- `lab02_gpu_utilization_tuning.py`
  - command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab02_gpu_utilization_tuning`
  - outputs: GPU before/after profile + tuning notes
  - pass: utilization improves without SLO breach
- `lab03_vector_db_scale_diagnostics.py`
  - command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab03_vector_db_scale_diagnostics`
  - outputs: recall/latency matrix + index tuning log
  - pass: retrieval quality and p95 latency both meet target
- `lab04_infra_incident_recovery.py`
  - command: `pwsh red-book/src/stage-11/run_all_stage11.ps1 -Lab lab04_infra_incident_recovery`
  - outputs: incident timeline + postmortem
  - pass: response is complete, reproducible, and prevention actions are assigned

## 26) Stage 11 Resource Expansion Checklist

Each module must cite at least one source from:
- serving docs (Ray Serve, vLLM, Ollama)
- GPU/CUDA references (PyTorch CUDA notes + profiler docs)
- vector DB docs (Qdrant)
- observability docs (OpenTelemetry/Prometheus/Grafana)
- autoscaling references (Kubernetes HPA)

## 27) Stage 11 Production Review Rubric (Stricter)

- p95 latency improvement >= 20% on selected runtime path
- GPU utilization >= 70% at target load without SLO violation
- retrieval p95 and recall targets both pass at scale
- incident drill produces complete timeline and prevention actions
- all improvement claims include before/after artifacts

## 28) Expert-Tier Infrastructure Addendum (2026-04-04, Additive-Only)

This addendum is additive and does not remove prior requirements.
It upgrades Stage 11 to 2026 production depth for:

- Blackwell-class local hardware (RTX 5090)
- high-throughput serving under variable request patterns
- Ontario GIS-scale retrieval/index operations
- infrastructure resilience in WSL2 and local deployment contexts

### 28.1 Blackwell-Native Profiling (Mandatory)

Lab 2 must include profiler-backed diagnostics beyond basic GPU utilization.

Required tooling path:

- NVIDIA Nsight Systems (`nsys`)
- NVIDIA Nsight Compute (`ncu`)

Required metrics to collect:

- Tensor Core/FP4 kernel occupancy proxy (`fp4_compute_utilization`)
- `sm_clock_throttle_events`
- memory pressure and kernel timeline evidence

Acceptance intent:

- distinguish compute saturation vs memory/transfer bottlenecks before tuning decisions.

### 28.2 In-Flight (Continuous) Batching (Mandatory)

Stage 11 serving module must explicitly teach continuous batching behavior in vLLM/TensorRT-style serving paths.

Required workflow:

1. fixed mixed-size request profile
2. compare static batching vs in-flight batching
3. report throughput/latency tradeoff under same load windows

Required artifact:

- `results/stage11/throughput_vs_latency_batch_profile.csv`

### 28.3 Vector DB Scale Tuning for Large GIS Data (Mandatory)

Add Qdrant HNSW and quantization tuning drill with explicit parameter evidence.

Required tuning dimensions:

- HNSW `m`
- HNSW `ef_construct`
- query-time recall/latency tradeoff
- scalar quantization (int8) path comparison

Required validation target:

- major memory reduction with bounded recall loss (target guidance: <1% recall drop where feasible for selected workload).

Required artifact:

- `results/stage11/vector_recall_vs_latency_matrix.csv`

### 28.4 WSL2 Production Hardening (Mandatory)

Add dedicated WSL2 infra operations guidance in Stage 11 infra module.

Required operational rules:

- keep model weights and vector indices inside WSL filesystem (avoid `/mnt/c` for hot-path I/O)
- document mirrored networking mode in `.wslconfig` for telemetry/collector connectivity
- verify storage path and networking configuration before benchmark runs

Required evidence:

- storage and network configuration notes in reproducibility artifacts.

### 28.5 Infrastructure Circuit Breaker (Mandatory)

Add stateful infra protection policy at serving layer.

Required trigger examples:

- GPU temperature > 85C
- `vram_fragmentation_ratio` > 0.90

Required behavior:

- trip infra circuit breaker and route to lightweight fallback (CPU path) or controlled `503` with retry policy
- prevent full process crash and uncontrolled degradation

Lab requirement:

- `lab04_infra_incident_recovery.py` must simulate VRAM-leak-like pressure and verify protection path.

### 28.6 Evidence Schema Expansion (Stage 11 Required Fields)

In addition to existing canonical fields, Stage 11 comparison tables should include:

- `p99_latency_ms`
- `vram_fragmentation_ratio`
- `tokens_per_watt`
- `fp4_compute_utilization`
- `sm_clock_throttle_events`

### 28.7 Unified Results Folder Expansion (`results/stage11/`)

Add these canonical outputs:

- `hardware_saturation_profile.jsonl`
- `vector_recall_vs_latency_matrix.csv`
- `incident_postmortem_infra.md`
- `throughput_vs_latency_batch_profile.csv`

### 28.8 Script/Lab Mapping Additions (Recommended)

Extend Stage 11 script package expectations with:

- `topic08*_inflight_batching_*`
- `topic09*_blackwell_profiling_*`
- `topic10*_wsl2_hardening_*`
- `topic11*_infra_circuit_breaker_*`

Recommended additive labs:

- `lab05_blackwell_profile_and_batching.py`
- `lab06_qdrant_hnsw_quantization_tuning.py`
- `lab07_wsl2_hardening_validation.py`
- `lab08_infra_circuit_breaker_drill.py`
