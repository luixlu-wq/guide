# Stage 12 - AI System Architecture Patterns

**Week 22**

---

## 0) If This Chapter Feels Hard

Use this sequence:

1. Learn the decision criteria first (not tools first).
2. Understand what problem each pattern is designed to solve.
3. Run one fixed comparison before debating architecture choices.
4. Diagnose one failure and verify one fix with rerun evidence.

This stage is architecture reasoning + operational verification.

---

## 1) Stage Goal

Choose the right architecture for the right problem, with explicit tradeoffs.

You must be able to:

- compare `llm_app`, `rag`, `agent`, `multi_agent` using common metrics
- explain why one pattern is better for a given requirement profile
- write ADRs that teams can audit and reuse
- identify failure ownership by component
- run `identify -> compare -> verify` troubleshooting workflow
- make `promote/hold/rollback` release decisions

---

## 2) Architecture Selection Framework (Theory + Practice)

### Pattern-selection dimensions

Evaluate each candidate on:

- task complexity
- knowledge freshness requirement
- need for grounded citations
- need for tool/action execution
- latency and cost limits
- operational complexity tolerance
- safety and governance requirements

### Core architecture tradeoff theory

- simpler architectures reduce failure surface and operating cost
- richer architectures increase capability but add coordination risk
- architecture choice should minimize total system risk, not maximize "feature count"

### Fast decision heuristic

- **LLM app** if task is language transformation and does not need private retrieval/tool actions
- **RAG** if grounded answers over changing/private knowledge are required
- **Agent** if dynamic tool selection and multi-step actions are required
- **Multi-agent** if role specialization is required and measurable

If two options are close in quality, choose the simpler one.

---

## 3) ADR Workflow (Mandatory)

Use one ADR for each architecture decision:

1. context and constraints
2. options considered
3. tradeoff table (quality, latency, cost, risk)
4. chosen option and rationale
5. known risks and mitigations
6. acceptance gates
7. rollback trigger
8. validation/rerun plan

No ADR means no audit trail, weak team alignment, and difficult incident recovery.

---

## 4) Module A - LLM App Pattern

### Conceptual model

Direct prompt-response with strict boundary controls:

`input validation -> prompt policy -> model -> output validation -> response`

### Best use cases

- explanation, rewrite, summarize
- low orchestration tasks
- latency-sensitive experiences with constrained scope

### Typical failure

- fluent but unsupported or policy-violating outputs

### Root causes

- weak prompt constraints
- missing schema and policy checks
- no fallback response path

### Resolution pattern

- structured prompts + strict response schema + policy validator + fallback template

### Related scripts

- `topic01*_llm_app_pattern_*`
- `lab01_pattern_baseline_compare.py`

---

## 5) Module B - RAG Pattern

### Conceptual model

`query -> retrieve -> rerank/filter -> context pack -> generation -> cite`

### Key theory

RAG quality is bounded by retrieval quality. Generation cannot reliably recover from irrelevant or stale retrieved context.

### Best use cases

- private enterprise documents
- changing policy/knowledge bases
- citation-required answers

### Typical failure

- wrong or stale answer with confident tone

### Root causes

- stale index
- weak chunking strategy
- poor metadata filters
- missing freshness governance

### Resolution pattern

- retrieval diagnostics + freshness SLO + chunk/filter redesign + rerun evaluation

### Related scripts

- `topic02*_rag_pattern_*`
- `lab02_rag_vs_agent_failure_drill.py`

---

## 6) Module C - Agent Pattern

### Conceptual model

`state -> plan -> select tool -> execute -> observe -> update state -> stop/continue`

### Key theory

Agents increase capability by adding decision loops, but they also increase uncertainty and failure modes.

### Best use cases

- dynamic tool routing
- multi-step workflows
- action-taking systems requiring conditional branching

### Typical failure

- tool loop, wrong tool, invalid tool parameters

### Root causes

- weak tool schema contracts
- no step budget
- weak stop conditions
- missing action audit logs

### Resolution pattern

- constrained function schemas + step limits + stop policies + tool success metrics

### Related scripts

- `topic03*_agent_pattern_*`
- `lab02_rag_vs_agent_failure_drill.py`

---

## 7) Module D - Multi-Agent Pattern

### Conceptual model

`orchestrator -> specialist agents -> shared artifacts -> synthesis -> decision`

### Key theory

Multi-agent systems help when role specialization is truly needed; otherwise they add coordination latency and conflict risk.

### Best use cases

- clear role separation (planner, researcher, critic, executor)
- traceable division of responsibilities
- tasks where one-agent baseline is proven insufficient

### Typical failure

- role overlap and contradictory outputs

### Root causes

- unclear responsibilities
- weak coordination protocol
- no shared-state discipline

### Resolution pattern

- role contracts + explicit handoff protocol + unified acceptance gates

### Related scripts

- `topic04*_multi_agent_pattern_*`
- `lab01_pattern_baseline_compare.py`

---

## 8) Module E - Runtime and Performance Evidence (PyTorch/CUDA)

Architecture decisions are incomplete without runtime evidence.

### Why this matters

- a high-quality architecture that misses latency/cost gates still fails in production
- runtime behavior determines practical viability under concurrency

### Required runtime checks

1. baseline p50/p95 latency per pattern
2. device consistency (`cpu` vs `cuda`)
3. memory pressure behavior and recovery policy
4. quality/latency/cost tradeoff comparison

### Stage 12 implementation note

Pattern comparison scripts include runtime benchmark artifacts:

- `topic05a_pattern_comparison_simple.py`
- `topic05_pattern_comparison_intermediate.py`
- `topic05c_pattern_comparison_advanced.py`

Outputs include `*_cuda_metrics.csv` for runtime evidence.

---

## 9) Module F - Safety and Governance

### Mandatory control points

- input schema validation
- retrieval and tool safety checks
- output policy validation
- decision/audit logging
- release gates and rollback triggers

### Governance rule

If architecture behavior cannot be audited, it cannot be trusted in production.

### Related scripts

- `topic06*_safety_governance_*`
- `topic07*_release_rollback_*`

---

## 10) Data Declaration Standard (Mandatory)

Every example must include:

```text
Data: <name and source>
Requests/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed eval set and replay method>
Type: <llm_app/rag/agent/multi_agent/comparison>
```

---

## 11) Example Complexity Scale

- L1 Simple: one pattern, one path, one metric family
- L2 Intermediate: fixed pattern comparison with common evaluation set
- L3 Advanced: failure injection + tradeoff decision + release gate

Where complexity is:

- routing/orchestration logic
- retrieval quality and freshness management
- tool execution safety and stability
- runtime latency/memory behavior
- governance and release controls

---

## 12) Stage 12 Script Mapping

Target package: `red-book/src/stage-12/`

Topics:

- `topic00*_architecture_decision_*`
- `topic01*_llm_app_pattern_*`
- `topic02*_rag_pattern_*`
- `topic03*_agent_pattern_*`
- `topic04*_multi_agent_pattern_*`
- `topic05*_pattern_comparison_*`
- `topic06*_safety_governance_*`
- `topic07*_release_rollback_*`

Labs:

- `lab01_pattern_baseline_compare.py`
- `lab02_rag_vs_agent_failure_drill.py`
- `lab03_architecture_decision_record.py`
- `lab04_pattern_to_production.py`

All scripts must:

- print data/schema declarations
- include clear functional comments
- generate deterministic artifacts in `results/`
- include interpretation output for decisions

---

## 13) Practice Labs (Detailed, Operatable)

## Lab 1: Pattern Baseline Compare

Goal:

- compare `llm_app`, `rag`, `agent`, `multi_agent` on one fixed evaluation set

Required workflow:

1. run lab baseline
2. inspect quality/latency/cost/failure metrics
3. compare by fixed criteria table
4. summarize recommendation and caveats

Required outputs:

- `results/lab1_pattern_metrics.csv`
- `results/lab1_tradeoff_matrix.csv`
- `results/lab1_pattern_summary.md`

Success criteria:

- recommendation is metric-backed and includes tradeoffs

## Lab 2: RAG vs Agent Failure Drill

Goal:

- reproduce realistic failure modes and verify targeted fixes

Required workflow:

1. execute failure replay cases
2. classify each failure (`retrieval`, `routing`, `tool`, `schema`)
3. propose two fix options
4. apply one option per failure group
5. rerun and verify deltas

Required outputs:

- `results/lab2_failure_cases.csv`
- `results/lab2_solution_options.csv`
- `results/lab2_verification_rerun.csv`

Success criteria:

- at least one key reliability metric improves with evidence

## Lab 3: Architecture Decision Record

Goal:

- produce a complete ADR with quantified alternatives

Required workflow:

1. define constraints and decision criteria
2. score each option with fixed weights
3. select one option and document rationale
4. define risks, gates, and rollback triggers

Required outputs:

- `results/lab3_decision_scores.csv`
- `results/lab3_adr.md`

Success criteria:

- ADR is complete and supports independent review

## Lab 4: Pattern to Production

Goal:

- move selected architecture from baseline to release decision

Required workflow:

1. capture baseline KPI snapshot
2. apply one targeted improvement
3. rerun and produce comparison deltas
4. evaluate release gates
5. publish release and rollback decisions

Required outputs:

- `results/lab4_baseline_metrics.csv`
- `results/lab4_improved_metrics.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_release_decision.md`
- `results/lab4_rollback_plan.md`

Success criteria:

- release decision is explicit and reversible

---

## 14) Troubleshooting Playbook (Identify -> Compare -> Verify)

1. **Identify**
   - reproduce with fixed test set and run id
   - mark failed stage (`input`, `retrieve`, `route`, `tool`, `runtime`, `output`)
2. **Compare**
   - design two fix options with expected quality/latency/cost impact
   - choose one minimal-risk change
3. **Verify**
   - rerun the same tests
   - compare deltas against acceptance gates
   - decide `promote`, `hold`, or `rollback`

---

## 15) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Pattern choice | team chooses trend, not fit | no objective scorecard | ADR + weighted decision matrix | `lab03_architecture_decision_record.py` |
| RAG quality | answer quality drifts over time | stale index/weak filters | diagnostics + freshness governance | `lab02_rag_vs_agent_failure_drill.py` |
| Agent reliability | unstable tool behavior | weak schema/guardrails | tool policy + step budget + audits | `lab02_rag_vs_agent_failure_drill.py` |
| Multi-agent complexity | overhead > benefit | role overlap/weak protocol | strict role contracts + handoff rules | `lab01_pattern_baseline_compare.py` |
| Release decisions | promotion without evidence | no fixed baseline/rerun gates | gate-based promote/hold/rollback | `lab04_pattern_to_production.py` |

---

## 16) Self-Test (Readiness)

You should answer with concrete operations detail:

1. How do you select between LLM app, RAG, agent, and multi-agent?
2. What must an ADR include for architecture governance?
3. How do you assign failure ownership by architecture component?
4. How do runtime metrics (including CUDA evidence) affect pattern choice?
5. What controls prevent unsafe tool execution?
6. How do you compare architecture options fairly?
7. What evidence is required for promotion?
8. What exact conditions trigger rollback?

If fewer than 6/8 are answerable with concrete workflow, rerun labs 1-4.

---

## 17) Resource Library

- LangChain docs: https://python.langchain.com/docs/
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- LlamaIndex docs: https://docs.llamaindex.ai/
- OpenAI Evals guide: https://platform.openai.com/docs/guides/evals
- NIST AI RMF: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- PyTorch CUDA semantics: https://docs.pytorch.org/docs/stable/notes/cuda.html

---

## 18) What Comes After Stage 12

Stage 13 moves from architecture decisions to capstone-grade implementation and delivery.

You carry forward:

- architecture selection discipline
- ADR and governance practice
- failure diagnosis and rerun verification
- release-gate and rollback discipline

## 19) Missing-Item Gap Closure (Stage 12 Addendum)

This section closes remaining gaps and makes Stage 12 architecture decisions operatable.

Mandatory additions for this chapter:
- weighted tradeoff scoring instead of intuition-based pattern choice
- explicit failure signatures for LLM app/RAG/agent/multi-agent patterns
- command-level runbook for pattern comparison and release checks
- stricter governance and rollback requirement for architecture choices

## 20) Stage 12 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Architecture Selection | Quality/latency/cost/risk/maintainability tradeoff model | Build weighted ADR scorecard before coding | Pattern selected by trend without evidence | `results/stage12/final_adr.md` + `scorecard.csv` | `topic00_architecture_decision` + `lab03_architecture_decision_record.py` |
| LLM App Pattern | I/O contract and fallback strategy | Run edge-case suite with strict schema validation | Good demo but output breaks on edge inputs | `results/stage12/llm_edge_case_report.csv` | `topic01_llm_app_pattern` + `lab01_pattern_baseline_compare.py` |
| RAG Pattern | Retrieval-grounding dependency theory | Tune retrieval on fixed queries; enforce citation-required answers | Fluent but unsupported response | `results/stage12/retrieval_grounding_eval.csv` | `topic02_rag_pattern` + `lab02_rag_vs_agent_failure_drill.py` |
| Agent Pattern | Planning/tool-use risks and bounded autonomy | Apply tool allowlist, max-step, timeout, escalation policy | Looping behavior or unsafe tool actions | `results/stage12/agent_trace_report.md` | `topic03_agent_pattern` + `lab02_rag_vs_agent_failure_drill.py` |
| Multi-Agent Pattern | Role specialization vs coordination overhead | Define role contracts and handoff arbitration policy | Handoff churn and latency blow-up | `results/stage12/handoff_latency_report.csv` | `topic04_multi_agent_pattern` + `lab04_pattern_to_production.py` |
| Safety/Governance | Shift-left policy controls and release blockers | Run policy gate before any promote recommendation | Late compliance blocker discovered pre-release | `results/stage12/release_gate_report.md` | `topic06_safety_governance` + `lab04_pattern_to_production.py` |

## 21) Stage 12 Lab Operation Runbook (Command-Level)

### Lab 1: Pattern Baseline Compare
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab01_pattern_baseline_compare`
- Required outputs:
  - `results/stage12/pattern_baseline_table.csv`
  - `results/stage12/initial_decision.md`
- Pass criteria:
  - All patterns evaluated under same data/prompt/eval protocol.
- First troubleshooting action:
  - Lock seed, prompt version, and evaluator before rerun.

### Lab 2: RAG vs Agent Failure Drill
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab02_rag_vs_agent_failure_drill`
- Required outputs:
  - `results/stage12/failure_trace.md`
  - `results/stage12/option_compare.csv`
- Pass criteria:
  - Root cause isolated and verified via one-change rerun.
- First troubleshooting action:
  - Separate retrieval diagnosis from planning diagnosis.

### Lab 3: Architecture Decision Record
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab03_architecture_decision_record`
- Required outputs:
  - `results/stage12/final_adr.md`
  - `results/stage12/scorecard.csv`
- Pass criteria:
  - ADR includes alternatives, weighted scoring, and rollback trigger.
- First troubleshooting action:
  - If scores tie, add operational risk weight and recalculate.

### Lab 4: Pattern to Production
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab04_pattern_to_production`
- Required outputs:
  - `results/stage12/release_gate_report.md`
  - `results/stage12/rollback_simulation.md`
- Pass criteria:
  - Release recommendation is traceable to evidence and policy gates.
- First troubleshooting action:
  - If governance gates fail, decision must be `hold`.

## 22) Stage 12 Resource-to-Module Mapping (Must Cite in Chapter Text)

- ADR process: adr.github.io
- Retrieval: Qdrant docs
- Agent orchestration: LangGraph docs
- Retrieval orchestration: LlamaIndex docs
- Safety: OWASP Top 10 for LLM Apps
- Runtime evidence: PyTorch CUDA notes
- Experiment tracking: MLflow docs

Requirement: each major Stage 12 module tutorial must cite at least one source above.

## 23) Stage 12 Production Review Rubric (Hard Gates)

- final ADR includes weighted score and rollback trigger
- selected pattern beats baseline on primary target metric
- safety/governance gates pass before release recommendation
- all comparisons use fixed evaluation protocol
- all claims include before/after evidence artifacts

If any hard gate fails: decision cannot be `promote`.
