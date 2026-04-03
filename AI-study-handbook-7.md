# Stage 7 — RAG Systems

*(Week 13–14)*

## Goal

Understand Retrieval-Augmented Generation (RAG), the foundation of most real-world AI applications.

You are learning:

- how to combine an LLM with a knowledge base
- how retrieval works
- how to ground LLM outputs with real data

This stage is where you move from:

> "I can ask an LLM questions"

to:

> "I can build a system that retrieves relevant knowledge first, then generates answers grounded in actual documents."

---

## Quick Summary

**RAG = LLM + External Knowledge**

```
user query
↓
retrieve relevant knowledge
↓
construct grounded prompt
↓
LLM generates answer
↓
return answer + citations
```

A beginner should finish this stage understanding:

- why RAG is needed
- what chunking is
- what embeddings do
- what a vector database is
- how retrieval works
- why retrieval quality often matters more than generation quality
- how to build grounded prompts
- how to debug RAG failures systematically

### Tools

- LangChain
- LlamaIndex
- FAISS
- ChromaDB

---

## Study Materials

**LangChain Docs**
https://python.langchain.com/docs/

**LlamaIndex Docs**
https://docs.llamaindex.ai/

---

## Key Knowledge (Deep Understanding)

### 1. Why RAG is Needed

LLMs have limitations:

- outdated knowledge
- hallucination
- no access to private data

RAG solves this by **retrieving relevant information before generating an answer**.

#### Beginner Explanation

An LLM by itself answers from what it learned during training. That means it may:

- not know recent updates
- not know your private company documents
- produce answers that sound correct but are unsupported

RAG helps by giving the LLM actual source material at answer time.

#### Simple Mental Model

```
Without RAG:  question → LLM memory → answer

With RAG:     question → retrieve relevant docs → LLM reads docs → grounded answer
```

#### When RAG is Useful

RAG is especially useful when:

- knowledge changes often
- you need answers from private data
- citations matter
- factual grounding matters
- you want enterprise Q&A
- you want document-based assistants

#### Important Algorithms / Mechanisms

**A. Retrieval-Augmented Generation Loop** — The core system pattern.

How it works:

1. User asks a question
2. System searches knowledge base
3. Top relevant chunks are retrieved
4. Retrieved text is sent to the LLM
5. LLM answers from the retrieved context

*Why important: This is the main architecture of modern grounded AI systems.*

---

**B. Grounded Generation** — Generation constrained by retrieved context.

*How it works: The prompt instructs the LLM to answer based on the provided documents.*

*Why important: This reduces unsupported guessing.*

---

**C. External Knowledge Injection** — Instead of depending only on model weights, inject current knowledge into the prompt.

*Why important: This makes systems more updatable and useful for private knowledge bases.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Improves factual grounding | Retrieval can fail |
| Gives access to private documents | Bad chunking can ruin answer quality |
| Avoids retraining for every knowledge update | Generated answer can still hallucinate |
| Supports citations and source traceability | More moving parts than prompt-only systems |

---

### 2. Core Components of RAG

| Component | Role |
|---|---|
| **Document Store** | Raw knowledge (PDFs, text, DB) |
| **Chunking** | Split documents into smaller pieces |
| **Embeddings** | Convert text → vector |
| **Vector Database** | Store and search embeddings |
| **Retriever** | Find most relevant chunks |
| **LLM** | Generate final answer using retrieved data |

#### Beginner Explanation

A RAG system is not "just one model." It is a **pipeline made of multiple parts**.

Each part has a job:

- Document store keeps raw knowledge
- Chunking splits long text into searchable units
- Embeddings turn text into vectors
- Vector database stores those vectors
- Retriever finds relevant chunks
- LLM writes the final answer

> If any one of these steps is weak, the whole system can fail.

#### Step-by-Step Mental Model

1. **Collect knowledge** — Gather files: PDFs, notes, policy docs, reports, product docs, database text exports.
2. **Extract text** — Convert files into clean text segments with metadata.
3. **Chunk text** — Break documents into smaller pieces that can be retrieved well.
4. **Embed chunks** — Turn each chunk into a vector representation.
5. **Store vectors** — Save chunk vectors in a vector database.
6. **Embed user query** — Turn the question into a vector too.
7. **Retrieve relevant chunks** — Find chunks most similar to the query.
8. **Build prompt** — Put retrieved chunks plus question into a grounded prompt.
9. **Generate answer** — Ask the LLM to answer from the provided context.

#### Important Algorithms / Mechanisms

**A. ETL-Style Ingestion Pipeline** — Document processing is similar to data engineering.

How it works: extract text → transform into chunks → load into vector store.

*Why important: RAG quality starts with clean ingestion, not just the retriever.*

---

**B. Embedding Indexing** — Every chunk is embedded and indexed for later search.

*Why important: Without indexing, scalable semantic retrieval is not possible.*

---

**C. Similarity Search** — The system compares query vector to chunk vectors.

*Why important: This is how semantically relevant chunks are found.*

---

**D. Prompt Assembly** — Retrieved chunks are formatted into the final LLM input.

*Why important: Even good retrieval can fail if context is injected poorly.*

---

### 3. Chunking (Critical)

| Chunk Size | Problem |
|---|---|
| Too large | Irrelevant info, noisy prompt |
| Too small | Missing context, incomplete answers |
| Just right | Meaningful unit — small but complete |

#### Beginner Explanation

Chunking is one of the most important parts of RAG.

A long document cannot be embedded and retrieved as one giant block, so you split it into smaller pieces called chunks.

The chunk must be:

- small enough to retrieve precisely
- large enough to preserve meaning

That balance is critical.

#### Why Chunking Is So Important

**If chunk is too big:**

- retrieval may bring too much irrelevant information
- prompt becomes noisy
- answer quality drops

**If chunk is too small:**

- meaning gets broken apart
- important context is lost
- answer becomes incomplete

> Chunking controls retrieval quality more than many beginners expect.

#### Step-by-Step Chunking Logic

1. **Start with raw extracted text** — Maybe a PDF page, note section, or document body.
2. **Decide chunking strategy** — fixed-size, paragraph-based, section-based, or sentence-window.
3. **Decide overlap** — Overlap helps preserve continuity across chunk boundaries.
4. **Attach metadata** — Save file name, page, section, chunk ID.
5. **Inspect actual chunks** — Always read samples to see whether they are meaningful.

#### Important Algorithms / Mechanisms

**A. Fixed-Size Chunking** — Split text by fixed character or token length.

```
chunk size = 500–800 characters
overlap    = 50–100 characters
```

*Why important: Simple baseline and easy to implement.*

---

**B. Sliding Window Chunking** — Chunks overlap so neighboring chunks share some content.

*Why important: Prevents important context from being lost at boundaries.*

---

**C. Semantic / Structure-Aware Chunking** — Split by headings, paragraphs, sections, or logical topic changes.

*Why important: Usually better than blind splitting when document structure is meaningful.*

---

**D. Token-Based Chunking** — Split by token count instead of character count.

*Why important: More aligned with model limits and embedding behavior.*

#### Strengths and Weaknesses

| Good Chunking | Bad Chunking |
|---|---|
| Better retrieval precision | Missing answer pieces |
| Better context completeness | Retrieving irrelevant text |
| Better citation quality | Incomplete citations |
| Lower prompt noise | Poor answer quality even with a good LLM |

---

### 4. Embeddings

Embedding maps text → vector space.

**Key idea:** Similar meaning → close vectors.

#### Beginner Explanation

Embeddings turn text into numbers that preserve semantic similarity.

- A chunk of text becomes a vector.
- A user question also becomes a vector.
- If the vectors are close together, the system assumes the chunk is relevant.

That is the foundation of semantic retrieval.

#### Simple Mental Model

Stored chunks:

```
"Reset your company password using the portal"
"Vacation policy for contractors"
"Stock price trend summary for NVDA"
```

If the user asks: *"How do I change my password?"*

The password-related chunk should be closer in embedding space than the vacation or stock chunk.

#### Important Algorithms / Mechanisms

**A. Dense Vector Representation** — Each chunk becomes a dense list of numbers.

*Why important: This allows semantic similarity search, not just keyword matching.*

---

**B. Embedding Model Inference** — An embedding model converts text into vectors.

*How it works: Text is passed through a trained model that produces a numeric representation.*

*Why important: The embedding model strongly affects retrieval quality.*

---

**C. Cosine Similarity** — A common way to compare embeddings.

*How it works: Measures the angle between two vectors.*

*Why important: Useful for judging semantic closeness.*

---

**D. Nearest Neighbor Search** — Find stored chunk vectors closest to the query vector.

*Why important: This is the retrieval step used in many vector databases.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Captures meaning better than exact keyword match | Not perfect for exact factual matching |
| Works well for semantic search | Can retrieve semantically similar but wrong chunks |
| Foundation of modern RAG systems | Depends strongly on embedding model and chunk quality |

---

### 5. Retrieval

Retrieve **top-k** relevant chunks.

> **Important: Retrieval quality determines answer quality.**

#### Beginner Explanation

Retrieval decides which chunks the LLM gets to read.

> If retrieval is bad, the answer will be bad.

Even a powerful LLM cannot answer correctly if it sees the wrong context. Retrieval is one of the **highest-leverage** parts of a RAG system.

#### Step-by-Step Retrieval Flow

1. **User asks a question** — e.g. "What is the contractor access policy?"
2. **Convert question to embedding** — The same embedding method used for chunks is used for the query.
3. **Compare query to stored vectors** — The retriever searches for similar chunks.
4. **Return top-k chunks** — Maybe top 3, top 5, or top 10.
5. **Pass them to prompt construction** — Now the LLM can use them.

#### Important Algorithms / Mechanisms

**A. Top-K Retrieval** — Return the k most similar chunks.

*Why important: Simple baseline retrieval strategy.*

---

**B. Similarity Search** — Search based on vector similarity.

*Why important: Core engine of semantic retrieval.*

---

**C. Metadata Filtering** — Restrict search by metadata (document type, department, date range).

*Why important: Can drastically improve retrieval precision.*

---

**D. Hybrid Retrieval** — Combine vector search with keyword or lexical search.

*Why important: Helps when exact phrases, IDs, names, or specific terminology matter.*

---

**E. Re-Ranking** — After initial retrieval, score candidates again with a stronger relevance model.

*Why important: Often improves final retrieval quality.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Semantic search can find relevant chunks beyond exact keywords | Top-k may still miss the best chunk |
| Flexible for natural-language queries | Irrelevant chunks may rank highly |
| Supports scalable knowledge access | Retrieval failure is often silent unless inspected |

---

### 6. Prompt Construction

LLM prompt includes retrieved context and user question.

```
Answer based only on context:
{documents}

Question: {query}
```

#### Beginner Explanation

After retrieval, the system must decide how to present the chunks to the LLM.

Good prompt construction helps the model:

- focus on evidence
- avoid guessing
- use the provided context correctly
- cite sources
- refuse when evidence is missing

> Bad prompt construction can waste good retrieval.

#### Step-by-Step Prompt Construction Logic

1. **Gather top retrieved chunks** — These are your evidence candidates.
2. **Format them clearly** — Include chunk text, source, and page/section if available.
3. **Add system instructions** — Tell the model: answer only from context, cite sources, say "unknown" if context is insufficient.
4. **Add the user question** — Put the user question after the context.
5. **Keep prompt concise** — Too much context can dilute relevance.

#### Important Algorithms / Mechanisms

**A. Context Injection** — Insert retrieved chunks into the prompt.

*Why important: The LLM can only use retrieved information if it is actually included well.*

---

**B. Instruction Grounding** — Explicitly tell the model to answer only from the provided context.

*Why important: Reduces unsupported answers.*

---

**C. Citation Formatting** — Attach source identifiers to chunks.

*Why important: Makes answers traceable and verifiable.*

---

**D. Context Ordering** — Place the most relevant chunks first when possible.

*Why important: Order can influence what the model focuses on.*

#### Good Prompt Design Rules

- Keep retrieved context organized
- Label sources clearly
- Tell the model what to do when evidence is missing
- Do not overload the prompt with irrelevant chunks

---

### 7. Grounding

Ensure the answer is based on retrieved content.

**Avoid:** hallucination and guessing.

#### Beginner Explanation

Grounding means the answer should come from **actual retrieved evidence**, not unsupported model invention.

A grounded answer is more trustworthy because it is tied to a document, a page, a chunk, or a traceable source.

#### What Grounding Looks Like

| Grounded Answer | Ungrounded Answer |
|---|---|
| Cites relevant chunks | Adds facts not in the retrieved context |
| Stays within evidence | Guesses details |
| Says "not found" when needed | Invents citations |
| | Mixes evidence with unsupported claims |

#### Important Algorithms / Mechanisms

**A. Evidence-Constrained Answering** — The model is instructed to answer only from retrieved evidence.

*Why important: This is the core behavior RAG is trying to achieve.*

---

**B. Citation-Based Grounding** — The answer references source metadata.

*Why important: Supports trust and verification.*

---

**C. Abstention / Refusal Logic** — If evidence is insufficient, the model should say so.

*Why important: A safe RAG system must handle unknowns well.*

---

**D. Grounded Answer Evaluation** — Check whether answer claims are actually supported by retrieved text.

*Why important: Retrieval success alone is not enough; the final answer must also be evidence-aligned.*

---

## Difficulty Points

### 1. Bad chunking

**Why it happens:** Beginners often use arbitrary chunk sizes without reading the actual chunks.

**Why it is a problem:** Important meaning gets split badly, or chunks become too broad and noisy.

**Fix strategy:** Inspect chunk samples manually, test several chunk sizes, use overlap, prefer logical boundaries when possible.

### 2. Poor retrieval

**Why it happens:** The embedding model, chunk quality, metadata setup, or search strategy may be weak.

**Why it is a problem:** The LLM receives irrelevant or incomplete evidence.

**Fix strategy:** Inspect top retrieved chunks, test different embedding models, try hybrid retrieval, add metadata filters, use re-ranking if needed.

### 3. Not inspecting retrieved data

**Why it happens:** People focus on the final answer only.

**Why it is a problem:** They blame the LLM when the real issue is retrieval.

**Fix strategy:** Always inspect retrieved chunk text, source metadata, ranking order, and relevance to the query.

### 4. Blaming LLM

**Why it happens:** The final answer is what users see, so it feels like the generation model must be the problem.

**Why it is a problem:** You waste time changing prompts or models while the retriever is broken.

**Fix strategy:** Debug in order:

1. document ingestion
2. chunking
3. embeddings
4. retrieval
5. prompt construction
6. final generation

### 5. Ignoring metadata

**Why it happens:** Beginners focus on text only.

**Why it is a problem:** Without metadata, citations are weak, debugging is harder, filtering becomes harder, and traceability is poor.

**Fix strategy:** Always attach metadata — file name, page number, section, chunk ID, source type.

### 6. Retrieving too many chunks

**Why it happens:** It feels safer to send more context.

**Why it is a problem:** Too much context can add noise, dilute the relevant answer, increase latency and cost, and confuse the model.

**Fix strategy:** Start with a small top-k and test quality before increasing.

### 7. No handling for unknown answers

**Why it happens:** People want the assistant to always respond confidently.

**Why it is a problem:** The model may invent unsupported answers when evidence is weak.

**Fix strategy:** Add instructions and logic for "not found in provided documents," "insufficient evidence," and clarification requests if needed.

---

## RAG Workflow (Real World)

1. Collect documents
2. Extract text
3. Clean and normalize text
4. Chunk documents
5. Attach metadata
6. Create embeddings
7. Store in vector database
8. Build retriever
9. Retrieve top-k chunks
10. Construct grounded prompt
11. Generate answer
12. Add citations
13. Evaluate retrieval quality
14. Evaluate answer grounding
15. Improve chunking / retrieval / prompting

### Beginner Explanation of Each Step

1. **Collect documents** — Gather raw knowledge sources.
2. **Extract text** — Convert files into usable text.
3. **Clean and normalize text** — Remove broken formatting and normalize whitespace if needed.
4. **Chunk documents** — Create retrievable units.
5. **Attach metadata** — Save source info for traceability.
6. **Create embeddings** — Convert chunks into vectors.
7. **Store in vector database** — Make chunk search scalable.
8. **Build retriever** — Define how the system searches.
9. **Retrieve top-k chunks** — Select evidence for the question.
10. **Construct grounded prompt** — Format evidence for the LLM.
11. **Generate answer** — Use the LLM to produce the response.
12. **Add citations** — Show where the answer came from.
13. **Evaluate retrieval quality** — Check whether the right chunks were found.
14. **Evaluate answer grounding** — Check whether the answer matches the evidence.
15. **Improve chunking / retrieval / prompting** — Tune the pipeline iteratively.

---

## Debugging Checklist for Stage 7

If the RAG system gives poor answers, check:

- [ ] Was text extraction correct?
- [ ] Are chunks meaningful when read by humans?
- [ ] Is metadata attached properly?
- [ ] Are embeddings generated correctly?
- [ ] Are retrieved chunks actually relevant?
- [ ] Is top-k too low or too high?
- [ ] Is prompt construction clear and grounded?
- [ ] Is the model instructed not to guess?
- [ ] Are citations linked to the correct chunks?
- [ ] Is the answer supported by retrieved evidence?
- [ ] Would hybrid retrieval help?
- [ ] Is the problem retrieval, prompt, or generation?

---

## Example Code (Conceptual)

```python
from langchain.vectorstores import FAISS
```

**Beginner Explanation:**

This line imports a vector store implementation. A vector store is where chunk embeddings are stored so the system can search them later.

> Using a vector store library does **not** automatically create a good RAG system.

Good RAG still depends on:

- good document extraction
- good chunking
- good embedding choice
- good retrieval tuning
- good prompt grounding
- good evaluation

> The library is only infrastructure. The real quality comes from the full pipeline design.

---

## Practice Project

### Project: AI PDF Q&A System

**Goal:** Build a system that uploads documents, answers questions, and cites sources.

You are not only trying to make a chatbot. You are learning:

- ingestion
- chunking
- retrieval
- grounding
- citation design
- systematic debugging

**Step 1 — Collect Documents**

Use PDFs or text files. Save to `data/raw/`.

*Why this step matters: You need a real document corpus to build the knowledge base.*

*Start small: 3 to 10 documents, clearly different topics, documents you can read manually. This makes debugging easier.*

---

**Step 2 — Extract Text**

Store: file, page, text.

*Why this step matters: RAG works on text, not raw PDF files.*

*When you extract text, preserve source mapping — file name, page number, text content. That mapping is critical for citations later.*

---

**Step 3 — Chunk Text**

Split into 500–800 characters with 50–100 overlap.

*Why this step matters: The system needs pieces small enough to retrieve, but large enough to keep meaning.*

After chunking, print sample chunks and ask:

- does this chunk make sense by itself?
- is it too long?
- is it cut awkwardly?
- is overlap enough?

---

**Step 4 — Create Embeddings**

Convert chunks → vectors.

*Why this step matters: This is how the system makes chunks searchable by meaning.*

Each chunk gets turned into a vector by an embedding model. Later, user questions get embedded the same way. Then the system can compare them.

---

**Step 5 — Store in Vector DB**

Use FAISS or ChromaDB.

*Why this step matters: The vector DB lets you search efficiently over many chunk embeddings. Without a vector store, semantic retrieval becomes slow and messy as the corpus grows.*

---

**Step 6 — Build Retrieval**

```
Query → embedding → search top-k chunks
```

*Why this step matters: The retriever is often the most important quality bottleneck in RAG. If you retrieve the wrong chunks, the LLM cannot fix that reliably.*

---

**Step 7 — Build Prompt**

```
Use only the context below to answer the question.
If the answer is not in the context, say you do not have enough information.
For every important claim, cite the source.

Context:
{chunks}

Question:
{query}
```

*Why this step matters: The model needs clear instructions on how to use the retrieved text.*

---

**Step 8 — Generate Answer**

Use the LLM.

*Why this step matters: The LLM is doing language synthesis here — RAG is retrieval **plus** generation, not just search.*

---

**Step 9 — Add Citations**

Return: answer, source document, page.

*Why this step matters: Citations make the system inspectable and more trustworthy. Return exact source links or metadata — not just "based on documents."*

---

**Step 10 — Test**

Test: direct question, multi-chunk question, unknown question.

Also test:

- exact-term question
- paraphrased question
- ambiguous question
- question with no answer in corpus
- question where answer spans multiple chunks
- misleading query that could trigger wrong retrieval

### Deliverables

- document dataset
- chunk file
- vector DB
- Q&A system
- outputs with citations
- README

### Experiment Tasks

**Experiment 1 — Chunk size comparison**

Try: 300 chars, 600 chars, 1000 chars.

- Purpose: See how chunk size changes retrieval quality.
- Lesson: Chunking is one of the most important RAG design decisions.

**Experiment 2 — Overlap comparison**

Try: no overlap, small overlap, larger overlap.

- Purpose: See how overlap affects boundary context.
- Lesson: Overlap can preserve meaning, but too much overlap adds redundancy.

**Experiment 3 — Top-k comparison**

Try: k=2, k=4, k=8.

- Purpose: See how too little vs too much context changes results.
- Lesson: More retrieved chunks are not always better.

**Experiment 4 — Prompt-only vs RAG**

Ask the same factual questions directly to LLM and through your RAG system.

- Purpose: Observe grounding improvements.
- Lesson: RAG often improves reliability when knowledge must come from documents.

**Experiment 5 — Metadata filtering**

Restrict retrieval to one file or document type.

- Purpose: See whether retrieval gets more precise.
- Lesson: Metadata is a quality tool, not just bookkeeping.

**Experiment 6 — Unknown-answer behavior**

Ask questions not covered by the document set.

- Purpose: Test whether the system refuses unsupported answers properly.
- Lesson: A good RAG system should handle "I don't know from provided context."

**Experiment 7 — Retrieval inspection notebook**

For each test query, print top chunks, scores, sources, and final answer.

- Purpose: Build debugging habit.
- Lesson: You must inspect retrieval, not only final generation.

### Common Mistakes

1. **Chunk too big or too small** — Retrieval becomes noisy or incomplete. *Fix: Test multiple chunk sizes and read chunk samples manually.*

2. **Not checking retrieved chunks** — You miss the real source of failure. *Fix: Always print and inspect top retrieved chunks during development.*

3. **No citations** — Users cannot verify answers, and debugging becomes much harder. *Fix: Always attach source metadata and expose citations.*

4. **Trusting LLM blindly** — The model may still hallucinate or over-generalize beyond retrieved evidence. *Fix: Treat the LLM as the answer writer, not the truth source.*

5. **Ignoring metadata** — Source tracing, filtering, and debugging become weak. *Fix: Store source metadata from the beginning.*

6. **Sending too much context** — Noise increases and relevance decreases. *Fix: Keep retrieved context focused and test top-k carefully.*

7. **No evaluation set** — You cannot measure whether changes improve the system. *Fix: Create a small benchmark set of questions with expected source coverage.*

---

## Final Understanding

> RAG improves LLM reliability by retrieving relevant knowledge and grounding the answer in real data.

> In most RAG systems, failures come from ingestion, chunking, embeddings, retrieval, or prompt construction **before** they come from the LLM itself.

---

## Self Test

### Questions

1. What does RAG stand for?
2. Why is RAG needed if LLMs are already powerful?
3. What are the main limitations of LLMs that RAG helps with?
4. What is a document store in RAG?
5. Why do we chunk documents?
6. What makes a good chunk?
7. Why can chunking be one of the most important parts of RAG quality?
8. What is an embedding in a RAG system?
9. Why do similar texts tend to retrieve each other in vector search?
10. What is a vector database used for?
11. What does a retriever do?
12. Why does retrieval quality often determine answer quality?
13. What is top-k retrieval?
14. Why can retrieving too many chunks be harmful?
15. What is metadata in a RAG pipeline?
16. Why is metadata useful?
17. What is prompt construction in RAG?
18. Why should the prompt tell the LLM to answer only from context?
19. What does grounding mean?
20. Why can a grounded system still fail?
21. Why should you inspect retrieved chunks manually?
22. What is overlap in chunking?
23. Why can overlap help?
24. What is hybrid retrieval?
25. What is re-ranking?
26. Why are citations important in RAG?
27. What should the system do when the answer is not found in the documents?
28. Why should you test unknown questions?
29. What is a common mistake beginners make when debugging RAG?
30. What is the main lesson of this stage?

### Answers

1. RAG stands for Retrieval-Augmented Generation.

2. Because LLMs may have outdated knowledge, no access to private documents, and can hallucinate unsupported answers.

3. Outdated information, lack of private knowledge access, and ungrounded hallucination.

4. It is the raw knowledge source, such as PDFs, text files, notes, or database text.

5. Because long documents must be broken into smaller retrievable pieces for embedding and search.

6. A good chunk is small enough to retrieve precisely but large enough to preserve meaningful context.

7. Because bad chunking can destroy meaning, weaken retrieval precision, and make good answers impossible even with a strong LLM.

8. It is a vector representation of text used for semantic similarity search.

9. Because semantically similar texts often have nearby vectors in embedding space.

10. It stores embeddings and supports efficient similarity search over them.

11. It finds the chunks most relevant to the user query.

12. Because the LLM can only answer well if it sees relevant and sufficient evidence.

13. It is a retrieval method that returns the k most relevant chunks.

14. Because it can add irrelevant context, increase noise, and confuse the model.

15. Metadata is source information attached to chunks, such as file name, page number, section, or chunk ID.

16. It improves traceability, filtering, citations, and debugging.

17. It is the process of formatting retrieved chunks and the user question into the final LLM prompt.

18. Because it helps reduce guessing and keeps the answer grounded in retrieved evidence.

19. Grounding means the answer is based on actual retrieved source material rather than unsupported model invention.

20. Because retrieval may miss the right evidence, chunks may be incomplete, or the model may still over-generalize or misread context.

21. Because many RAG failures are retrieval failures, and you cannot diagnose them by looking only at the final answer.

22. Overlap means adjacent chunks share some text content.

23. Because it preserves context across chunk boundaries and reduces the chance of splitting important information awkwardly.

24. Hybrid retrieval combines vector similarity with keyword or lexical search.

25. Re-ranking is a second-stage process that reorders retrieved candidates using a stronger relevance model.

26. Because they let users verify the answer and help developers debug source grounding.

27. It should say that the answer is not available in the provided context instead of guessing.

28. Because a good RAG system must handle missing evidence safely, not just answer known questions.

29. They blame the LLM first instead of checking chunking, retrieval, metadata, and prompt grounding.

30. RAG is not just "LLM plus search." It is a full pipeline where document quality, chunking, embeddings, retrieval, prompt construction, and grounding all determine reliability.

---

## What You Must Be Able To Do After Stage 7

- [ ] Explain what RAG is in plain English
- [ ] Explain why RAG is needed for real-world AI systems
- [ ] Describe the full RAG pipeline from documents to answer
- [ ] Explain chunking, embeddings, vector databases, retrievers, and grounding
- [ ] Understand why retrieval quality often matters more than model quality
- [ ] Build a small document Q&A system with citations
- [ ] Inspect retrieved chunks and debug retrieval quality
- [ ] Understand metadata, top-k tuning, and chunk overlap
- [ ] Design prompts that make the model answer from context only
- [ ] Understand that RAG engineering is a pipeline problem, not just a prompting problem
