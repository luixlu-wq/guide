# Stage 6 Handbook Improvement Plan (v2)

Target file: `red-book/AI-study-handbook-6.md`  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-6.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Stage 6 must teach AI agents in both:
  - theory
  - industry implementation patterns
- Collect more and better resources with exact tutorials that make this chapter easier to learn.
- Add detailed explanation and demonstration for all key agent concepts.
- Add clearer instructions on learning targets.
- Add detailed tutorials for key topics.
- Add examples for each learning topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare data source and data structure used in all examples.
- Create labs so students can build real AI agents (not only toy snippets).
- Add explicit troubleshooting guidance for realistic problems and how to resolve them.
- Include high-quality resources (official docs, papers, books, practical repos, platform docs).
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.
- Expand chapter coverage with missing high-impact topics:
  - interoperability protocols (MCP and A2A)
  - benchmark-driven agent evaluation
  - production operations (SLO/cost/latency/rate limits)
  - agent security threat modeling and incident response
  - PyTorch/CUDA applicability in agent systems (local inference, retrieval/reranking, and performance optimization)

- Mandatory request: include PyTorch and CUDA conceptual/tutorial content in the chapter.
- Mandatory request: include runnable PyTorch/CUDA example code (simple -> intermediate -> advanced) with very detailed and clear functional comments.

- Key request: collect the best tutorials, books, videos, official documentation, guides, instructions, and industry project references to build chapter content.
- Key request: chapter content must be detailed, easy to understand, and operatable from both theory and realistic project perspectives.
- Key request: create a learning library/track that leads students to real, industry-level projects.
- Key request: add more theory instruction in each chapter so learners understand principles, not only steps.
- Key request: explicitly teach troubleshooting capability as a core skill:
  - how to identify and classify problems from evidence/logs/metrics
  - how to compare possible solutions with clear tradeoff analysis
  - how to verify fixes using controlled reruns and before/after metrics
- Key request: include a new realistic lab that improves a project from beginning to production, with fixed deliverables and production-quality acceptance checks.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary (Current Chapter 6 State)

### What is already strong

- Core concepts are present: agent, tools, memory, workflow-vs-agent, RAG+agent.
- Includes project, checklist, and self-test.
- Beginner motivation exists.

### What is still missing

- Chapter is still mostly concept-first; operation details are not strict enough.
- No Stage 6 runnable script package (`red-book/src/stage-6/`) is defined yet.
- No simple -> intermediate -> advanced ladder mapping per topic.
- No strict observability/evaluation framework for agent runs (trace quality, tool success, step efficiency, failure class rates).
- Practice project is broad and should be converted into file-output runbook with fixed deliverables.
- Troubleshooting needs realistic incident patterns and response playbooks.
- Missing interoperability section (MCP vs A2A, when and why).
- Missing benchmark section (fixed eval set + regression gates).
- Missing production operations controls (budget, retries, idempotency, concurrency).
- Missing security threat model (prompt injection, tool abuse, data exfiltration, secret handling).

---

## 2) Target Outcomes (Measurable)

Stage 6 rewrite is complete only when:

- Learner can explain and execute a workflow-first agent build path.
- Learner can clearly distinguish:
  - deterministic workflow
  - router-based orchestration
  - dynamic agent loop
  - multi-agent coordination
- Learner can explain MCP and A2A at conceptual level and implementation level.
- Every module has operatable examples with data/schema declaration.
- Every Stage 6 script has:
  - very detailed functional comments
  - workflow comments
  - expected output notes
- Learner can diagnose common agent failures from logs and traces.
- Learner can define and enforce run budgets:
  - max steps
  - max latency
  - max token/cost
- Practice labs produce fixed deliverable files for before/after evaluation.
- Stage 6 scripts run via fail-fast runner and ladder runner.

---

## 3) Resource Upgrade (Exact Tutorials + Primary Sources)

Link verification status:

- Last verified: 2026-04-04
- Policy: replace/remove links after 2 failed checks

Use this layered stack:

- Layer 1: core tutorials (must complete)
- Layer 2: official framework/platform docs (must use while coding)
- Layer 3: foundational papers (theory)
- Layer 4: industry governance/safety/operations references
- Layer 5: practical GitHub implementations
- Layer 6: benchmark/evaluation suites
- Layer 7: interoperability protocol specs

### A. Core Tutorials (Must Complete)

- DeepLearning.AI: AI Agents in LangGraph
  - https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- DeepLearning.AI: Long-Term Agentic Memory With LangGraph
  - https://www.deeplearning.ai/alpha/short-courses/long-term-agentic-memory-with-langgraph/
- OpenAI Agents guide (best practices)
  - https://platform.openai.com/docs/guides/agents/best-practices

### B. Official Agent Framework / Platform Docs

- OpenAI Agents SDK guide
  - https://platform.openai.com/docs/guides/agents-sdk/
- OpenAI tools guide
  - https://platform.openai.com/docs/guides/tools?api-mode=responses
- OpenAI agent evals
  - https://platform.openai.com/docs/guides/agent-evals
- OpenAI safety in building agents
  - https://platform.openai.com/docs/guides/agent-builder-safety
- OpenAI prompt caching (cost and latency control)
  - https://platform.openai.com/docs/guides/prompt-caching
- OpenAI background mode (long-running tasks)
  - https://platform.openai.com/docs/guides/background
- Anthropic tool use overview
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- Anthropic implement tool use
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use
- Model Context Protocol (MCP) intro
  - https://modelcontextprotocol.io/docs/getting-started/intro
- MCP base specification
  - https://modelcontextprotocol.io/specification/2025-06-18
- MCP authorization specification
  - https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- MCP transport specification
  - https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
- MCP security best practices
  - https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
- LangChain agents docs
  - https://docs.langchain.com/oss/python/langchain/agents
- LangChain human-in-the-loop docs
  - https://docs.langchain.com/oss/python/langchain/human-in-the-loop
- LangGraph memory docs
  - https://docs.langchain.com/oss/javascript/langgraph/add-memory
- LangGraph repo + docs links
  - https://github.com/langchain-ai/langgraph
- LlamaIndex agent module guide
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/
- AutoGen docs
  - https://microsoft.github.io/autogen/stable/
- CrewAI quickstart
  - https://docs.crewai.com/en/quickstart
- Google ADK technical overview
  - https://adk.dev/get-started/about/

### C. Industry Platform Implementation References

- AWS Bedrock agents overview
  - https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- AWS: how Bedrock agents work
  - https://docs.aws.amazon.com/bedrock/latest/userguide/agents-how.html
- AWS: trace events for agent runs
  - https://docs.aws.amazon.com/bedrock/latest/userguide/trace-events.html
- AWS: multi-agent collaboration
  - https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html
- AWS Bedrock AgentCore overview
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- Azure Foundry Agent Service overview
  - https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview
- Azure agent tracing (OpenTelemetry)
  - https://learn.microsoft.com/en-us/azure/ai-services/agents/concepts/tracing
- Azure agent evaluators
  - https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators
- Google Vertex AI Agent Engine overview and framework options
  - https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/overview

### D. Theory / Foundations (Papers)

- ReAct (reason + act)
  - https://arxiv.org/abs/2210.03629
- Toolformer
  - https://arxiv.org/abs/2302.04761
- AutoGen paper
  - https://arxiv.org/abs/2308.08155
- CodeAct (executable actions)
  - https://arxiv.org/abs/2402.01030
- AgentBench (evaluate LLMs as agents)
  - https://arxiv.org/abs/2308.03688
- WebArena (realistic web-agent benchmark)
  - https://arxiv.org/abs/2307.13854
- SWE-bench (real software issue benchmark)
  - https://arxiv.org/abs/2310.06770
- GAIA (general AI assistants benchmark)
  - https://arxiv.org/abs/2311.12983

### E. Security / Governance / Reliability

- NIST AI RMF 1.0
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST AI RMF Playbook
  - https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- OWASP GenAI Security Project
  - https://genai.owasp.org/
- OpenTelemetry docs (trace/log/metric foundations)
  - https://opentelemetry.io/docs/

### F. Practical GitHub Resources

- OpenAI Agents SDK (Python)
  - https://github.com/openai/openai-agents-python
- OpenAI Agents SDK (JS/TS)
  - https://github.com/openai/openai-agents-js
- LangGraph
  - https://github.com/langchain-ai/langgraph
- AutoGen
  - https://github.com/microsoft/autogen
- CrewAI
  - https://github.com/crewAIInc/crewAI
- Google ADK Python
  - https://github.com/google/adk-python
- SWE-agent
  - https://github.com/princeton-nlp/SWE-agent
- SWE-bench benchmark suite
  - https://github.com/SWE-bench/SWE-bench
- AgentBench benchmark suite
  - https://github.com/THUDM/AgentBench
- WebArena benchmark environment
  - https://github.com/web-arena-x/webarena
- OpenHands
  - https://github.com/All-Hands-AI/OpenHands

### G. Interoperability Protocol References

- A2A protocol (current spec)
  - https://a2a-protocol.org/dev/specification/
- A2A protocol (versioned spec track)
  - https://a2a-protocol.org/v0.3.0/specification/

---

## 4) New Handbook Structure (Required)

1. If this chapter feels hard (how to learn in 3 passes)
2. Prerequisites and environment setup
3. Agent fundamentals (model + tools + state + loop)
4. Workflow vs agent vs multi-agent (decision framework)
5. Tool schema design and safe tool execution
6. Memory systems (short-term, long-term, retrieval memory)
7. Industry architecture patterns (supervisor-worker, specialist swarm)
8. Interoperability protocols (MCP vs A2A)
9. Reliability and guardrails (HITL, stop rules, policy checks)
10. Security threat model for agent systems
11. Observability and eval (trace, tool success, cost, latency, failure classes)
12. Benchmarking and regression strategy
13. Example complexity scale + where complexity is
14. Stage 6 script mapping (`src/stage-6`)
15. Practice labs (real projects) with deliverables
16. Troubleshooting realistic failures (runbook)
17. Self-test + weighted scoring rubric
18. What comes after Stage 6

---

## 5) Concept Module Template (Mandatory)

Every module must include:

- What it is
- Why it matters
- Data declaration block
- Input/output schema block
- Worked example
- Assumptions and limits
- Common beginner mistake + fix
- Demonstration checklist
- Quick check
- When to use / when not to use
- Failure injection mini test case
- Observability hooks (what to log)
- Security and permission boundary note
- Cost/latency budget note
- Very detailed code-comment expectation for mapped scripts

Hard requirement: no module ships with missing fields.

---

## 6) Example Complexity Scale (Use In All Modules)

- Simple:
  - one agent, 1-2 tools, no long-term memory, fixed stop rule
- Intermediate:
  - routing, retrieval memory, retries, structured tool outputs
- Advanced:
  - multi-agent coordination, HITL, eval harness, reliability gates, incident logs

Each module must explicitly state where complexity lives:

- orchestration complexity
- tool/schema complexity
- state/memory complexity
- reliability/safety complexity
- operations complexity (latency/cost/monitoring)
- protocol/interoperability complexity
- security/compliance complexity

---

## 7) Stage 6 Script Package Plan (`red-book/src/stage-6/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-optional.txt`
- `run_all_stage6.ps1`
- `run_ladder_stage6.ps1`

Core ladders (simple -> intermediate -> advanced):

1. Workflow vs Agent ladder
- `topic01a_workflow_first_simple.py`
- `topic01_workflow_vs_agent_intermediate.py`
- `topic01c_multi_step_agent_advanced.py`

2. Tooling and schema ladder
- `topic02a_tool_schema_simple.py`
- `topic02_tool_validation_intermediate.py`
- `topic02c_tool_failure_recovery_advanced.py`

3. Memory ladder
- `topic03a_memory_basics_simple.py`
- `topic03_memory_retrieval_intermediate.py`
- `topic03c_memory_policy_advanced.py`

4. Guardrails and HITL ladder
- `topic04a_guardrails_simple.py`
- `topic04_hitl_intermediate.py`
- `topic04c_policy_gated_actions_advanced.py`

5. Observability and eval ladder
- `topic05a_trace_basics_simple.py`
- `topic05_eval_metrics_intermediate.py`
- `topic05c_regression_suite_advanced.py`

6. Industry architecture bridge
- `topic06_industry_patterns.py`

7. Protocol/interoperability ladder
- `topic07a_mcp_tooling_simple.py`
- `topic07_protocol_interop_intermediate.py`
- `topic07c_a2a_collaboration_advanced.py`

8. Operations and reliability ladder
- `topic08a_budget_controls_simple.py`
- `topic08_latency_cost_optimization_intermediate.py`
- `topic08c_slo_regression_gate_advanced.py`

9. Security and incident ladder
- `topic09a_prompt_injection_defense_simple.py`
- `topic09_policy_and_permissions_intermediate.py`
- `topic09c_incident_response_advanced.py`

10. Labs
- `lab01_support_triage_agent.py`
- `lab02_finance_research_agent.py`
- `lab03_multi_agent_ops_assistant.py`
- `lab04_secure_agent_operations.py`

Script requirements:

- all scripts must include very detailed, clear, functional comments
- all scripts must print data/schema declarations
- all scripts must print expected metrics and interpretation text
- all scripts must include explicit failure-handling paths
- all scripts must include one test input and expected output format sample

---

## 8) Operable Roadmap (Week 12)

Day 1:
- workflow-first baseline, one deterministic pipeline

Day 2:
- single-agent with typed tools and validation

Day 3:
- memory patterns and retrieval memory

Day 4:
- guardrails, step limits, human-in-the-loop controls

Day 5:
- observability, tracing, evaluation harness

Day 6:
- industry mini case patterns (support + research + ops)

Day 7:
- final practice lab baseline run

Day 8:
- protocol interoperability drill (MCP vs A2A)

Day 9:
- cost/latency optimization pass with fixed budget targets

Day 10:
- security incident drills + postmortem writing

---

## 9) Notebook and Visuals Plan

Required visuals in chapter and scripts:

- architecture diagrams:
  - workflow pipeline
  - agent loop
  - multi-agent orchestrator pattern
- sequence diagrams:
  - user -> planner -> tool -> memory -> response
  - incident case with retry and fallback
- trace screenshots or JSON snippets for one successful run and one failed run
- benchmark summary table (before/after controlled change)

Notebook requirement:

- optional `stage6_explainer.ipynb` for visual walkthrough
- notebook must map 1:1 to script files and not introduce hidden steps

---

## 10) Practice Labs (Real, Operatable)

### Lab 1: Support Ticket Triage Agent

Goal:
- classify tickets, route to queue, generate structured response draft.

Required outputs:
- `results/lab1_outputs.jsonl`
- `results/lab1_metrics.csv`
- `results/lab1_failure_log.md`

### Lab 2: Finance Research Agent

Goal:
- retrieve notes + call analytics tool + produce grounded summary.

Required outputs:
- `results/lab2_outputs.jsonl`
- `results/lab2_grounding_report.md`
- `results/lab2_comparison_before_after.csv`

### Lab 3: Multi-Agent Ops Assistant

Goal:
- coordinator + specialist agents with policy gates and HITL checkpoint.

Required outputs:
- `results/lab3_trace.json`
- `results/lab3_policy_decisions.csv`
- `results/lab3_incident_postmortem.md`

### Lab 4: Secure Agent Operations Lab

Goal:
- harden tool permissions and defend against prompt injection + exfiltration attempts.

Required outputs:
- `results/lab4_security_tests.md`
- `results/lab4_guardrail_events.jsonl`
- `results/lab4_fix_validation.csv`

Lab rules:

1. fixed dataset and fixed eval set.
2. fixed prompt/version tags.
3. at least one controlled improvement rerun.
4. explicit before/after metric delta.
5. include one security test case.
6. include one operations test case (timeout/rate-limit/budget).

---

## 11) Troubleshooting and Realistic Problem Playbook

Required failure scenarios:

- wrong tool selected
- malformed tool arguments
- tool timeout / external API failure
- retrieval returns irrelevant context
- memory pollution (irrelevant stale state)
- runaway loops / excessive tool calls
- hallucinated action claims
- policy violation attempt (unsafe action)
- prompt injection attack succeeds
- data exfiltration attempt through tool call
- retry storm from poor backoff design
- non-deterministic regression after model/prompt change

Required troubleshooting workflow:

1. reproduce with fixed input and trace id
2. classify failure type
3. inspect tool input/output schema validity
4. inspect routing decision and stop conditions
5. inspect memory retrieval relevance
6. inspect grounding/citation evidence
7. inspect policy and permission decisions
8. apply one targeted fix only
9. rerun same case and record delta

Required logs per run:

- query id
- run id and trace id
- step index
- selected tool
- tool args
- tool return code
- latency and token/cost summary
- guardrail decision path
- prompt/policy/model version ids
- final answer and confidence note
- failure class (if any)

---

## 12) Debugging and Quality Gates

Required debugging flow:

- agent stalls -> inspect stop rule + tool response parsing + retry loop
- wrong tool choice -> inspect tool schema clarity + descriptions + routing hints
- unstable outputs -> inspect prompt/version drift + missing constraints + inconsistent state
- high cost -> inspect repeated context + missing cache + unnecessary tool calls
- low quality retrieval -> inspect chunking + retrieval policy + source coverage
- policy incidents -> inspect allowlist/denylist and escalation path

Quality gates:

- all Stage 6 scripts pass `run_all_stage6.ps1`
- ladders pass `run_ladder_stage6.ps1`
- lab outputs generated with expected files
- expected metrics documented and validated
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 13) Agent Reliability Implementation Spec

Required content:

- prompt/version control policy (`v1`, `v2`, `v3`)
- tool schema versioning policy
- deterministic fallback behavior for tool/API failures
- budget policy (steps, latency, token/cost)
- eval policy (task success, tool-call quality, safety, cost)
- regression policy (block merge when metric drops exceed threshold)

Required runnable checks:

- print prompt/tool/policy version ids in each run
- print parse/validation success rate for tool calls
- print cost and latency percentile summary
- print one failure sample and one corrected sample
- print before/after metric delta for one controlled change

---

## 14) Data and Schema Declaration Standard

Every example must include:

```
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Split/Eval policy: <fixed cases or split rule>
Type: <workflow/agent/multi-agent/eval>
```

Synthetic data must also declare generation method and purpose.

---

## 15) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Refactor chapter structure to Stage 3/4/5 pattern.
3. Add complexity scale and per-topic complexity explanation.
4. Refactor concept sections to mandatory module template.
5. Add protocol section (MCP vs A2A) with decision guide.
6. Add security threat-model section with realistic attack cases.
7. Add observability/eval section with fixed metrics and thresholds.
8. Create `red-book/src/stage-6/` ladders and runners.
9. Add explicit data/schema declarations in all examples.
10. Upgrade practice labs to operatable spec and fixed file outputs.
11. Add weighted self-test rubric and remediation flow.
12. Add resource catalog + link policy + verification date.
13. Final QA pass (terminology, encoding, duplicate cleanup).

---

## 16) Acceptance Criteria (Definition of Done)

Stage 6 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script mapping
- all Stage 6 scripts include very detailed, clear comments
- data and schema declarations are present in all examples
- labs are real, operatable, and file-output based
- chapter teaches both theory and industry implementation patterns
- chapter includes explicit MCP vs A2A distinctions and usage rules
- chapter includes benchmark/eval methodology and thresholds
- chapter includes operations controls (steps, latency, cost)
- troubleshooting section includes realistic failure drills and fixes
- stage-6 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 17) Additional Improvement Items

### A. Glossary and Notation

- lock notation: `task`, `state`, `tool_call`, `tool_result`, `trace_id`, `policy_decision`
- add glossary for: orchestration, agent loop, planner, supervisor, MCP, A2A, HITL, idempotency, retry storm, exfiltration

### B. Reproducibility

- fixed seed policy where randomness exists
- prompt/tool version log policy
- run-date and environment logging in project outputs

### C. Maintenance and QA

- link-check cadence (monthly)
- script smoke-test log template
- chapter changelog section

---

## 18) Priority Breakdown

P0 (must do):

- chapter restructure to operatable format
- Stage 6 script package + runners
- 4 real labs with fixed deliverables
- troubleshooting runbook with realistic incidents
- theory + industry implementation bridge
- detailed comment standard enforcement
- protocol section (MCP vs A2A) with examples
- security threat model + mitigation workflow
- benchmark/eval section with fixed thresholds

P1 (should do):

- stronger evaluation harness (quality, cost, latency, failure rate)
- optional framework adapters (OpenAI Agents SDK / LangGraph / CrewAI / AutoGen)
- operations controls and SLO-style run reports
- more failure drills with policy/HITL scenarios

P2 (nice to have):

- optional cloud deployment bridge (AWS/Azure)
- optional MCP server integration lab
- optional A2A cross-agent lab across two stacks

---

## 19) Chapter Simplification Blueprint (Mandatory)

Use this for every hard section:

1. Problem framing (what task this solves)
2. Intuition (mental model)
3. Mechanics (step-by-step execution)
4. Operatable code (ladder examples)
5. Failure pattern and fix

Per-module must include:

- `why this is hard`
- one checkpoint question before moving forward
- one explicit `do not trust this blindly` reliability note

---

## 20) Stage Transition Requirement

Handbook must end with `What Comes After Stage 6` and include:

- 2-3 sentence summary of Stage 7 focus
- mapping from Stage 6 skills to Stage 7 tasks
- readiness sentence before progression




