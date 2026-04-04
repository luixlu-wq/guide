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
- what multi-head attention is and why it is central
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

### Deep Study Path (Recommended Order)

Use this order if the chapter feels difficult:

1. **Transformer basics and attention math**
   - Attention Is All You Need: https://arxiv.org/abs/1706.03762
   - D2L multi-head attention: https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html
2. **Implementation-level understanding**
   - PyTorch MultiheadAttention: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
   - PyTorch TransformerEncoderLayer: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html
3. **Tokenization and practical NLP pipeline**
   - Hugging Face NLP Course: https://huggingface.co/learn/nlp-course
   - Hugging Face Tokenizers docs: https://huggingface.co/docs/tokenizers/index
4. **RAG and grounded generation**
   - RAG paper (Lewis et al., 2020): https://arxiv.org/abs/2005.11401
5. **Prompting and system reliability**
   - OpenAI docs: https://platform.openai.com/docs
   - OpenAI Cookbook: https://cookbook.openai.com/
6. **Deeper language-model theory**
   - CS224n: https://web.stanford.edu/class/cs224n/
   - Jurafsky & Martin SLP draft: https://web.stanford.edu/~jurafsky/slp3/

---

## Key Knowledge (Deep Understanding)

### 0. PyTorch and CUDA for LLM Workflows

You need this before training-oriented LLM code becomes clear.

- **PyTorch**: deep learning framework used to define tensors, models, losses, and optimizers.
- **CUDA**: NVIDIA GPU compute platform that PyTorch can use to accelerate training/inference.

Practical relationship:

- PyTorch is the software framework.
- CUDA is the GPU execution backend.
- In code, you usually choose a `device` (`cpu` or `cuda`) and move both model and tensors to that device.

Core training flow (device-aware):

1. Move tensors to device (`cpu` or `cuda`).
2. Forward pass computes prediction.
3. Loss compares prediction vs target.
4. Backward pass computes gradients.
5. Optimizer updates parameters.

Minimum operatable check:

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("torch_version:", torch.__version__)
print("cuda_available:", torch.cuda.is_available())
print("selected_device:", device)
```

What this means for this chapter:

- Stage 5 scripts are written to run on CPU by default and use CUDA when available.
- The mini LLM lab uses the same device selection pattern so you can observe real training behavior safely on both environments.

Runnable PyTorch/CUDA examples in this chapter:

- [topic00a_pytorch_cuda_simple.py](src/stage-5/topic00a_pytorch_cuda_simple.py)
  - device detection and tensor operations
- [topic00_pytorch_cuda_intermediate.py](src/stage-5/topic00_pytorch_cuda_intermediate.py)
  - device-aware model training loop
- [topic00c_pytorch_cuda_advanced.py](src/stage-5/topic00c_pytorch_cuda_advanced.py)
  - optional mixed precision (`amp`) training on CUDA

Run commands:

```powershell
python .\src\stage-5\topic00a_pytorch_cuda_simple.py
python .\src\stage-5\topic00_pytorch_cuda_intermediate.py
python .\src\stage-5\topic00c_pytorch_cuda_advanced.py
```

PyTorch/CUDA references:

- PyTorch getting started:
  - https://pytorch.org/get-started/locally/
- PyTorch CUDA semantics:
  - https://pytorch.org/docs/stable/notes/cuda.html

---

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

Multi-head attention runs multiple attention operations in parallel on different learned projections of Q, K, and V.

From the original Transformer paper:

- each head uses its own learned projections
- head outputs are concatenated
- then projected again to produce final output

Core equations:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V
MultiHead(Q, K, V) = Concat(head_1, ..., head_h)W^O
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

*Why important: It lets the model jointly attend to information from different representation subspaces at different positions.*

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

#### Multi-Head Attention Deep Dive (Step-by-Step)

Use this as the operational mental model.

Runnable script: [topic01_multihead_attention.py](src/stage-5/topic01_multihead_attention.py)

Assume token representations `X` with shape `(batch_size, seq_len, d_model)`.

1. **Linear projections per head**
   - for each head `i`, compute:
     - `Q_i = XW_i^Q`
     - `K_i = XW_i^K`
     - `V_i = XW_i^V`
   - shape per head is usually `(batch_size, seq_len, d_k)`
2. **Per-head attention scores**
   - `scores_i = Q_i K_i^T / sqrt(d_k)`
3. **Masking (if decoder causal attention)**
   - block future positions before softmax
4. **Per-head weighted values**
   - `A_i = softmax(scores_i)`
   - `H_i = A_i V_i`
5. **Concatenate all heads**
   - `H = Concat(H_1, ..., H_h)`
6. **Final output projection**
   - `Y = HW^O`

Interpretation:

- one head can learn short-range/local relations
- another can learn long-range dependencies
- another can track syntax-like or coreference-like patterns

The key point is not that each head is manually assigned a meaning, but that multiple heads increase representational flexibility.

#### Self-Attention vs Multi-Head Attention vs Transformer

| Concept | What it is | Scope |
|---|---|---|
| **Self-attention** | One attention operation over tokens in a sequence | A mechanism |
| **Multi-head attention** | Multiple self-attention heads in parallel + concat + output projection | A richer attention layer |
| **Transformer** | Full architecture stack using multi-head attention + feed-forward + residual + layer norm + positional handling (+ masking/cross-attention by context) | The complete model/block design |

If you are confused, remember:

- self-attention is a single tool
- multi-head attention is several copies of that tool working in parallel
- transformer is the full machine that includes multi-head attention as one major component

#### Where Multi-Head Attention Appears Inside Transformer

In the original encoder-decoder Transformer:

1. **Encoder self-attention**: `Q, K, V` all come from encoder hidden states.
2. **Decoder masked self-attention**: `Q, K, V` all come from decoder states, with future mask.
3. **Encoder-decoder (cross) attention**: `Q` comes from decoder, while `K, V` come from encoder outputs.

#### Mini Operatable Code (Shape-Level Understanding)

```python
import torch
import torch.nn as nn

batch_size, seq_len, d_model = 2, 5, 16
num_heads = 4

x = torch.randn(batch_size, seq_len, d_model)
mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, batch_first=True)

out, attn_weights = mha(x, x, x)  # self-attention path
print("input shape:", x.shape)            # (2, 5, 16)
print("output shape:", out.shape)         # (2, 5, 16)
print("attn shape:", attn_weights.shape)  # (2, 5, 5) averaged over heads by default
```

What this demonstrates:

- multi-head attention keeps token sequence length
- output remains in model dimension `d_model`
- attention weights describe how each position attends to others

#### Why This Part Is Hard (And How To Learn It)

Why it feels hard:

- too many terms (`Q`, `K`, `V`, heads, masking, projection)
- mechanism level and architecture level are often mixed together

How to learn it correctly:

1. Learn one attention head first.
2. Add multiple heads (parallel projections + concat).
3. Then place that layer inside a Transformer block.

Checkpoint question before moving on:

- If I remove feed-forward, residual, and layer norm, do I still have a Transformer?
  - No. You only have part of it (attention layer), not the full Transformer block.

#### Authoritative References For This Module

- Attention Is All You Need (Section 3.2.1 and 3.2.2):
  - https://arxiv.org/abs/1706.03762
- PyTorch `nn.MultiheadAttention`:
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
- PyTorch `nn.TransformerEncoderLayer`:
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html
- Dive into Deep Learning, Multi-Head Attention:
  - https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html

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

### 2. Confusing self-attention, multi-head attention, and transformer

**This is one of the most common Stage 5 confusion points.**

*Why this happens:* these terms are introduced close together and often explained at different abstraction levels.

*Why this is a problem:* if you mix mechanism level with architecture level, model debugging and design choices become unclear.

**Fix strategy:** memorize this hierarchy:

- self-attention = one mechanism
- multi-head attention = parallel set of self-attention heads + concat/projection
- transformer = full block/architecture containing multi-head attention plus other sublayers

---

### 3. Prompt instability

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

### 4. Hallucination

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

### 5. Output inconsistency

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

### 6. Over-reliance on LLM

**LLM should NOT handle everything.**

*Why this happens:* LLMs feel like universal tools.

*Why this is a problem:* Some tasks are better handled by rules, search, databases, calculators, APIs, validators, or classic ML.

**Fix strategy:** Use LLMs where language flexibility helps, and use deterministic systems where correctness matters.

---

### 7. Confusing embeddings with full understanding

*Why this happens:* Embeddings often produce surprisingly good semantic search results.

*Why this is a problem:* People may assume nearest-neighbor similarity means deep understanding or exact factual relevance.

**Fix strategy:** Treat embeddings as useful semantic signals, not perfect reasoning.

---

### 8. Treating RAG as automatic truth

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

## Stage 5 Script Mapping (for `/red-book/src/stage-5`)

Core run commands:

```powershell
powershell -ExecutionPolicy Bypass -File .\src\stage-5\run_all_stage5.ps1
powershell -ExecutionPolicy Bypass -File .\src\stage-5\run_ladder_stage5.ps1
powershell -ExecutionPolicy Bypass -File .\src\stage-5\run_ladder_stage5.ps1 -IncludeBridge
powershell -ExecutionPolicy Bypass -File .\src\stage-5\run_ladder_stage5.ps1 -IncludeBridge -IncludeLab
```

Script mapping:

- PyTorch/CUDA ladder:
  - [topic00a_pytorch_cuda_simple.py](src/stage-5/topic00a_pytorch_cuda_simple.py)
  - [topic00_pytorch_cuda_intermediate.py](src/stage-5/topic00_pytorch_cuda_intermediate.py)
  - [topic00c_pytorch_cuda_advanced.py](src/stage-5/topic00c_pytorch_cuda_advanced.py)
- Multi-head attention bridge:
  - [topic01_multihead_attention.py](src/stage-5/topic01_multihead_attention.py)
- Tokenization ladder:
  - [topic01a_tokenization_simple.py](src/stage-5/topic01a_tokenization_simple.py)
  - [topic01_tokenization_intermediate.py](src/stage-5/topic01_tokenization_intermediate.py)
  - [topic01c_tokenization_advanced.py](src/stage-5/topic01c_tokenization_advanced.py)
- Prompting ladder:
  - [topic02a_prompting_simple.py](src/stage-5/topic02a_prompting_simple.py)
  - [topic02_prompting_intermediate.py](src/stage-5/topic02_prompting_intermediate.py)
  - [topic02c_prompting_advanced.py](src/stage-5/topic02c_prompting_advanced.py)
- Structured output ladder:
  - [topic03a_structured_output_simple.py](src/stage-5/topic03a_structured_output_simple.py)
  - [topic03_structured_output_intermediate.py](src/stage-5/topic03_structured_output_intermediate.py)
  - [topic03c_structured_output_advanced.py](src/stage-5/topic03c_structured_output_advanced.py)
- RAG ladder:
  - [topic04a_rag_simple.py](src/stage-5/topic04a_rag_simple.py)
  - [topic04_rag_intermediate.py](src/stage-5/topic04_rag_intermediate.py)
  - [topic04c_rag_advanced.py](src/stage-5/topic04c_rag_advanced.py)
- Embeddings ladder:
  - [topic05a_embeddings_simple.py](src/stage-5/topic05a_embeddings_simple.py)
  - [topic05_embeddings_intermediate.py](src/stage-5/topic05_embeddings_intermediate.py)
  - [topic05c_embeddings_advanced.py](src/stage-5/topic05c_embeddings_advanced.py)
- Diagnostics and project:
  - [topic07_prompt_eval_regression.py](src/stage-5/topic07_prompt_eval_regression.py)
  - [topic08_project_baseline.py](src/stage-5/topic08_project_baseline.py)
- Step-by-step multi-head-attention mini-LLM lab:
  - [lab01_simple_mha_llm.py](src/stage-5/lab01_simple_mha_llm.py)

Expected output style per script:

- print data/schema declaration
- print key metrics
- print short interpretation text
- include very detailed and clear comments for every workflow block (data, preprocessing, model, training, evaluation, outputs)

### Detailed Comment Standard (Mandatory)

All Stage 5 example code should follow this comment style:

1. Add a top-of-file header explaining:
   - what the script teaches
   - data source and structure
   - expected outputs
2. Add `# Workflow:` comments before each major stage.
3. Add functional comments above non-trivial logic:
   - what the block does
   - why this step is needed
   - what can fail if skipped
4. Add output interpretation comments near printed metrics.
5. Keep comments explicit and beginner-readable; avoid vague comments like `# process data`.

---

## Example Code Matrix (Key LLM Concepts)

Use this map when you want runnable code for each core concept in this chapter.

| Concept | Best Stage 5 script(s) | Complexity focus |
|---|---|---|
| PyTorch and CUDA workflow | `topic00a` -> `topic00` -> `topic00c` | from device checks to mixed-precision GPU training |
| Tokenization and token budget | `topic01a` -> `topic01` -> `topic01c` | from token splitting basics to practical token analysis |
| Prompt engineering | `topic02a` -> `topic02` -> `topic02c` | from clear instruction writing to controlled prompt variants |
| Structured output | `topic03a` -> `topic03` -> `topic03c` | from fixed JSON shape to stronger validation/failure handling |
| RAG workflow | `topic04a` -> `topic04` -> `topic04c` | from retrieval intuition to diagnostic checks |
| Embeddings and semantic retrieval | `topic05a` -> `topic05` -> `topic05c` | from vector basics to retrieval metrics (`hit@k`) |
| Multi-head attention mechanism | `topic01_multihead_attention.py` | shape flow, Q/K/V mapping, head behavior |
| End-to-end mini LLM with MHA | `lab01_simple_mha_llm.py` | full data -> model -> training -> generation workflow |
| Prompt evaluation and regression | `topic07_prompt_eval_regression.py` | compare prompt versions on fixed evaluation set |
| Operatable project baseline | `topic08_project_baseline.py` | fixed deliverables and before/after comparison |

### Best External Teaching Examples (Curated)

These are high-value references for students who need more explanation depth:

- Annotated Transformer (line-by-line implementation):
  - https://nlp.seas.harvard.edu/2018/04/03/attention.html
- Illustrated Transformer (visual intuition):
  - https://jalammar.github.io/illustrated-transformer/
- PyTorch `nn.MultiheadAttention` docs:
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
- PyTorch transformer language-model tutorial:
  - https://docs.pytorch.org/tutorials/beginner/transformer_tutorial.html
- Hugging Face LLM course (train a causal LM from scratch):
  - https://huggingface.co/learn/llm-course/chapter7/6?fw=pt
- OpenAI prompt engineering guide:
  - https://platform.openai.com/docs/guides/prompt-engineering
- OpenAI structured outputs guide:
  - https://platform.openai.com/docs/guides/structured-outputs
- Popular educational repos:
  - https://github.com/karpathy/nanoGPT
  - https://github.com/karpathy/minGPT
  - https://github.com/rasbt/LLMs-from-scratch

---

## Step-by-Step Lab: Build a Simple Multi-Head-Attention LLM

Lab script: [lab01_simple_mha_llm.py](src/stage-5/lab01_simple_mha_llm.py)

### Lab Goal

Build and run a tiny decoder-only language model that uses multi-head attention for next-token prediction.

### Lab Environment

From `red-book/src/stage-5`:

```powershell
pip install -r requirements.txt
python .\lab01_simple_mha_llm.py
```

### Lab Workflow (Operatable)

1. Fix task and data: use the in-script corpus and do not change corpus during baseline run.
2. Read inline script comments first; use them as operation guide for each stage.
3. Confirm data declaration printed by script:
   - source
   - record count
   - vocab size
   - input/output schema
   - fixed split policy
4. Confirm tokenizer stage:
   - character vocabulary is built
   - text is encoded into token IDs
5. Confirm dataset stage:
   - sliding windows are created for `x_ids` and `y_ids`
   - fixed 90/10 train/validation split is applied
6. Confirm model stage:
   - token embedding + positional embedding
   - stacked decoder blocks
   - each block has masked `nn.MultiheadAttention`
   - feed-forward + residual + layer norm
7. Record baseline metrics before training:
   - `baseline_val_loss`
   - `baseline_val_perplexity`
8. Train model with fixed settings:
   - optimizer: AdamW
   - gradient clipping
   - periodic train/validation loss logging
9. Record final metrics:
   - `final_val_loss`
   - `final_val_perplexity`
10. Generate sample text from prompt `"multi-head attention "`.
11. Write one short interpretation:
   - whether loss decreased
   - whether generated text shows corpus pattern learning
   - one failure pattern you observed

### Required Lab Deliverables

- console log with baseline and final metrics
- one generated sample output
- short notes:
  - model config used
  - metric delta (`baseline -> final`)
  - one improvement idea (for example: more data, larger model, more steps)

### Where Complexity Is In This Lab

- Simple part: data preparation and vocabulary creation.
- Intermediate part: masked multi-head attention tensor flow.
- Advanced part: stable training behavior and generation quality interpretation.

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
12. What is multi-head attention?
13. Why are multiple heads useful compared with one head?
14. What is the difference between self-attention, multi-head attention, and transformer?
15. Why is positional information needed?
16. What is causal masking?
17. What is prompt engineering?
18. Why do small wording changes affect LLM output?
19. What is zero-shot prompting?
20. What is few-shot prompting?
21. Why is structured output important?
22. Why should JSON output still be validated?
23. What is hallucination?
24. Why can an LLM hallucinate even when it sounds confident?
25. What is temperature or sampling randomness in generation?
26. Why is an LLM not a truth engine?
27. What is RAG?
28. Why does RAG help factual tasks?
29. What is chunking in RAG?
30. Why can bad chunking hurt retrieval?
31. What is fine-tuning?
32. When should you try prompting/RAG before fine-tuning?
33. What is the main lesson of this stage?

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

**12. What is multi-head attention?**
It runs multiple attention heads in parallel on different learned projections of queries, keys, and values, then concatenates and projects their outputs.

**13. Why are multiple heads useful compared with one head?**
Because different heads can capture different dependency patterns or representation subspaces at the same time.

**14. What is the difference between self-attention, multi-head attention, and transformer?**
Self-attention is one attention mechanism, multi-head attention is multiple attention mechanisms in parallel, and Transformer is the full architecture that uses multi-head attention plus other components.

**15. Why is positional information needed?**
Because attention alone does not inherently know token order.

**16. What is causal masking?**
It prevents a token from attending to future tokens during next-token prediction.

**17. What is prompt engineering?**
Prompt engineering is designing instructions and examples to guide LLM behavior more reliably.

**18. Why do small wording changes affect LLM output?**
Because the model is sensitive to framing, specificity, examples, and context structure.

**19. What is zero-shot prompting?**
It is asking the model to perform a task without giving examples.

**20. What is few-shot prompting?**
It is giving a small number of examples so the model can imitate the desired pattern.

**21. Why is structured output important?**
Because software systems need predictable, parseable output formats.

**22. Why should JSON output still be validated?**
Because the model can produce malformed, incomplete, or semantically wrong JSON even if it looks correct.

**23. What is hallucination?**
Hallucination is when the model generates false, unsupported, or invented content.

**24. Why can an LLM hallucinate even when it sounds confident?**
Because fluency comes from pattern generation, not built-in fact verification.

**25. What is temperature or sampling randomness in generation?**
It controls how deterministic or diverse the generated output is.

**26. Why is an LLM not a truth engine?**
Because its core objective is next-token prediction, not guaranteed factual correctness.

**27. What is RAG?**
RAG stands for Retrieval-Augmented Generation: retrieve relevant documents first, then use them as context for the LLM.

**28. Why does RAG help factual tasks?**
Because it grounds the model in external documents instead of relying only on internal model memory.

**29. What is chunking in RAG?**
Chunking is splitting documents into smaller retrievable pieces.

**30. Why can bad chunking hurt retrieval?**
Because relevant information may be split poorly, mixed with noise, or made harder to retrieve accurately.

**31. What is fine-tuning?**
Fine-tuning is further training a model on task-specific examples to adapt its behavior.

**32. When should you try prompting/RAG before fine-tuning?**
When better instructions, structure, grounding, and validation may solve the problem more cheaply and safely.

**33. What is the main lesson of this stage?**
LLMs are powerful language models, but reliable systems require prompting, grounding, validation, and careful workflow design rather than blind trust.

---

## What You Must Be Able To Do After Stage 5

- [ ] Explain what a token is and why tokenization matters
- [ ] Explain what embeddings are and why they are useful
- [ ] Explain self-attention, multi-head attention, and how they fit inside transformers
- [ ] Explain how PyTorch and CUDA work together in LLM training workflows
- [ ] Design clearer prompts for better outputs
- [ ] Distinguish zero-shot and few-shot prompting
- [ ] Request and validate structured outputs
- [ ] Explain why LLMs hallucinate
- [ ] Explain what RAG is and why it helps
- [ ] Understand when prompting, retrieval, rules, or fine-tuning are appropriate
- [ ] Treat LLMs as powerful but fallible components in larger systems

