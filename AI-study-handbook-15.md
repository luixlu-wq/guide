# Stage 15 - When Model Does Not Work as Expected

**Week 26**

---

## 0) If This Chapter Feels Hard

Use this sequence:

1. define failure precisely with metrics
2. classify failure domain
3. collect evidence before changing anything
4. compare solution options
5. apply one change and rerun

This chapter is about disciplined diagnosis, not random tuning.

---

## 1) Stage Goal

Build a procedural and auditable troubleshooting system for ML, LLM, and RAG stacks.

You must be able to:

- define failure in measurable terms
- localize root causes with evidence
- run controlled experiments
- compare solution options with tradeoffs
- verify improvements by rerun
- decide promotion, hold, or rollback

### Mandatory Workflow: ICV Protocol (Identify -> Compare -> Verify)

Every incident and lab must follow the same named workflow:

1. `Identify`: measurable failure statement with threshold and reproducible case
2. `Compare`: at least two controlled options under fixed eval profile
3. `Verify`: rerun failing case with selected fix and publish before/after delta

No troubleshooting ticket is complete without an explicit ICV audit trail.

---

## 2) Failure Definition Standard

### Bad definition

`the model is bad`

### Good definition

- test F1 dropped from 0.71 to 0.58
- p95 latency increased from 0.9s to 2.4s
- JSON validity dropped from 97% to 72%
- RAG grounding score dropped below threshold

### Required failure statement template

```text
Observed symptom:
Affected metric(s):
Where observed (train/test/live):
When started:
Suspected domain:
Confidence level:
```

If the failure is vague, the fix will be vague.

---

## 3) Root-Cause Taxonomy

Classify every incident into one primary domain:

- data quality
- feature logic
- target definition
- ML training/evaluation
- LLM prompt/output control
- RAG retrieval/indexing
- runtime/infrastructure
- monitoring/governance
- hardware resource contention (WSL2/CUDA boundary)

### Why this matters

Domain classification narrows search space and avoids random tuning loops.

WSL2/CUDA contention note:

- throughput drops after long sessions may be runtime-resource problems (memory ballooning, CUDA context pressure, throttling), not model logic faults.

---

## 4) Evidence Collection Standard

Required evidence per incident:

- run ID and config versions
- data snapshot/version
- model/prompt/index version
- baseline vs current metrics
- sample failing cases
- logs/metrics/traces where applicable

### Evidence table template

| Evidence type | Source | Collected? | Notes |
|---|---|---|---|
| Metrics delta | eval report | yes/no | |
| Sample failures | output logs | yes/no | |
| Config diff | repo/config store | yes/no | |
| Runtime profile | telemetry | yes/no | |

No change should be applied without this evidence set.

---

## 5) Controlled Experiment Protocol

Use one-change experiments only.

### Required process

1. define hypothesis
2. select one variable to change
3. keep all other variables fixed
4. run fixed evaluation set
5. compare against baseline
6. record outcome and next action

### Anti-pattern

Changing model, data, and prompt at the same time makes root-cause attribution impossible.

---

## 6) Module A - ML Debugging Ladder

### Typical ML failure patterns

- underfitting
- overfitting
- class imbalance failure
- calibration failure
- data drift

### Operatable ladder

1. compare train vs validation vs test metrics
2. inspect confusion matrix by segment
3. inspect feature leakage and target alignment
4. test threshold and calibration changes
5. rerun and verify metric deltas

### Related scripts

- `topic03*_ml_debug_*`
- `lab01_ml_failure_diagnosis.py`

---

## 7) Module B - LLM Debugging Ladder

### Typical LLM failure patterns

- instruction non-compliance
- format violations
- hallucinated unsupported claims
- unstable outputs across similar prompts

### Operatable ladder

1. enforce prompt template and output schema
2. inspect failing prompts and responses
3. compare prompt variants on fixed case set
4. apply one policy change
5. rerun and verify format/quality metrics

### Related scripts

- `topic04*_llm_debug_*`
- `lab02_llm_prompt_regression.py`

---

## 8) Module C - RAG Debugging Ladder

### Typical RAG failure patterns

- irrelevant retrieval
- stale documents
- filter mismatch
- context packing failure

### Operatable ladder

1. inspect retrieved top-k for failed cases
2. measure relevance@k and freshness age
3. compare chunking/filter/index options
4. apply one retrieval change
5. rerun and verify grounding metrics

### Related scripts

- `topic05*_rag_debug_*`
- `lab03_rag_retrieval_failure.py`

---

## 9) Module D - Verification Gates and Regression Control

### Required verification gates

- quality metrics meet threshold
- latency and error budgets respected
- no severe regressions in safety or format
- failure class resolved or reduced

### Decision outcomes

- `promote` if gates pass
- `hold` if mixed or uncertain
- `rollback` if regression detected

### Related scripts

- `topic06*_verification_gates_*`
- `topic07*_postmortem_*`
- `lab04_option_compare_and_verify.py`

---

## 10) PyTorch and CUDA in Troubleshooting

### Why this is required

Runtime issues can mimic model-quality failures.

### Required checks

1. verify device consistency
2. inspect memory utilization and OOM events
3. compare CPU vs CUDA latency and stability
4. validate fallback behavior under runtime failure

Runtime diagnostics must be part of incident evidence.

---

## 11) Data Declaration Standard

Every example must include:

```text
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed replay set>
Type: <ml/llm/rag/runtime/verification>
```

---

## 12) Example Complexity Scale

- L1 Simple: diagnose one failure in one domain
- L2 Intermediate: compare two fixes on fixed evaluation set
- L3 Advanced: cross-domain failure chain with release decision

Where complexity is:

- root-cause attribution
- experiment isolation
- runtime interactions
- verification governance

---

## 13) Stage 15 Script Mapping

Target package: `red-book/src/stage-15/`

Topics:

- `topic00*_failure_definition_*`
- `topic01*_evidence_collection_*`
- `topic02*_experiment_design_*`
- `topic03*_ml_debug_*`
- `topic04*_llm_debug_*`
- `topic05*_rag_debug_*`
- `topic06*_verification_gates_*`
- `topic07*_postmortem_*`

Labs:

- `lab01_ml_failure_diagnosis.py`
- `lab02_llm_prompt_regression.py`
- `lab03_rag_retrieval_failure.py`
- `lab04_option_compare_and_verify.py`

Script requirements:

- detailed functional comments
- deterministic reruns
- explicit failure handling
- artifact generation in `results/`

---

## 14) Practice Labs (Detailed)

## Lab 1: ML Failure Diagnosis

Goal:

- diagnose one ML failure and verify one targeted fix.

Required outputs:

- `results/lab1_ml_baseline_metrics.csv`
- `results/lab1_ml_failure_analysis.md`
- `results/lab1_ml_verification_rerun.csv`

## Lab 2: LLM Prompt Regression

Goal:

- identify and fix prompt/output regression.

Required outputs:

- `results/lab2_prompt_cases.csv`
- `results/lab2_prompt_options.csv`
- `results/lab2_prompt_verification.csv`
- `results/stage15/lab02_prompt_regression.md` (golden-set regression report)

## Lab 3: RAG Retrieval Failure

Goal:

- diagnose retrieval weakness and verify improvement.
- run one GIS/tourism boundary failure drill and isolate projection vs retrieval-config root cause.

Required outputs:

- `results/lab3_retrieval_baseline.csv`
- `results/lab3_retrieval_options.csv`
- `results/lab3_retrieval_verification.csv`
- `results/stage15/lab03_gis_boundary_failure_report.md`
- `results/stage15/lab03_projection_vs_topk_compare.csv`

## Lab 4: Option Compare and Verify

Goal:

- compare two solution options and make final decision.

Required outputs:

- `results/lab4_solution_compare.csv`
- `results/lab4_verification_rerun.csv`
- `results/lab4_decision_record.md`
- `results/stage15/lab04_final_y_statement.md`

---

## 15) Troubleshooting Playbook (Identify -> Compare -> Verify)

1. identify: reproduce and classify failure
2. compare: evaluate at least two remediation options
3. verify: rerun fixed tests and validate deltas

ICV audit trail block (mandatory in all lab outputs):

```text
Identify:
  - failure metric and threshold
  - reproducible failing case ID
Compare:
  - option A vs option B (fixed eval profile)
  - risk/cost tradeoff
Verify:
  - before/after delta table
  - promote/hold/rollback recommendation
```

Required run record fields:

- run ID and version set
- failure class and evidence
- selected option and rationale
- before/after metrics
- final decision

---

## 16) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Failure definition | teams cannot agree on issue | vague symptoms | strict metric-based failure template | `lab01_ml_failure_diagnosis.py` |
| Evidence quality | random fixes do not hold | missing baseline and config diffs | mandatory evidence checklist | `topic01*_evidence_collection_*` |
| Experiment design | no causal conclusion | many changes at once | one-change experiment protocol | `topic02*_experiment_design_*` |
| LLM reliability | unstable output format | weak schema enforcement | prompt + schema + validation policy | `lab02_llm_prompt_regression.py` |
| RAG quality | answers not grounded | poor retrieval/index freshness | retrieval diagnostics and freshness policy | `lab03_rag_retrieval_failure.py` |
| Final decisions | regressions after fix | no verification gates | gate-based promote/hold/rollback | `lab04_option_compare_and_verify.py` |

---

## 17) Self-Test (Readiness)

1. Can you define failure precisely with metrics?
2. Can you classify root cause domain confidently?
3. Can you design one-change experiments?
4. Can you verify improvements by rerun?
5. Can you separate quality failures from runtime failures?
6. Can you justify promote/hold/rollback decisions?

If fewer than 5/6 are operationally answerable, rerun labs 2-4.

---

## 18) Resource Library

- scikit-learn model selection: https://scikit-learn.org/stable/model_selection.html
- PyTorch tutorials: https://pytorch.org/tutorials/
- W and B docs: https://docs.wandb.ai/
- MLflow docs: https://mlflow.org/docs/latest/
- Evidently docs: https://docs.evidentlyai.com/

---

## 19) What Comes After Stage 15

Stage 16 focuses on mastery-level engineering practice, leadership, and portfolio readiness.

## 20) Missing-Item Gap Closure (Stage 15 Addendum)

This section closes remaining gaps and makes Stage 15 troubleshooting fully operatable.

Mandatory additions for this chapter:
- clearer failure-definition and evidence standards per module
- explicit failure signatures and anti-patterns
- command-level lab runbook with verification requirements
- stronger option-compare and promote/hold/rollback discipline

## 21) Stage 15 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Failure Definition | measurable threshold-based failure statement theory | open each incident with metric threshold + reproduction steps | ambiguous issue report, no pass/fail condition | `results/stage15/ml_failure_statement.md` | `topic00_failure_definition` + `lab01_ml_failure_diagnosis.py` |
| Evidence Collection | evidence completeness and traceability theory | collect logs/metrics/traces/config/data snapshot before solution proposal | guess-driven debugging without baseline | `results/stage15/evidence_bundle_index.md` | `topic01_evidence_collection` + `lab01_ml_failure_diagnosis.py` |
| Controlled Experiments | one-change causal inference in debugging | maintain control-vs-variant ledger with fixed eval profile | multiple simultaneous changes hide root cause | `results/stage15/option_compare_table.csv` | `topic02_experiment_design` + `lab04_option_compare_and_verify.py` |
| ML Debug Ladder | data-first diagnosis (drift/leakage/slice analysis) | run data checks before model tuning | repeated retrain attempts with no stable gain | `results/stage15/ml_root_cause.md` | `topic03_ml_debug` + `lab01_ml_failure_diagnosis.py` |
| LLM Debug Ladder | category regression and output contract theory | evaluate prompts on fixed category suite and schema checks | local prompt fix breaks important categories | `results/stage15/prompt_regression_table.csv` | `topic04_llm_debug` + `lab02_llm_prompt_regression.py` |
| RAG Debug Ladder | retrieval-vs-generation isolation theory | diagnose retrieval first, then generation on same eval set | wrong subsystem gets optimized | `results/stage15/retrieval_diagnostics.csv` + `groundedness_delta.csv` | `topic05_rag_debug` + `lab03_rag_retrieval_failure.py` |
| Verification Gates | release gate and regression blocking theory | enforce gate checklist before final decision | fix appears good but causes silent regressions | `results/stage15/final_decision.md` | `topic06_verification_gates` + `lab04_option_compare_and_verify.py` |

## 22) Stage 15 Lab Operation Runbook (Command-Level)

### Lab 1: ML Failure Diagnosis
- Command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab01_ml_failure_diagnosis`
- Required outputs:
  - `results/stage15/ml_failure_statement.md`
  - `results/stage15/ml_root_cause.md`
  - `results/stage15/lab01_wsl_cuda_contention_report.md`
  - `results/stage15/lab01_gpu_telemetry_log.csv`
- Pass criteria:
  - Root cause is explicit and verified on fixed eval protocol.
  - Runtime throughput degradation is classified as logic vs WSL2/CUDA contention with evidence.
- First troubleshooting action:
  - Expand slice analysis and leakage checks before changing model hyperparameters.

Resource-contention drill (mandatory):
- reproduce a long-session throughput drop case
- inspect `nvidia-smi` telemetry and `nsys` summary (or equivalent trace evidence)
- decide whether cause is model logic, CUDA context pressure, or WSL2 memory contention

### Lab 2: LLM Prompt Regression
- Command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab02_llm_prompt_regression`
- Required outputs:
  - `results/stage15/prompt_regression_table.csv`
  - `results/stage15/prompt_fix_note.md`
  - `results/stage15/lab02_prompt_regression.md`
- Pass criteria:
  - Target improvement with no blocker category regressions.
  - Golden-set pass rate for high-priority project facts remains `100%` after prompt fix.
- First troubleshooting action:
  - Compare at least two prompt alternatives before deciding.

### Lab 3: RAG Retrieval Failure
- Command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab03_rag_retrieval_failure`
- Required outputs:
  - `results/stage15/retrieval_diagnostics.csv`
  - `results/stage15/groundedness_delta.csv`
  - `results/stage15/lab03_gis_boundary_failure_report.md`
  - `results/stage15/lab03_projection_vs_topk_compare.csv`
- Pass criteria:
  - Retrieval and groundedness both improve under one-change policy.
  - Boundary-case root cause is explicitly classified:
    - projection mismatch (`NAD83/WGS84`) OR
    - retrieval configuration (`Top-K`/ranking/filter)
- First troubleshooting action:
  - Revisit chunking and citation contract if groundedness remains low.

### Lab 4: Option Compare and Verify
- Command: `pwsh red-book/src/stage-15/run_all_stage15.ps1 -Lab lab04_option_compare_and_verify`
- Required outputs:
  - `results/stage15/option_compare_table.csv`
  - `results/stage15/final_decision.md`
  - `results/stage15/lab04_final_y_statement.md`
- Pass criteria:
  - Decision explicitly selects `promote`, `hold`, or `rollback` with evidence.
  - Final decision is documented in Y-Statement ADR format:
    - "In the context of `<project>`, we decided to use `<option>` to fix `<failure>`, because `<evidence>`, and `<measured delta>`."
- First troubleshooting action:
  - If options tie, pick lower-risk option and require follow-up validation.

## 23) Stage 15 Resource-to-Module Mapping (Must Cite in Chapter Text)

- Operational troubleshooting: SRE references
- ML evaluation and diagnostics: scikit-learn evaluation docs
- Data contract validation: Great Expectations docs
- Drift and monitoring patterns: Evidently docs
- Telemetry evidence: OpenTelemetry docs
- Retrieval operations: Qdrant docs
- Runtime debugging: PyTorch CUDA notes

Requirement: each module tutorial must cite at least one mapped source.

## 24) Stage 15 Production Review Rubric (Hard Gates)

- every incident starts with measurable failure statement
- evidence bundle complete before selecting fix
- at least two options compared before final decision
- verification rerun uses same data/split/eval profile
- all decisions include before/after artifacts and signed label
- ICV protocol audit trail is present for every lab decision
- Lab 1 includes WSL2/CUDA contention evidence when runtime degradation is observed
- Golden-set pass rate for prompt fixes is `>= 100%` on high-priority protected cases
- Final decision artifact uses Y-Statement ADR format

If any hard gate fails: decision cannot be `promote`.
