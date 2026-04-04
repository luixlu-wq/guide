# Stage 6 - AI Agents

*(Week 12)*

## Goal

Understand AI agents from both theory and industry implementation, then build operatable agent systems with clear guardrails, evaluation, and troubleshooting.

You are learning:

- what an AI agent is and is not
- how tools, memory, and orchestration loops work
- when to use workflow vs single-agent vs multi-agent
- how to evaluate reliability, cost, and safety
- how to debug real production-like failures

This stage moves you from:

> "I can prompt an LLM"

to:

> "I can build, evaluate, and operate an AI agent system with clear limits and recovery paths."

---

## If This Chapter Feels Hard

Use 3 passes:

1. Pass 1 (concept pass): only read `Quick Summary`, `Key Knowledge`, and `Workflow vs Agent`.
2. Pass 2 (operation pass): read `Practice Lab` and run one baseline workflow with fixed outputs.
3. Pass 3 (reliability pass): run failure drills in `Troubleshooting Playbook` and record before/after metrics.

Do not start from multi-agent systems. Start from deterministic workflow first.

---

## Prerequisites and Environment Setup

Required:

- Python 3.10+
- Basic prompt engineering understanding (Stage 5)
- JSON and API basics

Suggested setup:

```powershell
cd red-book
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r .\src\stage-6\requirements.txt
# Optional (includes torch and agent frameworks):
pip install -r .\src\stage-6\requirements-optional.txt
```

If you use framework examples (optional):

- OpenAI Agents SDK
- LangGraph
- LlamaIndex / AutoGen / CrewAI (compare only after baseline)

Operational rule:

- Every experiment must log version IDs: prompt version, tool schema version, model version.

---

## Quick Summary

An AI agent is an LLM-based system that can decide actions, call tools, inspect results, update state, and continue until a stop condition.

A reliable agent system must include:

- clear tool schema
- clear state/memory design
- explicit stop rules
- policy checks and optional HITL approval
- observability (trace/log/metrics)
- evaluation and regression gates

A beginner should finish this stage understanding:

- agent loop anatomy
- workflow vs agent vs multi-agent choices
- tool and memory design
- RAG + tools integration
- guardrails and security boundaries
- MCP vs A2A interoperability concepts
- realistic troubleshooting workflow

---

## Study Materials

Core tutorials:

- OpenAI agents best practices:
  - https://platform.openai.com/docs/guides/agents/best-practices
- DeepLearning.AI AI Agents in LangGraph:
  - https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- DeepLearning.AI Long-Term Agentic Memory:
  - https://www.deeplearning.ai/alpha/short-courses/long-term-agentic-memory-with-langgraph/

Protocol and interoperability:

- MCP intro + spec:
  - https://modelcontextprotocol.io/docs/getting-started/intro
  - https://modelcontextprotocol.io/specification/2025-06-18
- A2A spec:
  - https://a2a-protocol.org/dev/specification/

Industry operations references:

- AWS Bedrock Agents:
  - https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- Azure Foundry Agents overview:
  - https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview
- Google Vertex Agent Engine overview:
  - https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/overview

Evaluation and theory:

- ReAct: https://arxiv.org/abs/2210.03629
- Toolformer: https://arxiv.org/abs/2302.04761
- AgentBench: https://arxiv.org/abs/2308.03688
- WebArena: https://arxiv.org/abs/2307.13854
- SWE-bench: https://arxiv.org/abs/2310.06770
- GAIA: https://arxiv.org/abs/2311.12983

PyTorch and CUDA references:

- PyTorch local install guide:
  - https://pytorch.org/get-started/locally/
- PyTorch CUDA semantics:
  - https://pytorch.org/docs/stable/notes/cuda.html
- `torch.nn.functional` API reference:
  - https://pytorch.org/docs/stable/nn.functional.html

---

## Example Complexity Scale (Used in All Modules)

- Simple:
  - one agent
  - 1-2 tools
  - fixed stop rule
  - no long-term memory
- Intermediate:
  - routing across tools
  - retrieval memory
  - retries/fallback
  - structured outputs
- Advanced:
  - multi-agent orchestration
  - policy gates + HITL
  - eval harness + incident logging
  - budget control (latency/cost/steps)

Where complexity is:

- orchestration logic
- tool/schema design
- memory/state consistency
- safety/policy enforcement
- operations and cost control
- protocol interoperability

---

## Key Knowledge (Deep Understanding)

### 0. PyTorch and CUDA for Agent Systems

Runnable examples:

- [topic00a_pytorch_cuda_agent_simple.py](src/stage-6/topic00a_pytorch_cuda_agent_simple.py)
- [topic00_pytorch_cuda_agent_intermediate.py](src/stage-6/topic00_pytorch_cuda_agent_intermediate.py)
- [topic00c_pytorch_cuda_agent_advanced.py](src/stage-6/topic00c_pytorch_cuda_agent_advanced.py)
- [topic00m_local_model_capability_validation.py](src/stage-6/topic00m_local_model_capability_validation.py)

Short answer:

- Yes, PyTorch and CUDA are applicable to AI agents.

Where they are used:

- local model inference inside agent loops
- embedding and reranking for retrieval memory
- local classification/scoring tools used by the agent
- latency optimization for high-throughput operations

When they are not required:

- if your agent only calls hosted APIs and does not run local neural computation

Agent training/inference workflow (device-aware):

1. Select device (`cpu` or `cuda`).
2. Move tensors/model to same device.
3. Run forward pass for scoring/inference.
4. Optionally run backward pass if training/fine-tuning local components.
5. Use outputs inside tool decisions, retrieval ranking, or policy scoring.

Why this matters for Stage 6:

- Many real industry agents are hybrid systems:
  - LLM API for reasoning
  - local PyTorch components for retrieval/reranking/scoring
- CUDA availability can directly improve p95 latency in retrieval-heavy pipelines.

Common beginner mistake:

- Mistake: thinking PyTorch/CUDA is only for model training.
- Fix: treat PyTorch/CUDA as a runtime acceleration layer for agent subcomponents too.

How this works when training local agent submodules:

1. Build tensors from training/eval samples.
2. Move model and tensors to same device (`cpu` or `cuda`).
3. Forward pass computes predictions or similarity scores.
4. Loss compares prediction vs target for supervised tasks.
5. Backward pass computes gradients (`loss.backward()`).
6. Optimizer updates parameters (`optimizer.step()`).
7. Export updated component for agent pipeline use.

Quick run commands:

```powershell
python .\src\stage-6\topic00a_pytorch_cuda_agent_simple.py
python .\src\stage-6\topic00_pytorch_cuda_agent_intermediate.py
python .\src\stage-6\topic00c_pytorch_cuda_agent_advanced.py
```

Complete inline examples (operatable):

Code moved to lab/example scripts:

- Example A (simple): [topic00a_pytorch_cuda_agent_simple.py](src/stage-6/topic00a_pytorch_cuda_agent_simple.py)
- Example B (intermediate): [topic00_pytorch_cuda_agent_intermediate.py](src/stage-6/topic00_pytorch_cuda_agent_intermediate.py)
- Example C (advanced): [topic00c_pytorch_cuda_agent_advanced.py](src/stage-6/topic00c_pytorch_cuda_agent_advanced.py)
- Combined chapter code lab: [lab00_pytorch_cuda_agent_examples.py](src/stage-6/lab00_pytorch_cuda_agent_examples.py)

Run:

```powershell
python .\src\stage-6\lab00_pytorch_cuda_agent_examples.py
```

CUDA troubleshooting quick checks:

- verify device: `torch.cuda.is_available()`
- avoid device mismatch: model/tensors must be on same device
- if OOM: reduce batch size or vector count
- synchronize before timing CUDA paths for accurate latency

Cold-start capability gate (recommended before orchestration coding):

- Validate local model schema-following ability first, especially for quantized local models.
- Bridge practical runtime to Ollama/vLLM capability checks.
- Use:
  - [topic00m_local_model_capability_validation.py](src/stage-6/topic00m_local_model_capability_validation.py)

What to measure:

- schema adherence rate across fixed tool schemas
- tool argument accuracy
- mean latency per schema case

If schema adherence is low, improve model/runtime choice before building complex agent loops.

---

### 1. Agent Fundamentals

Runnable examples:

- [topic01a_workflow_first_simple.py](src/stage-6/topic01a_workflow_first_simple.py)
- [topic01_workflow_vs_agent_intermediate.py](src/stage-6/topic01_workflow_vs_agent_intermediate.py)
- [topic01c_multi_step_agent_advanced.py](src/stage-6/topic01c_multi_step_agent_advanced.py)

What it is:

- An LLM in a control loop that can choose actions, call tools, observe, and continue.

Why it matters:

- Most industry AI products now require action-taking systems, not only text generation.

Beginner mental model:

- `LLM` is planner/reasoner.
- `Tools` are capabilities.
- `State` is working memory.
- `Loop` is decision-execution cycle.

Core loop:

1. Read user goal.
2. Decide next action.
3. Call tool or answer.
4. Observe result.
5. Update state.
6. Check stop rule.

Important mechanisms:

- ReAct-style think-act-observe loops.
- Planner-executor split.
- Router-based single-step tool calling.

Common beginner mistake:

- Mistake: treating agent output as always reliable.
- Fix: require tool evidence and policy checks for critical actions.

When to use:

- tasks require dynamic steps and external data.

When not to use:

- tasks are deterministic and can be solved by fixed workflow.

---

### 2. Workflow vs Agent vs Multi-Agent

Runnable examples:

- [topic01a_workflow_first_simple.py](src/stage-6/topic01a_workflow_first_simple.py)
- [topic01_workflow_vs_agent_intermediate.py](src/stage-6/topic01_workflow_vs_agent_intermediate.py)
- [topic01c_multi_step_agent_advanced.py](src/stage-6/topic01c_multi_step_agent_advanced.py)
- [lab03_multi_agent_ops_assistant.py](src/stage-6/lab03_multi_agent_ops_assistant.py)

Decision framework:

- Use workflow when steps are known.
- Use single-agent when tool choice is dynamic.
- Use multi-agent only when role separation gives measurable value.

Operatable rule:

- Build baseline workflow first, then compare agent variant on same eval set.

Visual hierarchy tags:

- `[Workflow Chain]`:
  - `A -> B -> C -> Done`
- `[Agent Loop]`:
  - `Plan -> Act -> Observe -> Re-plan -> ... -> Stop/Budget Gate`

Instructional note:

- If a task can stay in `[Workflow Chain]`, prefer it.
- Move to `[Agent Loop]` only when dynamic decision value is clear and measurable.

Comparison table:

| System | Strength | Risk | Best use |
|---|---|---|---|
| Workflow | stable, testable | less flexible | known repeated tasks |
| Single-agent | adaptive | tool mistakes | moderate dynamic tasks |
| Multi-agent | scalable specialization | high coordination complexity | large role-divided tasks |

Common beginner mistake:

- Mistake: starting with multi-agent because it looks advanced.
- Fix: prove single-agent gains first.

---

### 3. Tool Design and Schema Discipline

Runnable examples:

- [topic02a_tool_schema_simple.py](src/stage-6/topic02a_tool_schema_simple.py)
- [topic02_tool_validation_intermediate.py](src/stage-6/topic02_tool_validation_intermediate.py)
- [topic02c_tool_failure_recovery_advanced.py](src/stage-6/topic02c_tool_failure_recovery_advanced.py)

What a good tool has:

- clear name
- clear description
- strict input schema
- strict output schema
- explicit error codes
- timeout and retry policy

Data declaration template for every tool example:

Data: `<name and source>`  
Records/Samples: `<count>`  
Input schema: `<fields and types>`  
Output schema: `<fields and types>`  
Split/Eval policy: `<fixed set rule>`  
Type: `<workflow/agent/multi-agent/eval>`

Operatable mini tool contract:

- `name`: `get_stock_snapshot`
- `input_schema`:
  - `symbol: string`
  - `start_date: YYYY-MM-DD`
  - `end_date: YYYY-MM-DD`
- `output_schema`:
  - `symbol: string`
  - `rows: int`
  - `close_prices: array<float>`
  - `return_5d: float`
- `errors`: `INVALID_SYMBOL`, `TIMEOUT`, `EMPTY_DATA`

Common beginner mistake:

- Mistake: vague tool descriptions and weak schema.
- Fix: explicit fields, types, and error outputs.

---

### 4. Memory and State Management

Runnable examples:

- [topic03a_memory_basics_simple.py](src/stage-6/topic03a_memory_basics_simple.py)
- [topic03_memory_retrieval_intermediate.py](src/stage-6/topic03_memory_retrieval_intermediate.py)
- [topic03c_memory_policy_advanced.py](src/stage-6/topic03c_memory_policy_advanced.py)

Two memory scopes:

- short-term: current thread/session context
- long-term: persisted user/project facts

Core risk:

- memory pollution (irrelevant stale data influences decisions)

Required controls:

- memory write policy
- memory TTL/expiry
- source tagging and confidence score
- state checkpointing after major steps/tool calls
- resume-from-checkpoint path for long-running loops

Simple memory policy example:

- write only verified facts from tool output
- never persist speculative model-only statements
- expire low-confidence items

Common beginner mistake:

- Mistake: storing everything.
- Fix: define `what can be stored` and `when to discard`.

Time-travel debugger pattern (must know):

- Save checkpoint after each critical step.
- If run fails at step N, reload checkpoint and continue from N instead of restarting at step 1.
- This pattern is implemented in:
  - [topic03_memory_retrieval_intermediate.py](src/stage-6/topic03_memory_retrieval_intermediate.py)

Checkpoint artifacts to inspect:

- `results/stage6/topic03_memory_checkpoint.json`
- `results/stage6/topic03_memory_recovery_report.csv`

---

### 5. RAG + Agent Integration

Runnable examples:

- [topic03_memory_retrieval_intermediate.py](src/stage-6/topic03_memory_retrieval_intermediate.py)
- [lab02_finance_research_agent.py](src/stage-6/lab02_finance_research_agent.py)

Why combine:

- RAG provides grounded context.
- Agent decides when retrieval is needed and how to use results.

Recommended flow:

1. classify query intent
2. decide retrieve or not
3. retrieve top-k chunks
4. cite evidence IDs
5. answer with confidence note

Minimum reliability checks:

- no citation -> low-confidence warning
- conflicting chunks -> surface ambiguity
- missing evidence -> abstain or ask follow-up

Common beginner mistake:

- Mistake: assuming retrieved text is always correct.
- Fix: add source quality checks and conflict handling.

---

### 6. Guardrails and Human-in-the-Loop (HITL)

Runnable examples:

- [topic04a_guardrails_simple.py](src/stage-6/topic04a_guardrails_simple.py)
- [topic04_hitl_intermediate.py](src/stage-6/topic04_hitl_intermediate.py)
- [topic04c_policy_gated_actions_advanced.py](src/stage-6/topic04c_policy_gated_actions_advanced.py)

Guardrail layers:

- input policy checks
- tool permission checks
- output policy checks
- action-level approvals (HITL)

HITL checkpoints (example):

- external transaction above threshold
- sensitive data export
- irreversible action

Operatable gate example:

`if action in ["send_email", "create_ticket", "execute_trade"] and risk_score >= 0.7 -> require_human_approval = true`

Common beginner mistake:

- Mistake: using only text moderation, no action gating.
- Fix: enforce policy at tool execution boundary.

---

### 7. Observability, Eval, and Regression

Runnable examples:

- [topic05a_trace_basics_simple.py](src/stage-6/topic05a_trace_basics_simple.py)
- [topic05_eval_metrics_intermediate.py](src/stage-6/topic05_eval_metrics_intermediate.py)
- [topic05c_regression_suite_advanced.py](src/stage-6/topic05c_regression_suite_advanced.py)
- [topic08c_slo_regression_gate_advanced.py](src/stage-6/topic08c_slo_regression_gate_advanced.py)

Trace per run must include:

- query_id, run_id, trace_id
- step index
- chosen tool + arguments
- tool latency + return status
- token/cost summary
- final decision path

Core metrics:

- task success rate
- tool call accuracy
- policy violation rate
- average steps per task
- p95 latency
- cost per task
- token efficiency (`total_tokens_used / successful_tool_calls`)

Token-efficiency interpretation:

- rising value usually means prompt drift or repeated low-value tool calls
- stable/lower value means agent is converting token budget into useful actions more efficiently

Regression rule:

- block promotion when safety drops or cost explodes beyond threshold.

Common beginner mistake:

- Mistake: evaluating only answer quality.
- Fix: evaluate quality + safety + cost + latency together.

---

### 8. Interoperability: MCP vs A2A

Runnable examples:

- [topic07a_mcp_tooling_simple.py](src/stage-6/topic07a_mcp_tooling_simple.py)
- [topic07_protocol_interop_intermediate.py](src/stage-6/topic07_protocol_interop_intermediate.py)
- [topic07c_a2a_collaboration_advanced.py](src/stage-6/topic07c_a2a_collaboration_advanced.py)

MCP (Model Context Protocol):

- standard interface for models/agents to use external context and tools.
- strongest use: tool and resource interoperability.

A2A (Agent2Agent):

- protocol for communication/collaboration between agents.
- strongest use: multi-agent task coordination.

Simple distinction:

- MCP: agent/tool boundary standard.
- A2A: agent/agent boundary standard.

When to use MCP:

- you need consistent tool/resource access across stacks.

When to use A2A:

- you need independent agents to coordinate tasks.

3-question protocol decision tree:

1. Is tool/resource running on different server/language boundary?
   - Yes -> prefer MCP.
2. Do two agents need negotiation/coordination as peers?
   - Yes -> prefer A2A.
3. Is capability just a local Python class/function in same repo?
   - Yes -> use standard class/function call; do not over-engineer protocol layer.

Common beginner mistake:

- Mistake: treating protocol choice as main goal.
- Fix: pick protocol only after architecture and reliability goals are clear.

---

### 9. Industry Architecture Patterns

Runnable examples:

- [topic06_industry_patterns.py](src/stage-6/topic06_industry_patterns.py)
- [lab01_support_triage_agent.py](src/stage-6/lab01_support_triage_agent.py)
- [lab03_multi_agent_ops_assistant.py](src/stage-6/lab03_multi_agent_ops_assistant.py)

Pattern A: Support triage agent

- intent classify
- retrieve policy docs
- draft response
- route by severity

Pattern B: Research analyst agent

- retrieve documents
- run calculation tools
- produce cited summary and uncertainty note

Pattern C: Ops assistant with policy gates

- coordinator agent
- specialist agents (SRE, compliance, reporting)
- HITL for high-risk actions

Industry reality:

- most successful deployments combine deterministic workflows with bounded agent autonomy.

---

### 10. Security Threat Model for Agents

Runnable examples:

- [topic09a_prompt_injection_defense_simple.py](src/stage-6/topic09a_prompt_injection_defense_simple.py)
- [topic09_policy_and_permissions_intermediate.py](src/stage-6/topic09_policy_and_permissions_intermediate.py)
- [topic09c_incident_response_advanced.py](src/stage-6/topic09c_incident_response_advanced.py)
- [lab04_secure_agent_operations.py](src/stage-6/lab04_secure_agent_operations.py)

High-frequency risks:

- prompt injection
- tool abuse
- data exfiltration
- secret leakage
- over-permissioned tools
- retry storms under failure

Sovereignty gate (Ontario GIS context):

- If request includes sensitive GeoJSON/provincial identifiers, block raw egress to external endpoints by default.
- Apply redact/generalize policy before any allowed external transfer.
- Track `privacy_leak_rate` as mandatory security metric.

Lab implementation:

- [lab04_secure_agent_operations.py](src/stage-6/lab04_secure_agent_operations.py)
- key outputs include:
  - `results/lab4_privacy_leak_report.csv`
  - `results/lab4_data_boundary_policy.md`

Mitigation baseline:

- strict allowlist tools
- least privilege credentials
- policy checks before tool execution
- output sanitization
- audit log for every high-risk action

Incident response mini workflow:

1. freeze risky tool path
2. capture trace/log evidence
3. classify incident type
4. patch policy or schema
5. rerun red-team case
6. publish postmortem

---

## Agent Workflow (Real World)

Reference runbook:

1. Define task and success metric.
2. Build deterministic baseline workflow.
3. Add one agent decision point only.
4. Add strict tool schema and policy gates.
5. Add trace + metrics logging.
6. Evaluate on fixed test set.
7. Inject failures and verify recovery paths.
8. Promote only if quality/safety/cost gates pass.

---

## Stage 6 Script Mapping (`/red-book/src/stage-6`)

Required ladders:

0. PyTorch/CUDA in agent systems
- `topic00a_pytorch_cuda_agent_simple.py`
- `topic00_pytorch_cuda_agent_intermediate.py`
- `topic00c_pytorch_cuda_agent_advanced.py`
- `topic00m_local_model_capability_validation.py`

1. Workflow vs agent
- `topic01a_workflow_first_simple.py`
- `topic01_workflow_vs_agent_intermediate.py`
- `topic01c_multi_step_agent_advanced.py`

2. Tooling and schema
- `topic02a_tool_schema_simple.py`
- `topic02_tool_validation_intermediate.py`
- `topic02c_tool_failure_recovery_advanced.py`

3. Memory
- `topic03a_memory_basics_simple.py`
- `topic03_memory_retrieval_intermediate.py`
- `topic03c_memory_policy_advanced.py`

4. Guardrails and HITL
- `topic04a_guardrails_simple.py`
- `topic04_hitl_intermediate.py`
- `topic04c_policy_gated_actions_advanced.py`

5. Observability and eval
- `topic05a_trace_basics_simple.py`
- `topic05_eval_metrics_intermediate.py`
- `topic05c_regression_suite_advanced.py`

6. Protocol and interoperability
- `topic07a_mcp_tooling_simple.py`
- `topic07_protocol_interop_intermediate.py`
- `topic07c_a2a_collaboration_advanced.py`

7. Operations and security
- `topic08a_budget_controls_simple.py`
- `topic08_latency_cost_optimization_intermediate.py`
- `topic08c_slo_regression_gate_advanced.py`
- `topic09a_prompt_injection_defense_simple.py`
- `topic09_policy_and_permissions_intermediate.py`

8. Labs
- `lab00_pytorch_cuda_agent_examples.py`
- `lab01_support_triage_agent.py`
- `lab02_finance_research_agent.py`
- `lab03_multi_agent_ops_assistant.py`
- `lab04_secure_agent_operations.py`

Detailed comment standard (mandatory):

- explain purpose of each function
- explain each workflow step and expected state transition
- explain why each guardrail exists
- explain failure paths and fallback behavior
- explain metric calculations and interpretation

---

## Practice Lab (Clear and Operatable)

Primary runnable lab script:

- [lab01_support_triage_agent.py](src/stage-6/lab01_support_triage_agent.py)

Additional runnable labs:

- [lab00_pytorch_cuda_agent_examples.py](src/stage-6/lab00_pytorch_cuda_agent_examples.py)
- [lab02_finance_research_agent.py](src/stage-6/lab02_finance_research_agent.py)
- [lab03_multi_agent_ops_assistant.py](src/stage-6/lab03_multi_agent_ops_assistant.py)
- [lab04_secure_agent_operations.py](src/stage-6/lab04_secure_agent_operations.py)

Run commands:

```powershell
python .\src\stage-6\lab00_pytorch_cuda_agent_examples.py
python .\src\stage-6\lab01_support_triage_agent.py --profile gis
python .\src\stage-6\lab01_support_triage_agent.py --profile generic
python .\src\stage-6\lab02_finance_research_agent.py
python .\src\stage-6\lab03_multi_agent_ops_assistant.py
python .\src\stage-6\lab04_secure_agent_operations.py
```

### Lab: Build a Support Triage Agent with Safety and Eval

#### Lab goal

Build one operatable agent pipeline that:

- classifies support ticket priority
- routes ticket to queue
- drafts response with citation to policy snippets
- enforces action policy gate
- logs metrics and failure classes

#### Fixed dataset and schema

Data source:

- profile `gis` (recommended): synthetic GIS/mapping support tickets aligned with Ontario-style projects
- profile `generic`: local file `red-book/data/stage-6/tickets_sample.csv` (create if missing)

Input schema:

- `ticket_id: string`
- `customer_tier: string`
- `subject: string`
- `body: string`
- `created_at: datetime`

Output schema:

- `ticket_id: string`
- `predicted_priority: enum(low, medium, high, critical)`
- `queue: enum(general, billing, outage, security)`
- `draft_reply: string`
- `citations: array<string>`
- `needs_human_approval: bool`
- `failure_class: string|null`

Eval split policy:

- fixed 30-ticket eval subset, saved as `eval_ids_stage6.txt`

#### Required workflow (strict)

1. Load fixed eval IDs.
2. Run deterministic baseline workflow.
3. Run agent-enabled workflow (same inputs).
4. Compare metrics.
5. Add one controlled improvement (example: better tool schema).
6. Rerun and explain delta.

#### Required deliverables

- `results/stage6_lab_outputs.jsonl`
- `results/stage6_lab_metrics.csv`
- `results/stage6_lab_trace.json`
- `results/stage6_lab_failure_log.md`
- `results/stage6_lab_before_after.md`

#### Minimum metrics

- task success rate
- tool call accuracy
- citation presence rate
- policy violation rate
- p95 latency
- average steps per ticket
- cost per ticket (if API-based)

#### Controlled improvement examples

Choose exactly one:

- stronger tool descriptions + schema constraints
- memory write filtering
- guardrail rule tuning
- retry/backoff tuning

#### Where complexity is in this lab

- routing quality vs stability tradeoff
- tool/schema rigidity vs flexibility
- safety gates vs automation speed
- cost/latency vs answer quality

---

## Troubleshooting and Realistic Problem Playbook

Failure scenarios you must test:

1. Wrong tool selected.
2. Malformed tool arguments.
3. Tool timeout.
4. Retrieval returns irrelevant context.
5. Memory pollution.
6. Loop runs too long.
7. Hallucinated action claim.
8. Prompt injection success.
9. Data exfiltration attempt.
10. Retry storm after transient failure.
11. Device mismatch between tensors and model (`cpu` vs `cuda`).
12. CUDA out-of-memory during batched scoring/reranking.

Standard troubleshooting workflow:

1. Reproduce with fixed input and trace ID.
2. Classify failure type.
3. Inspect schema and tool arguments.
4. Inspect routing and stop conditions.
5. Inspect memory read/write path.
6. Inspect guardrail decisions.
7. Apply one targeted fix only.
8. Rerun exact same case and record delta.
9. If GPU path fails, validate CPU fallback behavior.

Required run logs:

- `run_id`, `trace_id`, `query_id`
- `step_index`
- `selected_tool`
- `tool_args`
- `tool_status`
- `latency_ms`
- `token_cost`
- `policy_decision`
- `failure_class`

---

## Common Mistakes

- building multi-agent first without baseline
- vague tool schema and no error contract
- no explicit stop rule
- no policy checks before action tools
- no fixed eval set (cannot compare versions)
- no observability (cannot debug failures)
- optimizing quality only, ignoring cost/latency/safety

---

## Final Understanding

You should now be able to:

- design workflow-first agent systems
- choose between workflow, single-agent, and multi-agent
- design tools and memory with strict schemas
- apply guardrails and HITL correctly
- evaluate with quality/safety/cost/latency metrics
- troubleshoot realistic failure modes using traces
- explain MCP and A2A roles in interoperable systems

---

## Self Test

### Questions

1. Why should deterministic workflow come before multi-agent design?
2. What fields must every tool contract include to be operatable?
3. What is the practical difference between MCP and A2A?
4. Why is answer-quality-only evaluation insufficient for agents?
5. Give one example where HITL approval is mandatory.
6. What is memory pollution and one mitigation strategy?
7. What should you log to debug wrong-tool selection?
8. Why must experiments use fixed eval sets?
9. Give one prompt-injection defense at tool boundary.
10. What metric would detect runaway loops quickly?

### Answers

1. Workflow establishes baseline reliability and makes later agent gains measurable.
2. Name, description, input schema, output schema, and explicit error contract.
3. MCP standardizes tool/resource interaction; A2A standardizes agent-to-agent collaboration.
4. Agents can look good in text while failing on safety, cost, latency, or tool correctness.
5. Any high-risk or irreversible action, such as transaction execution or sensitive export.
6. Irrelevant stale state affecting decisions; mitigate with strict write policy + TTL.
7. Step index, selected tool, tool args, routing rationale, and tool return status.
8. Without fixed eval sets, metric changes are not comparable and regressions are hidden.
9. Validate arguments against allowlist schema and block sensitive commands by policy.
10. Average steps per task (and max steps threshold breaches).

---

## What You Must Be Able To Do After Stage 6

- Build one end-to-end agent pipeline with strict tool and output schemas.
- Run before/after experiments with fixed data and measurable deltas.
- Add policy gates and HITL checkpoints for high-risk actions.
- Diagnose failures using trace evidence and targeted fixes.
- Explain industry patterns and protocol choices (MCP vs A2A) with practical tradeoffs.
