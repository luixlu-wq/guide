# Stage 11 — AI Infrastructure

*(Week 21)*

---

## Goal

Understand how AI systems are deployed, served, and scaled in real environments.

This stage focuses on infrastructure:

- how models run in production
- how GPUs are used
- how serving systems work
- how vector databases scale
- when distributed systems are needed

You are moving from:

- building AI features

to:

- operating AI systems reliably

---

## Quick Summary

AI infrastructure is the layer that makes models usable in real systems.

A model alone is not enough.

A real AI system needs:

- a way to receive requests
- a way to load the model
- a way to run inference
- a way to return results
- a way to monitor latency and failures
- a way to scale when demand increases

A beginner should finish this stage understanding:

- what AI infrastructure really means
- what model serving is
- why GPUs matter for inference
- what latency and throughput mean
- how vector databases behave in production
- when distributed training becomes necessary
- what Ray, vLLM, and Ollama are used for
- how to measure infrastructure behavior instead of guessing

---

## Concepts

- Model Serving
- GPU Inference
- Vector Databases
- Distributed Training

---

## Study Materials

**Ray**
https://docs.ray.io/

**vLLM**
https://github.com/vllm-project/vllm

**Ollama**
https://ollama.com/

---

## Key Knowledge (Deep Understanding)

### 1. What AI Infrastructure Really Means

AI infrastructure is everything needed to make models usable in real systems.

A model alone is not enough.

A real system needs:

- a way to receive requests
- a way to load the model
- a way to run inference
- a way to return results
- a way to monitor performance
- a way to scale when usage grows

Think of infrastructure as:

```
user request → service → model → result → logging/monitoring
```

Without infrastructure:

- your model stays in a notebook
- nobody can use it reliably

#### Beginner Explanation

A lot of beginners think:

> "I trained a model, so I built an AI product."

That is not true yet.

Training a model means you created the core intelligence component.

Infrastructure is what makes that intelligence usable by:

- users
- apps
- teams
- APIs
- production systems

If a model cannot be called reliably, measured, scaled, and monitored, it is still mostly an experiment.

#### Simple Mental Model

Think of a model as an engine.

Infrastructure is the rest of the car:

- ignition
- steering
- fuel system
- brakes
- dashboard
- maintenance tools

The engine matters, but the car is what people can actually use.

#### Step-by-Step Mental Model

**Step 1 — A request arrives**

Example:

- summarize document
- answer RAG question
- generate embedding
- predict stock direction

**Step 2 — Infrastructure receives it**

Usually via:

- API
- queue
- batch job
- scheduled job

**Step 3 — Model is loaded or already available**

The system must know:

- where the model is
- whether it is warm
- whether enough memory is available

**Step 4 — Inference happens**

The model processes input and generates output.

**Step 5 — Output is returned**

Usually in structured form:

- JSON
- stream
- file
- database write

**Step 6 — System records what happened**

Infrastructure logs:

- latency
- error state
- resource use
- request metadata
- response status

#### Important Algorithms / Mechanisms for AI Infrastructure

**A. Request-Response Serving Pattern**

A client sends a request and waits for a response.

How it works:

- request enters server
- server validates input
- model runs
- response is returned

> **Why important:** This is the most common infrastructure pattern for online AI systems.

**B. Queue-Based Processing**

Requests are placed into a queue before being processed.

How it works:

- requests wait in line
- workers process them as resources become available

> **Why important:** Useful when work is slow, bursty, or too expensive to run immediately for every request.

**C. Service Lifecycle Management**

Models and services must be started, kept healthy, and restarted when needed.

> **Why important:** A model service is not just code. It is a running system that must stay available.

**D. Observability Layer**

Metrics, logs, and traces are collected around the model system.

> **Why important:** Without observability, production AI failures become guesswork.

#### Strengths of Good Infrastructure

- usable by real users
- stable under repeated usage
- measurable
- debuggable
- scalable
- maintainable

#### Weaknesses of Poor Infrastructure

- works only in notebooks
- breaks under real use
- hard to debug
- hard to scale
- hard to trust

---

### 2. Model Serving

Model serving means exposing a model so other systems or users can call it.

Typical serving flow:

```
client → API → model → response
```

Common serving patterns:

- REST API
- batch inference
- streaming output (common for LLMs)

#### Why serving matters

A trained model is only useful when it can be:

- called repeatedly
- used by other services
- monitored for latency and failure

Important serving ideas:

- request handling
- concurrency
- batching
- response schema
- retries / failures

#### Beginner Explanation

A notebook prediction is not serving.

Serving means:

- the model is loaded in a running process
- a request comes in
- the system sends input to the model
- the model returns an output
- this happens reliably many times

This is what turns a model into a product capability.

#### Types of Serving

**A. Online / Real-Time Serving**

A user sends a request and expects a quick response.

Examples:

- chatbot reply
- RAG answer
- image classification API

**B. Batch Serving**

Many inputs are processed together later.

Examples:

- nightly summarization
- offline embedding generation
- bulk scoring of customer records

**C. Streaming Serving**

Output is returned gradually.

Examples:

- LLM token streaming
- long generation tasks

#### Step-by-Step Serving Flow

**Step 1 — Request enters endpoint**

Example: `POST /predict`

**Step 2 — Input is validated**

Make sure fields are present and correctly typed.

**Step 3 — Request is routed**

Maybe:

- direct model inference
- retrieval + model inference
- batch queue
- streaming pipeline

**Step 4 — Model executes**

The request is processed.

**Step 5 — Output is formatted**

Return predictable schema.

**Step 6 — Logs and metrics are recorded**

Track:

- request time
- model time
- error rate
- response size

#### Important Algorithms / Mechanisms for Model Serving

**A. Concurrency Handling**

Multiple requests may arrive at the same time.

How it works: The server manages simultaneous requests using async handling, workers, or thread/process strategies.

> **Why important:** A system that works for one request may fail badly under many concurrent users.

**B. Batching**

Multiple inputs are grouped together into one model execution.

How it works: Instead of running the model once per item, several items are processed together.

> **Why important:** This can improve throughput significantly, especially on GPUs.

**C. Dynamic Batching**

The system automatically groups nearby incoming requests.

How it works: If several requests arrive within a short time window, they are merged into one batch.

> **Why important:** Very important for LLM serving efficiency.

**D. Streaming Token Output**

Instead of waiting for full generation, partial output is returned as it is produced.

> **Why important:** Improves user experience for long LLM responses.

**E. Retry / Timeout Control**

The system decides what happens when inference is slow or fails.

> **Why important:** Production systems need graceful failure behavior.

#### Strengths

- makes models reusable
- supports applications and APIs
- enables monitoring
- enables repeated reliable use

#### Weaknesses

- serving bugs can break good models
- poor concurrency design hurts reliability
- bad schemas hurt integration
- no timeout policy makes production fragile

---

### 3. GPU Inference

LLMs and deep learning models rely heavily on matrix operations.

GPUs are designed for:

- parallel computation
- fast matrix multiplication
- high throughput

#### Why GPUs matter

Compared to CPU:

- much faster for neural network inference
- better for large LLM generation workloads

Key tradeoff:

- **CPU** = easier, cheaper, slower
- **GPU** = faster, more complex, more expensive

Important concepts:

- **VRAM** (GPU memory)
- batch size
- latency
- throughput

#### Beginner Explanation

Inference means using a trained model to produce output.

Deep models do a lot of:

- matrix multiplication
- tensor operations
- attention operations

GPUs are especially good at these.

That is why large models that feel too slow on CPU often become usable on GPU.

#### CPU vs GPU Intuition

| | CPU | GPU |
|---|---|---|
| **Good for** | general-purpose logic, control flow, smaller workloads, development simplicity | large tensor math, neural nets, many similar operations in parallel, LLM and embedding workloads |

#### Important GPU Concepts

**VRAM**

GPU memory.

> **Why it matters:** If the model and its runtime state do not fit in VRAM, inference may fail or require slower fallback behavior.

**Batch Size**

How many inputs are processed together.

> **Why it matters:** Larger batch can increase throughput, but also increases memory usage.

**Latency**

Time for one request.

**Throughput**

Amount of work done per time period.

#### Step-by-Step GPU Inference Flow

**Step 1 — Input arrives**

Prompt, image, or batch of records.

**Step 2 — Input becomes tensors**

The framework converts input into model-ready numeric form.

**Step 3 — Tensors move to GPU**

The data is copied to GPU memory.

**Step 4 — GPU runs model operations**

Matrix math is executed in parallel.

**Step 5 — Output is produced**

Maybe:

- class label
- embedding vector
- generated tokens

#### Important Algorithms / Mechanisms for GPU Inference

**A. Parallel Tensor Execution**

Many operations are performed simultaneously.

> **Why important:** This is the main reason GPU inference is faster for deep learning.

**B. Matrix Multiplication Acceleration**

Neural layers are built heavily on matrix multiplication.

> **Why important:** GPUs are optimized for this exact workload.

**C. KV Cache (for LLMs)**

Previously computed attention state is reused during autoregressive generation.

How it works: The model does not recompute all prior token states from scratch every time.

> **Why important:** Huge speed benefit for LLM chat generation.

**D. Batch Parallelism**

Several requests or examples are processed together.

> **Why important:** Improves throughput, though it may increase individual latency depending on setup.

#### Strengths

- much faster inference for large models
- better throughput
- essential for many LLM workloads

#### Weaknesses

- higher cost
- deployment complexity
- memory constraints still matter
- underutilized GPUs waste money

---

### 4. Latency vs Throughput

This is one of the most important infrastructure concepts.

**Latency** — How long one request takes.

**Throughput** — How many requests the system can handle over time.

Example:

- chatbot wants lower latency
- batch summarization may care more about throughput

#### Why this matters

A system can be:

- fast for one user but bad at handling many users
- efficient for many users but too slow for one response

Infrastructure design always balances these.

#### Beginner Explanation

This is a classic engineering tradeoff.

A beginner often asks: *"Is my system fast?"*

But "fast" can mean two different things.

**Low latency** — One user gets an answer quickly.

**High throughput** — The system handles a lot of work overall.

Sometimes improving one hurts the other.

#### Examples

| Use Case | Needs |
|---|---|
| **Chat assistant** | low latency, responsive streaming, fast first token |
| **Bulk embedding pipeline** | high throughput, efficient batch processing, low total cost per record |

These are different infrastructure goals.

#### Important Algorithms / Mechanisms for Latency vs Throughput

**A. Batching Tradeoff**

More batching usually improves throughput.

But: queueing and waiting may increase latency for an individual request.

> **Why important:** This is a central serving tradeoff.

**B. Scheduling**

The system decides when to run which request.

> **Why important:** Good scheduling can balance fairness, latency, and utilization.

**C. Queueing Behavior**

Requests may wait before execution.

> **Why important:** Sometimes model time is not the main delay; queue time is.

**D. Token Streaming**

For LLMs, streaming may improve perceived latency even if total generation time is unchanged.

> **Why important:** User experience depends on perceived responsiveness too.

#### Practical Rule

Ask first:

- Is this a user-facing interactive system?
- Or a background/batch system?

That determines whether you optimize mainly for latency or throughput.

---

### 5. Vector Databases in Production

A vector database is used to:

- store embeddings
- search by semantic similarity
- support RAG systems

Examples:

- FAISS
- ChromaDB
- Weaviate
- Pinecone

#### What matters in production

- fast retrieval
- metadata filtering
- update / refresh strategy
- memory/storage size
- scaling with more documents

#### Why this matters

If retrieval gets slow or wrong:

- RAG quality drops
- user experience suffers

#### Beginner Explanation

A vector database in production is not just a demo storage layer.

In production, you care about:

- speed
- freshness
- update strategy
- filtering
- memory usage
- accuracy of returned chunks

> That means production vector retrieval is both a quality problem and an infrastructure problem.

#### Step-by-Step Production Vector Flow

**Step 1 — Documents are embedded**

Each chunk gets a vector.

**Step 2 — Vectors and metadata are stored**

Metadata may include:

- source
- date
- section
- user/org scope

**Step 3 — Query is embedded**

The user question becomes a vector.

**Step 4 — Retrieval runs**

The vector DB finds similar chunks.

**Step 5 — Results are filtered/ranked**

Metadata filters or reranking may improve relevance.

**Step 6 — Output is returned to downstream system**

Usually a RAG prompt builder or agent.

#### Important Algorithms / Mechanisms for Vector Databases in Production

**A. Metadata Filtering**

Restrict results using structured metadata.

Examples:

- only one customer
- only one document type
- only recent data

> **Why important:** Retrieval quality often improves dramatically with good filtering.

**B. ANN Indexing**

Approximate nearest neighbor structures accelerate large-scale vector search.

> **Why important:** Production systems need speed at scale.

**C. Index Refresh / Rebuild Strategy**

The system must decide how new vectors are added and when indexes are refreshed.

> **Why important:** Production corpora change over time.

**D. Hybrid Retrieval**

Combines vector similarity with keyword or lexical retrieval.

> **Why important:** Exact terms, IDs, and rare strings often need more than semantic search alone.

#### Strengths

- enables scalable semantic search
- core layer for RAG
- supports large corpora
- flexible with metadata and filters

#### Weaknesses

- poor embeddings still give poor results
- indexing choices affect speed and quality
- updating large indexes can be operationally tricky
- retrieval evaluation is mandatory

---

### 6. Distributed Training

Sometimes one machine is not enough.

Distributed training means:

- training across multiple GPUs
- or multiple machines

This becomes important when:

- model is large
- dataset is large
- training time is too long on one machine

**Important note**

Beginners usually do NOT need distributed training first.

But you should understand the concept because:

- modern AI systems often depend on it
- large-scale teams use it heavily

#### Beginner Explanation

Distributed training means splitting training work across more than one compute unit.

That can mean:

- multiple GPUs in one machine
- multiple machines in a cluster

The purpose is to make very large training jobs possible or faster.

#### When It Becomes Necessary

Distributed training matters when:

- the model does not fit on one GPU
- training takes too long on one device
- data volume is huge
- large experimentation throughput is needed

#### Important Algorithms / Mechanisms for Distributed Training

**A. Data Parallelism**

Each worker has a copy of the model and trains on different data batches.

How it works:

- split batch across devices
- each device computes gradients
- gradients are synchronized
- model weights are updated consistently

> **Why important:** This is one of the most common forms of distributed training.

**B. Model Parallelism**

The model itself is split across devices.

> **Why important:** Needed when the model is too large for one device.

**C. Gradient Synchronization**

Workers must combine learning updates.

> **Why important:** Without synchronization, the workers would drift apart.

**D. Distributed Checkpointing**

Save model state across a distributed system.

> **Why important:** Large training jobs need fault tolerance and resumability.

#### Practical Note for Beginners

You do not need to implement large distributed training immediately.

You do need to understand:

- why it exists
- when it becomes necessary
- why large AI teams depend on it

---

### 7. Ray

Ray is used for:

- distributed computation
- scaling workloads
- model serving (Ray Serve)
- orchestration of AI tasks

#### Why it matters

Ray helps when:

- workloads are larger
- systems need parallel execution
- you have multiple services or models

**Beginner perspective**

You do not need to master all of Ray now. You should understand:

- why distributed execution matters
- when a single machine stops being enough

#### Beginner Explanation

Ray is like a framework for turning Python workloads into scalable distributed workloads.

Instead of manually managing many machines and workers, Ray gives you patterns for:

- parallel tasks
- distributed execution
- scalable model serving
- orchestration

#### Important Algorithms / Mechanisms for Ray

**A. Task Parallelism**

Independent tasks can run in parallel.

> **Why important:** Good for many AI preprocessing and pipeline jobs.

**B. Actor Model**

Stateful workers can stay alive and keep internal state.

> **Why important:** Useful for model-serving style workloads.

**C. Ray Serve**

A serving layer built on Ray for scalable inference APIs.

> **Why important:** Brings together serving and distributed execution.

**D. Resource Scheduling**

Ray decides where tasks and actors run.

> **Why important:** This is what helps it manage CPU/GPU workloads efficiently.

#### Strengths

- good for scaling Python workloads
- useful for distributed AI pipelines
- supports serving and orchestration

#### Weaknesses

- more complexity than single-machine apps
- not needed for every beginner project
- adds operational overhead

---

### 8. vLLM

vLLM is designed for efficient LLM serving.

It improves:

- inference speed
- memory usage
- throughput

#### Why it matters

Serving LLMs naïvely can waste GPU resources.

vLLM helps by improving:

- batching
- scheduling
- cache efficiency

This matters for:

- chat systems
- many-user LLM APIs
- production assistants

#### Beginner Explanation

A normal script that loads an LLM and answers requests is usually not an efficient production server.

vLLM exists because LLM serving has special performance problems:

- long sequence generation
- many simultaneous users
- high memory pressure
- reuse of previously computed attention state

vLLM is built to make LLM serving more efficient.

#### Important Algorithms / Mechanisms for vLLM

**A. Paged KV Cache**

Manages attention cache memory more efficiently.

> **Why important:** This is one of the major reasons vLLM improves LLM serving efficiency.

**B. Continuous Batching**

Requests are dynamically scheduled and batched as generation proceeds.

> **Why important:** Improves throughput for multi-user generation workloads.

**C. Efficient Scheduling**

The server decides how to interleave generation work across requests.

> **Why important:** This helps keep GPUs busy without wasting resources.

#### Strengths

- strong LLM serving performance
- better GPU utilization
- useful for multi-user systems

#### Weaknesses

- more advanced than a simple local experiment
- requires understanding serving tradeoffs
- not necessary for the very first prototype

---

### 9. Ollama

Ollama is a very useful tool for:

- running local models
- experimenting with local inference
- testing ideas quickly

#### Why beginners should care

Ollama is one of the easiest ways to:

- run LLMs locally
- avoid cloud dependency for experiments
- understand local model serving

**Limitation**

Ollama is great for local experiments, but not the full answer for large-scale production.

#### Beginner Explanation

Ollama is useful because it lowers the barrier to experimenting with local LLMs.

You can learn:

- how local inference feels
- how prompt size affects latency
- how serving differs from notebook use
- how hardware constraints affect real usage

It is very good for learning infrastructure basics without building everything from scratch.

#### Important Algorithms / Mechanisms Related to Ollama

**A. Local Model Runtime**

The model runs on your machine instead of remote API infrastructure.

> **Why important:** This helps beginners understand real inference cost and local hardware limits.

**B. Local Serving Interface**

Ollama exposes a usable interface for model interaction.

> **Why important:** Makes local experimentation feel more like real serving.

**C. Model Packaging / Download Management**

Ollama simplifies acquiring and running supported local models.

> **Why important:** Useful for rapid experimentation.

#### Strengths

- easy local experimentation
- helps learn serving and latency behavior
- useful for private/offline experiments

#### Weaknesses

- not a full production serving platform by itself
- limited by local hardware
- still requires performance measurement and realism

---

## Difficulty Points

### 1. Thinking "I trained a model" means "I built a system"

Training a model is only one step.

Infrastructure is what makes it usable.

**Why this happens**

Because the model is the most visible part of AI work.

**Why this is a problem**

You may ignore:

- serving
- scaling
- monitoring
- schema design
- failure handling

**Fix strategy**

Always ask:

- How is this called?
- How fast is it?
- Can many users use it?
- How do I know if it fails?

### 2. Ignoring latency

Many beginners build systems that work once, but are too slow for real use.

**Why this happens**

Notebook demos do not reveal production timing issues.

**Why this is a problem**

A correct answer that arrives too slowly can still be a bad product experience.

**Fix strategy**

Measure:

- total latency
- model latency
- queue time
- retrieval time
- response size effects

### 3. Ignoring memory limits

Large models may:

- not fit in RAM
- not fit in GPU memory
- crash during inference

**Why this happens**

People focus on model quality but not runtime constraints.

**Why this is a problem**

The system may fail before it even serves a request.

**Fix strategy**

Track:

- RAM usage
- VRAM usage
- model size
- batch size
- prompt/context size

### 4. Confusing local success with production readiness

A notebook that works once is not a reliable service.

**Why this happens**

Local experiments are simpler and feel successful quickly.

**Why this is a problem**

Production requires:

- repeated use
- concurrency
- timeouts
- monitoring
- structured responses
- failure handling

**Fix strategy**

Convert working experiments into small services and test repeated calls.

### 5. Overengineering too early

Beginners often jump into:

- Kubernetes
- distributed systems
- advanced scaling

before they even have a stable single-machine system.

**Why this happens**

Infrastructure tools look impressive and "serious."

**Why this is a problem**

You add complexity before proving the core system works reliably.

**Fix strategy**

Build in this order:

- single-machine stable system
- measurement
- bottleneck identification
- selective scaling

### 6. No monitoring

If you do not track:

- latency
- failures
- resource usage

you do not really know how your system behaves.

**Why this happens**

Monitoring feels like "later work."

**Why this is a problem**

Production problems become invisible until users complain.

**Fix strategy**

Add basic metrics and logs early, even in small systems.

### 7. Mixing performance measurement with changing many variables at once

**Why this happens**

Beginners often test:

- new prompt
- new model
- new hardware setting
- new batch size

all at once.

**Why this is a problem**

You cannot tell what caused the change.

**Fix strategy**

Change one main variable at a time and record results systematically.

---

## AI Infrastructure Workflow (REAL WORLD)

```
1.  Choose target use case
2.  Decide serving pattern
3.  Choose runtime environment
4.  Load and expose model
5.  Measure baseline latency
6.  Measure memory usage
7.  Add logging and health checks
8.  Test repeated requests
9.  Test concurrency or batch behavior
10. Identify bottlenecks
11. Optimize only the real bottleneck
12. Add scaling only when needed
```

### Beginner Explanation of Each Step

**1. Choose target use case**

Is this:

- chatbot
- embedding API
- batch summarizer
- RAG backend

**2. Decide serving pattern**

Will it be:

- synchronous
- batch
- streaming

**3. Choose runtime environment**

Examples:

- local Ollama
- Python service
- GPU server
- vLLM server

**4. Load and expose model**

Turn the model into something callable.

**5. Measure baseline latency**

Do not guess speed.

**6. Measure memory usage**

Make sure the model fits and stays stable.

**7. Add logging and health checks**

Make the system observable.

**8. Test repeated requests**

One successful run is not enough.

**9. Test concurrency or batch behavior**

See how the system behaves under more realistic use.

**10. Identify bottlenecks**

Find what is actually slow:

- model
- I/O
- queue
- retrieval
- serialization

**11. Optimize only the real bottleneck**

Do not optimize blindly.

**12. Add scaling only when needed**

Scaling without measurement is just complexity.

---

## Debugging Checklist for Stage 11

If your AI infrastructure behaves poorly, check:

- [ ] Is the model actually loaded once, or repeatedly?
- [ ] Is the bottleneck model time, queue time, or API overhead?
- [ ] Does the model fit in RAM / VRAM?
- [ ] Are long prompts causing major latency increases?
- [ ] Are you measuring one run or many runs?
- [ ] Is the vector database retrieval fast enough?
- [ ] Are metadata filters helping or hurting performance?
- [ ] Is batch size too large for memory?
- [ ] Is throughput good but latency too high, or vice versa?
- [ ] Are logs detailed enough to explain failures?
- [ ] Is the local experiment being mistaken for production readiness?
- [ ] Are you adding complexity before stabilizing the baseline?

---

## Practice Project

### Project: Local Inference Performance Lab

#### Goal

Learn how local model inference behaves in practice.

You will:

- run a local model
- measure response time
- compare prompt sizes
- understand latency behavior

#### Required Tools

- Ollama
- Python
- optional FastAPI

#### Step-by-Step Instructions

**Step 1 — Install and run Ollama**

Choose one local model that is small enough for your machine.

The purpose is not model quality first.

The purpose is to understand:

- local serving
- latency
- repeated inference behavior

> **Why this step matters:** You need a stable local baseline before you can reason about infrastructure behavior.

**Beginner explanation**

Do not start with the biggest model you can find.

Start with a model that actually runs reliably on your hardware.

That teaches more than a model that crashes.

**Step 2 — Prepare prompt test set**

Create 3 prompt types:

- short prompt
- medium prompt
- long prompt

Save them in a file such as: `data/raw/prompts.txt`

Example:

- **short:** `"Explain AI in one sentence."`
- **medium:** `"Explain how neural networks learn using simple language."`
- **long:** large multi-paragraph instruction

> **Why this step matters:** Different prompt lengths affect tokenization cost, inference time, memory use, and generation delay.

**Beginner rule**

Do not compare random prompts. Create a small, controlled test set.

**Step 3 — Measure latency**

For each prompt:

- record start time
- send request to local model
- record end time
- compute response time

Save results into: `data/outputs/inference_timing.csv`

Include columns such as:

| Column | Description |
|---|---|
| `prompt_type` | short / medium / long |
| `prompt_length` | character count |
| `response_time_seconds` | measured time |
| `model_name` | which model was used |

> **Why this step matters:** This replaces guessing with measurement.

**Better beginner measurement design**

Also capture:

- run number
- output length
- timestamp
- whether model was cold-start or warm-start

Example columns:

| Column |
|---|
| `model_name` |
| `prompt_type` |
| `prompt_length_chars` |
| `output_length_chars` |
| `run_id` |
| `response_time_seconds` |
| `warm_or_cold` |

**Step 4 — Repeat tests**

Run each prompt multiple times.

This teaches:

- variability
- warm-start vs cold-start differences
- stability of response timing

> **Why this step matters:** One measurement is not reliable. You want to understand consistency, startup effect, average performance, and outliers.

**Beginner rule**

At least run each prompt several times.

**Step 5 — Compare results**

Answer questions such as:

- does long prompt increase latency?
- does repeated inference become faster?
- how much does response length affect time?

> **Why this step matters:** The project is not only about collecting numbers. It is about learning how infrastructure behaves.

**Better analysis questions**

- Is the first request much slower than later ones?
- Does output length matter as much as input length?
- Does the system slow down over repeated use?
- Does the model remain stable?

**Step 6 — Optional API wrapper**

If you are comfortable, expose the local model through a tiny FastAPI app.

Then test:

- direct call latency
- API call latency

This teaches the difference between:

- model runtime
- service overhead

> **Why this step matters:** Infrastructure is not just model time. API overhead, serialization, request parsing, and networking all matter too.

**Step 7 — Reflection**

Write short answers:

- what affects inference speed most?
- why is local serving useful?
- why is serving different from just running code in notebook?

> **Why this step matters:** Engineering understanding is not only code. It is being able to explain what the system is doing.

#### Deliverables

- prompt test set
- timing CSV
- measurement script
- optional API wrapper
- README
- short analysis of results

---

### Experiment Tasks

**Experiment 1 — Short vs medium vs long prompt**

**Purpose:** Measure how prompt length affects latency.

**Lesson:** Input size affects serving performance.

---

**Experiment 2 — Cold start vs warm start**

**Purpose:** Compare first request timing to later requests.

**Lesson:** Model startup and warm caches matter.

---

**Experiment 3 — Short response vs long response**

**Purpose:** Measure how generation length affects total time.

**Lesson:** Output length matters, not just prompt length.

---

**Experiment 4 — Direct local call vs API wrapper**

**Purpose:** Measure serving overhead.

**Lesson:** Infrastructure adds overhead beyond pure model runtime.

---

**Experiment 5 — Repeat runs and average**

**Purpose:** Reduce misleading one-off measurements.

**Lesson:** Infrastructure evaluation requires repeated testing.

---

**Experiment 6 — Two different local models**

**Purpose:** Compare size/performance tradeoff.

**Lesson:** Better model quality often costs more latency or memory.

---

**Experiment 7 — Optional concurrency test**

**Purpose:** Send multiple requests in a short time.

**Lesson:** Single-request performance is not the whole story.

---

### Evaluation

Students should evaluate:

**1. Functionality**

- does local model run reliably?
- are timing results saved correctly?

**2. Measurement quality**

- are prompts tested consistently?
- are multiple runs recorded?

**3. Interpretation**

- does student explain latency differences clearly?

**4. Understanding**

- can student explain why serving/inference matters?

### Grading Rubric

| Category | Weight |
|---|---|
| setup and execution | 25% |
| latency measurement quality | 30% |
| analysis and explanation | 25% |
| project organization | 20% |

---

### Common Mistakes

- not saving test results
- measuring only once
- changing multiple variables at the same time
- confusing answer quality with infrastructure performance

### Expanded Common Mistakes with Reasons and Fixes

**1. Not saving test results**

**Reason:** People think they will remember the numbers.

**Problem:** You cannot compare systematically later.

**Fix:** Always save measurements to CSV or structured logs.

**2. Measuring only once**

**Reason:** One run feels enough.

**Problem:** You may mistake noise or cold-start behavior for normal performance.

**Fix:** Repeat runs and compare averages plus outliers.

**3. Changing multiple variables at the same time**

**Reason:** It feels faster to test many ideas at once.

**Problem:** You do not know what caused the difference.

**Fix:** Change one main variable per experiment.

**4. Confusing answer quality with infrastructure performance**

**Reason:** Beginners focus on whether the answer "sounds good."

**Problem:** A strong answer can still come from a slow or unstable system.

**Fix:** Measure performance separately from content quality.

**5. Ignoring cold-start effects**

**Reason:** People only look at later requests.

**Problem:** First-user experience may be much worse than expected.

**Fix:** Measure both cold and warm behavior.

**6. Testing only the happy path**

**Reason:** It is more fun to test successful cases.

**Problem:** Real systems encounter long prompts, slow responses, and failures.

**Fix:** Test varied prompt sizes and stress conditions too.

---

## Final Understanding

> AI infrastructure is what makes models usable, scalable, and reliable in real systems.

A top AI engineer does not stop at:

- training a model

They also think about:

- how it runs
- how fast it responds
- how it scales
- how it is monitored

That is what this stage teaches.

---

## Self Test

### Questions

1. What does AI infrastructure mean?
2. Why is a trained model not enough for real-world use?
3. What is model serving?
4. What is the typical request flow in model serving?
5. What is the difference between REST serving, batch inference, and streaming output?
6. Why do GPUs matter for modern AI inference?
7. What is VRAM?
8. Why can a model fail even if the code is correct?
9. What is latency?
10. What is throughput?
11. Why are latency and throughput not the same thing?
12. Why might a chatbot care more about latency than throughput?
13. Why might a batch job care more about throughput than latency?
14. What is a vector database used for?
15. Why do vector databases matter for RAG systems?
16. What is approximate nearest neighbor search?
17. Why is metadata filtering important in production retrieval?
18. What is distributed training?
19. Why do beginners usually not need distributed training first?
20. What is Ray used for?
21. What is the actor model in Ray useful for?
22. What is vLLM mainly designed for?
23. Why is vLLM better than naïve LLM serving in many cases?
24. What is Ollama useful for?
25. Why is local experimentation not the same as production readiness?
26. Why is monitoring important?
27. Why is repeated measurement better than one measurement?
28. Why should you avoid changing many performance variables at once?
29. What should you measure besides answer quality in infrastructure work?
30. What is the main lesson of this stage?

---

### Answers

**1. What does AI infrastructure mean?**

AI infrastructure is the set of systems and runtime components that make models deployable, callable, measurable, and scalable in real environments.

**2. Why is a trained model not enough for real-world use?**

Because real use also requires serving, resource management, monitoring, failure handling, and repeatable access.

**3. What is model serving?**

Model serving is exposing a model through a usable runtime interface, usually an API or service.

**4. What is the typical request flow in model serving?**

Client sends request → service receives it → model runs inference → response is returned.

**5. What is the difference between REST serving, batch inference, and streaming output?**

REST serving usually returns one response per request, batch inference processes many items together, and streaming output returns results gradually as they are produced.

**6. Why do GPUs matter for modern AI inference?**

Because they are much faster than CPUs for the parallel tensor and matrix operations used by deep learning models.

**7. What is VRAM?**

VRAM is GPU memory used to store model weights, tensors, caches, and runtime state.

**8. Why can a model fail even if the code is correct?**

Because it may not fit in RAM or VRAM, may time out, or may be too slow for the serving environment.

**9. What is latency?**

Latency is the time one request takes from start to finish.

**10. What is throughput?**

Throughput is how much work the system can handle over time, such as requests per second.

**11. Why are latency and throughput not the same thing?**

Because a system can be fast for one request but poor at handling many, or efficient overall but slow for an individual user.

**12. Why might a chatbot care more about latency than throughput?**

Because an interactive user mainly feels response delay directly.

**13. Why might a batch job care more about throughput than latency?**

Because the goal is often to process a large total workload efficiently, not to answer one user immediately.

**14. What is a vector database used for?**

It stores embeddings and supports efficient semantic similarity search.

**15. Why do vector databases matter for RAG systems?**

Because RAG depends on retrieving relevant chunks quickly and accurately from embedded knowledge.

**16. What is approximate nearest neighbor search?**

It is a faster search method that finds likely nearest vectors without checking every vector exactly.

**17. Why is metadata filtering important in production retrieval?**

Because it improves relevance, enables scoped search, and supports better control over retrieved results.

**18. What is distributed training?**

Distributed training is training a model across multiple GPUs or machines.

**19. Why do beginners usually not need distributed training first?**

Because it adds significant complexity and is unnecessary before mastering stable single-machine training.

**20. What is Ray used for?**

Ray is used for distributed computation, orchestration, and scalable serving workloads.

**21. What is the actor model in Ray useful for?**

It is useful for stateful workers and long-lived service-like components.

**22. What is vLLM mainly designed for?**

vLLM is mainly designed for efficient large language model serving.

**23. Why is vLLM better than naïve LLM serving in many cases?**

Because it improves batching, scheduling, cache usage, and overall serving efficiency.

**24. What is Ollama useful for?**

Ollama is useful for running and testing local models easily.

**25. Why is local experimentation not the same as production readiness?**

Because production requires repeated reliability, concurrency handling, monitoring, scaling, and operational discipline.

**26. Why is monitoring important?**

Because without monitoring you do not really know system latency, failures, or resource behavior.

**27. Why is repeated measurement better than one measurement?**

Because one run may be noisy, affected by cold start, or otherwise unrepresentative.

**28. Why should you avoid changing many performance variables at once?**

Because then you cannot tell what actually caused the result difference.

**29. What should you measure besides answer quality in infrastructure work?**

You should measure latency, throughput, memory usage, stability, cold-start behavior, and failure rates.

**30. What is the main lesson of this stage?**

AI infrastructure is what turns models into usable systems, and serious AI engineering requires understanding serving, performance, resource limits, and operational reliability.

---

## What You Must Be Able To Do After Stage 11

- [ ] explain what AI infrastructure means in plain English
- [ ] explain what model serving is and why it matters
- [ ] explain why GPUs are important for deep model inference
- [ ] explain latency vs throughput clearly
- [ ] explain the production role of vector databases
- [ ] explain when distributed training becomes relevant
- [ ] describe what Ray, vLLM, and Ollama are each useful for
- [ ] measure local inference performance instead of guessing
- [ ] distinguish local experimentation from production readiness
- [ ] understand that infrastructure quality is part of AI product quality
