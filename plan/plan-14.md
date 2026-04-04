# Stage 14 Handbook Improvement Plan (v1)

Target file: red-book/AI-study-handbook-14.md  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve AI-study-handbook-14.md to be:
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

Stage-14-specific locked requirements:

- Enforce portfolio-risk-first implementation standards.
- Add execution realism and transaction-cost modeling workflow.
- Add drawdown, tail-risk, and stress-scenario diagnostics.
- Add governance and audit artifacts for strategy changes.

---

## 1) Review Summary (Current Chapter State)

### What is already strong

- Portfolio, risk, and execution components are present.
- Good transition from single prediction to system-level design.

### What still needs improvement

- Needs stronger risk controls and realistic execution assumptions.
- Needs auditability and compliance-oriented reporting.
- Needs stress testing and scenario analysis workflow.

---

## 2) Target Outcomes (Measurable)

Stage 14 rewrite is complete only when:

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
- Resource quality rule: use risk-first and transaction-cost-aware references.

### 3.1 Official Documentation (Primary)

- PyPortfolioOpt docs: https://pyportfolioopt.readthedocs.io/en/latest/
- CVXPY user guide: https://www.cvxpy.org/tutorial/index.html
- Backtrader docs: https://www.backtrader.com/docu/
- Backtesting.py docs: https://kernc.github.io/backtesting.py/
- pandas docs: https://pandas.pydata.org/docs/
- scikit-learn docs: https://scikit-learn.org/stable/
- statsmodels docs (time-series and diagnostics): https://www.statsmodels.org/stable/index.html
- PyTorch CUDA notes (GPU strategy simulation/training options): https://docs.pytorch.org/docs/stable/notes/cuda.html

### 3.2 Books (Quant + Risk)

- Advances in Financial Machine Learning: https://dev.store.wiley.com/en-us/Advances%2Bin%2BFinancial%2BMachine%2BLearning-p-00000140
- Designing Machine Learning Systems: https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- Practical MLOps: https://www.oreilly.com/library/view/practical-mlops/9781098103002/

### 3.3 Tutorials / Courses / Videos

- Backtesting.py examples/tutorials: https://kernc.github.io/backtesting.py/
- Backtrader examples/resources: https://www.backtrader.com/
- QuantStart articles (implementation patterns and pitfalls): https://www.quantstart.com/articles/

### 3.4 Practical Repos / Reference Implementations

- PyPortfolioOpt source: https://github.com/robertmartin8/PyPortfolioOpt
- Backtrader source: https://github.com/mementum/backtrader
- Backtesting.py source: https://github.com/kernc/backtesting.py
- CVXPY source: https://github.com/cvxpy/cvxpy

### 3.5 Resource-to-Chapter Mapping Rule (Mandatory)

- Every trading module must include a cost/slippage/stress reference from 3.1 or 3.3.
- Every optimization decision must include a risk-control citation and a reproducible code path.

---

## 4) Required Chapter Structure

1. System architecture for multi-asset trading
2. Signal generation and risk budgeting
3. Portfolio optimization and constraints
4. Execution simulation and slippage models
5. Performance/risk evaluation and stress testing
6. Failure analysis and strategy remediation
7. Operational governance and controls
8. Labs and production simulation

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

## 7) Stage 14 Script Package Plan (red-book/src/stage-14/)

Required files:

- README.md
- requirements.txt
- requirements-optional.txt
- run_all_stage14.ps1
- run_ladder_stage14.ps1
- verify_stage.ps1
- stage14_utils.py

Topic ladders:

- topic00*_trading_system_basics_*
- topic01*_signal_quality_*
- topic02*_risk_engine_*
- topic03*_portfolio_optimizer_*
- topic04*_execution_sim_*
- topic05*_stress_test_*
- topic06*_ops_governance_*

Labs:

- lab01_multi_asset_baseline.py
- lab02_risk_engine_improvement.py
- lab03_execution_slippage_impact.py
- lab04_stress_test_and_recovery.py

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
| Trading system basics | Profits in backtest vanish in live-like simulation | Look-ahead bias, unrealistic assumptions | Enforce time-safe pipeline and realistic execution assumptions | Backtest sanity checklist + bias tests | lab01_multi_asset_baseline.py |
| Signal quality | Signal decays after short period | Overfit factors, unstable feature regime | Add factor stability test and walk-forward validation | IC/IR stability across windows | lab01_multi_asset_baseline.py |
| Risk engine | Drawdowns exceed policy limits | Missing hard risk limits, weak stop logic | Add hard risk guardrails and kill-switch rules | Max DD, VaR/ES, breach count | lab02_risk_engine_improvement.py |
| Portfolio optimizer | Optimizer outputs unstable allocations | Ill-conditioned covariance, unconstrained objective | Add regularization + practical constraints + turnover limits | Turnover and risk-adjusted return delta | lab02_risk_engine_improvement.py |
| Execution simulation | Slippage and fees erase alpha | No transaction-cost model, optimistic fill assumptions | Add spread/impact/commission model and stress fill scenarios | Net alpha after cost vs before cost | lab03_execution_slippage_impact.py |
| Stress testing | Strategy fails in tail events | No scenario testing, narrow historical window | Run regime and shock stress tests before release | Stress scenario loss table | lab04_stress_test_and_recovery.py |
| Ops governance | Strategy changes are not auditable | Missing change log and approval process | Use strategy change request + review + approval gates | Audit trail completeness score | lab04_stress_test_and_recovery.py |

### 8.2 Required Matrix Usage Workflow

1. Run baseline strategy with full cost model enabled.
2. Identify top failure mode by risk-adjusted metrics.
3. Apply one risk/execution change and rerun identical period.
4. Validate improvement under stress scenarios.
5. Record governance decision and deployment status.

### 8.3 Mandatory Artifacts

- `results/stage14/risk_control_matrix.csv`
- `results/stage14/cost_impact_report.md`
- `results/stage14/stress_test_pack.md`

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

Stage 14 is accepted only if:

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

## 12) Operable Roadmap (Week 27-28)

### Week 27 (Foundation and Baseline)

Day 1:
- align learning targets with measurable outputs and acceptance gates

Day 2:
- run simple topic ladder scripts and capture baseline artifacts

Day 3:
- run intermediate topic ladder scripts and classify early failure patterns

Day 4:
- run advanced topic ladder scripts with one controlled stress/failure condition

Day 5:
- execute Lab 1 (lab01_multi_asset_baseline.py) and publish baseline evidence

Day 6:
- execute Lab 2 (lab02_risk_engine_improvement.py) and produce before/after comparison draft

Day 7:
- checkpoint review: identify gaps, prioritize fixes, and define rerun scope

### Week 28 (Verification and Release Readiness)

Day 8:
- execute Lab 3 (lab03_execution_slippage_impact.py) and complete incident/failure diagnosis notes

Day 9:
- compare at least two solution options with explicit tradeoffs

Day 10:
- apply one targeted change and rerun fixed test/eval/load set

Day 11:
- execute Lab 4 (lab04_stress_test_and_recovery.py) and generate release-readiness artifacts

Day 12:
- complete regression and gate checks; document residual risks

Day 13:
- finalize decision log (promote / hold / rollback)

Day 14:
- publish stage completion report and transition readiness note

---

## 13) Notebook and Visuals Plan

Notebook track (mandatory):

- stage14_notebook01_baseline.ipynb
- stage14_notebook02_intermediate_analysis.ipynb
- stage14_notebook03_advanced_failure_drill.ipynb
- stage14_notebook04_lab_walkthrough.ipynb

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

Lab 1: lab01_multi_asset_baseline.py

Goal:
- produce a reproducible baseline run with declared data, schema, and metrics.

Required outputs:
- one baseline metrics artifact (.csv or .json)
- one baseline narrative artifact (.md)

Lab 2: lab02_risk_engine_improvement.py

Goal:
- apply one controlled improvement and compare against the baseline.

Required outputs:
- one option-comparison artifact (solution_options/tradeoff)
- one before/after metric artifact

Lab 3: lab03_execution_slippage_impact.py

Goal:
- perform realistic failure diagnosis and produce verification rerun evidence.

Required outputs:
- one failure-class artifact
- one verification rerun artifact

Lab 4: lab04_stress_test_and_recovery.py

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

Mandatory gate thresholds for Stage 14:

- max_drawdown within predefined limit
- slippage_error within budget
- stress_scenario_loss within threshold
- audit_trail completeness = 100%

Hard-stop conditions:

- missing data/schema declaration in any lab output
- missing before/after artifact for improvement claims
- uncontrolled multi-change rerun
- missing decision log

---

## 16) Trading Risk and Execution Reliability Spec

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

Before Stage 15, learner must prove risk controls, execution realism, and stress-test recovery behavior with auditable artifacts.

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

Additive-only section to close remaining depth gaps for Stage 14.

Missing items that are now mandatory:
- deeper theory links between signal quality, risk, execution, and governance
- clearer topic-level failure signatures (not only strategy-level summaries)
- command-level runbook for all mandatory labs
- required artifact outputs for risk and stress validation
- stricter production review rubric for trading readiness

## 24) Stage 14 Module Deepening Backlog (Topic by Topic)

| Module | Theory to Add | Operatable Tutorial to Add | Typical Failure Signature | Required Evidence | Script/Lab Mapping |
|---|---|---|---|---|---|
| Data foundations | market data integrity and leakage theory | data audit and leak-safe split workflow | backtest optimism from leakage | data_audit.md + leakage_checks.csv | topic00_trading_system_basics + lab01_multi_asset_baseline.py |
| Signal quality | IC/IR stability and regime sensitivity theory | rolling-window factor diagnostics | alpha decay after regime shift | signal_stability_report.csv | topic01_signal_quality + lab01_multi_asset_baseline.py |
| Risk engine | VaR/ES and drawdown control theory | hard limit policy and kill-switch runbook | excessive drawdown and risk breaches | risk_control_matrix.csv | topic02_risk_engine + lab02_risk_engine_improvement.py |
| Portfolio optimizer | constrained optimization and turnover theory | regularized optimizer with practical constraints | unstable weights and turnover spikes | optimizer_constraint_report.md | topic03_portfolio_optimizer + lab02_risk_engine_improvement.py |
| Execution simulation | slippage, spread, and impact theory | cost-aware execution replay workflow | gross alpha disappears net of cost | slippage_decomposition.csv | topic04_execution_sim + lab03_execution_slippage_impact.py |
| Stress testing | tail-risk and scenario analysis theory | shock pack with recovery criteria | strategy collapse in extreme scenarios | stress_pack.md + recovery_runbook.md | topic05_stress_test + lab04_stress_test_and_recovery.py |

Rule: each row must appear in chapter tutorials and stage scripts.

## 25) Stage 14 Lab Operability Contract (Command-Level)

- `lab01_multi_asset_baseline.py`
  - command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab01_multi_asset_baseline`
  - outputs: baseline signal report + data audit
  - pass: baseline is leak-safe and signal diagnostics are stable
- `lab02_risk_engine_improvement.py`
  - command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab02_risk_engine_improvement`
  - outputs: risk before/after table + risk policy note
  - pass: risk breaches reduced while performance remains acceptable
- `lab03_execution_slippage_impact.py`
  - command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab03_execution_slippage_impact`
  - outputs: slippage decomposition + execution recommendation
  - pass: net-of-cost metrics remain above minimum threshold
- `lab04_stress_test_and_recovery.py`
  - command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab04_stress_test_and_recovery`
  - outputs: stress scenario pack + recovery playbook
  - pass: tail scenarios evaluated and operational recovery is clear

## 26) Stage 14 Resource Expansion Checklist

Each module must cite at least:
- one quantitative trading reference (optimization/backtesting/risk)
- one data/ML implementation reference (pandas/scikit-learn)
- one GPU/runtime reference when CUDA path is used
- one governance/operations reference for release and audit controls

## 27) Stage 14 Production Review Rubric (Stricter)

- leakage checks pass before any performance claim
- risk metrics satisfy policy thresholds in baseline and stress tests
- decisions are based on net-of-cost metrics, not gross-only metrics
- strategy changes are auditable with rollback readiness
- all improvements include before/after evidence artifacts

## 28) Stage 14 Expert-Tier Quant Addendum (Review Closure)

This section is additive-only and closes the remaining expert-tier gaps for Stage 14.

### 28.1 Point-in-Time Leakage Audit Gate (Mandatory)

Leakage must be treated as structural in quant pipelines, not only split overlap.

Required:
- add a formal Point-in-Time (PIT) audit to feature engineering workflow
- verify each feature timestamp is observable before prediction timestamp
- block model claims when PIT contract is violated

Mandatory artifact:
- `results/stage14/pit_audit_report.md`

Minimum PIT evidence fields:
- `feature_name`
- `feature_timestamp`
- `prediction_timestamp`
- `observable_before_prediction` (`true/false`)
- `violation_reason`

Hard gate:
- any PIT violation forces decision to `hold` or `rollback`.

### 28.2 Strategy Calibration Gate (S2_FilterNegative 130/30)

Stage 14 must use a strategy-specific hero example rather than generic classification/regression-only framing.

Required:
- calibrate labs to `S2_FilterNegative` portfolio logic (long-biased 130/30 with short-filter behavior)
- prove portfolio construction decisions follow filter policy
- explain short-leg exclusions for positive-score candidates under filter rules

Mandatory artifacts:
- `results/stage14/s2_filternegative_decision_log.csv`
- `results/stage14/portfolio_construction_130_30_report.md`

Lab binding:
- `lab02_risk_engine_improvement.py` must include short-filter policy checks and rejection reasons.

### 28.3 RTX 5090 Throughput Profiling Gate (LSTM Cross-Section)

Inference performance must be measured at cross-sectional scale, not single-ticker latency only.

Required:
- profile LSTM inference throughput for batched cross-sectional universe
- include Blackwell-targeted profiling using `nsys` where available
- diagnose bottlenecks (GPU compute, transfer, or CPU preprocessing/WSL I/O)

Mandatory artifacts:
- `results/stage14/batch_inference_latency_per_1k_tickers.csv`
- `results/stage14/lstm_blackwell_profile_summary.md`

Minimum metric fields:
- `batch_size`
- `tickers_count`
- `latency_ms_per_1k_tickers`
- `bottleneck_class`
- `device`

### 28.4 Net-of-Cost Decomposition Gate (Volatility-Aware)

Flat slippage assumptions are not sufficient for release decisions.

Required:
- decompose transaction cost into commission, spread, and market impact
- apply volatility-adjusted market-impact component (`lambda` term)
- report gross vs net alpha under identical replay period

Mandatory artifact:
- `results/stage14/slippage_decomposition.csv`

Required decomposition columns:
- `commission_cost`
- `spread_cost`
- `market_impact_lambda`
- `gross_return`
- `net_return`

### 28.5 Factor Neutrality and Hidden-Beta Gate

130/30 alpha must be validated against hidden factor exposures.

Required:
- evaluate model-return correlation against SPY and sector ETFs
- quantify unintended concentration (for example long tech/short energy drift)
- record mitigation action when exposure breaches limits

Mandatory artifacts:
- `results/stage14/factor_exposure_report.csv`
- `results/stage14/factor_neutrality_decision.md`

Hard gate:
- promotion blocked when factor exposure exceeds declared policy thresholds without mitigation evidence.

### 28.6 Stage 14 Expanded Hard Gates (Must All Pass)

Stage 14 is complete only when all below pass:

- PIT audit is clean and signed (`pit_audit_report.md`)
- S2_FilterNegative construction logic is evidenced (`portfolio_construction_130_30_report.md`)
- cross-sectional LSTM throughput profile is captured on target runtime path
- net-of-cost decomposition includes volatility-aware impact terms
- factor neutrality review is complete and signed
