# Stage 13 Handbook Improvement Plan (v1)

Target file: red-book/AI-study-handbook-13.md  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve AI-study-handbook-13.md to be:
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

Stage-13-specific locked requirements:

- Transform capstone chapter into a delivery-grade project playbook.
- Define milestone gates from baseline to production deployment.
- Add explicit owner mapping and incident escalation flow.
- Add complete acceptance evidence pack requirements.

---

## 1) Review Summary (Current Chapter State)

### What is already strong

- Capstone objective is clear and practical.
- Covers multi-layer integration scope.

### What still needs improvement

- Needs project governance, milestone gates, and production-readiness checks.
- Needs strict issue-triage and remediation workflow.
- Needs complete artifact checklist for deliverables.

---

## 2) Target Outcomes (Measurable)

Stage 13 rewrite is complete only when:

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
- Resource quality rule: capstone delivery must include reproducibility + CI/CD + observability references.

### 3.1 Official Documentation (Primary)

- MLflow docs: https://mlflow.org/docs/latest/
- DVC docs: https://dvc.org/doc
- Prefect docs: https://docs.prefect.io/v3/get-started
- GitHub Actions docs: https://docs.github.com/en/actions
- FastAPI docs: https://fastapi.tiangolo.com/
- OpenTelemetry docs: https://opentelemetry.io/docs/
- Weights & Biases docs: https://docs.wandb.ai/
- Evidently docs: https://docs.evidentlyai.com/introduction

### 3.2 Books (Delivery and MLOps)

- Machine Learning Engineering in Action: https://www.manning.com/books/machine-learning-engineering-in-action
- Practical MLOps: https://www.oreilly.com/library/view/practical-mlops/9781098103002/
- Building Machine Learning Powered Applications: https://www.oreilly.com/library/view/building-machine-learning/9781492045106/

### 3.3 Tutorials / Courses / Videos

- Full Stack Deep Learning (deployment, monitoring, testing): https://fullstackdeeplearning.com/
- DVC course (experiment and data reproducibility): https://learn.dvc.org/
- PyTorch tutorials (from experiment to deploy foundations): https://docs.pytorch.org/tutorials/

### 3.4 Practical Repos / Reference Implementations

- MLflow project: https://github.com/mlflow/mlflow
- DVC project: https://github.com/iterative/dvc
- Prefect project: https://github.com/PrefectHQ/prefect
- Evidently project: https://github.com/evidentlyai/evidently
- W&B client: https://github.com/wandb/wandb

### 3.5 Resource-to-Chapter Mapping Rule (Mandatory)

- Each capstone milestone must reference one reproducibility tool and one monitoring tool.
- Required deliverables must include exact links to the source docs used in implementation decisions.

---

## 4) Required Chapter Structure

1. Capstone scope and non-goals
2. Project architecture and contract map
3. Milestone plan with gated deliverables
4. Testing strategy by layer
5. Troubleshooting and incident escalation
6. Evaluation framework: technical + business metrics
7. Production readiness and rollback
8. Final defense rubric

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

## 7) Stage 13 Script Package Plan (red-book/src/stage-13/)

Required files:

- README.md
- requirements.txt
- requirements-optional.txt
- run_all_stage13.ps1
- run_ladder_stage13.ps1
- verify_stage.ps1
- stage13_utils.py

Topic ladders:

- topic00*_capstone_scope_*
- topic01*_contracts_validation_*
- topic02*_integration_pipeline_*
- topic03*_evaluation_pack_*
- topic04*_incident_workflow_*
- topic05*_release_readiness_*

Labs:

- lab01_capstone_baseline.py
- lab02_capstone_improvement_cycle.py
- lab03_capstone_incident_response.py
- lab04_capstone_production_readiness.py

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
| Capstone scope | Project scope expands and misses deadline | Undefined non-goals, weak milestone gates | Freeze MVP scope and require gate sign-off per milestone | Milestone checklist completion rate | lab01_capstone_baseline.py |
| Contract validation | Teams integrate incompatible payloads | Missing interface ownership and versioning | Assign contract owner + versioned schemas + contract CI tests | Contract CI pass report | lab01_capstone_baseline.py |
| Integration pipeline | Pipeline breaks after small changes | Hidden coupling, no integration test suite | Add stage-gate integration tests with seeded data | Integration success trend by commit | lab02_capstone_improvement_cycle.py |
| Evaluation pack | Results look good but cannot be trusted | Inconsistent metrics, missing baseline references | Standardize metrics pack with baseline and confidence intervals | Unified evaluation report with deltas | lab02_capstone_improvement_cycle.py |
| Incident workflow | Team cannot coordinate during failure | No escalation map, unclear owner | Introduce incident commander model + communication template | Incident timeline + MTTR | lab03_capstone_incident_response.py |
| Release readiness | Production launch delayed at last step | Missing runbooks, missing rollback validation | Add production readiness checklist + rollback drill | Go/No-go report + rollback drill output | lab04_capstone_production_readiness.py |

### 8.2 Required Matrix Usage Workflow

1. Define owner and evidence artifact for every milestone gate.
2. Run gate review at the end of each milestone.
3. Block progression if mandatory evidence is missing.
4. Execute one improvement cycle and one incident simulation.
5. Final release requires signed go/no-go review.

### 8.3 Mandatory Artifacts

- `results/stage13/milestone_gate_tracker.md`
- `results/stage13/integration_regression_report.csv`
- `results/stage13/final_release_review.md`

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

Stage 13 is accepted only if:

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

## 12) Operable Roadmap (Week 25-26)

### Week 25 (Foundation and Baseline)

Day 1:
- align learning targets with measurable outputs and acceptance gates

Day 2:
- run simple topic ladder scripts and capture baseline artifacts

Day 3:
- run intermediate topic ladder scripts and classify early failure patterns

Day 4:
- run advanced topic ladder scripts with one controlled stress/failure condition

Day 5:
- execute Lab 1 (lab01_capstone_baseline.py) and publish baseline evidence

Day 6:
- execute Lab 2 (lab02_capstone_improvement_cycle.py) and produce before/after comparison draft

Day 7:
- checkpoint review: identify gaps, prioritize fixes, and define rerun scope

### Week 26 (Verification and Release Readiness)

Day 8:
- execute Lab 3 (lab03_capstone_incident_response.py) and complete incident/failure diagnosis notes

Day 9:
- compare at least two solution options with explicit tradeoffs

Day 10:
- apply one targeted change and rerun fixed test/eval/load set

Day 11:
- execute Lab 4 (lab04_capstone_production_readiness.py) and generate release-readiness artifacts

Day 12:
- complete regression and gate checks; document residual risks

Day 13:
- finalize decision log (promote / hold / rollback)

Day 14:
- publish stage completion report and transition readiness note

---

## 13) Notebook and Visuals Plan

Notebook track (mandatory):

- stage13_notebook01_baseline.ipynb
- stage13_notebook02_intermediate_analysis.ipynb
- stage13_notebook03_advanced_failure_drill.ipynb
- stage13_notebook04_lab_walkthrough.ipynb

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

Lab 1: lab01_capstone_baseline.py

Goal:
- produce a reproducible baseline run with declared data, schema, and metrics.

Required outputs:
- one baseline metrics artifact (.csv or .json)
- one baseline narrative artifact (.md)

Lab 2: lab02_capstone_improvement_cycle.py

Goal:
- apply one controlled improvement and compare against the baseline.

Required outputs:
- one option-comparison artifact (solution_options/tradeoff)
- one before/after metric artifact

Lab 3: lab03_capstone_incident_response.py

Goal:
- perform realistic failure diagnosis and produce verification rerun evidence.

Required outputs:
- one failure-class artifact
- one verification rerun artifact

Lab 4: lab04_capstone_production_readiness.py

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

Mandatory gate thresholds for Stage 13:

- milestone_gate_pass_rate = 100%
- integration_regression_failures = 0 at release gate
- incident_drill_mttr <= 30 minutes
- go/no-go review signed

Hard-stop conditions:

- missing data/schema declaration in any lab output
- missing before/after artifact for improvement claims
- uncontrolled multi-change rerun
- missing decision log

---

## 16) Capstone Delivery Governance Spec

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

Before Stage 14, learner must pass capstone defense with baseline/improved evidence, incident timeline, and production-readiness signoff.

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
- When old and canonical names both exist, the stage README must state the mapping.




## 23) Missing-Item Gap Closure (Detailed)

Additive-only section to close remaining depth gaps for Stage 13.

Missing items that are now mandatory:
- milestone-level tutorial depth and gate criteria clarity
- stronger mapping from capstone modules to evidence artifacts
- command-level runbook for all capstone labs
- clearer failure signatures for integration, incident, and release phases
- stronger production-readiness rubric with non-negotiable checks

## 24) Stage 13 Module Deepening Backlog (Topic by Topic)

| Module | Theory to Add | Operatable Tutorial to Add | Typical Failure Signature | Required Evidence | Script/Lab Mapping |
|---|---|---|---|---|---|
| Scope and non-goals | scope-control and delivery-risk theory | change-request workflow and scope freeze rule | scope creep and milestone slippage | milestone_gate_tracker.md | topic00_capstone_scope + lab01_capstone_baseline.py |
| Contract validation | ownership/versioning theory | CI contract tests at each boundary | incompatible payloads between modules | contract_ci_report.md | topic01_contracts_validation + lab01_capstone_baseline.py |
| Integration pipeline | stage-gate integration theory | unit->integration->system test flow | late cross-module regressions | integration_regression_report.csv | topic02_integration_pipeline + lab02_capstone_improvement_cycle.py |
| Evaluation pack | reproducibility and confidence theory | fixed eval profile and before/after reporting | non-reproducible performance claims | evaluation_pack.md + delta table | topic03_evaluation_pack + lab02_capstone_improvement_cycle.py |
| Incident workflow | role-based incident command theory | commander timeline and escalation template | unclear ownership during failures | incident_timeline.md + postmortem | topic04_incident_workflow + lab03_capstone_incident_response.py |
| Release readiness | go/no-go and rollback theory | checklist-driven release review and rollback drill | promotion without full evidence | final_release_review.md + rollback_drill.md | topic05_release_readiness + lab04_capstone_production_readiness.py |

Rule: each row must be reflected in chapter tutorials and stage scripts.

## 25) Stage 13 Lab Operability Contract (Command-Level)

- `lab01_capstone_baseline.py`
  - command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab01_capstone_baseline`
  - outputs: baseline scope/contract evidence + baseline metrics
  - pass: baseline is reproducible and contracts are valid
- `lab02_capstone_improvement_cycle.py`
  - command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab02_capstone_improvement_cycle`
  - outputs: improvement delta + improvement note
  - pass: one controlled change with measurable benefit
- `lab03_capstone_incident_response.py`
  - command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab03_capstone_incident_response`
  - outputs: incident timeline + postmortem
  - pass: coordinated response and prevention actions are complete
- `lab04_capstone_production_readiness.py`
  - command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab04_capstone_production_readiness`
  - outputs: go/no-go review + rollback drill
  - pass: release decision is signed and fully evidence-backed

## 26) Stage 13 Resource Expansion Checklist

Each capstone module must cite at least:
- one delivery/governance source (DORA/SRE style)
- one reproducibility/experiment source (DVC/MLflow)
- one implementation source (FastAPI/Qdrant)
- one runtime source (PyTorch CUDA notes)

## 27) Stage 13 Production Review Rubric (Stricter)

- all milestone gates complete with required evidence artifacts
- one full improvement cycle completed and verified
- one full incident simulation completed with postmortem quality check
- final go/no-go includes rollback proof and owner signoff
- all claims are traceable to before/after evidence

## 28) Stage 13 Expert-Tier Capstone Addendum (Review Closure)

This section is additive-only and closes the remaining expert-tier gaps identified in the Stage 13 review.

### 28.1 Hardware Profiling Gate (Mandatory Deliverable)

Stage 13 capstone must be treated as a hardware-bound service, not only a software artifact.

Required:
- run a concurrent-load profile on local GPU environment
- capture VRAM/power/temperature saturation behavior
- prove capstone remains within declared runtime envelope

Mandatory artifact:
- `results/stage13/hardware_saturation_profile.jsonl`

Minimum required fields per record:
- `timestamp`
- `run_id`
- `device_name`
- `gpu_memory_used_mb`
- `gpu_memory_total_mb`
- `gpu_utilization_percent`
- `gpu_temperature_c`
- `power_draw_w`
- `active_request_count`
- `decision` (`promote` / `hold` / `rollback`)

Release gate:
- capstone fails release if runtime envelope is exceeded and no mitigation evidence exists.

### 28.2 Domain-Specific Capstone Rule (Ontario GIS / MapToGo)

Generic toy capstones are not sufficient for Stage 13 completion.

Required domain declaration in Lab 1:
- chosen domain: `ontario_gis` or `maptogo_tour_guide` (or explicitly declared equivalent real project)
- data source, schema, and target task must be domain-realistic

Lab binding rules:
- `lab01_capstone_baseline.py`: must ingest declared domain data (for GIS: GeoJSON/administrative boundary records; for tourism: destination POI/tour content)
- `lab02_capstone_improvement_cycle.py`: must improve one domain-relevant objective with before/after evidence (for GIS: retrieval correctness/projection validation; for tourism: grounded itinerary answer quality/format reliability)

Mandatory artifact:
- `results/stage13/domain_scope_and_metric_contract.md`

### 28.3 Local-First CI/CD Requirement (WSL2 + Local GPU)

If capstone depends on local GPU inference, cloud-only CI is insufficient.

Required:
- define a local-first CI/CD pathway using self-hosted runner in WSL2
- ensure integration tests that require local inference can run automatically
- include trigger rules for smoke, regression, and release-candidate pipelines

Mandatory artifacts:
- `results/stage13/local_ci_cd_runner_setup.md`
- `results/stage13/local_ci_pipeline_run_report.md`

Minimum checks in CI pipeline report:
- schema/contract validation
- integration regression
- capstone inference smoke test on local environment
- artifact generation check for required stage outputs

### 28.4 AI-Specific Incident Drill (Semantic Drift Required)

Lab 3 incident cannot be only API timeout or crash simulation.

Required incident scenario:
- semantic drift caused by data/index/chunking change
- degraded retrieval grounding or increased hallucination rate
- evidence-based diagnosis using traces/metrics and rollback decision

Mandatory artifacts:
- `results/stage13/semantic_drift_incident_report.md`
- `results/stage13/semantic_drift_before_after.csv`

Lab 3 pass condition:
- failure class identified as AI-system quality failure (not only transport/runtime)
- root cause hypothesis tested with controlled rerun
- mitigation validated on same eval set

### 28.5 ADR Reconciliation Gate (Design vs Reality)

Stage 13 final review must reconcile planned architecture vs delivered architecture.

Required:
- document architecture pivots with reasons and tradeoffs
- include constraint evidence (latency/cost/hardware/operational risk)
- explicitly sign off final architecture decision

Mandatory artifact:
- `results/stage13/adr_design_vs_reality.md`

Required ADR fields:
- `planned_architecture`
- `delivered_architecture`
- `why_changed`
- `evidence`
- `impact_on_quality_latency_cost`
- `final_decision`
- `owner_signoff`

### 28.6 Stage 13 Final Hard Gates (Expanded)

Stage 13 is not complete unless all below pass:

- hardware profiling gate completed with valid evidence
- domain-specific capstone baseline and improvement cycle completed
- local-first CI/CD runner and pipeline evidence completed
- semantic-drift incident drill completed with verified mitigation
- ADR design-vs-reality reconciliation signed
