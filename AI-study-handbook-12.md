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
9. mandatory Y-Statement with measured evidence links

No ADR means no audit trail, weak team alignment, and difficult incident recovery.

Mandatory ADR final output format:

> In the context of `<project>`, we decided to use `<choice>` to handle `<problem>`, because `<reasoning>`, and `<measured outcome>`.

Minimum required evidence links for ADR approval:

- weighted scorecard (`quality`, `latency`, `cost`, `risk`)
- rerun comparison artifact on fixed eval protocol
- explicit rollback trigger with threshold

---

## 4) Module A - LLM App Pattern

### Conceptual model

Direct prompt-response with strict boundary controls:

`input validation -> prompt policy -> model -> output validation -> response`

### Input/output schema block (code-first)

```json
{
  "input_schema": {
    "task_id": "string",
    "user_query": "string",
    "language": "string",
    "policy_profile": "string"
  },
  "output_schema": {
    "response_text": "string",
    "confidence": "number",
    "policy_flags": "array<string>",
    "trace_id": "string"
  }
}
```

### Worked example (minimal contract check)

```python
payload = {
    "task_id": "llm_app_001",
    "user_query": "Explain moving average crossover in simple terms.",
    "language": "en",
    "policy_profile": "standard"
}
required = {"task_id", "user_query", "language", "policy_profile"}
missing = required.difference(payload.keys())
if missing:
    raise ValueError(f"Input schema violation: missing={sorted(missing)}")
```

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

### Input/output schema block (code-first)

```json
{
  "input_schema": {
    "query": "string",
    "top_k": "integer",
    "allowed_scopes": "array<string>",
    "freshness_hours_max": "integer"
  },
  "output_schema": {
    "answer": "string",
    "citations": "array<object>",
    "retrieval_latency_ms": "number",
    "trace_id": "string"
  }
}
```

### Worked example (retrieval contract check)

```python
retrieval_output = {
    "answer": "The policy requires quarterly refresh.",
    "citations": [{"doc_id": "policy_2026_q1", "chunk_id": "c17"}],
    "retrieval_latency_ms": 82.5,
    "trace_id": "trace_rag_001",
}
if not retrieval_output["citations"]:
    raise ValueError("RAG output invalid: citations required")
```

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

### Input/output schema block (code-first)

```json
{
  "input_schema": {
    "task_id": "string",
    "goal": "string",
    "max_steps": "integer",
    "tool_allowlist": "array<string>"
  },
  "output_schema": {
    "status": "string",
    "steps_used": "integer",
    "tool_calls": "array<object>",
    "final_answer": "string",
    "trace_id": "string"
  }
}
```

### Worked example (local circuit breaker for loop safety)

```python
MAX_STEPS = 8
MAX_REPEATED_TOOL_ERRORS = 3
tool_errors = 0

for step in range(1, MAX_STEPS + 1):
    result = call_tool_safely()
    if not result["ok"]:
        tool_errors += 1
    if tool_errors >= MAX_REPEATED_TOOL_ERRORS:
        return {
            "status": "fallback",
            "final_answer": "Tool path unstable; switched to safe fallback.",
            "steps_used": step,
        }

return {"status": "complete", "steps_used": MAX_STEPS}
```

This guard is mandatory for local high-power runs so loop spirals do not pin GPU and starve other processes.

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

### Input/output schema block (code-first)

```json
{
  "input_schema": {
    "orchestrator_task_id": "string",
    "request": "string",
    "target_agent": "string",
    "context_refs": "array<string>"
  },
  "output_schema": {
    "handoff_status": "string",
    "agent_response": "object",
    "handoff_latency_ms": "number",
    "trace_id": "string"
  }
}
```

### Worked example (A2A handoff payload)

```json
{
  "orchestrator_task_id": "mtg_route_203",
  "request": "Validate Ontario subdivision geometry before itinerary publish",
  "target_agent": "gis_validation_agent",
  "context_refs": ["geojson_batch_2026_04_04", "route_plan_203"],
  "trace_id": "trace_a2a_203"
}
```

If this handoff contract is missing, multi-agent reliability cannot be audited.

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
- `topic08*_a2a_mcp_interop_*`
- `topic09*_blackwell_nvfp4_prefix_cache_*`
- `topic10*_owasp_llm_v2_security_*`

Labs:

- `lab01_pattern_baseline_compare.py`
- `lab02_rag_vs_agent_failure_drill.py`
- `lab03_architecture_decision_record.py`
- `lab04_pattern_to_production.py`
- `lab05_a2a_mcp_interoperability.py`
- `lab06_blackwell_nvfp4_prefix_caching.py`
- `lab07_owasp_llm_v2_redteam.py`
- `lab08_gis_projection_and_loop_breaker.py`

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

## Lab 5: A2A + MCP Interoperability

Goal:

- validate cross-agent handoff contracts and tool interoperability contracts.

Required workflow:

1. define agent cards for each specialist role
2. simulate A2A handoff events on a fixed task
3. validate MCP tool schemas and safety constraints
4. publish interoperability trace evidence

Required outputs:

- `results/agent_card_registry.json`
- `results/a2a_handoff_trace.jsonl`
- `results/mcp_tool_contracts.md`

Success criteria:

- handoff and tool-contract behavior is traceable and auditable.

## Lab 6: Blackwell NVFP4 + Prefix Caching

Goal:

- measure quality/latency tradeoff for NVFP4 and prefix-caching loop optimization.

Required workflow:

1. run fixed eval set on baseline precision path
2. run same eval set on NVFP4 path
3. run loop latency profile with and without prefix caching
4. compare tradeoff and document recommendation

Required outputs:

- `results/nvfp4_throughput_quality.csv`
- `results/prefix_cache_latency_profile.csv`
- `results/agent_loop_latency_report.md`

Success criteria:

- recommended runtime path is evidence-backed, not speed-only.

## Lab 7: OWASP LLM v2 Security Drill

Goal:

- run red-team scenarios for indirect injection and unbounded consumption.

Required workflow:

1. replay indirect prompt-injection cases
2. verify containment and policy guard response
3. replay high-consumption loop pressure
4. verify budget/stop guards and fallback behavior

Required outputs:

- `results/indirect_injection_case_log.jsonl`
- `results/unbounded_consumption_guard.csv`
- `results/owasp_llm_v2_redteam_report.md`

Success criteria:

- security drill results include explicit containment evidence.

## Lab 8: GIS Projection Validation + Loop Breaker

Goal:

- ensure Ontario GIS coordinate correctness and prevent reasoning/tool call spirals.

Required workflow:

1. inject projection mismatch cases (for example NAD83 vs WGS84)
2. validate schema/projection guard behavior
3. simulate repeated tool-loop attempts
4. verify loop breaker and mobile latency guard behavior

Required outputs:

- `results/geojson_schema_guard_failures.csv`
- `results/loop_breaker_events.jsonl`
- `results/coordinate_projection_validation_report.md`
- `results/mobile_latency_guard_report.md`

Success criteria:

- incorrect projection responses are blocked and loop spirals are terminated safely.

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

### Lab 5: A2A + MCP Interoperability
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab05_a2a_mcp_interoperability`
- Required outputs:
  - `results/stage12/agent_card_registry.json`
  - `results/stage12/a2a_handoff_trace.jsonl`
  - `results/stage12/mcp_tool_contracts.md`
- Pass criteria:
  - Handoff and tool contracts are traceable and schema-valid.
- First troubleshooting action:
  - Validate agent-card capability and trust-boundary tags before replay.

### Lab 6: Blackwell NVFP4 + Prefix Caching
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab06_blackwell_nvfp4_prefix_caching`
- Required outputs:
  - `results/stage12/nvfp4_throughput_quality.csv`
  - `results/stage12/prefix_cache_latency_profile.csv`
  - `results/stage12/agent_loop_latency_report.md`
- Pass criteria:
  - Runtime recommendation includes both throughput and quality deltas.
- First troubleshooting action:
  - Confirm prompt-order policy before tuning precision path.

### Lab 7: OWASP LLM v2 Redteam
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab07_owasp_llm_v2_redteam`
- Required outputs:
  - `results/stage12/indirect_injection_case_log.jsonl`
  - `results/stage12/unbounded_consumption_guard.csv`
  - `results/stage12/owasp_llm_v2_redteam_report.md`
- Pass criteria:
  - Security containment behavior is explicit and replayable.
- First troubleshooting action:
  - Separate injection handling from budget-guard handling in incident notes.

### Lab 8: GIS Projection + Loop Breaker
- Command: `pwsh red-book/src/stage-12/run_all_stage12.ps1 -Lab lab08_gis_projection_and_loop_breaker`
- Required outputs:
  - `results/stage12/geojson_schema_guard_failures.csv`
  - `results/stage12/loop_breaker_events.jsonl`
  - `results/stage12/coordinate_projection_validation_report.md`
  - `results/stage12/mobile_latency_guard_report.md`
- Pass criteria:
  - Projection mismatches are blocked and loop spirals are terminated safely.
- First troubleshooting action:
  - Validate CRS mismatch detector before loop-breaker threshold tuning.

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

---

## 24) Expert-Tier Addendum (Blackwell + A2A/MCP + OWASP 2026)

This section upgrades Stage 12 to 2026 production architecture standards for local high-performance development and interoperable agent systems.

### 24.1 Blackwell NVFP4 Runtime Guidance (Mandatory)

Use fixed workloads to compare:

- baseline precision path (`bf16` or equivalent)
- Blackwell low-precision path (`nvfp4`)

Decision rule:

- no promotion if precision change lacks quality delta evidence
- no promotion if latency gains come with unacceptable grounding/faithfulness regression

Required evidence:

- `results/stage12/nvfp4_throughput_quality.csv`
- `results/stage12/prefix_cache_latency_profile.csv`
- `results/stage12/agent_loop_latency_report.md`

### 24.2 Prefix Caching and Prompt Reordering

For multi-step loops:

1. keep static instructions in stable prefix
2. place dynamic tool output near prompt tail
3. measure loop-latency impact before/after

If loop latency remains unstable, architecture must stay `hold`.

### 24.3 A2A and MCP Interoperability (Mandatory)

Stage 12 interoperability package must include:

- agent-card registry for discovery/capability boundaries
- A2A handoff trace evidence
- MCP tool contracts for portable tool integration

Required evidence:

- `results/stage12/agent_card_registry.json`
- `results/stage12/a2a_handoff_trace.jsonl`
- `results/stage12/mcp_tool_contracts.md`

### 24.4 GIS + Tourism Domain Reliability Drills

Domain-specific checks are mandatory:

- coordinate/projection validation (NAD83/WGS84 mismatch handling)
- loop-breaker behavior under repeated tool routing attempts
- mobile-latency guard behavior for user-facing path

Required evidence:

- `results/stage12/coordinate_projection_validation_report.md`
- `results/stage12/geojson_schema_guard_failures.csv`
- `results/stage12/loop_breaker_events.jsonl`
- `results/stage12/mobile_latency_guard_report.md`

### 24.5 OWASP LLM Top 10 (2026) Drill Requirement

Required attack classes:

- indirect prompt injection
- unbounded consumption / runaway loops

Required evidence:

- `results/stage12/owasp_llm_v2_redteam_report.md`
- `results/stage12/indirect_injection_case_log.jsonl`
- `results/stage12/unbounded_consumption_guard.csv`

### 24.6 ADR Y-Statement Requirement (Mandatory)

Final architecture recommendation must include Y-Statement format:

> In the context of `<project>`, we decided to use `<choice>` to handle `<problem>`, because `<reasoning>`, and `<measured outcome>`.

Required evidence:

- `results/stage12/architecture_decision_y_statement.md`
- `results/stage12/adr_scorecard_with_thresholds.csv`

No Y-Statement with measurable evidence means decision defaults to `hold`.
