# Stage 5 — Large Language Models (LLM)

*(Week 10–11)*

## Goal

Understand Large Language Models and how to use them effectively.

**This is the most important modern AI topic.**

You are learning:

- how LLMs work
- how to control them (prompting)
- how to integrate them into systems

This stage is where you move from:

> "I can ask ChatGPT questions"

to:

> "I understand how LLMs process text, why they fail, how prompting changes behavior, and how to build reliable systems around them."

---

## Quick Summary

A Large Language Model is a neural network trained to predict the next token in text.

That sounds simple, but at large scale it becomes extremely powerful.

LLMs can:

- answer questions
- summarize text
- extract information
- classify text
- generate code
- transform content
- reason in limited ways through pattern-based computation

But they also have limits:

- they can hallucinate
- they can be inconsistent
- they do not truly verify facts by default
- they should often be combined with retrieval, tools, validation, and system design

A beginner should finish this stage understanding:

- what a token is
- what embeddings are
- how transformers enable LLMs
- how prompting changes outputs
- why structured output matters
- why hallucination happens
- what RAG is and why it matters
- how to build safer, more reliable LLM workflows

---

## Study Materials

**HuggingFace NLP Course**
https://huggingface.co/learn/nlp-course

**OpenAI / LLM Guides (general concepts)**
https://platform.openai.com/docs

**Dive Into Deep Learning (Transformer chapters)**
https://d2l.ai/

### Topics

- Tokenization
- Embeddings
- Transformers
- Prompt Engineering
- Fine-tuning (intro)
- RAG (intro)

---

## Key Knowledge (Deep Understanding)

### 1. What is a Token

LLMs do **NOT** see words. They see **tokens**.

```
"ChatGPT is powerful"
→ ["Chat", "G", "PT", " is", " powerful"]
```

> **Key idea:** token = basic unit of text for model

#### Beginner Explanation

A token is the piece of text the model actually processes.

Humans naturally think in:

- words
- sentences
- meaning

But LLMs do not directly see text the way humans do. They first convert text into smaller units called tokens.

A token may be:

- a whole word
- part of a word
- punctuation
- whitespace-attached text
- a special symbol

*Example: `"unbelievable"` may become `"un"`, `"believ"`, `"able"` depending on the tokenizer.*

So when you send text to an LLM, the system first breaks it into tokens.

#### Why Tokens Matter

Tokens affect:

- cost
- context window usage
- truncation
- latency
- prompt design
- chunking for RAG

If your prompt is too long in tokens, it may:

- cost more
- run slower
- exceed model context limits
- cut off important content

#### Step-by-Step Mental Model

1. **Raw text enters the tokenizer** — Example: `"The stock went up today."`
2. **Text is split into tokens** — The tokenizer breaks it into model-specific pieces.
3. **Tokens are converted to IDs** — Each token becomes a numeric ID.
4. **IDs are fed into the model** — The model works with numbers, not raw text.

#### Key Algorithms / Mechanisms for Tokenization

**A. Subword Tokenization**

Most modern LLMs do not tokenize by full words only. They use subword units.

- Common words may stay whole
- Rare words are split into smaller pieces

*Why important: This lets the model handle large vocabularies, unknown words, misspellings, and mixed text forms.*

---

**B. Byte Pair Encoding (BPE)**

A common tokenization algorithm.

How it works:

1. Start with small text units
2. Repeatedly merge frequent pairs
3. Build a vocabulary of useful token pieces

*Why important: BPE balances vocabulary size and text coverage well.*

---

**C. WordPiece**

Builds subword vocabularies optimized to represent text efficiently.

*Why important: Used in many transformer systems.*

---

**D. SentencePiece / Unigram-style tokenization**

Treats text in a language-independent way and can work directly on raw text.

*Why important: Useful for multilingual and flexible tokenization pipelines.*

---

#### Strengths and Weaknesses of Subword Tokenization

| | Detail |
|---|---|
| **Strength** | Handles unknown words better |
| **Strength** | Reduces vocabulary explosion |
| **Strength** | Supports many languages and word forms |
| **Weakness** | Tokens do not align cleanly with human words |
| **Weakness** | Token count can be surprising |
| **Weakness** | Prompt length can be harder to estimate intuitively |

---

### 2. Embeddings

```
Embedding = convert text → vector

"apple" → [0.23, -0.11, ...]
```

> **Meaning:** similar words → similar vectors

#### Beginner Explanation

An embedding is a numeric representation of meaning-like information.

Computers do not understand text directly. They need numbers.

So the model converts each token or piece of text into a vector — a long list of numbers.

But this list is special: texts with similar usage often get vectors that are **close together in vector space**.

*Example: `"dog"`, `"puppy"`, `"canine"` may end up closer to each other than to `"table"` or `"airplane"`.*

#### Why Embeddings Matter

Embeddings are used for:

- semantic search
- retrieval
- clustering
- recommendation
- classification
- similarity comparison
- RAG pipelines

> They are one of the most practical concepts in modern AI systems.

#### Step-by-Step Mental Model

1. **Token or text enters the embedding layer/model** — a word, sentence, paragraph, or document chunk.
2. **It becomes a vector** — the text is mapped to a list of numbers.
3. **Similar meanings tend to map nearby** — the system can now compare texts numerically.
4. **Use vector math** — compute similarity, search, clustering, or retrieval.

#### Key Algorithms / Mechanisms for Embeddings

**A. Embedding Lookup**

Each token ID maps to a learned vector from an embedding table.

*Why important: This is how raw token IDs become dense numeric representations.*

---

**B. Contextual Embeddings**

Modern LLM embeddings depend on context.

*Example: The word `"bank"` in `"river bank"` vs `"bank account"` may produce different representations.*

*Why important: Context matters in language understanding.*

---

**C. Cosine Similarity**

Measures the angle between vectors rather than raw magnitude.

*Why important: Very useful for semantic similarity and retrieval.*

---

**D. Vector Search / Nearest Neighbor Search**

How it works:

1. Convert query into embedding
2. Compare against stored embeddings
3. Return nearest matches

*Why important: This powers semantic search and RAG retrieval.*

---

#### Strengths and Weaknesses of Embeddings

| | Detail |
|---|---|
| **Strength** | Powerful for semantic similarity |
| **Strength** | Useful across many AI systems |
| **Strength** | Practical foundation for retrieval and search |
| **Weakness** | Similarity is approximate, not perfect truth |
| **Weakness** | Embedding quality depends on model and chunk quality |
| **Weakness** | Poor chunking can hurt retrieval badly |

---

### 3. Transformers

Core architecture behind LLMs.

```
Key idea: attention mechanism learns relationships between words
```

Instead of sequential processing (RNN), Transformers:

- process all tokens **in parallel**
- use **attention** to focus on important parts

#### Beginner Explanation

Transformers are the architecture that made modern LLMs possible.

Older sequence models like RNNs processed text one step at a time. Transformers changed that by letting each token look at other tokens directly using attention.

This makes them:

- better at long-range relationships
- easier to train in parallel
- much more scalable

*That is why transformers became the foundation of models like GPT and many other LLMs.*

#### Step-by-Step Mental Model

1. **Tokens become embeddings** — each token is represented as a vector.
2. **Positional information is added** — because the transformer needs to know order.
3. **Self-attention is computed** — each token checks which other tokens matter.
4. **Information is mixed** — tokens gather useful context from other tokens.
5. **Feed-forward layers refine representation** — each position is processed further.
6. **Repeat across many layers** — the model builds richer contextual understanding.

#### Key Algorithms / Mechanisms for Transformers

**A. Self-Attention**

Each token computes how much attention to pay to other tokens.

*Why important: Lets the model capture relationships across the full sequence.*

---

**B. Query-Key-Value (QKV)**

| Component | Role |
|---|---|
| **Query** | What this token is looking for |
| **Key** | What this token offers |
| **Value** | The information this token contributes |

Attention scores are computed between queries and keys, then used to combine values.

*Why important: This is how attention becomes a learnable information-routing system.*

---

**C. Multi-Head Attention**

Uses multiple attention heads in parallel. Different heads can focus on different relationships.

*Why important: Lets the model capture multiple types of patterns at once.*

---

**D. Positional Encoding / Position Information**

Adds token order information.

*Why important: Without position, the model would not know whether a word came first or last.*

---

**E. Feed-Forward Networks**

After attention, each token passes through additional learned transformations.

*Why important: This increases expressive power beyond attention alone.*

---

**F. Causal Masking**

A token can only attend to **previous** tokens, not future ones.

*Why important: This allows next-token prediction training.*

---

#### Strengths and Weaknesses of Transformers

| | Detail |
|---|---|
| **Strength** | Handles long-range dependencies better than older sequence models |
| **Strength** | Highly parallelizable |
| **Strength** | Scales well with large datasets and large parameter counts |
| **Weakness** | Can be expensive in memory and compute |
| **Weakness** | Long contexts can still be difficult |
| **Weakness** | Attention cost can grow significantly with sequence length |

---

### 4. Prompt Engineering

LLM behavior depends heavily on prompt.

| Prompt | Quality |
|---|---|
| `"Explain stock"` | Vague — poor results |
| `"Explain stock trends in simple terms for beginners, include examples."` | Specific — better results |

#### Beginner Explanation

Prompt engineering is the practice of giving the model better instructions so it behaves more reliably.

LLMs are very sensitive to:

- wording
- specificity
- examples
- output format
- role framing
- task boundaries

> A vague prompt often gives vague results. A precise prompt often gives more useful results.

#### Why Prompting Matters

Prompting changes:

- clarity
- correctness
- depth
- style
- structure
- consistency
- usefulness

**Prompt design is often the fastest way to improve an LLM system before moving to fine-tuning.**

#### Step-by-Step Mental Model

1. **Define the task clearly** — What exactly do you want?
2. **Define the audience** — Beginner, expert, executive, developer?
3. **Define constraints** — Length, tone, format, scope.
4. **Define output structure** — Paragraph, bullets, JSON, table, schema.
5. **Add examples if needed** — Few-shot prompting can stabilize behavior.

#### Key Algorithms / Mechanisms for Prompting

**A. Zero-Shot Prompting**

Give instructions without examples. The model uses its prior training to perform the task from description alone.

*Why important: Fast and simple baseline.*

---

**B. Few-Shot Prompting**

Provide a few input-output examples. The model imitates the demonstrated pattern.

*Why important: Often improves consistency and formatting.*

---

**C. Role / System Framing**

Set the model's behavioral context.

```
"You are a financial analyst writing for beginners."
```

*Why important: Helps shape tone, depth, and perspective.*

---

**D. Chain-of-Thought Style Scaffolding**

Ask the model to reason in steps or follow a structured process.

*Why important: Can improve performance on complex tasks when used appropriately.*

---

**E. Instruction Decomposition**

Break one big task into smaller subtasks.

*Why important: Large prompts become more reliable when tasks are separated.*

---

#### Strengths and Weaknesses of Prompting

| | Detail |
|---|---|
| **Strength** | Fast improvement without retraining |
| **Strength** | Cheaper than fine-tuning |
| **Strength** | Great for prototyping and workflow design |
| **Weakness** | Prompts can still be unstable |
| **Weakness** | Prompt quality alone cannot fix knowledge gaps |
| **Weakness** | Prompting does not replace validation |

---

### 5. Structured Output

LLMs are powerful but inconsistent. The solution is to **enforce format**.

```json
{
  "summary": "...",
  "risk": "...",
  "recommendation": "..."
}
```

#### Beginner Explanation

Free-form text is flexible, but it is hard for software systems to depend on.

If you want an LLM to be part of a real application, you often need **predictable output**.

Structured output examples:

- JSON
- fixed fields
- schema-based objects
- classification labels
- extracted entities

Structured output makes LLM results easier to:

- validate
- parse
- store
- display
- feed into downstream systems

#### Step-by-Step Mental Model

1. **Define the exact output schema** — What fields should exist?
2. **Tell the model the required format** — Be explicit.
3. **Ask for only the schema** — Reduce extra commentary.
4. **Validate the output** — Never assume correctness just because it "looks like JSON."

#### Key Algorithms / Mechanisms for Structured Output

**A. Schema-Constrained Prompting**

Give the exact format in the prompt. The model imitates the requested structure.

*Why important: Simple and widely used.*

---

**B. JSON Validation / Parsing**

Programmatically verify the output. Try to parse the result and reject invalid structure.

*Why important: LLM output should be treated like external input — validate it.*

---

**C. Function / Tool Calling Style Interfaces**

Modern LLM systems can be guided toward structured tool arguments.

*Why important: Improves reliability for downstream automation.*

---

**D. Post-Processing and Repair**

If the model output is almost right but malformed, a repair step may fix it.

*Why important: Useful in production pipelines, but should not replace proper prompting and validation.*

---

#### Strengths and Weaknesses of Structured Output

| | Detail |
|---|---|
| **Strength** | Reliable downstream integration |
| **Strength** | Easier automation |
| **Strength** | Easier validation and storage |
| **Weakness** | Model may still produce invalid JSON |
| **Weakness** | Strict structure can reduce expressiveness |
| **Weakness** | Validation logic is still needed |

---

### 6. Hallucination

LLMs can generate **incorrect but fluent** answers.

> **Key understanding:** LLM ≠ truth engine

#### Beginner Explanation

A hallucination is when the model produces content that sounds good but is **wrong, unsupported, invented, or misleading**.

This is dangerous because LLMs are often very fluent — the answer may sound professional while still being false.

Examples of hallucinations:

- invented citations
- wrong facts
- fake APIs
- made-up legal rules
- imaginary company details
- unsupported conclusions

#### Why Hallucination Happens

An LLM is trained to generate likely text patterns. Its main training objective is **not**:

- truth
- verification
- source-grounded accuracy

Its core objective is **next-token prediction**.

So if it lacks reliable grounding, it may still produce a confident answer.

#### Key Mechanisms Related to Hallucination

**A. Next-Token Prediction**

The model predicts the next token given previous tokens.

*Why important: This explains why fluency does not guarantee truth.*

---

**B. Temperature / Sampling Effects**

Higher randomness can produce more diverse but less stable outputs.

*Why important: Sampling behavior can influence hallucination risk.*

---

**C. Retrieval Grounding**

Use external documents to anchor answers.

*Why important: Grounding can reduce unsupported generation.*

---

**D. Verification / Validation Layers**

Post-check model outputs against sources, rules, schemas, or external systems.

*Why important: Real systems need verification, not trust alone.*

---

#### Hallucination Risk Factors

Higher risk when:

- prompt is vague
- knowledge is missing
- task is high-stakes
- user asks for exact facts without grounding
- citations are requested without sources
- output format encourages invention

#### Fix Strategies

- retrieve real documents
- require citations when appropriate
- validate outputs
- restrict scope
- use structured prompts
- use external tools or databases
- ask the model to say "unknown" when unsure

---

### 7. RAG (Preview)

```
LLM + external knowledge

Flow: query → retrieve docs → LLM → answer
```

#### Beginner Explanation

**RAG** means **Retrieval-Augmented Generation**.

Instead of asking the LLM to rely only on its internal training, you first **retrieve relevant documents** and then give those documents to the model. This helps the model answer with more grounded information.

> RAG is one of the most important practical LLM system patterns.

#### Why RAG Matters

RAG helps when:

- knowledge changes over time
- your documents are private
- you need source grounding
- you want lower hallucination risk
- you need enterprise search or Q&A

#### Step-by-Step Mental Model

1. **User asks a question** — Example: *"What does our onboarding policy say about contractor access?"*
2. **Convert question to embedding** — used for retrieval.
3. **Search document chunks** — find relevant passages.
4. **Send top passages with the question to the LLM** — now the LLM has context.
5. **Generate grounded answer** — preferably citing the retrieved documents.

#### Key Algorithms / Mechanisms for RAG

**A. Chunking**

Split documents into retrievable pieces. Large documents are broken into smaller chunks.

*Why important: Bad chunking is one of the biggest causes of poor retrieval quality.*

---

**B. Embedding-Based Retrieval**

Convert chunks and query to vectors, then compare similarity.

*Why important: Supports semantic search, not just keyword match.*

---

**C. Top-K Retrieval**

Return the K most relevant chunks.

*Why important: The model cannot read the entire corpus every time.*

---

**D. Re-ranking**

After retrieval, reorder candidate chunks using a stronger relevance model.

*Why important: Improves retrieval precision.*

---

**E. Context Injection**

Pass retrieved chunks into the prompt.

*Why important: The model can only use retrieved knowledge if that context is actually included well.*

---

#### Strengths and Weaknesses of RAG

| | Detail |
|---|---|
| **Strength** | Grounds answers in real documents |
| **Strength** | Helps with private/company knowledge |
| **Strength** | Reduces dependence on model memory |
| **Strength** | Improves updateability |
| **Weakness** | Retrieval can fail |
| **Weakness** | Bad chunking ruins results |
| **Weakness** | Too much context can confuse the model |
| **Weakness** | Grounded answers still need evaluation |

---

### 8. Fine-Tuning (Intro)

Fine-tuning means further training a model on task-specific data.

*This topic is only introduced at this stage.*

#### Beginner Explanation

- **Prompting** changes behavior at inference time.
- **Fine-tuning** changes the model itself.

You fine-tune when you want the model to:

- adopt a consistent style
- follow a domain pattern
- classify or format more reliably
- specialize to your tasks

But fine-tuning is usually **not** the first step.

In many practical systems, you should first try:

- better prompting
- structured output
- retrieval
- validation
- tool use

*Then only consider fine-tuning if those are not enough.*

#### Key Algorithms / Mechanisms for Fine-Tuning

**A. Supervised Fine-Tuning (SFT)**

Train on prompt-response examples. The model learns to imitate desired responses more reliably.

*Why important: Common entry point for adapting LLM behavior.*

---

**B. Parameter-Efficient Fine-Tuning (PEFT) / LoRA-style methods**

Update only a smaller set of parameters.

*Why important: Makes adaptation cheaper and more practical.*

---

**C. Instruction Tuning**

Fine-tune on many instruction-following examples.

*Why important: Improves general instruction-following behavior.*

---

#### Strengths and Weaknesses of Fine-Tuning

| | Detail |
|---|---|
| **Strength** | Can improve consistency |
| **Strength** | Can adapt style or domain behavior |
| **Strength** | Useful when prompting alone is insufficient |
| **Weakness** | Requires good data |
| **Weakness** | Can be expensive |
| **Weakness** | Can overfit or degrade behavior |
| **Weakness** | Not a substitute for retrieval on changing facts |

---

## Difficulty Points

### 1. Thinking LLM "understands"

**It predicts next token. It does NOT understand.**

*Why this happens:* LLM outputs can look thoughtful, coherent, and human-like.

*Why this is a problem:* You may trust the model too much or assume it has verified knowledge.

**Fix strategy:** Use this mental model:

> LLM = pattern-based sequence model, not a built-in truth engine

Always ask: *Is this grounded? Is this verified? Does this need retrieval or external checking?*

---

### 2. Prompt instability

**Small changes → big output difference**

*Why this happens:* LLMs are sensitive to wording, order, examples, and framing.

*Why this is a problem:* A system that works "sometimes" is not reliable enough for production.

**Fix strategy:**

- standardize prompts
- version prompts
- separate task from formatting
- evaluate prompts on test sets
- use examples and schemas for stability

---

### 3. Hallucination

**LLM may confidently give wrong answers.**

*Why this happens:* The model is optimized for plausible continuation, not automatic truth-checking.

*Why this is a problem:* Fluent wrong answers are dangerous, especially in business, legal, financial, or technical systems.

**Fix strategy:**

- use RAG
- validate facts
- require grounding
- restrict scope
- use structured output
- add refusal logic for unknowns

---

### 4. Output inconsistency

**Same input → slightly different output**

*Why this happens:* Sampling, randomness, prompt ambiguity, and model variability can all affect outputs.

*Why this is a problem:* It becomes hard to build deterministic workflows.

**Fix strategy:**

- lower randomness when needed
- define strict output formats
- use examples
- post-validate
- separate generation from decision rules

---

### 5. Over-reliance on LLM

**LLM should NOT handle everything.**

*Why this happens:* LLMs feel like universal tools.

*Why this is a problem:* Some tasks are better handled by rules, search, databases, calculators, APIs, validators, or classic ML.

**Fix strategy:** Use LLMs where language flexibility helps, and use deterministic systems where correctness matters.

---

### 6. Confusing embeddings with full understanding

*Why this happens:* Embeddings often produce surprisingly good semantic search results.

*Why this is a problem:* People may assume nearest-neighbor similarity means deep understanding or exact factual relevance.

**Fix strategy:** Treat embeddings as useful semantic signals, not perfect reasoning.

---

### 7. Treating RAG as automatic truth

*Why this happens:* People assume retrieved documents automatically solve hallucinations.

*Why this is a problem:* Retrieval can miss the right chunk, retrieve irrelevant chunks, provide outdated content, or give contradictory passages.

**Fix strategy:** Evaluate retrieval quality separately from answer quality.

---

## LLM Workflow (Real World)

| Step | Action |
|---|---|
| 1 | Define the task |
| 2 | Decide whether an LLM is actually needed |
| 3 | Choose input format |
| 4 | Design prompt |
| 5 | Choose output format |
| 6 | Add grounding if needed |
| 7 | Run model |
| 8 | Validate output |
| 9 | Log results |
| 10 | Evaluate systematically |
| 11 | Improve prompt / retrieval / validation |
| 12 | Deploy with safeguards |

### Explanation of Each Step

1. **Define the task** — summarize text, classify support tickets, extract entities, answer questions over documents.
2. **Decide whether an LLM is actually needed** — sometimes a rule, SQL query, regex, or search engine is better.
3. **Choose input format** — what text or context will be sent?
4. **Design prompt** — be explicit about goal, audience, constraints, and format.
5. **Choose output format** — free text, JSON, labels, bullet list, etc.
6. **Add grounding if needed** — if the task depends on facts or private docs, retrieval may be needed.
7. **Run model** — call the LLM.
8. **Validate output** — check structure, logic, allowed values, and source usage.
9. **Log results** — save prompts, outputs, errors, and metadata.
10. **Evaluate systematically** — use a test set instead of impressions only.
11. **Improve prompt / retrieval / validation** — iterate on the full system, not only the prompt.
12. **Deploy with safeguards** — add fallbacks, monitoring, refusal logic, and validation.

---

## Debugging Checklist for Stage 5

If LLM results are poor, check:

- [ ] Is the task clearly defined?
- [ ] Is the prompt too vague?
- [ ] Is important context missing?
- [ ] Is the output format too loose?
- [ ] Are you asking for facts without grounding?
- [ ] Is token length too large?
- [ ] Are retrieved chunks relevant?
- [ ] Is chunking poor?
- [ ] Are you evaluating systematically or only impressionistically?
- [ ] Are you validating JSON and structured output?
- [ ] Is randomness too high for the use case?
- [ ] Should some part of the task be done by rules or tools instead?

---

## Example Code

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

print(generator("AI will change", max_length=30))
```

### Beginner Walkthrough of the Example

| Line | What it does |
|---|---|
| `pipeline("text-generation", model="gpt2")` | Loads a text generation pipeline using GPT-2 |
| `generator("AI will change", max_length=30)` | Asks the model to continue the prompt |
| `max_length=30` | Limits the total generated sequence length |

This example shows the core LLM pattern:

```
prompt in → generated continuation out
```

But this is only the beginning. Real LLM systems usually need:

- better prompts
- validation
- structure
- grounding
- evaluation

---

## Practice Project

### Project: Prompt Engineering Playground

#### Goal

Understand how prompts affect LLM outputs.

You are not only trying to get interesting output. You are learning:

- how prompt clarity changes results
- how structure affects reliability
- how few-shot examples affect behavior
- how hallucinations appear
- how to compare outputs systematically

---

#### Step 1 — Choose one task

Examples:

- summarize news
- explain concept
- extract structured info

> **Beginner rule:** Do NOT change the task while also changing the prompt style. Otherwise you will not know what caused the output difference.

---

#### Step 2 — Create input dataset

Create 10–20 examples:

```json
[
  {"text": "NVDA stock rises due to AI demand"},
  {"text": "Fed signals rate changes"}
]
```

Use examples with different difficulty:

- short text
- longer text
- easy cases
- ambiguous cases
- fact-heavy cases

---

#### Step 3 — Create multiple prompts

| Prompt Type | Example |
|---|---|
| **A. Vague prompt** | `"Summarize this."` |
| **B. Specific prompt** | `"Summarize this in 3 sentences for a beginner investor."` |
| **C. Few-shot prompt** | Give 2–3 examples of desired summaries |
| **D. JSON format prompt** | Require fixed fields: `summary`, `sentiment`, `risks` |

---

#### Step 4 — Run LLM

Save outputs:

```python
results = []
```

Always save:

- input
- prompt version
- raw output
- parsed output if applicable
- notes on errors

---

#### Step 5 — Compare outputs

Evaluate:

- correctness
- clarity
- consistency
- structure

Also evaluate:

- hallucination risk
- formatting validity
- usefulness for downstream systems
- variability across repeated runs

> **Prompt engineering without evaluation becomes guessing.**

---

#### Step 6 — Test structured output

Force JSON output and validate.

Try:

- parse the JSON
- detect failures
- count invalid outputs
- improve prompt until valid rate improves

*This simulates real-world app integration.*

---

#### Step 7 — Add grounding experiment

Take one fact-based task and compare:

- prompt only
- prompt + provided reference passage

*This teaches why grounding changes reliability.*

---

#### Deliverables

- prompt definitions
- outputs
- comparison report

---

### Experiment Tasks

| Experiment | Purpose | Lesson |
|---|---|---|
| **1 — Repeat the same prompt** | Measure variability and inconsistency | Same prompt may not always yield identical output |
| **2 — Vague vs specific prompt** | See how specificity affects clarity and relevance | Prompt detail strongly affects usefulness |
| **3 — Zero-shot vs few-shot** | See whether examples stabilize format and behavior | Few-shot prompting can improve consistency |
| **4 — Free text vs JSON output** | See tradeoffs between flexibility and reliability | Structured output is better for systems |
| **5 — Prompt-only vs grounded prompt** | See whether a provided passage reduces unsupported claims | Grounding often improves factual reliability |
| **6 — Force refusal behavior** | Teach safer prompting — ask for "unknown" if evidence is missing | Good prompts can reduce overconfident guessing |

---

## Common Mistakes

### Quick Overview

- not saving outputs
- changing prompt and task together
- ignoring hallucinations
- trusting fluent answers

### Expanded Common Mistakes with Reasons and Fixes

| # | Mistake | Reason | Problem | Fix |
|---|---|---|---|---|
| 1 | Not saving outputs | Beginners test casually and rely on memory | Cannot compare prompts systematically | Store prompt version, input, output, and notes |
| 2 | Changing prompt and task together | Keep experimenting without controlled comparison | Do not know what caused improvement or failure | Change one variable at a time |
| 3 | Ignoring hallucinations | The answer sounds convincing | May ship false content into a product or workflow | Treat ungrounded factual output as unverified until checked |
| 4 | Trusting fluent answers | Fluency feels like intelligence | Style hides mistakes | Evaluate correctness separately from writing quality |
| 5 | Using free-form output for system workflows | Free text is easy to ask for | Parsing becomes fragile and inconsistent | Use schemas or structured output when integrating with software |
| 6 | Using LLM when a rule-based method is better | LLMs are exciting and flexible | Adds cost and uncertainty to deterministic tasks | Use the simplest reliable solution for each subtask |
| 7 | Sending too much irrelevant context | It feels safer to include everything | Model may become distracted, slower, and less accurate | Retrieve and include only the most relevant context |

---

## Final Understanding

> LLMs generate text based on patterns, and their behavior is controlled by prompts, not true understanding.

**Also:**

> Reliable LLM systems do not rely on prompt magic alone. They use structure, grounding, validation, and good workflow design.

---

## Self Test

### Questions

1. What is a token?
2. Why do LLMs use tokens instead of directly processing words as humans do?
3. What is tokenization?
4. What is BPE?
5. Why does token count matter?
6. What is an embedding?
7. Why are embeddings useful?
8. What does cosine similarity measure?
9. What is the core idea of transformers?
10. What does self-attention do?
11. What are queries, keys, and values?
12. Why is positional information needed?
13. What is causal masking?
14. What is prompt engineering?
15. Why do small wording changes affect LLM output?
16. What is zero-shot prompting?
17. What is few-shot prompting?
18. Why is structured output important?
19. Why should JSON output still be validated?
20. What is hallucination?
21. Why can an LLM hallucinate even when it sounds confident?
22. What is temperature or sampling randomness in generation?
23. Why is an LLM not a truth engine?
24. What is RAG?
25. Why does RAG help factual tasks?
26. What is chunking in RAG?
27. Why can bad chunking hurt retrieval?
28. What is fine-tuning?
29. When should you try prompting/RAG before fine-tuning?
30. What is the main lesson of this stage?

---

### Answers

**1. What is a token?**
A token is the basic unit of text the model processes.

**2. Why do LLMs use tokens instead of directly processing words as humans do?**
Because the model works with numerical units derived from text, and tokenization provides a manageable way to represent language computationally.

**3. What is tokenization?**
Tokenization is the process of splitting text into tokens and converting them into model-readable IDs.

**4. What is BPE?**
BPE, or Byte Pair Encoding, is a subword tokenization algorithm that repeatedly merges frequent text pairs to build a useful token vocabulary.

**5. Why does token count matter?**
Because it affects cost, context limits, latency, and whether important prompt content gets truncated.

**6. What is an embedding?**
An embedding is a vector representation of text that captures semantic or usage-related information.

**7. Why are embeddings useful?**
Because they let systems compare text semantically, perform retrieval, clustering, and similarity search.

**8. What does cosine similarity measure?**
It measures how similar two vectors are based on the angle between them.

**9. What is the core idea of transformers?**
The core idea is attention: tokens can directly use information from other relevant tokens.

**10. What does self-attention do?**
It calculates how much each token should pay attention to other tokens in the same sequence.

**11. What are queries, keys, and values?**
They are learned representations used inside attention to compute relevance and combine information.

**12. Why is positional information needed?**
Because attention alone does not inherently know token order.

**13. What is causal masking?**
It prevents a token from attending to future tokens during next-token prediction.

**14. What is prompt engineering?**
Prompt engineering is designing instructions and examples to guide LLM behavior more reliably.

**15. Why do small wording changes affect LLM output?**
Because the model is sensitive to framing, specificity, examples, and context structure.

**16. What is zero-shot prompting?**
It is asking the model to perform a task without giving examples.

**17. What is few-shot prompting?**
It is giving a small number of examples so the model can imitate the desired pattern.

**18. Why is structured output important?**
Because software systems need predictable, parseable output formats.

**19. Why should JSON output still be validated?**
Because the model can produce malformed, incomplete, or semantically wrong JSON even if it looks correct.

**20. What is hallucination?**
Hallucination is when the model generates false, unsupported, or invented content.

**21. Why can an LLM hallucinate even when it sounds confident?**
Because fluency comes from pattern generation, not built-in fact verification.

**22. What is temperature or sampling randomness in generation?**
It controls how deterministic or diverse the generated output is.

**23. Why is an LLM not a truth engine?**
Because its core objective is next-token prediction, not guaranteed factual correctness.

**24. What is RAG?**
RAG stands for Retrieval-Augmented Generation: retrieve relevant documents first, then use them as context for the LLM.

**25. Why does RAG help factual tasks?**
Because it grounds the model in external documents instead of relying only on internal model memory.

**26. What is chunking in RAG?**
Chunking is splitting documents into smaller retrievable pieces.

**27. Why can bad chunking hurt retrieval?**
Because relevant information may be split poorly, mixed with noise, or made harder to retrieve accurately.

**28. What is fine-tuning?**
Fine-tuning is further training a model on task-specific examples to adapt its behavior.

**29. When should you try prompting/RAG before fine-tuning?**
When better instructions, structure, grounding, and validation may solve the problem more cheaply and safely.

**30. What is the main lesson of this stage?**
LLMs are powerful language models, but reliable systems require prompting, grounding, validation, and careful workflow design rather than blind trust.

---

## What You Must Be Able To Do After Stage 5

- [ ] Explain what a token is and why tokenization matters
- [ ] Explain what embeddings are and why they are useful
- [ ] Explain the core idea of transformers and self-attention
- [ ] Design clearer prompts for better outputs
- [ ] Distinguish zero-shot and few-shot prompting
- [ ] Request and validate structured outputs
- [ ] Explain why LLMs hallucinate
- [ ] Explain what RAG is and why it helps
- [ ] Understand when prompting, retrieval, rules, or fine-tuning are appropriate
- [ ] Treat LLMs as powerful but fallible components in larger systems
