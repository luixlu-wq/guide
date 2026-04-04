# Stage 5 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-5.md`  
Plan owner: You + Codex  
Version date: 2026-04-03

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-5.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Chapter 5 is concept-heavy and can be hard for beginners; collect strong resources and design the best practical improvement path.
- Add detailed explanation and demonstration for key LLM concepts.
- Add clearer instructions for learning targets.
- Add detailed tutorials for key topics.
- Add examples for each learning topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare data source and data structure used in all examples.
- Include high-quality resources (official docs, books, papers, practical repos).
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.

Carry-over quality requirements from Stage 3 and Stage 4 (apply to Stage 5):

- Add more example code for each topic, from simple to complicated.
- Add clear functional comments to all Stage 5 topic scripts.
- Add and enforce `Example Complexity Scale (Used In All Modules)` and explicit `where complexity is` explanation per topic.
- Make practice project section clear and operatable with exact workflow and deliverables.
- Add strict debugging checklist and quality gates.
- Keep links and references maintainable (verification date + replacement policy).

Stage-5-specific locked requirements:

- Prompting content must be operational, not generic.
- Structured output section must include schema validation and failure handling.
- Hallucination section must include grounding and verification workflow.
- RAG section must include chunking, retrieval quality checks, and answer-grounding checks.
- LLM workflow must include evaluation methodology, not one-off examples.
- Add dedicated content for multi-head attention as a formal chapter topic.
- Multi-head attention content must include detailed tutorial-style explanation so students can deeply understand it.
- Multi-head attention section must explicitly guide students to distinguish:
  - self-attention
  - multi-head attention
  - transformer architecture scope
- Include best-available learning resources for this topic (paper + official docs + implementation references).
- Many core LLM concepts in Chapter 5 still need more runnable examples; add best-teaching examples for each key concept (from official docs, tutorials, books, papers, and popular GitHub repos).
- Add a step-by-step lab operation to build a simple multi-head-attention LLM, with complete data, model, training loop, evaluation, and expected outputs.
- The step-by-step lab must be executable from `red-book/src/stage-5` without copy-paste editing.
- Add dedicated PyTorch and CUDA content in Chapter 5:
  - conceptual explanation (what PyTorch does, what CUDA does)
  - operational usage in LLM training/inference workflows
  - device management and CPU/GPU execution checks
  - runnable examples that print selected device and training behavior
  - simple/intermediate/advanced PyTorch/CUDA example ladder in `red-book/src/stage-5`
- Reviewer-additive requirement: add a dedicated `Transformer Architecture` module with explicit Q/K/V contract and troubleshooting patterns.
- Reviewer-additive requirement: add a dedicated `Tokenization & Embeddings` module with complete encoding pipeline and failure diagnostics.
- Reviewer-additive requirement: add section-focused runnable suites for:
  - manual attention math
  - minimal decoder-only GPT training
  - performance/distributed transformer path
  - tokenizer visualization
  - embedding similarity search
  - domain tokenizer training
- Reviewer-additive requirement: include an LLM hardware configuration subsection for BF16/FP16 selection and Flash-Attention-style SDP kernel guidance.
- Reviewer-additive requirement: include explicit failure labs for:
  - causal masking leakage
  - context-window memory pressure (quadratic attention cost)
  - unknown-token and out-of-vocabulary behavior

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

- Key request: for each chapter topic, list industry-project pain points, root causes, and practical resolution strategies, and provide related lab practice examples so learners can understand and operate solutions more easily.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary (Chapter 5 Current State)

### What is already strong

- Core topic coverage exists: tokens, embeddings, transformers, prompting, structured output, hallucination, RAG, fine-tuning intro.
- Beginner-friendly motivation is present.
- Includes project, checklist, and self-test.

### What still needs improvement

- Chapter still uses mostly concept-first narrative; operation rules are not strict enough.
- Some key concepts still need clearer code mapping from concept -> runnable example.
- Need an explicit "best examples by concept" learning path to reduce student confusion.
- Need one guided, end-to-end mini-LLM lab for multi-head attention training.
- Practice project is still broad; deliverables and evaluation standards are not strict enough.
- No formal output-quality metrics framework (format validity, factual grounding score, retrieval hit quality, refusal behavior).
- No prompt versioning policy and no regression-test workflow for prompt changes.
- No explicit data schema declaration standard for LLM experiments.
- Need a fail-fast runner spec that includes new concept scripts and the lab entrypoint.

---

## 2) Target Outcomes (Measurable)

Stage 5 rewrite is complete only when:

- Learner can explain and execute an end-to-end LLM workflow:
  - task definition
  - prompt design
  - output schema
  - grounding/retrieval
  - validation
  - evaluation
- Every core topic has simple/intermediate/advanced runnable examples.
- Every Stage 5 script has:
  - data declaration
  - workflow comments
  - expected output notes
- Chapter includes explicit reliability checkpoints:
  - format validity
  - hallucination risk
  - retrieval quality
  - consistency across runs
- Practice project has fixed workflow, fixed outputs, and reproducibility notes.
- Stage 5 scripts run with fail-fast runner and ladder runner.
- Self-test uses weighted scoring and remediation path.

---

## 3) Resource Upgrade (High-Quality Catalog)

Use this layered stack:

- Layer 1: core learning path (must complete)
- Layer 2: official implementation docs (must use while coding)
- Layer 3: books and papers (deeper theory)
- Layer 4: practical repos (operational skill)

Link verification status:

- Last verified: 2026-04-03
- Policy: replace/remove links after 2 failed checks

### A. Core Learning Path (Must Complete)

- Hugging Face NLP Course
  - https://huggingface.co/learn/nlp-course
- OpenAI docs (concepts + API patterns)
  - https://platform.openai.com/docs
- OpenAI Cookbook
  - https://cookbook.openai.com/
- D2L transformer chapters
  - https://d2l.ai/
- Stanford CS224n course page (selected lectures)
  - https://web.stanford.edu/class/cs224n/

### B. Official Docs (Implementation-First)

- Transformers docs
  - https://huggingface.co/docs/transformers/index
- PyTorch `nn.MultiheadAttention`
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
- PyTorch transformer tutorial
  - https://docs.pytorch.org/tutorials/beginner/transformer_tutorial.html
- Tokenizers docs
  - https://huggingface.co/docs/tokenizers/index
- OpenAI structured outputs guide
  - https://platform.openai.com/docs/guides/structured-outputs
- OpenAI prompt engineering guide
  - https://platform.openai.com/docs/guides/prompt-engineering
- Sentence Transformers docs
  - https://www.sbert.net/
- FAISS docs
  - https://faiss.ai/
- Chroma docs
  - https://docs.trychroma.com/
- LangChain docs (for orchestration reference)
  - https://python.langchain.com/docs/introduction/
- LlamaIndex docs (for RAG reference)
  - https://docs.llamaindex.ai/

### C. Books and Papers (Priority Order)

- Speech and Language Processing (Jurafsky & Martin, draft)
  - https://web.stanford.edu/~jurafsky/slp3/
- Attention Is All You Need
  - https://arxiv.org/abs/1706.03762
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
  - https://arxiv.org/abs/2005.11401
- Language Models are Few-Shot Learners
  - https://arxiv.org/abs/2005.14165
- Lost in the Middle: How Language Models Use Long Contexts
  - https://arxiv.org/abs/2307.03172

### D. Practical Repos and Ecosystem Resources

- OpenAI Cookbook repo
  - https://github.com/openai/openai-cookbook
- The Annotated Transformer (line-by-line tutorial)
  - https://nlp.seas.harvard.edu/2018/04/03/attention.html
- The Illustrated Transformer (visual intuition)
  - https://jalammar.github.io/illustrated-transformer/
- Hugging Face Transformers repo
  - https://github.com/huggingface/transformers
- nanoGPT (minimal GPT training repo)
  - https://github.com/karpathy/nanoGPT
- minGPT (compact educational GPT repo)
  - https://github.com/karpathy/minGPT
- LLMs-from-scratch (step-by-step PyTorch implementation)
  - https://github.com/rasbt/LLMs-from-scratch
- LangChain repo
  - https://github.com/langchain-ai/langchain
- LlamaIndex repo
  - https://github.com/run-llama/llama_index
- Anthropic prompt engineering guides (reference)
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

### E. Resource-to-Stage Mapping (Week 10-11)

- Week 10 foundations:
  - tokenization + embeddings + transformer basics + prompt engineering
- Week 11 reliability and systems:
  - structured output + hallucination controls + RAG + evaluation and project

### F. Time Budget (Must / Should / Optional)

Must:

- tokenization/embeddings/transformer fundamentals: 8-10h
- prompting + structured output + validation: 8-10h
- RAG + reliability checks + project baseline: 10-14h

Should:

- selected papers and deeper theory: 6-8h
- framework-level implementation practice: 6-10h

Optional:

- advanced orchestration/agent patterns: 4-8h

Recommended Stage 5 budget:

- Minimum track: 32-40h
- Strong track: 45-60h

---

## 4) New Handbook Structure (Required)

1. How to Use This Chapter (if you feel lost)
2. Prerequisites and Environment Setup
3. LLM Foundations (token, embedding, transformer)
4. Multi-Head Attention Deep-Dive Module (dedicated topic)
5. Example Complexity Scale + Where Complexity Is
6. Prompting and Structured Output Modules
7. Hallucination and Grounding Modules
8. RAG Basics Module (operatable)
9. LLM Reliability Debugging Playbook
10. Practice Project Lab (operatable workflow + deliverables)
11. Self-Test + weighted scoring rubric
12. What Comes After Stage 5

Section requirements:

- Section 1 must include a 4-pass learning flow (problem -> intuition -> mechanics -> code).
- Section 4 must define `simple/intermediate/advanced` complexity dimensions.
- Section 9 must include exact outputs and acceptance checks.

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

Core Stage 5 modules:

- Tokenization and token budget management
- Embeddings and semantic similarity
- Transformer/attention concept bridge
- Multi-head attention deep dive:
  - equations and tensor-shape walkthrough
  - attention-head behavior intuition
  - explicit comparison vs self-attention and transformer block
- Prompt engineering (zero-shot/few-shot/role/instruction decomposition)
- Structured output and schema validation
- Hallucination risk and mitigation workflow
- RAG basics (chunking/retrieval/context injection)
- Output evaluation and prompt regression testing
- Fine-tuning decision framework (when to use and when not)

Hard requirement: no module ships with missing fields.

---

## 5.1 Reviewer-Mandated Deep-Dive Modules (Additive)

This subsection is additive and does not remove existing module requirements.

### Topic 05 - Transformer Architecture (Engine of Modern LLMs)

5.1 What it is and why it matters:

- Transformer replaces sequential recurrence with parallel attention over tokens.
- It is the architecture foundation of modern GPT/Claude/Llama-style systems.

5.2 Mechanics contract (must appear in chapter + scripts):

- Query (`Q`): what this token is looking for.
- Key (`K`): what this token offers for matching.
- Value (`V`): information contributed when selected.
- Scaled dot-product attention:
  - `Attention(Q, K, V) = softmax((QK^T) / sqrt(d_k)) V`

5.3 Operatable practice suite (section-focused aliases):

- `topic05a_attention_manual.py`:
  - NumPy manual attention on tiny sentence-level matrix
  - prints score matrix, normalized attention weights, and weighted output
- `topic05b_min_gpt.py`:
  - minimal decoder-only transformer in PyTorch
  - includes causal masking and next-token objective
- `topic05c_distributed_transformer.py`:
  - performance-oriented transformer run path
  - DDP-ready path and SDP-kernel acceleration path with CPU fallback

5.4 Failure lab requirements:

- Causal masking leakage:
  - red flag: suspiciously low loss with poor generation quality
  - check: mask matrix correctness and autoregressive shift alignment
- Context-window memory pressure:
  - red flag: OOM when sequence length increases
  - check: quadratic attention cost visibility, then apply sequence/batch reduction or checkpointing

### Topic 06 - Tokenization & Embeddings (Text to Numbers)

6.1 Intuition and purpose:

- tokenizer converts text into token IDs
- embeddings convert token IDs to dense vectors used by transformer layers

6.2 Encoding pipeline contract (must appear in chapter + scripts):

1. normalization
2. pre-tokenization
3. model tokenization (for example BPE/WordPiece)
4. embedding lookup to shape `[batch, seq_len, hidden_dim]`

6.3 Operatable practice suite (section-focused aliases):

- `topic06a_bpe_visualizer.py`:
  - tokenizes sample text and prints token boundaries + IDs
- `topic06b_embedding_search.py`:
  - builds sentence embeddings and cosine-similarity retrieval demo
- `topic06c_custom_tokenizer.py`:
  - trains domain tokenizer on local corpus and compares tokenization efficiency

6.4 Failure lab requirements:

- unknown-token saturation:
  - red flag: high `[UNK]` rate / broken segmentation quality
  - check: vocabulary size, normalization policy, and domain token coverage
- out-of-vocabulary bias:
  - red flag: poor handling of non-English or domain-specific terms
  - check: tokenizer corpus mismatch, then retrain/extend tokenizer and re-evaluate

---

## 6) Operable Roadmap (Week 10-11)

### Week 10 (Foundations and Prompt Control)

- Day 1: tokenization and token-count effects
- Day 2: embeddings and similarity search basics
- Day 3: transformer attention concept-to-code bridge
- Day 4: prompt engineering patterns
- Day 5: structured output and schema validation
- Day 6: failure drills (prompt ambiguity, malformed JSON)
- Day 7: recap and concept checks

### Week 11 (Grounding, Reliability, and Project)

- Day 8: hallucination patterns and verification checks
- Day 9: RAG pipeline basics and retrieval diagnostics
- Day 10: prompt versions and evaluation harness
- Day 11: project baseline implementation
- Day 12: controlled improvement and rerun
- Day 13: error analysis and final model/prompt choice
- Day 14: self-test and readiness decision

---

## 7) Stage 5 Script Package Plan (`red-book/src/stage-5/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-optional.txt`
- `run_all_stage5.ps1`
- `run_ladder_stage5.ps1`

Core ladders (simple -> intermediate -> advanced):

1. PyTorch/CUDA ladder
- `topic00a_pytorch_cuda_simple.py`
- `topic00_pytorch_cuda_intermediate.py`
- `topic00c_pytorch_cuda_advanced.py`

2. Tokenization ladder
- `topic01a_tokenization_simple.py`
- `topic01_tokenization_intermediate.py`
- `topic01c_tokenization_advanced.py`

3. Prompt engineering ladder
- `topic02a_prompting_simple.py`
- `topic02_prompting_intermediate.py`
- `topic02c_prompting_advanced.py`

4. Structured output ladder
- `topic03a_structured_output_simple.py`
- `topic03_structured_output_intermediate.py`
- `topic03c_structured_output_advanced.py`

5. RAG ladder
- `topic04a_rag_simple.py`
- `topic04_rag_intermediate.py`
- `topic04c_rag_advanced.py`

6. Embeddings ladder
- `topic05a_embeddings_simple.py`
- `topic05_embeddings_intermediate.py`
- `topic05c_embeddings_advanced.py`

7. Multi-head attention bridge + lab
- `topic01_multihead_attention.py`
- `lab01_simple_mha_llm.py`

8. Diagnostics and project support
- `topic07_prompt_eval_regression.py`
- `topic08_project_baseline.py`

Script requirements:

- all scripts must include clear `# Workflow:` comments
- all scripts must print data/schema declarations
- all scripts must print expected metrics and interpretation text
- concept-to-script mapping must be explicit in Chapter 5 so students can find each runnable example quickly
- lab script must include numbered steps that match chapter instructions exactly

Section-focused deep-dive aliases (additive; do not remove existing ladders):

- Transformer architecture suite:
  - `topic05a_attention_manual.py`
  - `topic05b_min_gpt.py`
  - `topic05c_distributed_transformer.py`
- Tokenization & embedding suite:
  - `topic06a_bpe_visualizer.py`
  - `topic06b_embedding_search.py`
  - `topic06c_custom_tokenizer.py`

Alias compatibility rule:

- Existing stage script names remain valid and must not be deleted.
- If both legacy and section-focused names exist, add `artifact_name_map.md` and README mapping.

---

## 8) Practice Project Spec (Clear and Operatable)

Project goal:

- Build and evaluate a reliable LLM mini-workflow for one fixed text task.

Recommended default track:

- Task: short financial/news summary + risk extraction
- Input data: fixed JSONL set (20-40 records)
- Output schema: `summary`, `risks`, `confidence_note`, `citations`

Required workflow:

1. Declare dataset and schema (input fields, output fields, record counts).
2. Fix one evaluation split (dev/test or fixed case list) and fixed prompt versions (`v1`, `v2`).
3. Run baseline prompt (`v1`) and save raw outputs.
4. Validate structured output and record parse-valid rate.
5. Add one controlled improvement (few-shot examples, stricter schema, or grounding context).
6. Run improved prompt (`v2`) under same data and settings.
7. Compare before/after using same metric set.
8. Write final prompt/system selection rationale with tradeoffs.

Required deliverables:

- `results/raw_outputs_before.jsonl`
- `results/raw_outputs_after.jsonl`
- `results/metrics_before.csv`
- `results/metrics_after.csv`
- `results/format_validity_report.json`
- `results/hallucination_audit.md`
- `results/final_prompt_selection.md`
- `results/reproducibility.md`

Minimum acceptance checks:

- same input set and evaluation policy across versions
- before/after evidence exists
- output schema validation is documented
- one concrete failure diagnosis + fix is documented

### 8.1 Stage-Specific Industry Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped script/lab |
|---|---|---|---|---|---|
| Tokenization | Prompt behavior changes unexpectedly across inputs | Token boundary assumptions and truncation | Add token budget checks and truncation policy | Token-length and truncation audit | `topic01_tokenization_intermediate.py` |
| Multi-head attention | Students can run code but not reason about heads | Weak tensor-shape intuition and head semantics | Add shape-trace walkthrough and head-by-head diagnostics | Attention shape and head behavior report | `topic01_multihead_attention.py` |
| Prompt engineering | Prompt improvements are not reproducible | No prompt versioning or regression suite | Use versioned prompts and fixed eval set | Prompt regression comparison table | `topic02_prompting_intermediate.py`, `topic07_prompt_eval_regression.py` |
| Structured output | JSON output breaks in production | Schema not enforced and weak retry logic | Add strict schema validation + repair strategy | Parse-valid rate and error-class report | `topic03_structured_output_intermediate.py` |
| RAG basics | Fluent answers are weakly grounded | Retrieval quality and context assembly issues | Add retrieval diagnostics + citation-required answers | Groundedness/citation coverage report | `topic04_rag_intermediate.py` |
| Embeddings | Similarity search returns near-duplicates | Embedding mismatch and no dedup policy | Tune embedding/index settings and dedup filters | Retrieval diversity and relevance table | `topic05_embeddings_intermediate.py` |
| PyTorch/CUDA path | LLM example fails on local hardware | Device mismatch/OOM/no fallback | Add device checks, batch ladder, and CPU fallback | GPU stability and parity report | `topic00_pytorch_cuda_intermediate.py` |
| End-to-end mini LLM lab | Lab runs but no objective quality evidence | Missing baseline and acceptance gates | Compare baseline vs improved setup under fixed eval | Lab before/after results and decision | `lab01_simple_mha_llm.py` |

### 8.2 Required Matrix Usage Workflow

1. Reproduce issue with fixed prompt/data/run ID.
2. Capture baseline output quality and failure classes.
3. Compare at least 2 options and apply one change.
4. Rerun identical eval and verify deltas.
5. Record promote/hold/rollback decision.

### 8.3 Mandatory Artifacts

- `results/stage5/pain_point_matrix.md`
- `results/stage5/quality_before_after.csv`
- `results/stage5/release_decision.md`

---

## 9) Debugging and Quality Gates

Required debugging flow:

- poor answer quality -> check task definition -> check prompt clarity -> check context relevance -> check output constraints
- malformed structure -> schema enforcement -> parser validation -> repair/fail-fast policy
- hallucination risk -> check grounding availability -> check citation behavior -> apply refusal/unknown policy
- weak RAG behavior -> inspect chunking -> inspect retrieval top-k relevance -> inspect context injection quality

Quality gates:

- all Stage 5 scripts pass `run_all_stage5.ps1`
- ladders pass `run_ladder_stage5.ps1`
- expected outputs documented and validated
- project outputs complete and reproducible
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 10) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Refactor chapter structure to Stage 3/4 pattern.
3. Add complexity scale and per-topic complexity explanation.
4. Refactor concept sections to mandatory module template.
5. Add detailed prompting/structured-output/hallucination tutorials.
6. Create `red-book/src/stage-5/` ladders and runners.
7. Add explicit data/schema declarations to all examples.
8. Add "best examples by concept" section (official docs + tutorials + popular repos) with direct script mapping.
9. Add a step-by-step multi-head-attention mini-LLM lab (chapter instructions + runnable script).
10. Upgrade practice project to operatable spec and file outputs.
11. Add weighted self-test rubric and remediation flow.
12. Add resource catalog + link policy + verification date.
13. Final QA pass (terminology, encoding, duplicate cleanup).

---

## 11) Acceptance Criteria (Definition of Done)

Stage 5 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script links
- all Stage 5 scripts include functional workflow comments
- data and schema declarations are present in all examples
- practice project is clear, operatable, and file-output based
- multi-head attention appears as an explicit chapter topic with deep tutorial guidance and clear distinction from self-attention/transformer
- chapter includes a step-by-step lab operation for building a simple multi-head-attention LLM
- chapter includes a concept-to-example matrix covering all core LLM concepts
- chapter includes explicit PyTorch/CUDA guide and operational instructions
- hallucination and RAG sections include operational verification steps
- stage-5 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 12) Data and Schema Declaration Standard

Every example must include:

```
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Split/Eval policy: <fixed cases or split rule>
Type: <generation/classification/extraction/RAG>
```

Synthetic data must also declare generation method and purpose.

---

## 13) Stage Transition Requirement

Handbook must end with `What Comes After Stage 5` and include:

- 2-3 sentence summary of Stage 6 focus
- mapping from Stage 5 skills to Stage 6 tasks
- readiness sentence before progression

---

## 14) LLM Reliability Implementation Spec

Required content:

- prompt versioning policy (`v1`, `v2`, `v3`...)
- schema-constrained output strategy
- output parser + validator behavior
- grounding policy (when to retrieve context)
- uncertainty/refusal policy when evidence is missing
- evaluation policy (format validity, groundedness, usefulness)

Required runnable checks:

- print prompt version in every run
- print structured-output parse success rate
- print before/after metric delta
- print one failure example and one corrected example
- print deterministic fallback note when external model/API unavailable

### 14.1 LLM Hardware-Aware Configuration (Reviewer Additive)

Mandatory chapter/script guidance:

- choose `device = cuda|cpu` explicitly
- choose `dtype` with BF16 priority on supported GPUs, else FP16/FP32 fallback
- include SDP-kernel/flash-attention compatibility path with safe fallback
- print selected runtime path in every advanced run

Reference configuration pattern (must be explained and adapted per script):

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if (torch.cuda.is_available() and torch.cuda.is_bf16_supported()) else torch.float16

# Use high-performance SDP kernel path when supported; fallback safely otherwise.
with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=False):
    output = model(input_tensor)
```

Runtime evidence requirements:

- report tokens/sec or samples/sec
- report peak VRAM usage
- report stability note (for example overflow/NaN checks)

---

## 15) Additional Improvement Items

### A. Glossary and Notation

- lock notation: `prompt`, `context`, `response`, `schema`, `citation`, `ground_truth`
- add glossary for: token budget, hallucination, grounding, chunking, top-k, schema validation, refusal behavior

### B. Reproducibility

- fixed dataset snapshots for experiments
- prompt version log policy
- run-date and environment logging in project outputs

### C. Maintenance and QA

- link-check cadence
- script smoke-test log template
- chapter changelog section

---

## 16) Priority Breakdown

P0 (must do):

- chapter simplification rewrite with module template
- Stage 5 runnable script ladders + fail-fast runners
- practice project operatable rewrite
- prompting/structured-output/hallucination/RAG operational guides
- complexity scale + where-complexity-is blocks
- encoding cleanup

P1 (should do):

- weighted rubric improvements
- stronger evaluation harness and regression checks
- additional RAG diagnostics and retrieval-quality metrics

P2 (nice to have):

- optional framework adapters (LangChain/LlamaIndex)
- optional local-model experiment track

---

## 17) Chapter Simplification Blueprint (Mandatory)

Use this for every hard section:

1. Problem framing (what task this solves)
2. Intuition (mental model and why it works)
3. Mechanics (algorithm and constraints)
4. Operatable code (ladder examples)
5. Failure pattern and fix

Per-module must include:

- `why this is hard`
- one checkpoint question before moving forward
- one explicit `do not trust this blindly` reliability note for LLM outputs





---


## Cross-Plan Consistency Addendum (2026-04-04, Additive-Only)

This addendum is additive and does not remove or override existing content. Existing file names, workflows, and section details remain valid.

### A) Canonical Decision Labels (Use Across All Stages)

- `promote`: change passes all required gates and can move forward
- `hold`: change is promising but evidence is incomplete or mixed
- `rollback`: change increases risk/regression and must be reverted to prior baseline

### B) Canonical Troubleshooting Flow Labels

Use these labels in reports for consistency (even if stage-specific wording differs):

1. `identify` (problem statement + failure class)
2. `evidence` (logs/metrics/traces/schema snapshots)
3. `compare` (>=2 options and tradeoffs)
4. `change` (one targeted change only)
5. `verify` (same dataset/split/eval/load profile)
6. `decide` (`promote` / `hold` / `rollback`)

### C) Canonical Artifact Naming Convention (Recommended)

Keep all existing stage-specific filenames. In addition, produce or map to these canonical artifact names:

- `pain_point_matrix.md`
- `before_after_metrics.csv`
- `verification_report.md`
- `decision_log.md`
- `reproducibility.md`

If a stage already uses different names, add one of the following without deleting existing files:

- a short mapping file: `artifact_name_map.md`
- or duplicate/export canonical alias files that point to existing outputs

### D) Evidence Schema (Minimum Fields for Any Metric Table)

Every before/after metric table should include these columns (additive requirement):

- `run_id`
- `stage`
- `topic_or_module`
- `metric_name`
- `before_value`
- `after_value`
- `delta`
- `dataset_or_eval_set`
- `seed_or_config_id`
- `decision`

### E) Failure Class Taxonomy (Cross-Stage)

Use common labels for easier comparison across plans:

- `data_schema`
- `data_quality`
- `feature_or_representation`
- `training_or_optimization`
- `retrieval_or_context`
- `generation_or_reasoning`
- `tool_or_api`
- `latency_or_cost`
- `security_or_policy`
- `operations_or_release`

### F) Stage Folder and Result Folder Convention

Recommended unified pattern:

- scripts: `red-book/src/stage-<N>/`
- outputs: `results/stage<N>/`

If a plan already uses another path, keep it and add a path mapping note in stage README.

### G) No-Delete Compatibility Rule

- Do not delete prior deliverable names from existing plan text.
- Add normalization as aliases/mappings only.
- When old and canonical names both exist, the stage README must state the mapping.

## Global Key Request Addendum (2026-04-04)

- Key request: emphasize industry standard instruction, operation, issue identification, troubleshooting, result evaluation, solution improvement in chapter content, scripts, labs, and acceptance criteria.



