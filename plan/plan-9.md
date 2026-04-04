# Stage 9 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-9.md`  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-9.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Keep chapter content implementation-first, not concept-only.
- Add clear and complete examples for each key topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare data source and data structure used in all examples.
- Add detailed explanation and demonstration for concepts.
- Add clearer instruction on learning targets.
- Add detailed tutorials for key topics.
- Add practical labs with fixed deliverables.
- Add troubleshooting guidance for realistic failures and fixes.
- Add and maintain high-quality resources:
  - official docs
  - books/papers
  - practical repos
  - framework docs
  - industry platform implementation guides
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.
- Mandatory request: include PyTorch and CUDA conceptual/tutorial content in the chapter.
- Mandatory request: include runnable PyTorch/CUDA example code (simple -> intermediate -> advanced) with very detailed and clear functional comments.

Carry-over key requirements from prior plans (must remain active):

- Key request: collect the best tutorials, books, videos, official documentation, guides, instructions, and industry project references to build chapter content.
- Key request: chapter content must be detailed, easy to understand, and operatable from both theory and realistic project perspectives.
- Key request: create a learning library/track that leads students to real, industry-level projects.
- Key request: add more theory instruction in each chapter so learners understand principles, not only steps.
- Key request: explicitly teach troubleshooting capability as a core skill:
  - how to identify and classify problems from evidence/logs/metrics
  - how to compare possible solutions with clear tradeoff analysis
  - how to verify fixes using controlled reruns and before/after metrics
- Key request: include a new realistic lab that improves a project from beginning to production, with fixed deliverables and production-quality acceptance checks.
- Key request: for each chapter topic, list industry-project pain points, root causes, and practical resolution strategies, and provide related lab practice examples so learners can understand and operate solutions more easily.

Stage-9-specific locked requirements:

- Make AI architecture an operatable engineering workflow, not only component definitions.
- Teach strict component boundaries: API, orchestration, retrieval/vector DB, model serving, monitoring, and scaling.
- Add local vector DB track (Qdrant) for retrieval architecture and ops checks.
- Add model serving comparison track (Ollama vs vLLM vs Ray Serve baseline patterns).
- Add production scaling guide with concrete metrics and threshold-based decisions.
- Add inference reliability section with GPU scheduling, memory pressure, timeout/retry, and backpressure handling.
- Add observability section with request tracing, latency budget breakdown, error taxonomy, and rollback signals.
- Add architecture decision record (ADR) style section for why a given design is chosen.
- For each Stage 9 topic, document industry pain points, root causes, practical resolution strategies, and at least one related runnable lab practice example.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary (Current Chapter 9 State)

### What is already strong

- Core topics are present: vector databases, serving, scaling, GPU inference.
- Includes beginner-friendly architecture framing and common mistakes.
- Includes a basic backend practice project.

### What still needs improvement

- Chapter remains mostly high-level; not yet strict enough for real implementation.
- No fixed Stage 9 script package mapping (`red-book/src/stage-9/`) yet.
- No ladder examples (simple -> intermediate -> advanced) per topic.
- No concrete, measurable architecture metrics baseline.
- No explicit latency budget method (component-by-component).
- No robust production failure playbook (timeouts, queue spikes, OOM, retrieval drift).
- Vector DB section is conceptual; needs full local Qdrant workflow with diagnostics.
- Serving section lacks strict comparison workflow across serving stacks.
- Scaling section lacks capacity planning formulas and trigger thresholds.
- PyTorch/CUDA is mentioned conceptually but not yet operationalized in stage scripts.
- Potential encoding cleanup needed (`â€”` artifacts indicate UTF-8/mojibake risk).

---

## 2) Target Outcomes (Measurable)

Stage 9 rewrite is complete only when:

- Learner can draw and implement a full AI request lifecycle:
  - ingress -> validation -> retrieval -> model serving -> post-process -> response -> telemetry
- Learner can explain and measure:
  - p50/p95/p99 latency
  - throughput
  - error rate
  - queue depth
  - GPU memory utilization
- Every Stage 9 module has simple/intermediate/advanced runnable examples.
- Every Stage 9 script includes:
  - very detailed functional comments
  - data/schema declarations
  - expected outputs and interpretation notes
- Stage 9 includes strict baseline-vs-improved comparison with regression gates.
- Stage 9 includes one beginning-to-production architecture improvement lab with fixed deliverables.
- Stage 9 includes PyTorch/CUDA inference path with CPU fallback behavior.
- Stage 9 includes local vector DB (Qdrant) integration path and troubleshooting drills.

---

## 3) Resource Upgrade (High-Quality Catalog)

Link verification status:

- Last verified: 2026-04-04
- Policy: replace/remove links after 2 failed checks

### A. Core Learning Path (Must Complete)

- FastAPI deployment docs
  - https://fastapi.tiangolo.com/deployment/
- Qdrant quickstart
  - https://qdrant.tech/documentation/quickstart/
- vLLM OpenAI-compatible server
  - https://docs.vllm.ai/en/stable/serving/openai_compatible_server/
- Ray Serve getting started
  - https://docs.ray.io/en/latest/serve/getting_started.html
- Kubernetes HPA concept
  - https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/

### B. Official Docs (Implementation-First)

- Ollama docs index
  - https://docs.ollama.com/
- Ollama API intro
  - https://docs.ollama.com/api
- Ollama OpenAI compatibility
  - https://docs.ollama.com/openai
- Ray Serve LLM docs
  - https://docs.ray.io/en/latest/serve/llm/index.html
- Ray Serve LLM architecture
  - https://docs.ray.io/en/latest/serve/llm/architecture/overview.html
- Kubernetes HPA walkthrough
  - https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough
- Docker Compose basics
  - https://docs.docker.com/compose/intro/compose-application-model/
- Prometheus query basics
  - https://prometheus.io/docs/prometheus/latest/querying/basics/
- OpenTelemetry Python instrumentation
  - https://opentelemetry.io/docs/languages/python/instrumentation/
- PyTorch CUDA semantics
  - https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch AMP recipe
  - https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- CUDA programming guide
  - https://docs.nvidia.com/cuda/cuda-programming-guide/index.html

### C. Books and Structured Learning

- Designing Data-Intensive Applications
  - https://dataintensive.net/
- Machine Learning Systems Design Interview
  - https://www.mlsysbook.ai/
- Building Machine Learning Powered Applications
  - https://www.oreilly.com/library/view/building-machine-learning/9781492045106/
- Designing Machine Learning Systems
  - https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/

### D. Papers and Core Theory

- Attention Is All You Need (architecture baseline context)
  - https://arxiv.org/abs/1706.03762
- LoRA (adapter serving relevance)
  - https://arxiv.org/abs/2106.09685
- QLoRA (memory-constrained serving implications)
  - https://arxiv.org/abs/2305.14314
- Retrieval-Augmented Generation
  - https://arxiv.org/abs/2005.11401

### E. Practical Repos and Framework References

- vLLM
  - https://github.com/vllm-project/vllm
- Ray
  - https://github.com/ray-project/ray
- Qdrant
  - https://github.com/qdrant/qdrant
- FastAPI
  - https://github.com/fastapi/fastapi
- Ollama
  - https://github.com/ollama/ollama
- Kubernetes
  - https://github.com/kubernetes/kubernetes
- Prometheus
  - https://github.com/prometheus/prometheus

### F. Videos and Talks (Operational Perspective)

- Ray Serve LLM serving talk
  - https://www.youtube.com/watch?v=TJ5K1CO9Wbs
- NVIDIA Triton getting started
  - https://www.youtube.com/watch?v=NQDtfSi5QF4

---

## 4) New Handbook Structure (Required)

1. If this chapter feels hard (3-pass learning strategy)
2. Prerequisites and environment setup (CPU + optional CUDA)
3. AI architecture mental model and boundary definitions
4. Request lifecycle and latency budget breakdown
5. Vector DB architecture module (Qdrant local track)
6. Model serving module (Ollama, vLLM, Ray Serve patterns)
7. Scaling module (capacity planning, queueing, autoscaling triggers)
8. GPU inference module (PyTorch/CUDA operational guide)
9. Reliability and failure handling module
10. Observability module (logs, metrics, traces)
11. Security and guardrails module (input validation, abuse controls)
12. Industry deployment patterns (single node -> multi-node -> k8s)
13. Architecture decision records (ADR) and tradeoff framework
14. Example complexity scale + where complexity is
15. Stage 9 script mapping (`src/stage-9`)
16. Practice labs with fixed deliverables
17. Troubleshooting and failure playbook
18. Self-test with weighted rubric
19. What comes after Stage 9

---

## 5) Concept Module Template (Mandatory)

Every module must include:

- What it is
- Why it matters
- Data declaration block
- Input/output schema block
- Worked example
- Assumptions and limits
- Common beginner mistake + fix
- Demonstration checklist
- Quick check
- When to use / when not to use
- Failure injection mini test case
- Observability hooks (what to log)
- Cost/latency note
- Very detailed code-comment expectation for mapped scripts

Hard requirement: no module ships with missing fields.

---

## 6) Example Complexity Scale (Use in All Modules)

- Simple:
  - one service, one model path, one metric family
  - local run only
- Intermediate:
  - multi-component flow (API + retrieval + model)
  - latency split + error handling + benchmark output
- Advanced:
  - traffic/load variation + autoscaling policy
  - rollback criteria + production readiness gates

Each module must explicitly state where complexity lives:

- data and schema complexity
- request orchestration complexity
- compute/memory complexity (CPU/GPU)
- observability complexity
- operations complexity (cost, latency, rollback, on-call)

---

## 7) Stage 9 Script Package Plan (`red-book/src/stage-9/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-optional.txt`
- `run_all_stage9.ps1`
- `run_ladder_stage9.ps1`
- `stage9_utils.py`

Core ladders (simple -> intermediate -> advanced):

0. Architecture flow fundamentals
- `topic00a_system_flow_simple.py`
- `topic00_system_flow_intermediate.py`
- `topic00c_system_flow_advanced.py`

1. Vector DB and retrieval architecture (Qdrant local)
- `topic01a_qdrant_ingest_simple.py`
- `topic01_qdrant_retrieval_intermediate.py`
- `topic01c_qdrant_failure_diagnostics_advanced.py`

2. Model serving architecture
- `topic02a_ollama_serving_simple.py`
- `topic02_vllm_serving_intermediate.py`
- `topic02c_ray_serve_orchestration_advanced.py`

3. Scaling and capacity planning
- `topic03a_latency_budget_simple.py`
- `topic03_queue_backpressure_intermediate.py`
- `topic03c_autoscaling_policy_advanced.py`

4. PyTorch/CUDA inference operations
- `topic04a_pytorch_device_basics_simple.py`
- `topic04_pytorch_amp_intermediate.py`
- `topic04c_cuda_oom_recovery_advanced.py`

5. Observability and diagnostics
- `topic05a_structured_logging_simple.py`
- `topic05_metrics_tracing_intermediate.py`
- `topic05c_incident_triage_advanced.py`

6. Reliability and guardrails
- `topic06a_input_validation_simple.py`
- `topic06_retry_timeout_intermediate.py`
- `topic06c_sla_slo_error_budget_advanced.py`

7. Deployment patterns
- `topic07a_single_node_compose_simple.py`
- `topic07_k8s_deploy_intermediate.py`
- `topic07c_canary_rollback_advanced.py`

8. Architecture decision records and tradeoffs
- `topic08a_decision_matrix_simple.py`
- `topic08_tradeoff_analysis_intermediate.py`
- `topic08c_architecture_review_board_advanced.py`

9. Labs
- `lab01_modular_ai_backend.py`
- `lab02_vector_retrieval_service_qdrant.py`
- `lab03_serving_stack_comparison.py`
- `lab04_scaling_and_observability_incident_lab.py`
- `lab05_architecture_project_baseline_to_production.py`

Script requirements:

- all scripts must include very detailed, clear, functional comments
- all scripts must print data/schema declarations
- all scripts must print metrics and interpretation text
- all scripts must include explicit failure-handling paths
- all scripts must support deterministic reruns (fixed seed / fixed test cases)

---

## 8) Operable Roadmap (Week 17-18)

### Week 17 (Architecture Foundations)

Day 1:
- system boundary mapping and request lifecycle

Day 2:
- vector DB ingestion/retrieval with fixed evaluation queries

Day 3:
- serving baseline with Ollama and API contracts

Day 4:
- vLLM serving baseline and latency profile

Day 5:
- PyTorch/CUDA inference path and AMP checks

Day 6:
- scaling basics (queueing, batching, concurrency)

Day 7:
- architecture baseline report

### Week 18 (Reliability and Productionization)

Day 8:
- observability instrumentation (logs/metrics/traces)

Day 9:
- failure taxonomy and incident triage drills

Day 10:
- retry/timeout/backpressure policy validation

Day 11:
- deployment track (compose -> k8s concepts)

Day 12:
- controlled improvement rerun (one change only)

Day 13:
- canary + rollback drill

Day 14:
- final production-readiness decision and report

---

## 9) Notebook and Visuals Plan

Required visuals:

- end-to-end architecture flow diagram
- latency budget waterfall chart
- retrieval quality vs latency chart
- serving stack comparison table (Ollama/vLLM/Ray)
- incident triage decision tree

Notebook requirement:

- optional `stage9_explainer.ipynb`
- no hidden steps; notebook must map directly to scripts

---

## 10) Practice Labs (Real, Operatable)

### Lab 1: Modular AI Backend

Goal:
- build clean API/service/retrieval/model boundaries with schema validation.

Required outputs:
- `results/lab1_api_contract.json`
- `results/lab1_latency_breakdown.csv`
- `results/lab1_boundary_checklist.md`

### Lab 2: Qdrant Retrieval Service

Goal:
- build local vector retrieval service with data ingestion, query, and diagnostics.

Required outputs:
- `results/lab2_qdrant_collection_stats.json`
- `results/lab2_retrieval_quality.csv`
- `results/lab2_failure_cases.md`

### Lab 3: Serving Stack Comparison

Goal:
- compare serving behavior across Ollama, vLLM, and one orchestrated path.

Required outputs:
- `results/lab3_serving_latency_compare.csv`
- `results/lab3_throughput_compare.csv`
- `results/lab3_operational_tradeoffs.md`

### Lab 4: Scaling and Observability Incident Lab

Goal:
- reproduce traffic spikes and diagnose failures with logs/metrics/traces.

Required outputs:
- `results/lab4_load_test_summary.csv`
- `results/lab4_incident_timeline.md`
- `results/lab4_fix_options_comparison.csv`
- `results/lab4_verification_rerun.csv`

### Lab 5: Realistic Project Improvement (Beginning -> Production)

Goal:
- improve one architecture project from baseline to production readiness with evidence-based troubleshooting.

Required outputs:
- `results/lab5_baseline_architecture.md`
- `results/lab5_improved_architecture.md`
- `results/lab5_metrics_comparison.csv`
- `results/lab5_rollback_plan.md`
- `results/lab5_production_readiness.md`

Lab rules:

1. fixed dataset/test requests and fixed eval cases
2. fixed version tags for model/service/config
3. at least one controlled improvement rerun
4. explicit before/after metric deltas

---

## 11) Industry Pain-Point Matrix (Topic -> Cause -> Solution -> Lab)

This section is mandatory and must be reflected in the final chapter content.

### 11.1 Stage-Specific Industry Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped lab |
|---|---|---|---|---|---|
| Architecture boundaries | System becomes unmaintainable and failures spread | Layer coupling and unclear ownership | Enforce modular contracts and per-layer ownership map | Contract test report by layer | `lab01_modular_ai_backend.py` |
| Vector DB retrieval | Retrieval quality degrades under real data growth | Weak chunk/index policy, stale index, missing filters | Add ingestion contracts, index tuning, freshness and filter diagnostics | Recall@k + freshness lag + filter accuracy | `lab02_vector_retrieval_service_qdrant.py` |
| Serving stack selection | Chosen serving runtime fails SLO under load | No apples-to-apples benchmark across runtimes | Benchmark Ollama/vLLM/Ray Serve on identical workload | QPS/latency/error comparison matrix | `lab03_serving_stack_comparison.py` |
| Scaling policy | Autoscaling triggers too late or too often | No capacity model, weak trigger thresholds | Define queue/latency/error triggers and test under staged load | Trigger accuracy and cost-impact report | `lab04_scaling_and_observability_incident_lab.py` |
| GPU inference reliability | OOM/device mismatch breaks service | Unbounded batch policy, missing fallback logic | Add device guards, AMP, OOM recovery and CPU fallback | OOM recovery success + throughput stability | `topic04c_cuda_oom_recovery_advanced.py` |
| Observability | Incident triage is slow and inconclusive | Missing trace IDs and inconsistent telemetry | Standardize logs/metrics/traces and incident templates | MTTD/MTTR and trace coverage report | `topic05c_incident_triage_advanced.py` |
| Reliability policy | Fix for one metric harms another | No one-change policy or regression gates | One-change rerun protocol with hard gate thresholds | Before/after gate table and decision log | `lab04_scaling_and_observability_incident_lab.py` |
| Deployment rollback | Canary fails but rollback is delayed | No rollback trigger or runbook | Define rollback triggers and run timed rollback drills | Rollback drill timing and success report | `topic07c_canary_rollback_advanced.py` |
| Architecture decisions | Endless debates without measurable criteria | Missing ADR framework and tradeoff scoring | Use ADR matrix tied to SLO/cost/risk constraints | ADR scorecard with signed decision | `topic08c_architecture_review_board_advanced.py` |

### 11.2 Required Matrix Usage Workflow

1. Reproduce pain point with fixed load and run ID.
2. Capture telemetry baseline (latency, errors, resource use).
3. Compare 2+ solution options and choose one targeted fix.
4. Rerun same load profile and verify deltas.
5. Publish production decision with rollback condition.

### 11.3 Mandatory Artifacts

- `results/stage9/pain_point_matrix.md`
- `results/stage9/architecture_benchmark_before_after.csv`
- `results/stage9/release_or_rollback_decision.md`

---

## 12) Troubleshooting and Realistic Failure Playbook

Required failure scenarios:

- API timeout and retry storm
- model server cold-start latency spike
- model loaded per request by mistake
- Qdrant retrieval irrelevance (high similarity, low usefulness)
- queue buildup and backpressure failure
- CUDA OOM and mixed-device tensor errors
- p95 latency regression after optimization
- log volume explosion and missing trace correlation
- deployment drift between local/stage/prod configs
- canary rollout quality regression

Required troubleshooting workflow:

1. reproduce with fixed request set and run ID
2. classify failure type from evidence
3. inspect layer ownership (API/retrieval/model/ops)
4. inspect data/schema/config consistency
5. inspect latency budget by component
6. compare at least two fix options with tradeoffs
7. apply one targeted fix only
8. rerun same tests and record deltas
9. promote/hold/rollback decision with reason

Required logs per run:

- run id and config versions
- dataset/version and request-set IDs
- serving stack and model identifier
- latency stats and throughput stats
- error taxonomy counts
- GPU/CPU utilization summary
- selected fix and verification outcome

---

## 13) Debugging and Quality Gates

Required debugging flow:

- retrieval irrelevant -> inspect chunking/embedding/filter first
- latency spike -> inspect component waterfall before model changes
- error burst -> inspect timeout/retry/backpressure policy
- OOM -> inspect batch/context/memory policy
- scaling failure -> inspect autoscaling triggers and queue depth

Quality gates:

- all Stage 9 scripts pass `run_all_stage9.ps1`
- ladders pass `run_ladder_stage9.ps1`
- expected outputs generated and validated
- benchmark table generated with before/after deltas
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 14) Data and Schema Declaration Standard

Every example must include:

```text
Data: <name and source>
Requests/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed request set and metric policy>
Type: <serving/retrieval/scaling/observability/deployment>
```

Synthetic data must declare generation method and purpose.

---

## 15) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Refactor chapter structure to Stage 8-style operatable format.
3. Add complexity scale and per-topic complexity notes.
4. Refactor each concept section to module template.
5. Add strict data/schema declaration blocks.
6. Create `red-book/src/stage-9/` ladders and runners.
7. Add vector DB (Qdrant) full pipeline examples.
8. Add serving comparison examples (Ollama/vLLM/Ray patterns).
9. Add PyTorch/CUDA inference module and runnable ladder.
10. Add topic-by-topic industry pain-point matrix with causes, fix strategies, and mapped lab drills.
11. Add evaluation/regression gate section for architecture reliability.
12. Upgrade project into fixed deliverable lab format.
13. Add troubleshooting runbook and quality gates.
14. Add weighted self-test and remediation path.
15. Add resource catalog with verification policy.
16. Final QA pass (terminology, encoding, duplicate cleanup).

---

## 16) Acceptance Criteria (Definition of Done)

Stage 9 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script mapping
- all Stage 9 scripts include very detailed, clear comments
- data and schema declarations are present in all examples
- labs are real, operatable, and file-output based
- each topic has explicit industry pain points, root causes, and resolution strategy with related lab drill
- chapter includes strict troubleshooting workflow (identify -> compare -> verify)
- chapter includes explicit PyTorch/CUDA guidance with CPU fallback
- chapter includes local vector DB operational workflow (Qdrant track)
- chapter includes beginning-to-production improvement lab with fixed deliverables
- stage-9 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 17) Priority Breakdown

P0 (must do):

- chapter restructure to operatable architecture format
- Stage 9 script package + runners
- 5 real labs with fixed deliverables
- strict troubleshooting and verification workflow
- detailed comment standard enforcement
- PyTorch/CUDA section with runnable ladder examples
- local vector DB (Qdrant) operatable path

P1 (should do):

- richer serving comparison benchmarks
- deeper autoscaling and canary examples
- extended observability dashboards and alert rules

P2 (nice to have):

- multi-cluster serving extension
- Triton/KServe alternative serving extension track

---

## 18) Chapter Simplification Blueprint (Mandatory)

Use this for every hard section:

1. Problem framing (what this solves)
2. Intuition (mental model)
3. Mechanics (step-by-step flow)
4. Operatable code (ladder examples)
5. Failure pattern and fix

Per-module must include:

- `why this is hard`
- one checkpoint question before moving forward
- one explicit reliability warning

---

## 19) Stage Transition Requirement

Handbook must end with `What Comes After Stage 9` and include:

- 2-3 sentence summary of Stage 10 focus
- mapping from Stage 9 skills to Stage 10 tasks
- readiness sentence before progression

---


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
- When old and canonical names both exist, the stage README must state the mapping.

## Global Key Request Addendum (2026-04-04)

- Key request: emphasize industry standard instruction, operation, issue identification, troubleshooting, result evaluation, solution improvement in chapter content, scripts, labs, and acceptance criteria.



