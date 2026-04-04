# Stage 10 - Final AI System

**Week 18-20**

---

## 0) If This Chapter Feels Hard

Use this 4-pass method:

1. Pass 1: learn system boundaries and layer contracts only.
2. Pass 2: run baseline pipeline and collect artifacts.
3. Pass 3: diagnose one failure and verify one fix.
4. Pass 4: make a release decision with evidence.

This stage is systems engineering, not model-only learning.

---

## 1) Stage Goal

Build a production-style end-to-end AI system that integrates:

- market data ingestion
- feature engineering
- ML prediction
- retrieval/news context
- LLM reasoning
- API serving
- observability and operations

Reference project: **AI Trading Assistant**.

By the end of Stage 10, you must be able to:

- define strict contracts between all layers
- run baseline and improved versions with fixed evaluation policy
- localize failures to the correct layer
- troubleshoot using `identify -> compare -> verify`
- decide `promote`, `hold`, or `rollback` using gates

---

## 2) Prerequisites and Environment

### Required background

- Python and pandas basics
- ML training/evaluation basics
- LLM prompting basics
- basic API knowledge (FastAPI)

### Environment

- Python 3.10+
- optional CUDA GPU
- optional local vector DB (Qdrant)

### Core dependencies

- `pandas`, `numpy`, `scikit-learn`
- `fastapi`, `uvicorn`
- optional: `torch`, `qdrant-client`

### Data declaration (mandatory in all examples)

```text
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Split/Eval policy: <fixed split or fixed scenario set>
Type: <data/feature/ml/retrieval/llm/api/integration>
```

---

## 3) System Architecture and Layer Contracts

Reference flow:

`request -> data -> features -> ML signal -> retrieval context -> LLM reasoning -> API response -> telemetry`

### Contract-first rule

Each layer must define:

- input schema
- output schema
- owner
- validation rules
- failure behavior

### Contract map

| Layer | Input | Output | Owner | Common failure |
|---|---|---|---|---|
| Data | ticker/time range | OHLCV table | data module | missing values, schema drift |
| Features | OHLCV table | feature table | feature module | leakage, parity mismatch |
| ML | feature table | class/probability | model module | overfit, poor calibration |
| Retrieval | query/date | context bundle | retrieval module | stale or irrelevant context |
| LLM | ML signal + context | explanation JSON | reasoning module | unsupported claims |
| API | request payload | response payload | API module | schema mismatch, timeout |
| Ops | all events | logs/metrics/traces | ops module | missing correlation IDs |

If ownership is unclear, incident response becomes slow and unsafe.

---

## 4) End-to-End Workflow (Industry Standard)

Use this fixed workflow:

1. define objective and acceptance gates
2. lock data and evaluation policy
3. run baseline end to end
4. capture per-layer artifacts
5. identify bottleneck or failure layer
6. compare at least two fix options
7. apply one controlled change
8. rerun identical tests
9. compare before/after deltas
10. decide `promote`, `hold`, or `rollback`

### Minimum baseline metrics

- data quality: schema pass rate, missing rate
- ML quality: accuracy/F1/AUC (or MAE/RMSE)
- reasoning quality: format validity and rubric score
- system quality: p50/p95 latency, error rate

---

## 5) Module A - Data Layer

### What it is

Ingestion and normalization for structured market data and optional text/news data.

### Why it matters

Most downstream failures begin as data contract failures.

### Operatable checklist

1. enforce schema validation at ingest
2. handle missing values explicitly
3. version snapshots
4. log row count and date range

### Typical issues

- date gaps
- missing columns
- stale snapshots
- outlier spikes from bad source records

### Troubleshooting

- compare raw source vs normalized table
- isolate first invalid record
- rerun with same source version

### Metrics

- schema pass rate
- missing rate by column
- freshness lag

### Related scripts

- `topic01*_data_contracts_*`
- `lab02_pipeline_contract_validation.py`

---

## 6) Module B - Feature Layer

### What it is

Transforms normalized data into deterministic ML-ready features.

### Why it matters

Feature quality usually dominates model quality in tabular systems.

### Operatable checklist

1. compute features with deterministic rules
2. enforce train/inference parity
3. version feature list
4. validate leakage absence

### Typical issues

- target leakage
- inconsistent feature columns
- unstable rolling windows

### Troubleshooting

- compare train vs inference feature snapshots
- verify target alignment offsets
- run leakage tests

### Metrics

- feature null rate
- drift statistics
- leakage test pass/fail

### Related scripts

- `topic02*_feature_pipeline_*`

---

## 7) Module C - ML Prediction Layer

### What it is

Generates structured prediction signals (`class`, `probability`, optional confidence bands).

### Why it matters

This layer is the disciplined numeric signal engine.

### Operatable checklist

1. use fixed split or fixed CV
2. persist model and config versions
3. evaluate on holdout set
4. log probability distribution

### Typical issues

- low recall in critical class
- train/test gap
- unstable probabilities

### Troubleshooting

- segment confusion matrix analysis
- compare baseline vs tuned model
- verify class imbalance policy

### Metrics

- accuracy/F1/AUC or MAE/RMSE
- calibration score
- segment-level error analysis

### Related scripts

- `topic03*_ml_prediction_*`

---

## 8) Module D - Retrieval Context Layer

### What it is

Builds contextual evidence from news/documents for LLM grounding.

### Why it matters

Weak retrieval quality appears as LLM hallucination in final output.

### Operatable checklist

1. declare data source and chunk strategy
2. log retrieval latency and relevance@k
3. enforce freshness policy
4. track metadata filter effectiveness

### Typical issues

- stale context
- low relevance retrieval
- wrong metadata filters

### Troubleshooting

- inspect top-k retrieved snippets for failed cases
- rerun with fixed queries
- compare chunk/filter strategy options

### Metrics

- relevance@k
- retrieval latency
- freshness age

### Related scripts

- `topic04*_retrieval_context_*`

---

## 9) Module E - LLM Reasoning Layer

### What it is

Converts structured signals and evidence into controlled natural-language decisions.

### Why it matters

LLM output must be faithful to upstream signals and evidence.

### Operatable checklist

1. use structured prompt template
2. enforce output schema validation
3. include source attribution policy
4. add fallback behavior on invalid output

### Typical issues

- fluent but unsupported claims
- invalid JSON format
- contradiction with ML signal

### Troubleshooting

- compare failed outputs by prompt version
- validate evidence grounding
- apply one prompt policy change at a time

### Metrics

- format validity rate
- grounding score
- contradiction rate

### Related scripts

- `topic05*_llm_reasoning_*`

---

## 10) Module F - API and Operations Layer

### What it is

Exposes the pipeline as a service with telemetry, alerting, and release controls.

### Why it matters

A model is not usable in production without stable interface and observability.

### Operatable checklist

1. enforce request/response schemas
2. implement timeout/retry policy
3. emit logs/metrics/traces with run ID
4. define release and rollback gates

### Typical issues

- timeout spikes
- missing run correlation
- silent regressions after deployment

### Troubleshooting

- inspect endpoint latency by route
- trace failing requests across layers
- run controlled rollback drill

### Metrics

- p50/p95 latency
- error rate
- availability

### Related scripts

- `topic06*_api_serving_*`
- `topic08*_ops_release_*`

---

## 11) PyTorch and CUDA in Stage 10

### Why this is required

Even in hybrid ML + LLM systems, runtime behavior (device, memory, throughput) affects release decisions.

### Required checks

1. confirm device placement consistency
2. capture p50/p95 inference latency
3. test OOM handling and fallback path
4. compare CPU vs CUDA cost/performance profile

### Stage mapping

- `topic07*_evaluation_regression_*`
- `lab03_incident_diagnosis_and_fix.py` (runtime branch)

---

## 12) Example Complexity Scale

- L1 Simple: single-path run and one metric family
- L2 Intermediate: baseline vs improved comparison on fixed test set
- L3 Advanced: failure injection + tradeoff analysis + release decision

Where complexity is:

- data/schema complexity
- cross-layer dependency complexity
- compute/memory complexity
- evaluation complexity
- operations complexity

---

## 13) Stage 10 Script Mapping

Target package: `red-book/src/stage-10/`

Topic ladders:

- `topic00*_integration_flow_*`
- `topic01*_data_contracts_*`
- `topic02*_feature_pipeline_*`
- `topic03*_ml_prediction_*`
- `topic04*_retrieval_context_*`
- `topic05*_llm_reasoning_*`
- `topic06*_api_serving_*`
- `topic07*_evaluation_regression_*`
- `topic08*_ops_release_*`

Labs:

- `lab01_end_to_end_baseline.py`
- `lab02_pipeline_contract_validation.py`
- `lab03_incident_diagnosis_and_fix.py`
- `lab04_baseline_to_production_integration.py`

All scripts must:

- print data/schema declaration
- include detailed functional comments
- run deterministically
- generate artifacts under `results/`

---

## 14) Practice Labs (Detailed and Operatable)

## Lab 1: End-to-End Baseline

Goal:

- run complete pipeline and capture baseline metrics.

Required workflow:

1. fix dataset and evaluation scope
2. run baseline pipeline
3. collect per-layer outputs
4. store baseline metrics and sample outputs

Required outputs:

- `results/lab1_baseline_outputs.jsonl`
- `results/lab1_layer_metrics.csv`
- `results/lab1_system_metrics.csv`

## Lab 2: Pipeline Contract Validation

Goal:

- enforce strict schema/contract checks and localize contract failures.

Required outputs:

- `results/lab2_contract_checks.csv`
- `results/lab2_failure_cases.csv`
- `results/lab2_contract_fix_report.md`

## Lab 3: Incident Diagnosis and Fix

Goal:

- execute troubleshooting loop on one injected incident.

Required outputs:

- `results/lab3_incident_baseline.csv`
- `results/lab3_solution_options.csv`
- `results/lab3_verification_rerun.csv`
- `results/lab3_decision.md`

## Lab 4: Baseline to Production Integration

Goal:

- move from baseline to release-ready state with gates.

Required outputs:

- `results/lab4_baseline_outputs.jsonl`
- `results/lab4_improved_outputs.jsonl`
- `results/lab4_layer_metrics.csv`
- `results/lab4_solution_options.csv`
- `results/lab4_verification_report.md`
- `results/lab4_production_readiness.md`

---

## 15) Troubleshooting Standard (Identify -> Compare -> Verify)

Use this exact process:

1. reproduce with fixed run ID and fixed test set
2. classify failure layer (`data`, `feature`, `ml`, `retrieval`, `llm`, `api`, `ops`)
3. collect evidence (logs, metrics, traces, outputs)
4. compare two solution options
5. apply one targeted change only
6. rerun same tests
7. verify deltas and make decision

Required run log fields:

- run ID
- data/model/prompt/config versions
- latency/quality/cost metrics
- failure class
- selected fix and decision

---

## 16) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Data contracts | pipeline breaks after source update | schema drift, weak validation | strict schema gates and versioning | `lab02_pipeline_contract_validation.py` |
| Feature pipeline | model unstable in production | leakage or parity mismatch | parity checks and feature lock | `topic02*_feature_pipeline_*` |
| ML signal | strong train but weak live behavior | overfit, bad threshold | segment analysis and threshold tuning | `topic03*_ml_prediction_*` |
| Retrieval context | explanation uses weak evidence | stale or low relevance context | retrieval diagnostics and freshness SLO | `topic04*_retrieval_context_*` |
| LLM reasoning | fluent but unfaithful output | weak prompt constraints | schema validation and grounding checks | `topic05*_llm_reasoning_*` |
| API ops | latency and timeout storms | no backpressure or tracing | timeout/retry policy plus tracing | `topic06*_api_serving_*` |
| Release decisions | regressions after release | no fixed rerun gate | baseline/improved gate policy | `lab04_baseline_to_production_integration.py` |

---

## 17) Self-Test (Readiness)

You should answer with concrete workflow:

1. How do you enforce contracts across all layers?
2. How do you identify the layer that caused a bad final recommendation?
3. Which metrics must pass before promotion?
4. How do you prevent LLM drift from ML signals?
5. How do you handle CUDA failure while keeping service available?
6. What is your one-change rerun protocol?
7. What exactly triggers rollback?
8. How do you compare two fix options fairly?

If you cannot answer at least 6/8 operationally, rerun labs 2-4.

---

## 18) Resource Library

- FastAPI: https://fastapi.tiangolo.com/
- Pandas: https://pandas.pydata.org/docs/
- scikit-learn: https://scikit-learn.org/stable/
- Qdrant: https://qdrant.tech/documentation/
- PyTorch CUDA semantics: https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch AMP recipe: https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- OpenTelemetry: https://opentelemetry.io/docs/

---

## 19) What Comes After Stage 10

Stage 11 focuses on infrastructure operations and scaling. You carry forward:

- contract-first system design
- evidence-based troubleshooting
- measurable release decisions
- baseline-to-production improvement discipline

## 20) Missing-Item Gap Closure (Stage 10 Addendum)

This section closes the remaining gaps and makes Stage 10 execution-ready.

Mandatory additions for this chapter:
- Topic-level deepening for each module, not only architecture-level summary.
- Command-level lab operation details with pass/fail signals.
- Explicit failure signatures so students know what bad behavior looks like.
- Required evidence artifacts for every improvement claim.
- Stronger topic -> script -> lab -> artifact mapping.
- Stricter production gate criteria tied to measurable thresholds.

## 21) Stage 10 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Data Layer | Data contract, freshness, null/type policy, schema drift | Run schema validator before every integration run; block on critical violations | Schema mismatch, stale snapshots, mixed timezone assumptions | `results/stage10/data_validation_report.md` | `topic01_data_contracts` + `lab02_pipeline_contract_validation.py` |
| Feature Layer | Train-serve feature parity and leakage prevention | Use one transform library for offline/online; run parity check with fixed seed | Offline feature value differs from online value for same sample | `results/stage10/feature_parity.csv` | `topic02_feature_pipeline` + `lab02_pipeline_contract_validation.py` |
| ML Prediction Layer | Fixed-split evaluation and regression control | Compare baseline vs candidate on same split and same seed | Candidate improves one metric but degrades stability/generalization | `results/stage10/before_after_metrics.csv` | `topic03_ml_prediction` + `lab03_incident_diagnosis_and_fix.py` |
| Retrieval Context Layer | Chunk/filter/top-k/rerank tradeoff in RAG | Tune one parameter at a time using fixed evaluation questions | Low recall, irrelevant context, retrieval latency jump | `results/stage10/retrieval_eval.csv` | `topic04_retrieval_context` + `lab03_incident_diagnosis_and_fix.py` |
| LLM Reasoning Layer | Grounded reasoning and output contract enforcement | Require citation format and response schema checks | Fluent but unsupported answer, format-breaking output | `results/stage10/citation_coverage.csv` | `topic05_llm_reasoning` + `lab03_incident_diagnosis_and_fix.py` |
| API/Ops Layer | SLO, canary, rollback logic and release governance | Run canary gate and rollback drill before any promote decision | p95 spikes, timeout bursts, error-rate drift after rollout | `results/stage10/release_decision.md` + `rollback_drill.md` | `topic06_api_serving` + `lab04_baseline_to_production_integration.py` |

## 22) Stage 10 Lab Operation Runbook (Command-Level)

### Lab 1: End-to-End Baseline
- Command: `pwsh red-book/src/stage-10/run_all_stage10.ps1 -Lab lab01_end_to_end_baseline`
- Required outputs:
  - `results/stage10/baseline_metrics.csv`
  - `results/stage10/baseline_runbook.md`
- Pass criteria:
  - All core layer contracts pass.
  - Baseline run is reproducible with same seed/config.
- First troubleshooting action:
  - If contract checks fail, run `topic01_data_contracts` standalone and fix schema violations first.

### Lab 2: Pipeline Contract Validation
- Command: `pwsh red-book/src/stage-10/run_all_stage10.ps1 -Lab lab02_pipeline_contract_validation`
- Required outputs:
  - `results/stage10/contract_violation_report.md`
  - `results/stage10/feature_parity.csv`
- Pass criteria:
  - No critical schema violation.
  - Feature parity delta under declared threshold.
- First troubleshooting action:
  - Pin transform version and rerun parity check with identical seed.

### Lab 3: Incident Diagnosis and Fix
- Command: `pwsh red-book/src/stage-10/run_all_stage10.ps1 -Lab lab03_incident_diagnosis_and_fix`
- Required outputs:
  - `results/stage10/incident_evidence.md`
  - `results/stage10/before_after_metrics.csv`
- Pass criteria:
  - One-change fix improves target metric.
  - No blocker regressions on fixed eval suite.
- First troubleshooting action:
  - Split diagnosis into retrieval-only and reasoning-only before changing both.

### Lab 4: Baseline to Production Integration
- Command: `pwsh red-book/src/stage-10/run_all_stage10.ps1 -Lab lab04_baseline_to_production_integration`
- Required outputs:
  - `results/stage10/release_decision.md`
  - `results/stage10/rollback_drill.md`
- Pass criteria:
  - Promote/hold/rollback is explicitly justified by evidence.
  - Rollback path is tested, not theoretical.
- First troubleshooting action:
  - If gates conflict, set decision to `hold` and assign remediation owner/date.

## 23) Stage 10 Resource-to-Module Mapping (Must Cite in Chapter Text)

- Contracts/API: FastAPI + Pydantic docs
- Data quality: Great Expectations docs
- Baseline ML/eval: scikit-learn user guide
- Retrieval stack: Qdrant docs and examples
- Observability: OpenTelemetry + Prometheus + Grafana
- Runtime behavior: PyTorch CUDA notes

Requirement: each Stage 10 module tutorial must cite at least one resource above as required reading.

## 24) Stage 10 Production Review Rubric (Hard Gates)

A Stage 10 improvement can be promoted only if all gates pass:
- `contract_pass_rate >= 99%`
- `quality_regression <= 2%` vs baseline
- `p95_latency <= 2.5s` under declared load profile
- rollback drill completed before final decision
- all claims have before/after evidence artifacts

If any hard gate fails: default decision is `hold` or `rollback`, never `promote`.
