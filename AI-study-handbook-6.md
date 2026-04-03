# Stage 6 — AI Agents

*(Week 12)*

## Goal

Understand AI agents and how they interact with tools, memory, and workflows.

This stage is critical for building real AI systems such as trading assistants.

You are learning:

- how agents work
- how tools are used
- when to use workflows vs agents

This stage is where you move from:

> "I can ask ChatGPT questions"

to:

> "I understand how LLMs process text, why they fail, how prompting changes behavior, and how to build reliable systems around them."

---

## Quick Summary

An AI agent is **not "just a chatbot."**

It is a system where an LLM can:

- interpret a user request
- decide what action is needed
- choose a tool
- call that tool
- inspect the result
- continue or stop

This makes agents powerful, but also harder to control.

A beginner should finish this stage understanding:

- what an agent is
- what tools are
- why deterministic workflows should come first
- what memory means in agent systems
- how RAG and tools combine with agents
- why agents are useful but risky
- how to design safe, traceable agent systems

---

## Study Materials

**LangChain Documentation**
https://python.langchain.com/docs/get_started/introduction

### Concepts

- Agents
- Tools
- Memory
- RAG
- Workflows

---

## Key Knowledge (Deep Understanding)

### 1. What is an AI Agent

An AI agent is an LLM that can **decide what actions to take**.

Instead of just answering questions, it:

- selects tools
- executes actions
- returns results

#### Beginner Explanation

A normal LLM-only system works like this:

```
user input → LLM → response
```

An agent system is different:

```
user input → LLM decides → tool call → result → LLM decides again → final answer
```

The model is not only generating language — it is also **participating in a control loop**. That control loop is what makes it an agent.

#### Simple Mental Model

Think of an agent like a junior analyst with access to tools.

The analyst can:

- read the request
- decide whether data is needed
- open a calculator
- fetch stock prices
- search a document
- summarize results

Without tools, the analyst can only guess. With tools, the analyst can act.

#### Why Agents Matter

Agents are useful when a task requires:

- multiple steps
- outside information
- calculation
- retrieval
- dynamic decision-making

Examples: market assistant, coding assistant, document Q&A assistant, research assistant, internal enterprise automation assistant.

#### Step-by-Step Agent Flow

1. **Receive user goal** — e.g. "Analyze NVDA and tell me whether momentum looks strong."
2. **Decide what is needed** — fetch recent stock data, compute indicators, summarize findings.
3. **Call tool** — A tool gets real data.
4. **Observe tool result** — The agent sees the output of the tool.
5. **Decide whether more action is needed** — It may call another tool or stop.
6. **Produce final answer** — The agent explains results to the user.

#### Important Algorithms / Mechanisms

**A. ReAct-style Reason-and-Act Loop** — A very important agent pattern.

How it works:

1. Think about what to do
2. Choose an action/tool
3. Observe the result
4. Think again
5. Repeat until done

*Why important: This is one of the clearest conceptual foundations for tool-using agents.*

---

**B. Planner-Executor Pattern** — Used in more structured agents.

How it works:

1. Planner breaks task into steps
2. Executor performs each step
3. Results are combined

*Why important: Separates reasoning from execution and can make agents easier to debug.*

---

**C. Single-Step Tool Routing** — A simpler agent pattern.

*How it works: The LLM chooses one tool directly based on the user query.*

*Why important: Useful when you want limited agent behavior without full autonomy.*

---

**D. Multi-Step Decision Loop** — The agent can call several tools in sequence.

*Why important: Supports dynamic tasks, but increases complexity and failure risk.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Flexible | Harder to control |
| Can use real tools and real data | Harder to debug |
| Can handle multi-step tasks | Can choose wrong tools |
| More powerful than plain prompting | May loop unnecessarily |
| | Can produce unstable behavior without guardrails |

---

### 2. Tools

Tools are **functions the agent can call**.

Examples: fetch stock data, search documents, calculate indicators.

**Key idea:** Tools extend LLM capability.

#### Beginner Explanation

A tool is just a function or external capability the agent can use.

Examples:

- a Python function
- a search API
- a database query
- a stock data fetcher
- a calculator
- a file retriever
- a weather API

> LLM = language reasoning/generation
> Tool = action or external capability

#### Simple Mental Model

If the LLM is the "brain," tools are the "hands and instruments."

| Tool | Purpose |
|---|---|
| calculator tool | do accurate math |
| retrieval tool | access documents |
| market data tool | fetch real prices |
| indicator tool | compute RSI, moving averages, returns |

#### What Makes a Good Tool

| Good Tool | Bad Tool |
|---|---|
| One clear purpose | Vague purpose |
| Clear inputs | Mixed responsibilities |
| Clear outputs | Unclear return structure |
| Reliable behavior | Hidden side effects |
| Useful error handling | |

#### Step-by-Step Tool Design Thinking

1. **Define one job** — `fetch_stock_price(symbol)` should fetch data, not also summarize.
2. **Define input schema** — What input is needed? (e.g. ticker symbol, time range)
3. **Define output schema** — What exactly comes back? (e.g. rows of prices, or a dictionary with fields)
4. **Define failure behavior** — What happens if ticker is invalid? API fails? No data exists?
5. **Keep tool deterministic when possible** — Tools should usually be more reliable than the LLM itself.

#### Important Algorithms / Mechanisms

**A. Tool Selection / Routing** — The agent chooses which tool to call.

*How it works: The LLM matches the user request to tool descriptions.*

*Why important: If routing is bad, even good tools fail in practice.*

---

**B. Function Calling / Structured Arguments** — The LLM provides arguments in a structured format.

Instead of free-form text, the model outputs fields like:

```
symbol = "NVDA"
period = "1mo"
```

*Why important: This reduces ambiguity and makes tool use safer.*

---

**C. Input Validation** — The tool checks whether inputs are valid before running.

*Why important: Prevents garbage input from silently causing bad downstream results.*

---

**D. Output Normalization** — Tool outputs should be returned in consistent structure.

*Why important: The agent and downstream logic should not need to guess how to parse tool results.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Give LLMs access to real-world data and actions | Poor tool design causes fragile agents |
| Reduce hallucination when used correctly | Unclear tool descriptions cause wrong calls |
| Support automation | Side effects can create risk |
| Enable powerful workflows | Tools need monitoring and validation too |

---

### 3. Workflow vs Agent

```
Workflow (recommended first):  input → step1 → step2 → output
Agent (dynamic):               input → decide → tool → decide → output
```

#### Beginner Explanation

**A workflow is fixed.** You already know the steps:

1. get input
2. fetch data
3. compute indicators
4. send summary prompt
5. return output

**An agent is dynamic.** It decides what to do next — more flexibility, but also more unpredictability.

#### Why Workflow Should Come First

Beginners often jump into agents too early because agents sound powerful.

But most real systems should start as workflows, because workflows are:

- easier to test
- easier to debug
- easier to trust
- easier to monitor
- often fully sufficient

Then, only add agent behavior if true dynamic decision-making is needed.

#### Comparison

| Aspect | Workflow | Agent |
|---|---|---|
| Steps | Fixed | Dynamic |
| Debugging | Easier | Harder |
| Control | High | Lower |
| Flexibility | Lower | Higher |
| Recommended for beginners | Yes | After workflow |

#### When to Use Each

**Use a workflow when:**

- steps are known in advance
- you need reliability
- you need traceability
- task is repeatable

**Use an agent when:**

- steps vary by request
- tool choice is dynamic
- user intent is open-ended
- flexibility is worth extra complexity

#### Important Algorithms / Mechanisms

**A. Deterministic Pipeline** — The system always runs the same sequence of steps.

*Why important: This is the safest starting point for production-grade AI systems.*

---

**B. Rule-Based Router** — A hybrid approach.

Example:

```
if user asks for stock analysis  → market workflow
if user asks for document Q&A    → retrieval workflow
```

*Why important: Often better than a full agent for many business systems.*

---

**C. LLM-Based Router** — The LLM classifies the request and selects a path.

*Why important: More flexible than rules, but also less deterministic.*

---

**D. Agentic Orchestration** — A fully dynamic decision loop selects next steps during execution.

*Why important: Useful for open-ended tasks, but should be introduced carefully.*

#### Strengths and Weaknesses

| Workflow-First Strengths | Going Full Agent Too Early |
|---|---|
| Easier to build | Unpredictable behavior |
| Easier to evaluate | Debugging becomes difficult |
| Easier to deploy safely | Harder to measure failure points |
| Lower operational risk | Can waste tokens and tool calls |

---

### 4. Memory

Memory allows the agent to remember past steps and maintain conversation context.

| Type | Description |
|---|---|
| Short-term | Conversation / session memory |
| Long-term | Stored knowledge across sessions |

#### Beginner Explanation

Without memory, every step is isolated. With memory, the system can remember:

- what the user asked earlier
- what tools were already called
- what results were found
- user preferences
- long-term stored knowledge

#### Two Main Types

**A. Short-Term Memory** — Session or conversation memory.

Examples: earlier user messages, current task state, current tool outputs.

*This helps the agent stay coherent during one interaction.*

---

**B. Long-Term Memory** — Stored across sessions.

Examples: user preferences, saved summaries, persistent notes, prior research results, indexed knowledge base.

*This helps the system improve continuity over time.*

#### Important Design Question

Not everything should be remembered.

Too much memory causes:

- noise
- confusion
- cost
- privacy risk
- retrieval clutter

> Good memory design means storing only useful, relevant information.

#### Important Algorithms / Mechanisms

**A. Conversation Buffer Memory** — Store recent conversation turns.

*How it works: The system includes previous messages in future prompts.*

*Why important: Simplest form of memory.*

---

**B. Summary Memory** — Compress long history into shorter summaries.

*How it works: Older content is summarized and retained compactly.*

*Why important: Helps with long conversations and context limits.*

---

**C. Retrieval-Based Memory** — Store memories externally and retrieve relevant ones when needed.

How it works:

1. Store memory entries
2. Search relevant entries later
3. Inject them into context

*Why important: Scales better than stuffing all past text into prompts.*

---

**D. State Memory / Task State Tracking** — Track what the agent has already done.

Examples: tool already called, documents already searched, hypothesis already tested.

*Why important: Prevents repeated work and supports multi-step execution.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Improves continuity | Irrelevant memory can confuse the model |
| Supports multi-step tasks | Too much memory increases cost |
| Avoids repeating work | Long-term memory needs retrieval quality |
| Can personalize behavior | Privacy and correctness matter |

---

### 5. RAG + Agent

Agents often use both **retrieval (RAG)** and **tools** together.

```
Combined system = more powerful + more complex
```

#### Beginner Explanation

A strong real-world agent often needs both:

- **RAG** for knowledge access
- **Tools** for actions and computation

*Example: A user asks "Summarize recent NVDA performance and compare it with our internal research note."*

The system may need to:

1. fetch market data with tools
2. retrieve internal note with RAG
3. compare both
4. summarize findings

This is more capable than prompt-only, tool-only, or retrieval-only — but also harder to design correctly.

#### Typical Combined Flow

```
user query
→ decide if retrieval is needed
→ retrieve documents
→ decide if tool action is needed
→ call tool
→ combine retrieved context + tool results
→ final answer
```

#### Why This Matters

Many enterprise AI systems are combinations of:

- LLM
- retrieval
- tools
- workflow/agent controller
- logging
- validation

> That is the practical architecture of modern AI apps.

#### Important Algorithms / Mechanisms

**A. Retrieval Step** — Search relevant documents before answer generation.

*Why important: Provides knowledge grounding.*

---

**B. Tool-Augmented Reasoning** — Use tools for real actions or calculations.

*Why important: Retrieval alone cannot compute or act.*

---

**C. Context Fusion** — Combine retrieved documents, tool outputs, conversation state, and user request.

*Why important: The final answer quality depends on how well these sources are combined.*

---

**D. Multi-Stage Orchestration** — Different stages decide: retrieve? act? ask follow-up? stop?

*Why important: This is the heart of more advanced agent systems.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Highly capable | More moving parts |
| Grounded + actionable | Harder evaluation |
| Useful for enterprise assistants, research tools, analysts, copilots | Retrieval can fail |
| | Tool use can fail |
| | Orchestration can fail |

---

## Difficulty Points

### 1. Starting with agents too early

**Why it happens:** Agents sound more advanced and exciting.

**Why it is a problem:** You may build something flexible but impossible to debug.

**Fix strategy:** Start with plain functions, deterministic workflow, logging, and evaluation. Only then add agent behavior if you truly need dynamic decision-making.

### 2. Too many tools

**Why it happens:** Beginners think more tools = more power.

**Why it is a problem:** Too many tools increase wrong tool selection, confusion, debugging complexity, and overlapping functionality.

**Fix strategy:** Start with a small toolset — one tool per clear purpose, no overlapping tools, strong descriptions, strong schemas.

### 3. No control over agent behavior

**Why it happens:** LLMs are probabilistic and may misroute or over-act.

**Why it is a problem:** The agent may call unnecessary tools, skip needed steps, loop, answer without grounding, or misuse a tool.

**Fix strategy:** Add guardrails: max steps, allowed tool list, structured tool arguments, stopping rules, fallback to workflow, human review for high-risk actions.

### 4. Debugging difficulty

**Why it happens:** There are more moving parts — prompts, routing, tool calls, memory, retrieval, outputs.

**Why it is a problem:** A failure could come from bad tool, bad routing, bad prompt, bad retrieval, or bad memory injection.

**Fix strategy:** Log everything:

- user input
- tool chosen
- tool input
- tool output
- retrieved docs
- final response
- errors
- step count

### 5. Poor tool design

**Why it happens:** People wrap messy code as "tools" without clear interface design.

**Why it is a problem:** The agent cannot reliably use tools if descriptions are vague, input schema is unclear, output format changes, or error behavior is inconsistent.

**Fix strategy:** Design tools like APIs — one purpose, explicit schema, explicit errors, stable outputs, easy examples.

### 6. Memory overload

**Why it happens:** People think remembering more is always better.

**Why it is a problem:** The model may get distracted by irrelevant context or exceed token budget.

**Fix strategy:** Use selective memory, summarization, retrieval-based memory, expiration rules, and relevance filtering.

### 7. Confusing autonomy with reliability

**Why it happens:** Agent demos make autonomy look impressive.

**Why it is a problem:** In production, reliability often matters more than flexibility.

**Fix strategy:** Prefer the simplest system that solves the task:

1. rules first
2. workflow second
3. agent third

---

## Agent Workflow (Real World)

1. Define the task
2. Decide whether workflow or agent is needed
3. Design tools
4. Define tool schemas
5. Build deterministic version first
6. Add logging and validation
7. Add agent loop carefully
8. Add memory only if needed
9. Add retrieval if knowledge access is needed
10. Evaluate failure cases
11. Add guardrails
12. Deploy with monitoring

### Beginner Explanation of Each Step

1. **Define the task** — e.g. "Analyze stock trend and explain risk."
2. **Decide whether workflow or agent is needed** — Do not assume agent first.
3. **Design tools** — Create clear functions: `fetch_stock`, `compute_indicators`, `search_notes`.
4. **Define tool schemas** — Specify inputs/outputs clearly.
5. **Build deterministic version first** — Prove the system can work without autonomy.
6. **Add logging and validation** — Make each step observable.
7. **Add agent loop carefully** — Allow the model to choose actions only after basics work.
8. **Add memory only if needed** — Avoid unnecessary complexity.
9. **Add retrieval if knowledge access is needed** — Especially for internal or changing knowledge.
10. **Evaluate failure cases** — Invalid symbol, empty result, irrelevant docs, unclear user query.
11. **Add guardrails** — Limits, fallbacks, validation, refusal conditions.
12. **Deploy with monitoring** — Watch real behavior over time.

---

## Debugging Checklist for Stage 6

If an agent behaves badly, check:

- [ ] Does the task really need an agent?
- [ ] Could a workflow solve this more reliably?
- [ ] Are tool descriptions clear enough?
- [ ] Are tool inputs validated?
- [ ] Are tool outputs consistent?
- [ ] Is the agent choosing the wrong tool?
- [ ] Is retrieval poor?
- [ ] Is memory injecting irrelevant context?
- [ ] Is the agent looping too long?
- [ ] Are logs complete enough to trace the failure?
- [ ] Are stopping rules defined?
- [ ] Does the system have safe fallback behavior?

---

## Example Code

```python
from langchain.agents import initialize_agent

# (Simple placeholder — full implementation comes in project)
```

**Beginner Explanation:**

Importing an agent framework does **not** create a good agent automatically.

A good agent still depends on:

- tool design
- prompt design
- schemas
- logging
- control logic
- evaluation

> The framework is only infrastructure. The real engineering work is in system design.

---

## Practice Project

### Project: Tool-Based Market Assistant

**Goal:** Build an AI assistant that fetches stock data, analyzes trends, and provides a summary.

**Step 1 — Build plain functions (NO agent yet)**

```python
def fetch_stock(symbol):
    pass

def calculate_indicators(df):
    pass

def summarize(df):
    pass
```

*Why this step matters: This forces you to separate the system into clear components and proves the core logic works before adding agent complexity.*

*Start with ordinary Python functions — one gets data, one computes indicators, one summarizes findings. If these functions are weak, the agent version will also be weak.*

---

**Step 2 — Build deterministic workflow**

```
input → fetch → indicators → LLM summary → output
```

*This is your FIRST working version.*

*Why this step matters: This gives you a stable baseline. Before making the system dynamic, make it correct.*

> **Beginner rule:** If the deterministic workflow is not working well, do not build the agent yet. Fix the workflow first.

---

**Step 3 — Add LLM explanation**

Use prompt:

```
Given these indicators, explain trend and risk.
```

Better structured prompt version:

```
Given these stock indicators, explain the current trend and risk in simple language for a beginner investor.
Include:
1. trend direction
2. momentum interpretation
3. main risk
4. one cautious conclusion
```

*Why this step matters: The LLM is used where it is strongest — language explanation. The deterministic steps fetch and compute real data first. That is good system design.*

---

**Step 4 — Convert functions into tools**

Wrap functions for agent use.

*Why this step matters: You now expose your reliable functions to the LLM as callable actions. Do not let the agent directly "do everything" — let it choose among well-designed capabilities.*

---

**Step 5 — Build simple agent**

Agent decides: which tool to use, when to stop.

*Why this step matters: This introduces dynamic behavior gradually.*

*Start with: only 2–3 tools, max step limit, simple user queries, logs turned on.*

---

**Step 6 — Add logging**

Track: tool calls, inputs, outputs.

Suggested log fields:

- timestamp
- user query
- chosen tool
- tool input
- tool output summary
- final answer
- error if any
- number of steps used

*Why this step matters: Without logs, agent debugging becomes guesswork.*

---

**Step 7 — Test failures**

Test: invalid ticker, missing data, unclear query.

Also test:

- tool timeout
- empty retrieval result
- unsupported user request
- contradictory data
- repeated tool loop

*Why this step matters: Good systems are tested not only on success cases, but also on failure cases.*

### Deliverables

- tool functions
- workflow script
- agent version
- logs
- README

### Experiment Tasks

**Experiment 1 — Workflow vs agent comparison**

Build both versions and compare: reliability, complexity, quality, debuggability.

- Lesson: Agent is not automatically better.

**Experiment 2 — Add too many tools on purpose**

Add several overlapping tools.

- Purpose: See how routing quality degrades.
- Lesson: Tool minimalism matters.

**Experiment 3 — Add memory vs no memory**

Compare whether memory helps or only adds noise.

- Lesson: Memory should be added intentionally, not automatically.

**Experiment 4 — Add retrieval**

Let the assistant search one small research-note corpus.

- Lesson: RAG + tools can be powerful, but adds failure modes.

**Experiment 5 — Force invalid inputs**

Use bad tickers and empty results.

- Lesson: Tool error handling is essential.

**Experiment 6 — Add step limit**

Compare behavior with and without maximum step constraints.

- Lesson: Guardrails reduce runaway loops.

### Common Mistakes

1. **Skipping workflow stage** — You lose a stable baseline and make debugging harder. *Fix: Always build deterministic workflow first.*

2. **Too many tools** — Tool routing becomes noisy and unreliable. *Fix: Start with minimal, non-overlapping tools.*

3. **No logging** — You cannot trace why the system failed. *Fix: Log every decision and tool call.*

4. **Unclear tool schema** — The agent passes bad arguments or misreads outputs. *Fix: Use explicit schemas and stable return structures.*

5. **Letting the agent act without limits** — The agent may loop, overuse tools, or make unsafe calls. *Fix: Use max steps, allowed tools, stop conditions, and fallbacks.*

6. **Using memory without relevance filtering** — Irrelevant context hurts decision quality. *Fix: Store selectively and retrieve only relevant memory.*

7. **No failure-case testing** — Production failures appear later and are harder to explain. *Fix: Test negative and edge cases intentionally.*

---

## Final Understanding

> Agents extend LLMs by allowing them to take actions using tools, but require careful control and design.

> The best agent systems are usually built on top of clear tools, deterministic workflows, logging, and guardrails — not pure autonomy.

---

## Self Test

### Questions

1. What is an AI agent?
2. How is an agent different from a plain LLM chatbot?
3. What is a tool in an agent system?
4. Why do tools extend LLM capability?
5. What makes a good tool?
6. Why should workflows usually come before agents?
7. What is the difference between a workflow and an agent?
8. When should you choose a workflow instead of an agent?
9. What is short-term memory in an agent?
10. What is long-term memory in an agent?
11. Why can too much memory be harmful?
12. What is retrieval-based memory?
13. Why is RAG useful in agent systems?
14. What does RAG + agent allow that prompt-only systems cannot do as well?
15. What is ReAct-style reasoning?
16. What is the planner-executor pattern?
17. Why can too many tools hurt performance?
18. Why is logging critical in agent systems?
19. What kinds of things should you log?
20. Why is tool schema clarity important?
21. What is tool routing?
22. Why do agents need stopping rules?
23. What is a max-step limit for?
24. Why is workflow-first design safer?
25. What is a common failure mode when beginners start with agents too early?
26. Why is deterministic output often easier to trust?
27. What should you test besides happy-path success cases?
28. Why is autonomy not the same as reliability?
29. What is the simplest safe build order for an agent system?
30. What is the main lesson of this stage?

### Answers

1. An AI agent is an LLM-based system that can decide which actions to take, often by selecting and using tools before producing a final answer.

2. A plain LLM chatbot mostly generates text directly from the prompt. An agent can also choose actions, call tools, inspect results, and continue step by step.

3. A tool is a callable function or external capability the agent can use, such as fetching stock data, searching documents, or doing calculations.

4. Because tools let the LLM access real data, perform computations, and take actions that text generation alone cannot do reliably.

5. A good tool has one clear purpose, clear inputs, clear outputs, reliable behavior, and good error handling.

6. Because workflows are easier to test, debug, monitor, and trust. They give you a stable baseline before adding dynamic agent behavior.

7. A workflow follows fixed steps. An agent decides dynamically which steps or tools to use next.

8. When the steps are already known, reliability matters more than flexibility, and the task does not require open-ended dynamic decisions.

9. Short-term memory is temporary context from the current conversation or task, such as recent messages or recent tool outputs.

10. Long-term memory is persistent stored information that can be reused later, such as user preferences, saved notes, or indexed past knowledge.

11. Because it can add irrelevant context, increase token cost, confuse the model, and reduce answer quality.

12. It is a memory system where stored memories are searched and only relevant items are retrieved and injected into the current context.

13. Because it lets the agent access external knowledge sources and ground its answers in retrieved documents instead of relying only on model memory.

14. It allows a system to both retrieve knowledge and take actions, combining grounding with computation or external operations.

15. It is an agent pattern where the model alternates between thinking about what to do, taking an action, observing results, and continuing until completion.

16. It is a pattern where one component plans the steps and another component executes them, making the system more structured and often easier to debug.

17. Because the agent may choose the wrong one, tool descriptions may overlap, and the routing problem becomes harder.

18. Because without logs you cannot trace how the agent made decisions, which tools it called, or where the failure happened.

19. You should log user input, chosen tool, tool input, tool output, retrieved context, final response, errors, and step count.

20. Because agents need clear argument and output formats. If schemas are vague, tool calls become unreliable.

21. Tool routing is the process of deciding which tool should be used for a given request.

22. Because otherwise they may keep calling tools unnecessarily, loop, waste cost, or fail to terminate correctly.

23. It limits how many reasoning/action steps an agent can take, helping control loops and runaway behavior.

24. Because it keeps behavior deterministic and easier to inspect before introducing dynamic control decisions.

25. They build something flexible but unstable, with unclear tool use, poor traceability, and hard-to-debug failures.

26. Because you know exactly what the system will do under the same conditions, which makes testing and operational reliability easier.

27. You should test invalid input, empty data, tool errors, unclear requests, bad retrieval, unsupported requests, and loop behavior.

28. Because a system can make more decisions on its own while still making poor or inconsistent decisions. More freedom does not guarantee correctness.

29. Build plain functions first, then a deterministic workflow, then add logging and validation, then add agent behavior only if needed.

30. Agents are powerful because they let LLMs use tools and take actions, but good agent systems require careful tool design, workflow-first thinking, logging, validation, and guardrails.

---

## What You Must Be Able To Do After Stage 6

- [ ] Explain what an AI agent is in plain English
- [ ] Explain the difference between a workflow and an agent
- [ ] Explain what tools are and why they matter
- [ ] Design a small, clear tool set
- [ ] Explain short-term vs long-term memory
- [ ] Explain why RAG and agents are often combined
- [ ] Build a deterministic tool-based workflow first
- [ ] Identify common agent failure modes
- [ ] Explain why logging, schemas, and guardrails are essential
- [ ] Understand that real agent engineering is about controlled orchestration, not just autonomy
