# Stage 12 — AI System Architectures

**(Week 22)**

---

## Goal

Understand the major architecture patterns used in modern AI systems.

This stage is about thinking like a system designer, not just a model user.

**You are learning:**

- how different AI architectures work
- when to use each architecture
- how to compare tradeoffs
- how to design systems before coding them

---

## Quick Summary

Two AI systems can use the same model and still perform very differently because the architecture is different.

**Architecture decides:**

- what data enters the system
- how information flows
- where decisions happen
- where retrieval happens
- whether tools are used
- whether outputs are constrained
- how failures are handled
- how the system is evaluated

A beginner should finish this stage understanding:

- what architecture means in AI systems
- when simple LLM apps are enough
- when RAG is the right design
- when agents are useful
- when multi-agent systems are justified
- why workflow-first thinking is often safer
- how to compare architectures before writing code

---

## Key Architectures

- LLM Application Architecture
- RAG Architecture
- AI Agent Architecture
- Multi-Agent Systems

---

## Study Materials

- **LangChain Documentation** — https://python.langchain.com/docs/
- **LangGraph Documentation** — https://langchain-ai.github.io/langgraph/
- **LlamaIndex Documentation** — https://docs.llamaindex.ai/

---

## Key Knowledge (Deep Understanding)

### 1. Why Architecture Matters

Two systems can use the same model and get very different results because architecture is different.

**Architecture determines:**

- what data enters the system
- how information flows
- where decisions happen
- how retrieval is done
- how outputs are controlled
- how failures are handled

**A top AI engineer asks:**

- What is the problem?
- What type of architecture fits it?
- What should be deterministic?
- What should be learned?
- What should be retrieved?
- What can fail first?

#### Beginner Explanation

A lot of beginners ask:

> "Which model should I use?"

That is important, but it is not enough.

A stronger question is:

> "What kind of system structure should I build?"

Because the model is only one part.

For example, the same LLM can be used inside:

- a plain chat app
- a document Q&A system
- a tool-using agent
- a multi-agent planning workflow

The model may be identical, but the behavior, reliability, cost, latency, and failure patterns can be very different.

#### Simple Mental Model

Architecture is the shape of the system.

If the model is the brain, architecture is:

- the nervous system
- the memory layout
- the tool access
- the decision path
- the failure-control structure

So architecture determines how the system behaves in the real world.

#### Step-by-Step Thinking Pattern

Before coding, ask:

**Step 1 — What is the real problem?**

Examples:
- explain a concept
- answer from documents
- use tools to perform multi-step actions
- coordinate multiple specialized roles

**Step 2 — What kind of information is needed?**

- general model knowledge?
- private documents?
- real-time API data?
- multi-step reasoning state?

**Step 3 — What parts should be fixed vs dynamic?**

- fixed workflow?
- dynamic routing?
- human review step?
- retrieval step?

**Step 4 — What failure is most likely?**

- hallucination?
- wrong retrieval?
- tool misuse?
- too much latency?
- bad coordination?

**Step 5 — What is the simplest architecture that solves the problem?**

This is one of the most important architecture rules.

#### Important Algorithms / Mechanisms for Why Architecture Matters

**A. Information Flow Design**

The architecture decides how input moves through the system.

How it works:
- input enters one component
- component transforms it
- result moves to another component
- final output is produced

> **Why important:** Even a strong model can fail if information flows badly.

**B. Control Flow Design**

Architecture defines where decisions happen.

Examples:
- fixed workflow
- LLM-based routing
- tool-calling loop
- multi-agent orchestration

> **Why important:** Control flow determines system complexity and reliability.

**C. Boundary and Interface Design**

Every component should have a clear job and output format.

> **Why important:** Poor boundaries create fragile systems.

**D. Failure Surface Design**

Every architecture creates a different set of likely failures.

> **Why important:** A good system architect designs with failure in mind, not after failure happens.

#### Strengths of Good Architecture Thinking

- better system fit
- fewer unnecessary components
- easier debugging
- clearer tradeoffs
- better production readiness

#### Weaknesses of Poor Architecture Thinking

- wrong system for the task
- unnecessary complexity
- hard-to-debug behavior
- weak reliability
- poor cost/latency tradeoffs

---

### 2. LLM Application Architecture

This is the simplest architecture.

**Basic flow:**

```
user input
   ↓
prompt construction
   ↓
LLM
   ↓
formatted response
```

#### Best for

- summarization
- explanation
- writing assistants
- basic chat apps

#### Strengths

- simple to build
- fast to prototype
- good for general knowledge tasks

#### Weaknesses

- no external knowledge grounding
- hallucination risk
- weak for private or changing knowledge

#### Important design elements

- prompt templates
- output formatting
- validation
- fallback handling

#### Beginner Explanation

This is the simplest kind of modern AI application.

The user gives input.
The system builds a prompt.
The LLM produces a response.

That is it.

This architecture is best when:

- you do not need private documents
- you do not need external tools
- you do not need multi-step action
- the task is mostly language transformation

**Examples:**

- "Explain reinforcement learning in simple words"
- "Rewrite this email more professionally"
- "Summarize this paragraph"
- "Generate a draft blog outline"

#### Step-by-Step Mental Model

**Step 1 — User sends text**

Example: "Explain what overfitting means."

**Step 2 — Prompt is constructed**

The system may add:
- role
- tone
- format instructions
- constraints

**Step 3 — LLM generates answer**

The model uses internal learned patterns to respond.

**Step 4 — Output is formatted or validated**

The app may:
- trim output
- parse JSON
- check schema
- show final text to user

#### Important Algorithms / Mechanisms for LLM App Architecture

**A. Prompt Template Construction**

The system places user input inside a defined prompt pattern.

How it works:
- system instructions
- task instructions
- user content
- format instructions

> **Why important:** Prompt structure strongly affects behavior.

**B. Zero-Shot Prompting**

The model is asked to do the task without examples.

> **Why important:** Simple baseline for many LLM-only applications.

**C. Few-Shot Prompting**

The prompt includes sample examples.

> **Why important:** Can improve consistency and formatting.

**D. Output Validation**

The result may be checked for:
- required fields
- valid JSON
- length constraints
- allowed labels

> **Why important:** Even simple LLM apps need reliability controls.

#### Best For

Use plain LLM architecture when:

- general knowledge is enough
- task is simple
- no private data is required
- speed of prototyping matters

#### Common Failure Modes

- hallucinated facts
- vague answers from vague prompts
- inconsistent structure
- poor performance on knowledge-sensitive tasks

---

### 3. RAG Architecture

**Basic flow:**

```
user query
   ↓
retrieval
   ↓
documents/chunks
   ↓
prompt construction
   ↓
LLM
   ↓
grounded answer
```

#### Best for

- Q&A over documents
- enterprise knowledge systems
- PDF assistants
- research assistants

#### Strengths

- brings in external knowledge
- reduces hallucination
- works with private data
- easier to update than fine-tuning

#### Weaknesses

- retrieval can fail
- chunking matters a lot
- answer quality depends on retrieval quality

#### Important design elements

- ingestion pipeline
- chunking strategy
- embeddings
- vector DB
- retrieval filters
- citations

#### Beginner Explanation

**RAG** stands for **Retrieval-Augmented Generation**.

Instead of asking the model to answer only from what it learned during training, the system first retrieves relevant documents and then asks the LLM to answer using those documents.

This architecture is powerful when the answer depends on:

- private files
- changing documents
- enterprise knowledge
- policy manuals
- PDFs
- notes
- research sources

#### Simple Mental Model

Without RAG:

```
question → LLM memory → answer
```

With RAG:

```
question → search docs → give evidence to LLM → grounded answer
```

That is the key difference.

#### Step-by-Step Mental Model

**Step 1 — User asks a question**

Example: "What does the onboarding policy say about contractor access?"

**Step 2 — Query is embedded or processed for retrieval**

The system prepares the query for search.

**Step 3 — Relevant chunks are retrieved**

The system finds document pieces likely to contain the answer.

**Step 4 — Prompt is built with context**

The retrieved text is injected into the LLM prompt.

**Step 5 — LLM answers from context**

The output should be grounded in the retrieved evidence.

**Step 6 — Citations may be added**

The system can show:
- source document
- chunk ID
- page number

#### Important Algorithms / Mechanisms for RAG Architecture

**A. Document Chunking**

Documents are split into smaller retrievable pieces.

> **Why important:** Bad chunking can destroy retrieval quality.

**B. Embedding-Based Retrieval**

Query and chunks are converted into vectors and compared.

> **Why important:** This supports semantic search.

**C. Top-K Retrieval**

The retriever returns the most relevant chunks.

> **Why important:** The model cannot read the full corpus every time.

**D. Re-Ranking**

Retrieved results may be reordered using a stronger relevance model.

> **Why important:** Can improve retrieval precision.

**E. Grounded Prompt Construction**

The LLM is instructed to answer only from retrieved context.

> **Why important:** This reduces unsupported guessing.

#### Best For

Use RAG when:

- knowledge changes often
- private docs are needed
- grounded answers matter
- citations matter
- you want enterprise or document Q&A

#### Common Failure Modes

- wrong chunks retrieved
- chunks too small or too large
- missing citations
- answer goes beyond evidence
- too much irrelevant context injected

---

### 4. AI Agent Architecture

**Basic flow:**

```
user request
   ↓
LLM planner/controller
   ↓
tool choice
   ↓
tool execution
   ↓
observation/result
   ↓
LLM continues or answers
```

#### Best for

- multi-step tasks
- tool use
- assistants that act, not just answer
- automation flows

#### Strengths

- dynamic behavior
- flexible decision-making
- can use tools/APIs
- can combine reasoning and action

#### Weaknesses

- harder to control
- more difficult to debug
- can loop or misuse tools
- expensive in tokens/latency

#### Important design elements

- tool schema
- step limits
- error handling
- memory/state
- logging/tracing

#### Beginner Explanation

An agent architecture is used when the system must **do things**, not just answer with text.

The system may need to:

- search documents
- call an API
- run a calculator
- fetch stock data
- query a database
- decide what to do next based on results

That is what makes it more agent-like.

#### Simple Mental Model

Plain LLM app:
- read prompt
- answer once

Agent:
- read request
- decide next action
- use a tool
- inspect result
- maybe continue
- then answer

That extra control loop is the big difference.

#### Step-by-Step Mental Model

**Step 1 — User asks for something**

Example: "Analyze NVDA, compare recent trend, and summarize risk."

**Step 2 — LLM decides what is needed**

Maybe:
- fetch stock data
- compute indicators
- retrieve research note

**Step 3 — Tool is selected**

The agent chooses one available capability.

**Step 4 — Tool runs**

The tool returns structured result.

**Step 5 — Agent observes result**

The LLM sees the tool output.

**Step 6 — Agent decides whether to continue**

Maybe:
- use another tool
- ask a follow-up
- stop and answer

**Step 7 — Final answer is produced**

The user sees a synthesized result.

#### Important Algorithms / Mechanisms for Agent Architecture

**A. ReAct-Style Loop**

Reason → act → observe → continue.

> **Why important:** This is one of the most important mental models for tool-using agents.

**B. Tool Routing**

The controller chooses which tool fits the current subtask.

> **Why important:** Wrong routing breaks agent quality quickly.

**C. Function Calling / Structured Tool Arguments**

The LLM outputs structured tool inputs.

> **Why important:** Reduces ambiguity and makes tool execution safer.

**D. Step Limit / Guardrail Logic**

The system limits how many actions the agent can take.

> **Why important:** Prevents runaway loops and waste.

**E. State Tracking**

The agent remembers:
- what was already done
- what tool outputs were observed
- what remains unresolved

> **Why important:** Multi-step tasks require execution state.

#### Best For

Use agent architecture when:

- system must use tools
- task is multi-step
- dynamic action selection is valuable
- workflow cannot be fully fixed in advance

#### Common Failure Modes

- wrong tool choice
- repeated unnecessary steps
- tool loops
- weak logging
- poor schema design
- agent acts when simple workflow would be better

---

### 5. Multi-Agent Systems

**Basic flow:**

```
user request
   ↓
planner agent
   ↓
specialized agents
   ├─ retrieval agent
   ├─ analysis agent
   ├─ critique/reviewer agent
   ↓
combined result
```

#### Best for

- large complex tasks
- specialized responsibilities
- workflow decomposition
- research and planning systems

#### Strengths

- separation of responsibilities
- specialization
- modular design

#### Weaknesses

- coordination complexity
- higher latency
- harder debugging
- risk of overengineering

#### Important design elements

- communication protocol between agents
- shared state or memory
- orchestration logic
- evaluation of each agent

#### Beginner Explanation

A multi-agent system means you do not have one general agent doing everything.

Instead, different agents have different roles.

**Examples:**
- one agent retrieves documents
- one agent analyzes facts
- one agent critiques or reviews
- one agent plans next steps

This sounds powerful, but it is also much more complex.

So multi-agent is not automatically better.

#### Simple Mental Model

Imagine a team instead of one person:

- **planner** = project manager
- **retrieval agent** = researcher
- **analysis agent** = analyst
- **reviewer agent** = quality checker

This can work well when the job is large and roles are clearly separable.

#### Step-by-Step Mental Model

**Step 1 — A high-level request arrives**

Example: "Create a strategic report about AI chip competition using internal notes and recent public news."

**Step 2 — Planner breaks task apart**

It decides:
- gather sources
- summarize evidence
- critique final draft

**Step 3 — Specialized agents do their sub-jobs**

Each agent focuses on one narrower task.

**Step 4 — Results are combined**

The outputs are merged or reviewed.

**Step 5 — Final answer is returned**

The system presents a coordinated result.

#### Important Algorithms / Mechanisms for Multi-Agent Systems

**A. Task Decomposition**

Split a large task into smaller role-specific tasks.

> **Why important:** This is the heart of multi-agent usefulness.

**B. Role Specialization**

Each agent has a narrow function.

> **Why important:** Prevents one agent from becoming overly broad and messy.

**C. Inter-Agent Communication Protocol**

Agents must exchange information in a structured way.

> **Why important:** Poor communication creates coordination failure.

**D. Shared State / Shared Memory**

Some systems maintain central task state or memory store.

> **Why important:** Agents need a consistent view of the task.

**E. Orchestration Layer**

A controller coordinates ordering, retries, and final synthesis.

> **Why important:** Without orchestration, multi-agent systems become chaotic.

#### Best For

Use multi-agent only when:

- one agent is not enough
- responsibilities are clearly separable
- complexity is justified by the task

#### Common Failure Modes

- too much coordination overhead
- duplicated effort between agents
- unclear roles
- inconsistent outputs
- overengineering compared with simpler architectures

---

### 6. Workflow vs Agent

This is one of the most important decisions.

**Workflow** — Fixed steps.

Example:
```
fetch data
→ calculate features
→ retrieve docs
→ generate answer
```

**Agent** — Dynamic steps.

Example:
```
decide what to do
→ call tool
→ inspect result
→ choose next action
```

> **Rule of thumb:** Start with workflow first. Use agents only when the task truly needs dynamic choice.

#### Beginner Explanation

This is one of the most practical architecture decisions in all of AI engineering.

Many systems should not start as agents.

A workflow is often better.

**Why?**

Because workflows are:
- easier to debug
- easier to test
- easier to trust
- easier to monitor
- often fully sufficient

An agent is useful when fixed steps are not enough.

#### Decision Rule

**Use a workflow when:**
- the steps are already known
- the task is repeatable
- the order is stable
- reliability matters more than flexibility

**Use an agent when:**
- the next step depends on what just happened
- tool choice varies by request
- the task is open-ended
- flexibility is worth extra complexity

#### Important Algorithms / Mechanisms for Workflow vs Agent

**A. Deterministic Pipeline**

Every request goes through known steps.

> **Why important:** This is the safest and cleanest default.

**B. Rule-Based Router**

Simple rules pick a workflow path.

> **Why important:** Often enough for many business systems.

**C. LLM-Based Router**

An LLM classifies the request and chooses a path.

> **Why important:** More flexible, but less deterministic.

**D. Dynamic Action Loop**

An agent keeps choosing actions until done.

> **Why important:** Supports open-ended tasks, but increases control difficulty.

#### Best Practice Rule

Start with:
1. plain workflow
2. add routing if needed
3. add agent behavior only if needed
4. add multi-agent only if clearly justified

---

### 7. Hybrid Architectures

Most real systems combine multiple architecture types.

**Example:**

```
user query
   ↓
workflow orchestrator
   ↓
ML model + RAG + LLM
   ↓
response
```

Or:

```
agent
   ↓
uses retrieval tool
uses calculation tool
uses LLM summarization
```

Real systems are often:
- partly deterministic
- partly model-driven
- partly retrieval-based

This is the level where architecture thinking becomes important.

#### Beginner Explanation

Real systems are often not pure examples of one architecture.

You may have:
- workflow + RAG
- agent + tools + retrieval
- ML prediction + LLM explanation
- RAG + structured validation + routing

That is normal.

The important thing is not to collect architectures randomly.

The important thing is:
- each part must have a reason
- each part must solve a real need
- complexity must be justified

#### Step-by-Step Mental Model

**Step 1 — Start from the simplest core**

Example: RAG-only or workflow-only

**Step 2 — Add another pattern only if needed**

Example: add tool use because retrieval alone is insufficient

**Step 3 — Keep component roles clear**

Example: retrieval gives evidence, LLM explains, validator checks schema

**Step 4 — Evaluate the added complexity**

Did the added architecture piece actually improve quality?

#### Important Algorithms / Mechanisms for Hybrid Architectures

**A. Layered Orchestration**

A deterministic controller coordinates multiple subsystems.

> **Why important:** This is common in real enterprise AI systems.

**B. Routing + Retrieval + Generation Combination**

Different components handle different phases.

> **Why important:** Many useful AI systems are really hybrid by nature.

**C. Tool-Augmented RAG**

An agent or workflow uses both retrieval and tools.

> **Why important:** Retrieval gives knowledge, tools give action.

**D. Validation Layers**

Outputs from one architecture stage are checked before moving onward.

> **Why important:** Hybrid systems need strong boundaries.

#### Strengths

- more capable
- can combine best aspects of multiple patterns
- often closer to real business needs

#### Weaknesses

- easier to overcomplicate
- more moving parts
- harder debugging
- more evaluation work needed

---

### 8. Choosing the Right Architecture

Use this decision style:

**Use plain LLM architecture when:**
- general knowledge is enough
- task is simple
- no private data required

**Use RAG when:**
- knowledge changes often
- private docs are needed
- grounded answers matter

**Use Agent architecture when:**
- system must use tools
- task is multi-step
- dynamic action selection is useful

**Use Multi-Agent only when:**
- one agent is not enough
- responsibilities are clearly separable
- complexity is justified

#### Beginner Explanation

Architecture choice should not be based on hype.

It should be based on the problem.

**Ask:**

1. Does the task depend on external knowledge?
   - If yes, RAG may be needed.

2. Does the system need to act or use tools?
   - If yes, agent architecture may be needed.

3. Is the task simple and mainly language-based?
   - If yes, plain LLM app may be enough.

4. Is one controller overloaded with many clearly separable jobs?
   - If yes, multi-agent may be worth considering.

#### Architecture Selection Heuristic

Start with the lowest-complexity option that can reasonably solve the task:

1. Plain LLM
2. LLM + validation
3. RAG
4. Workflow + RAG + LLM
5. Agent
6. Multi-agent

This is not a strict law, but it is a very good beginner rule.

#### Important Algorithms / Mechanisms for Architecture Selection

**A. Decision-by-Constraints**

Choose architecture based on constraints:
- freshness
- privacy
- tool use
- latency
- budget
- complexity tolerance

> **Why important:** Architecture is constrained engineering, not abstract preference.

**B. Tradeoff Analysis**

Compare architectures across:
- complexity
- reliability
- cost
- latency
- maintainability

> **Why important:** There is no universally best architecture.

**C. Failure-Oriented Design**

Choose the architecture whose failure modes you can control.

> **Why important:** A simpler system with manageable failure modes is often better than a more powerful but fragile one.

---

## Difficulty Points

### 1. Choosing complex architecture too early

Beginners often jump to:
- agent
- multi-agent
- too many layers

...when a workflow or RAG system is enough.

**Why this happens**

Because complex architectures look more advanced and impressive.

**Why this is a problem**

You add:
- more debugging difficulty
- more latency
- more cost
- more failure modes

...without necessarily improving the result.

**Fix strategy**

Start from the simplest architecture that can solve the task.

---

### 2. No clear separation of responsibilities

If everything is mixed together:
- hard to debug
- hard to improve
- hard to evaluate

**Why this happens**

People draw architecture boxes but do not define what each box is responsible for.

**Why this is a problem**

Components overlap and responsibilities become muddy.

**Fix strategy**

For every component, define:
- what it receives
- what it outputs
- what it is responsible for
- what it is not responsible for

---

### 3. Thinking architecture is only diagrams

Architecture is also:
- interfaces
- contracts
- failure handling
- observability

**Why this happens**

Diagramming feels like architecture work, so people stop there.

**Why this is a problem**

A nice diagram without runtime contracts and failure thinking is not enough.

**Fix strategy**

Always define:
- interfaces
- error behavior
- logging plan
- evaluation plan
- latency expectations

---

### 4. Ignoring failure points

Every architecture needs to ask:
- what if retrieval returns nothing?
- what if tool fails?
- what if output is invalid?
- what if latency is too high?

**Why this happens**

People focus on happy-path design.

**Why this is a problem**

The real system fails at the edges.

**Fix strategy**

For each architecture, list likely failure points before building.

---

### 5. No evaluation plan

A good architecture includes:
- how to measure it
- what success means
- where failures are expected

**Why this happens**

People assume architecture quality will be obvious from demos.

**Why this is a problem**

Without evaluation, you cannot tell whether the architecture is actually working better than alternatives.

**Fix strategy**

Define metrics and test cases during design, not after deployment.

---

### 6. Using one architecture because it is trendy

**Why this happens**

People copy what is popular instead of what fits.

**Why this is a problem**

The architecture may be badly matched to the use case.

**Fix strategy**

Choose architecture by problem shape, not by popularity.

---

### 7. No workflow-first discipline

**Why this happens**

Agent systems seem exciting, so beginners skip stable baselines.

**Why this is a problem**

You lose control and make debugging much harder.

**Fix strategy**

Build deterministic workflow first, then add dynamic architecture only if needed.

---

## AI Architecture Workflow (REAL WORLD)

1. Define the use case
2. Define user input and desired output
3. Decide what knowledge is needed
4. Decide whether tools/actions are needed
5. Choose the simplest suitable architecture
6. Draw system flow
7. Define component responsibilities
8. Define interfaces and schemas
9. Identify likely failure points
10. Define evaluation plan
11. Compare with simpler alternatives
12. Only then start implementation

### Beginner Explanation of Each Step

**1. Define the use case**

Be specific.

- **Bad:** "Build an AI assistant"
- **Good:** "Build a PDF Q&A assistant for employee policy documents"

**2. Define user input and desired output**

What exactly comes in? What exactly should come out?

**3. Decide what knowledge is needed**

General model knowledge, private docs, real-time APIs, or all three?

**4. Decide whether tools/actions are needed**

If the system must act, workflow or agent patterns may be needed.

**5. Choose the simplest suitable architecture**

Do not choose complexity first.

**6. Draw system flow**

Make the sequence explicit.

**7. Define component responsibilities**

Every component should have one main job.

**8. Define interfaces and schemas**

Know how data moves between components.

**9. Identify likely failure points**

Design for failure, not only success.

**10. Define evaluation plan**

Know how you will measure the architecture.

**11. Compare with simpler alternatives**

A simpler design may be better.

**12. Only then start implementation**

Architecture should guide coding, not come after random coding.

---

## Debugging Checklist for Stage 12

If an AI system architecture performs badly, check:

- [ ] Is the chosen architecture too complex for the task?
- [ ] Could a simpler workflow solve it better?
- [ ] Are component responsibilities clearly separated?
- [ ] Does the system really need RAG, or is plain LLM enough?
- [ ] Does the system really need agents, or is a workflow enough?
- [ ] Are interfaces and schemas clearly defined?
- [ ] Are likely failure modes identified ahead of time?
- [ ] Is retrieval quality the real issue instead of generation quality?
- [ ] Is tool routing causing problems?
- [ ] Are multi-agent roles too overlapping?
- [ ] Is there an evaluation plan for each layer?
- [ ] Are you optimizing architecture choice based on real constraints or hype?

---

## Practice Project

### Project: Architecture Design Workbook

#### Goal

Practice designing AI systems before coding them.

This project is about:
- architecture thinking
- use-case matching
- tradeoff analysis
- technical communication

#### What You Will Build

You will create 4 short design documents:

1. LLM Application Architecture
2. RAG Architecture
3. AI Agent Architecture
4. Multi-Agent Architecture

Each one should use a different use case.

#### Recommended Use Cases

**LLM App**

Example:
- concept explainer
- writing assistant

**RAG App**

Example:
- PDF Q&A
- company knowledge assistant

**Agent App**

Example:
- market assistant
- research assistant using tools

**Multi-Agent App**

Example:
- planning + research + reviewer system

#### Step-by-Step Instructions

**Step 1 — Define one use case per architecture**

For each architecture, write:
- problem statement
- who the user is
- what input the user gives
- what output the system should produce

> **Why this step matters:** If the use case is vague, the architecture choice will also be vague.

**Beginner rule:** Each use case should be different enough that the architecture choice actually makes sense.

**Step 2 — Draw system flow**

Create a simple flow like:

```
user
↓
component
↓
component
↓
output
```

Do not make the diagram complicated. Clarity matters more than beauty.

> **Why this step matters:** Architecture is easier to reason about when flow is visible.

**Beginner advice:** Do not try to look "advanced." Try to look clear.

**Step 3 — List system components**

For each architecture, list:
- input layer
- prompt/retrieval/tool logic
- LLM or model
- output layer
- logging/monitoring if relevant

> **Why this step matters:** This turns a vague diagram into a real system design.

**Better component checklist** — Also define:
- what each component receives
- what each component returns
- what each component depends on

**Step 4 — Explain why this architecture fits**

Students must explain:
- why this design fits the use case
- why a simpler design may not be enough
- why a more complex design may be unnecessary

This is one of the most important parts.

> **Why this step matters:** Good architects justify architecture choice, not just draw it.

**Step 5 — Identify likely failure points**

For each architecture, list:
- likely failure modes
- what would be hard to debug
- where latency may appear
- what could go wrong in production

Examples:
- hallucination
- retrieval misses
- tool failure
- slow response
- invalid output format

> **Why this step matters:** Architecture quality includes failure awareness.

**Step 6 — Define evaluation plan**

For each architecture, answer:
- how will I know it works?
- what metrics matter?
- what sample test cases would I use?

Examples:
- answer correctness
- retrieval relevance
- tool success rate
- latency
- output structure validity

> **Why this step matters:** An architecture without evaluation is only a sketch.

**Step 7 — Compare all 4 architectures**

At the end, write a short comparison:
- when is LLM-only enough?
- when is RAG better?
- when is agent necessary?
- when is multi-agent too much?

This comparison is where architecture maturity starts to show.

> **Why this step matters:** The goal is not just to understand each architecture separately. The goal is to learn selection judgment.

#### Deliverables

- 4 design documents
- 4 simple architecture diagrams
- 1 comparison summary document
- README explaining project purpose

---

## Experiment Tasks

### Experiment 1 — Replace one architecture with a simpler one

Take one design and ask: could this be done with a simpler architecture?

> **Lesson:** Complexity must be justified.

### Experiment 2 — Add a failure scenario section

For each design, add:
- top 3 failure modes
- top 3 observability needs

> **Lesson:** Architecture includes failure handling.

### Experiment 3 — Add interface contracts

For each component, define:
- input schema
- output schema

> **Lesson:** Architecture is also about boundaries.

### Experiment 4 — Add evaluation metrics

For each design, define:
- one quality metric
- one reliability metric
- one latency/cost metric

> **Lesson:** Architecture must be measurable.

### Experiment 5 — Compare workflow vs agent version of one use case

Take one problem and design both:
- deterministic workflow
- agent-based version

> **Lesson:** Agent is not automatically better.

### Experiment 6 — Add hybrid architecture design

Create one additional design combining:

- workflow + RAG
  or
- agent + tools + retrieval

> **Lesson:** Most real systems are hybrids.

---

## Evaluation

Students should be evaluated on:

1. **Correctness of architecture choice** — Did they choose a design that matches the use case?
2. **Clarity of system flow** — Can another person understand the design?
3. **Tradeoff awareness** — Does the student explain why this architecture is better than alternatives?
4. **Failure thinking** — Did the student identify realistic failure points?
5. **Evaluation thinking** — Did the student define how the system would be tested?

### Grading Rubric

| Category | Weight |
|---|---|
| Architecture fit | 30% |
| Clarity of diagrams and component breakdown | 25% |
| Tradeoff analysis | 20% |
| Failure/evaluation reasoning | 15% |
| Organization and writing quality | 10% |

---

## Common Mistakes

- choosing the most complex architecture by default
- drawing components without defining responsibilities
- not explaining tradeoffs
- no discussion of failure points
- no evaluation plan

### Expanded Common Mistakes with Reasons and Fixes

**1. Choosing the most complex architecture by default**

- **Reason:** It feels more advanced.
- **Problem:** The design becomes harder to build, debug, and justify.
- **Fix:** Start from the simplest architecture that can solve the task.

**2. Drawing components without defining responsibilities**

- **Reason:** People focus on boxes and arrows only.
- **Problem:** The design is visually clear but operationally vague.
- **Fix:** Define each component's job explicitly.

**3. Not explaining tradeoffs**

- **Reason:** Students describe architecture but do not compare alternatives.
- **Problem:** The choice feels arbitrary.
- **Fix:** Always explain why this architecture beats simpler and more complex alternatives for the use case.

**4. No discussion of failure points**

- **Reason:** Happy-path thinking dominates early design work.
- **Problem:** The architecture looks good on paper but is fragile in practice.
- **Fix:** Write likely failure modes during the design phase.

**5. No evaluation plan**

- **Reason:** Testing is treated as later work.
- **Problem:** You cannot tell whether the architecture is actually successful.
- **Fix:** Include metrics and test scenarios in the design doc.

**6. Treating multi-agent as automatically superior**

- **Reason:** It sounds powerful and modular.
- **Problem:** It may create coordination overhead without real benefit.
- **Fix:** Use multi-agent only when roles are clearly separable and justified.

**7. Forgetting observability**

- **Reason:** Architecture is reduced to model flow only.
- **Problem:** Production failure handling becomes weak.
- **Fix:** Include logging, tracing, and monitoring in architecture thinking.

---

## Final Understanding

You should understand:

> Architecture is the structure that turns AI capabilities into usable systems.

A top AI engineer does not just ask: *which model is best?*

They ask: **which architecture best solves this problem with the right tradeoffs?**

That is what this stage teaches.

Also:

> Good AI architecture is not about maximizing complexity. It is about choosing the right structure, defining clear responsibilities, anticipating failure, and making the system measurable.

---

## Self Test

### Questions

1. Why does architecture matter even when two systems use the same model?
2. What does architecture determine in an AI system?
3. What is the basic flow of a plain LLM application architecture?
4. When is plain LLM architecture usually enough?
5. What are the main weaknesses of plain LLM architecture?
6. What is the basic flow of RAG architecture?
7. Why is RAG useful for private or changing knowledge?
8. What parts most strongly affect RAG quality?
9. What is the basic flow of an agent architecture?
10. When is agent architecture useful?
11. What are common risks of agent architecture?
12. What is a multi-agent system?
13. When is multi-agent architecture justified?
14. Why can multi-agent systems be overengineering?
15. What is the difference between a workflow and an agent?
16. Why is workflow-first design often recommended?
17. What is a hybrid architecture?
18. Why are many real AI systems hybrid?
19. What is a good rule for choosing the right architecture?
20. Why should failure points be part of architecture design?
21. Why is architecture more than diagrams?
22. What should be defined besides component names?
23. What is one sign that an architecture is too complex for the task?
24. Why is evaluation planning part of architecture design?
25. Why should simpler alternatives always be considered?
26. Why is clear responsibility separation important?
27. What does observability add to architecture?
28. Why should you define input/output interfaces?
29. What is the main beginner mistake in architecture selection?
30. What is the main lesson of this stage?

### Answers

**1. Why does architecture matter even when two systems use the same model?**

Because the architecture changes how data enters, how decisions happen, how knowledge is retrieved, how outputs are controlled, and how failures are handled.

**2. What does architecture determine in an AI system?**

It determines system structure, information flow, control flow, component responsibilities, failure handling, and evaluation design.

**3. What is the basic flow of a plain LLM application architecture?**

User input → prompt construction → LLM → formatted response.

**4. When is plain LLM architecture usually enough?**

When the task is simple, mainly language-based, and does not require private data, retrieval, or tool use.

**5. What are the main weaknesses of plain LLM architecture?**

Hallucination risk, lack of grounding, and weakness on private or changing knowledge tasks.

**6. What is the basic flow of RAG architecture?**

User query → retrieval → documents/chunks → prompt construction → LLM → grounded answer.

**7. Why is RAG useful for private or changing knowledge?**

Because it retrieves current or private documents at answer time instead of relying only on model memory.

**8. What parts most strongly affect RAG quality?**

Chunking, embeddings, retrieval quality, prompt grounding, and citation design.

**9. What is the basic flow of an agent architecture?**

User request → LLM planner/controller → tool choice → tool execution → observation/result → LLM continues or answers.

**10. When is agent architecture useful?**

When the system must use tools, take actions, or solve multi-step tasks with dynamic decision-making.

**11. What are common risks of agent architecture?**

Wrong tool choice, looping, higher latency, higher cost, and harder debugging.

**12. What is a multi-agent system?**

A multi-agent system is an architecture where multiple specialized agents handle different parts of a larger task.

**13. When is multi-agent architecture justified?**

When responsibilities are clearly separable and one agent is not enough for the task.

**14. Why can multi-agent systems be overengineering?**

Because they add coordination complexity, latency, and debugging difficulty without always adding enough value.

**15. What is the difference between a workflow and an agent?**

A workflow follows fixed steps, while an agent decides dynamically what to do next.

**16. Why is workflow-first design often recommended?**

Because workflows are easier to test, debug, trust, and control.

**17. What is a hybrid architecture?**

A hybrid architecture combines multiple architecture patterns, such as workflow + RAG or agent + retrieval + tools.

**18. Why are many real AI systems hybrid?**

Because real-world tasks often need both deterministic steps and model-driven behavior.

**19. What is a good rule for choosing the right architecture?**

Choose the simplest architecture that can solve the problem reliably.

**20. Why should failure points be part of architecture design?**

Because real systems fail in predictable places, and good architecture anticipates those failures.

**21. Why is architecture more than diagrams?**

Because it also includes interfaces, schemas, failure handling, observability, and evaluation planning.

**22. What should be defined besides component names?**

Inputs, outputs, responsibilities, interfaces, likely failure modes, and evaluation methods.

**23. What is one sign that an architecture is too complex for the task?**

A much simpler workflow could solve the problem with less cost and less operational risk.

**24. Why is evaluation planning part of architecture design?**

Because you need to know how success and failure will be measured before implementation.

**25. Why should simpler alternatives always be considered?**

Because simpler systems are often easier to build, test, maintain, and trust.

**26. Why is clear responsibility separation important?**

Because it makes systems easier to debug, improve, and reason about.

**27. What does observability add to architecture?**

It adds visibility into logs, traces, failures, latency, and system behavior in practice.

**28. Why should you define input/output interfaces?**

Because components need stable contracts to work together reliably.

**29. What is the main beginner mistake in architecture selection?**

Choosing the most complex architecture by default instead of matching architecture to the problem.

**30. What is the main lesson of this stage?**

AI architecture is about choosing the right system structure for the problem, with clear responsibilities, realistic tradeoffs, and measurable behavior.

---

## What You Must Be Able To Do After Stage 12

- [ ] explain why architecture matters in AI systems
- [ ] distinguish plain LLM, RAG, agent, and multi-agent architectures
- [ ] explain when each architecture fits best
- [ ] compare workflow vs agent thinking clearly
- [ ] identify when hybrid architecture is justified
- [ ] design simple system flows before coding
- [ ] define component responsibilities and interfaces
- [ ] identify likely failure points during design
- [ ] include evaluation thinking in architecture planning
- [ ] choose architecture based on problem fit, not hype
