# Stage 13 - Capstone Delivery Project

**Week 23**

---

## 0) If This Chapter Feels Hard

Use this execution sequence:

1. define capstone scope and non-goals
2. lock architecture contracts and milestone gates
3. run baseline integration
4. improve one bottleneck with evidence
5. prepare production readiness package

This stage is about delivery quality, not only technical completion.

---

## 1) Stage Goal

Ship a capstone AI system as an auditable project with engineering discipline.

Capstone reference: **AI Trading Assistant End-to-End Delivery**.

You must be able to:

- manage project milestones with explicit entry/exit criteria
- validate integration contracts across all layers
- produce baseline and improved evidence packs
- run incident response and escalation workflow
- make release decisions from objective gates
- prove hardware-bound runtime safety under concurrent load (RTX 5090 class)

---

## 2) Capstone Scope and Non-Goals

### In scope

- end-to-end integration from data to API
- measurable quality/latency/cost objectives
- deterministic rerun and verification process
- production-readiness review artifacts
- hardware saturation control (VRAM/temperature/SM utilization) as release evidence
- WSL2 boundary performance validation for data and service I/O

### Out of scope

- infinite model tuning without gates
- architecture changes without ADR
- ad-hoc releases without rollback criteria

### Delivery principle

`working demo` is not enough. `repeatable and auditable operation` is required.

---

## 3) Capstone Architecture Contract Map

Core flow:

`data -> features -> model -> context -> reasoning -> API -> monitoring`

Each component must provide:

- input schema
- output schema
- version metadata
- owner
- failure behavior

Boundary performance contract (WSL2):

- if large capstone data is loaded from `/mnt/c/`, run a boundary performance check
- if boundary I/O causes gate breach, capstone cannot pass production readiness
- heavy data/index/model artifacts must be moved to native Linux filesystem before release gate
- validate WSL2 service-to-client boundary latency before release signoff

Capstone integration schema (code-first, mandatory):

- Every capstone must provide `results/stage13/contract_definitions.json`.
- Schema must define handoff contracts for `features -> model -> context`.

Pydantic-style reference contract:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class FeaturePayload(BaseModel):
    run_id: str
    entity_id: str
    feature_vector: List[float]
    feature_version: str
    projection: Optional[str] = None  # e.g., "WGS84" or "NAD83" for GIS tasks

class ModelPayload(BaseModel):
    run_id: str
    entity_id: str
    score: float
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str

class ContextPayload(BaseModel):
    run_id: str
    entity_id: str
    context_ids: List[str]
    citations: List[str]
    context_version: str
    grounded: bool

class CapstoneContract(BaseModel):
    features: FeaturePayload
    model: ModelPayload
    context: ContextPayload
```

`contract_definitions.json` must be the serialized contract reference used by integration checks.

### Owner mapping example

| Component | Owner | On-failure responsibility |
|---|---|---|
| Data ingestion | Data owner | source validation and freshness |
| Feature pipeline | ML owner | parity and leakage controls |
| Prediction service | ML owner | calibration and drift checks |
| Context service | Retrieval owner | index freshness and relevance |
| Reasoning service | LLM owner | format validity and grounding |
| API gateway | Platform owner | schema, timeout, retry |
| Observability | Ops owner | logs/metrics/traces and alerts |

---

## 4) Milestone Plan with Gates

## Milestone 1: Baseline Integration

Entry:

- all layer contracts defined

Exit:

- baseline pipeline run completed
- baseline artifact set produced

## Milestone 2: Improvement Cycle

Entry:

- bottleneck identified with evidence

Exit:

- one controlled change applied
- before/after delta report produced

## Milestone 3: Incident Readiness

Entry:

- runbook and alert definitions available

Exit:

- one incident drill completed
- escalation and rollback exercised

## Milestone 4: Production Readiness

Entry:

- all previous milestones accepted

Exit:

- release recommendation documented
- rollback plan approved

---

## 5) Module A - Contract Validation

### What it is

Validation of interface contracts between capstone components.

### Why it matters

Integration failures are usually contract failures, not algorithm failures.

### Operatable steps

1. execute schema checks for each interface
2. validate required fields and types
3. validate version compatibility
4. fail fast on mismatch

### Typical issues

- missing required fields
- incompatible schema versions
- silent type coercion errors

### Related scripts

- `topic01*_contracts_validation_*`
- `lab01_capstone_baseline.py`

---

## 6) Module B - Integration Pipeline

### What it is

Controlled orchestration of all capstone components with run ID tracking.

### Why it matters

Without deterministic orchestration, debugging and verification are unreliable.

### Operatable steps

1. lock config versions
2. run full baseline pipeline
3. persist per-layer outputs
4. produce integrated metrics summary

### Typical issues

- hidden dependency mismatch
- inconsistent intermediate outputs
- non-deterministic behavior

### Related scripts

- `topic02*_integration_pipeline_*`
- `lab01_capstone_baseline.py`

---

## 7) Module C - Evaluation Pack

### What it is

A standard evidence package combining technical and product metrics.

### Required evidence

- quality metrics by layer
- latency p50/p95 by endpoint
- failure classification counts
- cost profile snapshot

### Why it matters

Capstone decisions must be reviewable by others.

### Related scripts

- `topic03*_evaluation_pack_*`
- `lab02_capstone_improvement_cycle.py`

---

## 8) Module D - Incident Workflow and Escalation

### What it is

Structured incident response workflow with owner escalation.

### Escalation model

1. detect alert breach
2. classify domain and severity
3. assign owner and incident commander
4. compare fix options
5. apply one controlled change
6. verify and close with postmortem

### Severity levels

- Sev1: customer-impacting outage
- Sev2: major degradation
- Sev3: localized or non-critical issue

### Related scripts

- `topic04*_incident_workflow_*`
- `lab03_capstone_incident_response.py`

---

## 9) Module E - Release Readiness

### What it is

Formal go/no-go decision based on objective gates.

### Required release gates

- contract validation pass
- quality metric thresholds pass
- latency/error thresholds pass
- critical incidents resolved
- rollback procedure validated

### Decision outcomes

- `promote`
- `hold`
- `rollback`

### Related scripts

- `topic05*_release_readiness_*`
- `lab04_capstone_production_readiness.py`

---

## 10) PyTorch and CUDA in Capstone Delivery

### Why this is required

Runtime behavior directly affects service-level gates.

### Required checks

1. verify device placement consistency
2. compare CPU vs CUDA latency profile
3. test OOM and fallback behavior
4. include runtime evidence in release review

### Capstone rule

No performance claim is accepted without measured runtime artifacts.

---

## 11) Data Declaration Standard

Every example must include:

```text
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed run and replay>
Type: <contract/integration/evaluation/incident/release>
```

---

## 12) Example Complexity Scale

- L1 Simple: single path and baseline artifact
- L2 Intermediate: baseline vs improved comparison
- L3 Advanced: incident simulation plus release decision

Where complexity is:

- cross-component dependencies
- run coordination and reproducibility
- runtime and latency behavior
- governance and release decisions

---

## 13) Stage 13 Script Mapping

Target package: `red-book/src/stage-13/`

Topics:

- `topic00*_capstone_scope_*`
- `topic01*_contracts_validation_*`
- `topic02*_integration_pipeline_*`
- `topic03*_evaluation_pack_*`
- `topic04*_incident_workflow_*`
- `topic05*_release_readiness_*`

Labs:

- `lab01_capstone_baseline.py`
- `lab02_capstone_improvement_cycle.py`
- `lab03_capstone_incident_response.py`
- `lab04_capstone_production_readiness.py`

Script requirements:

- detailed functional comments
- deterministic reruns
- explicit failure handling
- artifact generation in `results/`

---

## 14) Practice Labs (Detailed)

## Lab 1: Capstone Baseline

Goal:

- complete baseline run and produce initial evidence pack.
- establish hardware-safe and domain-valid baseline before any improvement cycle.

Required outputs:

- `results/lab1_capstone_baseline_metrics.csv`
- `results/lab1_capstone_layer_outputs.jsonl`
- `results/lab1_capstone_contract_status.csv`
- `results/stage13/hardware_saturation_log.jsonl`
- `results/stage13/contract_definitions.json`
- `results/stage13/domain_baseline_checks.md`
- `results/stage13/wsl_boundary_performance.csv`

Domain-specific baseline constraints (mandatory):

- choose one domain profile and declare it at run start:
  - `maptogo_tour_guide`
  - `ontario_gis`
- if `maptogo_tour_guide`: include no-hallucination check against Baidu Baike-backed source set
- if `ontario_gis`: include coordinate projection validation (NAD83 vs WGS84 mismatch detection)

Hardware saturation log minimum fields:

- `timestamp`
- `run_id`
- `sm_utilization`
- `vram_allocated_mb`
- `gpu_temp_c`
- `request_concurrency`

## Lab 2: Capstone Improvement Cycle

Goal:

- improve one bottleneck via controlled change.

Required outputs:

- `results/lab2_solution_options.csv`
- `results/lab2_before_after_delta.csv`
- `results/lab2_improvement_decision.md`

## Lab 3: Capstone Incident Response

Goal:

- run one realistic incident drill with escalation process.
- diagnose one AI-specific silent failure and close with verified mitigation.

Required outputs:

- `results/lab3_incident_timeline.csv`
- `results/lab3_root_cause_analysis.md`
- `results/lab3_verification_rerun.csv`
- `results/stage13/semantic_drift_incident_report.md`
- `results/stage13/semantic_drift_trace_evidence.md`

Mandatory incident scenario:

- one of:
  - semantic drift after new data/index ingestion (retrieval quality drops silently)
  - tool-loop/runaway tool-calling behavior
- use OpenTelemetry traces to show where failure appeared and why fix works

## Lab 4: Capstone Production Readiness

Goal:

- complete release readiness review with rollback plan.

Required outputs:

- `results/lab4_release_gate_checklist.csv`
- `results/lab4_release_decision.md`
- `results/lab4_rollback_plan.md`

---

## 15) Troubleshooting Workflow (Identify -> Compare -> Verify)

1. reproduce with fixed run ID and fixed test set
2. classify failure domain (`contract`, `integration`, `runtime`, `quality`, `ops`)
3. gather logs, metrics, traces, sample outputs
4. compare two remediation options
5. apply one change only
6. rerun same tests
7. verify deltas and update release decision

---

## 16) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Project delivery | team ships demo, not system | no gates, weak ownership | milestone gates and owner map | `lab01_capstone_baseline.py` |
| Integration | hidden contract mismatches | unversioned interfaces | strict contract validation | `lab01_capstone_baseline.py` |
| Improvement | random tuning cycles | no controlled change protocol | one-change rerun policy | `lab02_capstone_improvement_cycle.py` |
| Incident response | slow and chaotic recovery | unclear escalation | severity model and runbook | `lab03_capstone_incident_response.py` |
| Release | subjective go/no-go decisions | missing gate evidence | release checklist and rollback plan | `lab04_capstone_production_readiness.py` |

---

## 17) Self-Test (Readiness)

1. Can you define capstone non-goals and avoid scope creep?
2. Can you prove interface compatibility across layers?
3. Can you produce baseline and improved evidence packs?
4. Can you run incident escalation with explicit ownership?
5. Can you justify release decision with objective gates?
6. Can you execute rollback safely?

If fewer than 5/6 are actionable, rerun labs 2-4.

---

## 18) Resource Library

- MLflow docs: https://mlflow.org/docs/latest/
- DVC docs: https://dvc.org/doc
- Backtesting.py docs: https://kernc.github.io/backtesting.py/
- FastAPI docs: https://fastapi.tiangolo.com/
- OpenTelemetry docs: https://opentelemetry.io/docs/

---

## 19) What Comes After Stage 13

Stage 14 upgrades delivery into hedge-fund-style portfolio and risk operations.

## 20) Missing-Item Gap Closure (Stage 13 Addendum)

This section closes remaining gaps and makes Stage 13 capstone delivery truly operatable.

Mandatory additions for this chapter:
- milestone-level gating with explicit evidence requirements
- stronger module-level failure signatures for integration/release work
- command-level capstone lab operations
- stricter go/no-go and rollback proof standards

## 21) Stage 13 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Scope and Non-Goals | Scope control and delivery risk theory | Freeze MVP scope and require change request for additions | Scope creep and gate misses | `results/stage13/milestone_gate_tracker.md` | `topic00_capstone_scope` + `lab01_capstone_baseline.py` |
| Contract Validation | Contract ownership/versioning in multi-module systems | Run CI contract tests at every boundary | Integration failures from schema mismatch | `results/stage13/contract_ci_report.md` | `topic01_contracts_validation` + `lab01_capstone_baseline.py` |
| Integration Pipeline | Progressive integration strategy (unit->integration->system) | Execute staged test pipeline with fixed seeded inputs | Late-stage regressions after small changes | `results/stage13/integration_regression_report.csv` | `topic02_integration_pipeline` + `lab02_capstone_improvement_cycle.py` |
| Evaluation Pack | Reproducibility and confidence framing | Compare baseline/candidate under fixed eval profile | Irreproducible claims across reruns | `results/stage13/evaluation_pack.md` | `topic03_evaluation_pack` + `lab02_capstone_improvement_cycle.py` |
| Incident Workflow | Role-based incident command and escalation theory | Run incident drill with timeline and owner checkpoints | Chaotic response and unclear ownership | `results/stage13/incident_timeline.md` | `topic04_incident_workflow` + `lab03_capstone_incident_response.py` |
| Release Readiness | Go/no-go decision discipline and rollback theory | Run release checklist and rollback simulation before promote | Launch decision with incomplete evidence | `results/stage13/final_release_review.md` + `rollback_drill.md` | `topic05_release_readiness` + `lab04_capstone_production_readiness.py` |

## 22) Stage 13 Lab Operation Runbook (Command-Level)

### Lab 1: Capstone Baseline
- Command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab01_capstone_baseline`
- Required outputs:
  - `results/stage13/baseline_scope_contracts.md`
  - `results/stage13/baseline_metrics.csv`
  - `results/stage13/hardware_saturation_log.jsonl`
  - `results/stage13/contract_definitions.json`
- Pass criteria:
  - Scope/contract baseline is complete and reproducible.
  - Hardware saturation baseline is captured and within release-safe envelope.
  - Domain baseline checks (MapToGo no-hallucination or Ontario GIS projection validation) pass.
- First troubleshooting action:
  - Freeze seed/data versions and rerun baseline before tuning anything.

### Lab 2: Capstone Improvement Cycle
- Command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab02_capstone_improvement_cycle`
- Required outputs:
  - `results/stage13/improvement_delta.csv`
  - `results/stage13/improvement_note.md`
- Pass criteria:
  - One controlled change produces measurable improvement.
- First troubleshooting action:
  - If mixed outcomes, run option comparison and hold release.

### Lab 3: Capstone Incident Response
- Command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab03_capstone_incident_response`
- Required outputs:
  - `results/stage13/incident_timeline.md`
  - `results/stage13/postmortem.md`
  - `results/stage13/semantic_drift_incident_report.md`
- Pass criteria:
  - Response flow complete, prevention actions assigned.
  - Incident is AI-specific (`semantic_drift` or `tool_loop`) with OpenTelemetry evidence.
- First troubleshooting action:
  - Re-run simulation if ownership/escalation paths were unclear.

### Lab 4: Capstone Production Readiness
- Command: `pwsh red-book/src/stage-13/run_all_stage13.ps1 -Lab lab04_capstone_production_readiness`
- Required outputs:
  - `results/stage13/final_release_review.md`
  - `results/stage13/rollback_drill.md`
- Pass criteria:
  - Signed go/no-go with rollback proof.
  - Final release review includes reconciled ADR Y-Statement:
    - "In the context of <project>, we decided to use <choice> because <evidence/tradeoff>, and accepted <consequence>."
- First troubleshooting action:
  - If any gate missing, decision defaults to `hold`.

## 23) Stage 13 Resource-to-Module Mapping (Must Cite in Chapter Text)

- Delivery and reliability metrics: DORA references
- Reproducible pipelines: DVC learning resources
- Experiment tracking: MLflow docs
- Incident/SLO fundamentals: SRE references
- Contracts/API implementation: FastAPI docs
- Retrieval system operations: Qdrant docs
- Runtime evidence: PyTorch CUDA notes

Requirement: each module tutorial must cite at least one mapped source.

## 24) Stage 13 Production Review Rubric (Hard Gates)

- all milestone gates complete with required artifacts
- one full improvement cycle with measurable delta
- one full incident drill with postmortem quality check
- signed go/no-go with rollback proof
- all claims tied to before/after evidence artifacts
- hardware saturation gate passes:
  - `vram_utilization_threshold < 90%` at gate load profile
  - `sm_clock_throttle_count = 0` during release candidate load test
- WSL2 boundary performance gate passes:
  - capstone heavy data/index/model assets are not served from `/mnt/c/` in release profile
- semantic-incident gate passes:
  - at least one `semantic_drift` or `tool_loop` drill resolved with trace evidence
- release review includes final ADR Y-Statement with owner signoff

If any hard gate fails: decision cannot be `promote`.
