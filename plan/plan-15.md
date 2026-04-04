# Stage 15 Handbook Improvement Plan (v1)

Target file: red-book/AI-study-handbook-15.md  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve AI-study-handbook-15.md to be:
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

Stage-15-specific locked requirements:

- Make diagnosis and tuning process fully procedural and auditable.
- Add fixed issue-taxonomy and evidence collection templates.
- Add solution-option comparison matrix and verification rerun protocol.
- Add ML + LLM + RAG unified troubleshooting runbook.

---

## 1) Review Summary (Current Chapter State)

### What is already strong

- Strong diagnosis-first message already exists.
- Lists many realistic failure sources.

### What still needs improvement

- Needs stricter root-cause framework with evidence templates.
- Needs controlled experiment protocol and rollback criteria.
- Needs more operatable ML/LLM/RAG troubleshooting ladders.

---

## 2) Target Outcomes (Measurable)

Stage 15 rewrite is complete only when:

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
- Resource quality rule: debugging workflow must be evidence-first and regression-safe.

### 3.1 Official Documentation (Primary)

- scikit-learn model selection and evaluation: https://scikit-learn.org/stable/model_selection.html
- PyTorch tutorials: https://docs.pytorch.org/tutorials/
- MLflow docs (experiment/metric tracking): https://mlflow.org/docs/latest/
- Weights & Biases docs (run comparison): https://docs.wandb.ai/
- Evidently docs (data/model drift checks): https://docs.evidentlyai.com/introduction
- Ragas docs (RAG eval loops): https://docs.ragas.io/en/stable/
- LangSmith docs (traces/evals): https://docs.langchain.com/langsmith/home
- Promptfoo docs (prompt and RAG regression testing): https://www.promptfoo.dev/docs/intro/
- TruLens docs (LLM app eval and tracing): https://www.trulens.org/
- OpenTelemetry docs (cross-layer tracing): https://opentelemetry.io/docs/

### 3.2 Books (Failure Analysis Mindset)

- Designing Machine Learning Systems: https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- Machine Learning Engineering in Action: https://www.manning.com/books/machine-learning-engineering-in-action
- Practical MLOps: https://www.oreilly.com/library/view/practical-mlops/9781098103002/

### 3.3 Tutorials / Courses / Videos

- Full Stack Deep Learning (troubleshooting + monitoring modules): https://fullstackdeeplearning.com/
- Hugging Face course troubleshooting chapter: https://huggingface.co/docs/course/en/chapter1/1
- DVC course (controlled reruns and reproducibility): https://learn.dvc.org/

### 3.4 Practical Repos / Reference Implementations

- Evidently repository: https://github.com/evidentlyai/evidently
- Ragas repository: https://github.com/explodinggradients/ragas
- Promptfoo repository: https://github.com/promptfoo/promptfoo
- LangSmith docs hub: https://docs.langchain.com/langsmith/home

### 3.5 Resource-to-Chapter Mapping Rule (Mandatory)

- Each debugging ladder (ML/LLM/RAG) must map to one eval framework and one observability source.
- Option comparison tables must include linked evidence for metric definitions and rerun protocol.

---

## 4) Required Chapter Structure

1. Define failure precisely and measurable symptoms
2. Root-cause taxonomy and evidence capture
3. Controlled experiments and change isolation
4. ML debugging ladder
5. LLM prompt and output debugging ladder
6. RAG retrieval and grounding debugging ladder
7. Verification and regression gates
8. Labs and incident postmortem templates

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

## 7) Stage 15 Script Package Plan (red-book/src/stage-15/)

Required files:

- README.md
- requirements.txt
- requirements-optional.txt
- run_all_stage15.ps1
- run_ladder_stage15.ps1
- verify_stage.ps1
- stage15_utils.py

Topic ladders:

- topic00*_failure_definition_*
- topic01*_evidence_collection_*
- topic02*_experiment_design_*
- topic03*_ml_debug_*
- topic04*_llm_debug_*
- topic05*_rag_debug_*
- topic06*_verification_gates_*
- topic07*_postmortem_*

Labs:

- lab01_ml_failure_diagnosis.py
- lab02_llm_prompt_regression.py
- lab03_rag_retrieval_failure.py
- lab04_option_compare_and_verify.py

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
| Failure definition | Team argues about whether system is broken | Ambiguous success criteria | Use strict failure statement template with measurable thresholds | Signed failure statement + threshold table | lab01_ml_failure_diagnosis.py |
| Evidence collection | Debugging starts with guesses | Missing traces, no baseline snapshots | Require evidence bundle before proposing fixes | Evidence checklist completion score | lab01_ml_failure_diagnosis.py |
| Experiment design | Multiple changes hide true cause | Uncontrolled experiments | One-change-at-a-time protocol with fixed seed/data | Experiment ledger with controlled variables | lab04_option_compare_and_verify.py |
| ML debug | Model quality unstable after retraining | Data drift, leakage, label noise | Run data quality + drift + leakage diagnostics first | Train/test delta, drift metrics, error slices | lab01_ml_failure_diagnosis.py |
| LLM debug | Prompt tweak helps one case, hurts others | No regression set, weak output contract | Use fixed prompt eval set + strict output schema | Pass/fail by category + regression diff | lab02_llm_prompt_regression.py |
| RAG debug | Retrieval improves but final answer still wrong | Context contamination, ranking mismatch | Separate retrieval and generation diagnosis loops | Recall@k vs groundedness comparison | lab03_rag_retrieval_failure.py |
| Verification gates | Fix shipped without robust validation | Missing gate criteria and blocker policy | Add mandatory verification gates before release | Gate pass/fail log + blocker decisions | lab04_option_compare_and_verify.py |
| Postmortem | Same issue repeats later | Weak root-cause documentation | Standard postmortem template with preventive action tracking | Recurrence rate and action closure report | lab04_option_compare_and_verify.py |

### 8.2 Required Matrix Usage Workflow

1. Open incident with measurable failure definition.
2. Build evidence bundle before suggesting fixes.
3. Compare at least two fix options with risk/cost tradeoffs.
4. Apply one fix and rerun fixed regression suite.
5. Publish postmortem with preventive actions.

### 8.3 Mandatory Artifacts

- `results/stage15/evidence_bundle_index.md`
- `results/stage15/option_compare_table.csv`
- `results/stage15/postmortem_and_prevention.md`

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

Stage 15 is accepted only if:

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

## 12) Operable Roadmap (Week 29-30)

### Week 29 (Foundation and Baseline)

Day 1:
- align learning targets with measurable outputs and acceptance gates

Day 2:
- run simple topic ladder scripts and capture baseline artifacts

Day 3:
- run intermediate topic ladder scripts and classify early failure patterns

Day 4:
- run advanced topic ladder scripts with one controlled stress/failure condition

Day 5:
- execute Lab 1 (lab01_ml_failure_diagnosis.py) and publish baseline evidence

Day 6:
- execute Lab 2 (lab02_llm_prompt_regression.py) and produce before/after comparison draft

Day 7:
- checkpoint review: identify gaps, prioritize fixes, and define rerun scope

### Week 30 (Verification and Release Readiness)

Day 8:
- execute Lab 3 (lab03_rag_retrieval_failure.py) and complete incident/failure diagnosis notes

Day 9:
- compare at least two solution options with explicit tradeoffs

Day 10:
- apply one targeted change and rerun fixed test/eval/load set

Day 11:
- execute Lab 4 (lab04_option_compare_and_verify.py) and generate release-readiness artifacts

Day 12:
- complete regression and gate checks; document residual risks

Day 13:
- finalize decision log (promote / hold / rollback)

Day 14:
- publish stage completion report and transition readiness note

---

## 13) Notebook and Visuals Plan

Notebook track (mandatory):

- stage15_notebook01_baseline.ipynb
- stage15_notebook02_intermediate_analysis.ipynb
- stage15_notebook03_advanced_failure_drill.ipynb
- stage15_notebook04_lab_walkthrough.ipynb

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

Lab 1: lab01_ml_failure_diagnosis.py

Goal:
- produce a reproducible baseline run with declared data, schema, and metrics.

Required outputs:
- one baseline metrics artifact (.csv or .json)
- one baseline narrative artifact (.md)

Lab 2: lab02_llm_prompt_regression.py

Goal:
- apply one controlled improvement and compare against the baseline.

Required outputs:
- one option-comparison artifact (solution_options/tradeoff)
- one before/after metric artifact

Lab 3: lab03_rag_retrieval_failure.py

Goal:
- perform realistic failure diagnosis and produce verification rerun evidence.

Required outputs:
- one failure-class artifact
- one verification rerun artifact

Lab 4: lab04_option_compare_and_verify.py

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

Mandatory gate thresholds for Stage 15:

- rerun_reproducibility >= 99%
- regression_gate_failures = 0 before promote
- option_compare_table complete
- postmortem_action_closure >= 90%

Hard-stop conditions:

- missing data/schema declaration in any lab output
- missing before/after artifact for improvement claims
- uncontrolled multi-change rerun
- missing decision log

---

## 16) Diagnosis and Verification Reliability Spec

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

Before Stage 16, learner must demonstrate a complete identify->compare->verify loop across ML, LLM, and RAG failures.

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

Additive-only section to close remaining depth gaps for Stage 15.

Missing items that are now mandatory:
- topic-level diagnosis theory (failure definition, evidence, controlled experiments)
- clearer module-specific failure signatures and anti-patterns
- command-level runbook for all troubleshooting labs
- explicit option-comparison and verification artifact requirements
- stricter promote/hold/rollback rubric for fixes

## 24) Stage 15 Module Deepening Backlog (Topic by Topic)

| Module | Theory to Add | Operatable Tutorial to Add | Typical Failure Signature | Required Evidence | Script/Lab Mapping |
|---|---|---|---|---|---|
| Failure definition | measurable failure statement theory | threshold-based incident opening template | ambiguous issue reports | failure_statement.md | topic00_failure_definition + lab01_ml_failure_diagnosis.py |
| Evidence collection | evidence completeness theory | logs/metrics/traces/config/data snapshot checklist | guess-driven debugging | evidence_bundle_index.md | topic01_evidence_collection + lab01_ml_failure_diagnosis.py |
| Experiment protocol | one-change causal inference theory | control-vs-variant run ledger | multiple changes hide root cause | option_compare_table.csv | topic02_experiment_design + lab04_option_compare_and_verify.py |
| ML debugging ladder | data-first root-cause theory | leakage, drift, and error-slice workflow | repeated model retraining without data fix | ml_root_cause.md | topic03_ml_debug + lab01_ml_failure_diagnosis.py |
| LLM debugging ladder | regression-set and output-contract theory | category-based prompt regression checks | local fix breaks important categories | prompt_regression_table.csv | topic04_llm_debug + lab02_llm_prompt_regression.py |
| RAG debugging ladder | retrieval vs generation isolation theory | retrieval-only then generation-only diagnostics | wrong subsystem is optimized | retrieval_diagnostics.csv + groundedness_delta.csv | topic05_rag_debug + lab03_rag_retrieval_failure.py |
| Verification gates | release gate and risk-control theory | gate checklist before decision | fix shipped with silent regressions | final_decision.md + gate_log | topic06_verification_gates + lab04_option_compare_and_verify.py |

Rule: each row must be reflected in chapter tutorials and stage scripts.

## 25) Stage 15 Lab Operability Contract (Command-Level)

- `lab01_ml_failure_diagnosis.py`
  - command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab01_ml_failure_diagnosis`
  - outputs: failure statement + root-cause report
  - pass: root cause is explicit and validated with identical eval protocol
- `lab02_llm_prompt_regression.py`
  - command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab02_llm_prompt_regression`
  - outputs: prompt regression table + fix note
  - pass: target improvement with no blocker category regression
- `lab03_rag_retrieval_failure.py`
  - command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab03_rag_retrieval_failure`
  - outputs: retrieval diagnostics + groundedness delta
  - pass: retrieval and groundedness both improve under one-change policy
- `lab04_option_compare_and_verify.py`
  - command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab04_option_compare_and_verify`
  - outputs: option comparison table + final decision log
  - pass: promote/hold/rollback decision is explicitly justified

## 26) Stage 15 Resource Expansion Checklist

Each module must cite at least:
- one troubleshooting operations source (SRE style)
- one ML evaluation source (scikit-learn/evidence tools)
- one monitoring/telemetry source (OpenTelemetry or equivalent)
- one retrieval operations source (Qdrant docs)
- one runtime debugging source (PyTorch CUDA notes)

## 27) Stage 15 Production Review Rubric (Stricter)

- every incident starts with measurable failure definition
- evidence bundle is complete before solution proposal
- at least two options are compared before final decision
- verification rerun uses same data/split/eval profile
- all decisions include before/after artifacts and signed label
