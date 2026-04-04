# Stage 6 Runnable Examples

This folder contains runnable Stage 6 examples for AI agents, workflow-vs-agent design, guardrails, observability, interoperability, and production-style troubleshooting.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional packages for external framework experiments:

```powershell
pip install -r requirements-optional.txt
```

## Run

Fail-fast core path:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage6.ps1
```

Ladder path (simple -> intermediate -> advanced):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage6.ps1
```

Include labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage6.ps1 -IncludeLabs
python .\lab01_support_triage_agent.py --profile gis
```

## Topics

- PyTorch/CUDA in agent systems ladder:
  - `topic00a_pytorch_cuda_agent_simple.py`
  - `topic00_pytorch_cuda_agent_intermediate.py`
  - `topic00c_pytorch_cuda_agent_advanced.py`
  - `topic00m_local_model_capability_validation.py`
- Workflow vs agent ladder:
  - `topic01a_workflow_first_simple.py`
  - `topic01_workflow_vs_agent_intermediate.py`
  - `topic01c_multi_step_agent_advanced.py`
- Tool/schema ladder:
  - `topic02a_tool_schema_simple.py`
  - `topic02_tool_validation_intermediate.py`
  - `topic02c_tool_failure_recovery_advanced.py`
- Memory ladder:
  - `topic03a_memory_basics_simple.py`
  - `topic03_memory_retrieval_intermediate.py`
  - `topic03c_memory_policy_advanced.py`
- Guardrails and HITL ladder:
  - `topic04a_guardrails_simple.py`
  - `topic04_hitl_intermediate.py`
  - `topic04c_policy_gated_actions_advanced.py`
- Observability/eval ladder:
  - `topic05a_trace_basics_simple.py`
  - `topic05_eval_metrics_intermediate.py`
  - `topic05c_regression_suite_advanced.py`
- Industry/protocol/operations/security:
  - `topic06_industry_patterns.py`
  - `topic07a_mcp_tooling_simple.py`
  - `topic07_protocol_interop_intermediate.py`
  - `topic07c_a2a_collaboration_advanced.py`
  - `topic08a_budget_controls_simple.py`
  - `topic08_latency_cost_optimization_intermediate.py`
  - `topic08c_slo_regression_gate_advanced.py`
  - `topic09a_prompt_injection_defense_simple.py`
  - `topic09_policy_and_permissions_intermediate.py`
  - `topic09c_incident_response_advanced.py`
- Labs:
  - `lab00_pytorch_cuda_agent_examples.py`
  - `lab01_support_triage_agent.py`
  - `lab02_finance_research_agent.py`
  - `lab03_multi_agent_ops_assistant.py`
  - `lab04_secure_agent_operations.py`

## Review-to-Script Mapping (Industry Upgrade)

This table maps Chapter 6 review improvements to runnable scripts.

| Review improvement | Script(s) |
|---|---|
| Local model capability validation (cold start gate) | `topic00m_local_model_capability_validation.py` |
| State checkpointing and resume (time-travel debugger) | `topic03_memory_retrieval_intermediate.py` |
| GIS/sovereignty guardrails and leak-rate testing | `lab04_secure_agent_operations.py` |
| Token efficiency metric (`Total Tokens / Successful Tool Calls`) | `topic05_eval_metrics_intermediate.py` |
| Orchestration divergence stop rule + backoff prompt | `topic08c_slo_regression_gate_advanced.py` |
| Workflow vs Agent loop differentiation | `topic01a_workflow_first_simple.py`, `topic01_workflow_vs_agent_intermediate.py` |
| MCP vs A2A protocol comparison | `topic07a_mcp_tooling_simple.py`, `topic07_protocol_interop_intermediate.py`, `topic07c_a2a_collaboration_advanced.py` |

Suggested run order for these upgrades:

```powershell
python .\lab00_pytorch_cuda_agent_examples.py
python .\topic00m_local_model_capability_validation.py
python .\topic03_memory_retrieval_intermediate.py
python .\topic05_eval_metrics_intermediate.py
python .\topic08c_slo_regression_gate_advanced.py
python .\lab04_secure_agent_operations.py
```

## Data and Outputs

Input data:

- `red-book/data/stage-6/tickets_sample.csv`
- `red-book/data/stage-6/eval_ids_stage6.txt`

All lab outputs are written to:

- `red-book/src/stage-6/results/`

Detailed examples include:

- JSONL outputs
- metrics CSV files
- trace JSON/JSONL
- failure log markdown
- before/after comparison reports
- sovereignty/privacy leak-rate reports for secure operations lab

PyTorch/CUDA note:

- These Stage 6 scripts are runnable even if `torch` is not installed.
- If PyTorch is missing, scripts switch to educational fallback mode.
- For full CUDA demonstrations, install PyTorch with CUDA support.

## Comment Standard

All Stage 6 scripts are intentionally commented in detail to explain:

- the function purpose
- step-by-step workflow
- safety and reliability checks
- expected outputs and metrics interpretation
