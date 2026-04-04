# Stage 7 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-7.md`  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-7.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Keep chapter content implementation-first, not concept-only.
- Add clear and complete examples for each key topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare data source and data structure used in all examples.
- Add detailed explanation and demonstration for concepts.
- Add clearer instruction on learning targets.
- Add detailed tutorials for key topics.
- Add practical labs with fixed deliverables.
- Add troubleshooting guidance for realistic failures and fixes.
- Add and maintain high-quality resources:
  - official docs
  - books/papers
  - practical repos
  - framework docs
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.
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
- Key request: examples and instructions must include local vector database usage (Qdrant), because learner environment already has local vector DB installed.
- Key request: Stage 7 must provide runnable Qdrant-based indexing/retrieval examples with fallback guidance when local DB is unavailable.
- Key request: add an explicit video-first learning path (watch -> run -> verify) for students who learn better with guided visual instruction.
- Key request: add an explicit industry project library (beginner/intermediate/advanced) with fixed datasets, constraints, and acceptance checks.
- Key request: include production-RAG operations topics as mandatory learning content:
  - index freshness and incremental re-ingestion
  - document-level access control
  - cost/latency/SLO operations
  - observability and incident response

- Key request: for each chapter topic, list industry-project pain points, root causes, and practical resolution strategies, and provide related lab practice examples so learners can understand and operate solutions more easily.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary (Current Chapter 7 State)

### What is already strong

- Core RAG concepts are present: why RAG, chunking, embeddings, retrieval, prompt construction, grounding.
- Includes workflow, debugging checklist, project, and self-test.
- Good beginner narrative for motivation.

### What still needs improvement

- Encoding artifacts still exist and reduce readability (`â€”`, `â†“`, etc.).
- Stage 7 is concept-heavy and not strict enough on runnable operation flow.
- Example code is still marked conceptual; full runnable package is missing.
- No clear simple -> intermediate -> advanced ladder per topic.
- Missing deep treatment of retrieval quality controls:
  - reranking
  - hybrid retrieval (keyword + vector)
  - query rewriting/expansion
  - metadata filtering policy
- Evaluation is not strict enough:
  - retrieval metrics
  - answer quality metrics
  - groundedness/citation checks
  - before/after regression gates
- Practice project is broad and should become fixed input -> fixed output lab runbook.
- PyTorch/CUDA bridge for local embedding/rerank acceleration should be explicit and operatable.
- No dedicated video learning path for students who learn better from guided visual explanations.
- No explicit industry project library that maps concepts to real production-like project tracks.
- Missing production RAG operations topics:
  - index freshness and re-ingestion policy
  - access control and document-level permissions
  - cost/latency/SLO management
  - observability and incident response for retrieval failures

---

## 2) Target Outcomes (Measurable)

Stage 7 rewrite is complete only when:

- Learner can build an end-to-end RAG pipeline with fixed dataset and fixed eval set.
- Learner can explain and implement:
  - ingestion
  - chunking
  - embedding
  - retrieval
  - reranking
  - grounded answer generation
- Learner can compare baseline vs improved RAG with metric deltas.
- Learner can diagnose common RAG failures from traces and retrieval logs.
- Every Stage 7 script includes:
  - very detailed functional comments
  - data/schema declaration output
  - expected output and interpretation notes
- Stage 7 scripts run via fail-fast and ladder runners.
- Learner can use PyTorch/CUDA for local scoring/reranking paths (with CPU fallback).
- Learner can follow a structured learning library to complete at least one industry-level capstone project.
- Learner can run and compare multiple RAG variants:
  - baseline vector retrieval
  - reranked retrieval
  - hybrid retrieval (dense + lexical)
- Learner can run one local vector-DB workflow using Qdrant:
  - create collection
  - upsert vectors with metadata
  - query with filters
  - compare vs non-DB baseline
- Learner can execute a full troubleshooting loop:
  - identify and classify failure from logs/metrics/traces
  - compare at least 2 solution options with explicit tradeoffs
  - verify chosen fix with controlled before/after rerun
- Learner can report task metrics and retrieval metrics together:
  - answer quality
  - groundedness/citation quality
  - retrieval quality
- Learner can run at least one production-style operation drill:
  - stale-index detection and re-sync
  - permission-filter validation
  - latency/cost budget check
- Learner can complete one guided industry project from the Stage 7 project library with fixed deliverables.

---

## 3) Resource Upgrade (High-Quality Catalog)

Link verification status:

- Last verified: 2026-04-04
- Policy: replace/remove links after 2 failed checks

### A. Core Learning Path (Must Complete)

- RAG concept and architecture fundamentals
  - https://arxiv.org/abs/2005.11401
- LangChain RAG tutorials
  - https://python.langchain.com/docs/tutorials/rag/
- LlamaIndex RAG guides
  - https://docs.llamaindex.ai/

### B. Official Docs (Implementation-First)

- OpenAI embeddings guide
  - https://platform.openai.com/docs/guides/embeddings
- OpenAI vector stores guide
  - https://platform.openai.com/docs/guides/retrieval
- LangChain retrievers docs
  - https://python.langchain.com/docs/modules/data_connection/retrievers/
- LlamaIndex retrieval module docs
  - https://developers.llamaindex.ai/python/framework/module_guides/retrievers/
- FAISS docs
  - https://faiss.ai/
- Chroma docs
  - https://docs.trychroma.com/

### C. Books and Papers (Priority Order)

- Speech and Language Processing (IR and QA sections)
  - https://web.stanford.edu/~jurafsky/slp3/
- Attention Is All You Need (context for transformer representations)
  - https://arxiv.org/abs/1706.03762
- RAG paper
  - https://arxiv.org/abs/2005.11401

### D. Practical Repos and Ecosystem Resources

- LangChain
  - https://github.com/langchain-ai/langchain
- LlamaIndex
  - https://github.com/run-llama/llama_index
- FAISS
  - https://github.com/facebookresearch/faiss
- Chroma
  - https://github.com/chroma-core/chroma
- Haystack
  - https://github.com/deepset-ai/haystack

### E. Resource-to-Stage Mapping (Week 13-14)

- Week 13:
  - ingestion/chunking/retrieval fundamentals + first runnable baseline
- Week 14:
  - reranking/hybrid retrieval/evaluation/project hardening

### F. Time Budget (Must / Should / Optional)

- Must:
  - official RAG tutorials and baseline scripts
- Should:
  - reranking and hybrid retrieval extension
- Optional:
  - framework comparison track (LangChain vs LlamaIndex vs Haystack)

### G. Video Learning Path (Watch -> Run -> Verify)

- Building and Evaluating Advanced RAG (DeepLearning.AI)
  - https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- Advanced Retrieval for AI with Chroma (DeepLearning.AI)
  - https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/
- Knowledge Graphs for RAG (DeepLearning.AI)
  - https://www.deeplearning.ai/short-courses/knowledge-graphs-rag/

### H. Evaluation Frameworks and Benchmarks

- LangSmith: Evaluate a RAG application
  - https://docs.langchain.com/langsmith/evaluate-rag-tutorial
- Ragas docs
  - https://docs.ragas.io/
- LlamaIndex retrieval evaluation guide
  - https://docs.llamaindex.ai/en/stable/examples/evaluation/retrieval/retriever_eval/
- BEIR benchmark repository
  - https://github.com/beir-cellar/beir
- MS MARCO datasets
  - https://microsoft.github.io/msmarco/Datasets.html

### I. Production and Cloud RAG References

- OpenAI retrieval guide
  - https://platform.openai.com/docs/guides/retrieval
- OpenAI file search guide
  - https://platform.openai.com/docs/guides/tools-file-search/
- Amazon Bedrock knowledge base build guide
  - https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build.html
- Amazon Bedrock data sync / ingestion guide
  - https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html
- Amazon Bedrock retrieval filters API
  - https://docs.aws.amazon.com/bedrock/latest/APIReference/API_RetrievalFilter.html
- Azure AI Search RAG overview
  - https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
- Azure AI Search RAG tutorial
  - https://learn.microsoft.com/en-us/azure/search/search-get-started-rag
- Vertex AI RAG Engine overview
  - https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
- Qdrant hybrid queries
  - https://qdrant.tech/documentation/concepts/hybrid-queries/
- Qdrant filtering
  - https://qdrant.tech/documentation/concepts/filtering/
- Qdrant rerankers (FastEmbed)
  - https://qdrant.tech/documentation/fastembed/fastembed-rerankers/
- Weaviate hybrid search
  - https://docs.weaviate.io/weaviate/search/hybrid

### J. Industry Project Library References

- Onyx docs (open-source enterprise search assistant)
  - https://docs.onyx.app/
- PrivateGPT repository
  - https://github.com/zylon-ai/private-gpt
- AnythingLLM repository
  - https://github.com/Mintplex-Labs/anything-llm
- Haystack tutorials repository
  - https://github.com/deepset-ai/haystack-tutorials

---

## 4) New Handbook Structure (Required)

1. If this chapter feels hard (3-pass learning strategy)
2. Prerequisites and environment setup
3. Why RAG (problem framing and limits of vanilla LLM)
4. RAG architecture and data flow
5. Ingestion and document cleaning
6. Chunking strategies and tradeoffs
7. Embeddings and vector indexing
8. Retrieval strategies (vector, lexical, hybrid)
9. Reranking and relevance optimization
10. Prompt construction and context packing
11. Grounding and citation policies
12. Evaluation and regression gates
13. Example complexity scale and where complexity is
14. Stage 7 script mapping (`src/stage-7`)
15. Production RAG operations (freshness, ACL, latency/cost, SLOs)
16. Practice labs with fixed deliverables
17. Troubleshooting realistic failures
18. Self-test with weighted rubric
19. What comes after Stage 7

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
- Failure injection test case
- Observability hooks (what to log)
- Very detailed code-comment expectation for mapped scripts

Hard requirement: no module ships with missing fields.

---

## 6) Example Complexity Scale (Use in All Modules)

- Simple:
  - one dataset
  - one chunking strategy
  - one retriever
  - no reranker
- Intermediate:
  - metadata filtering
  - query rewrite
  - reranking
  - evaluation table
- Advanced:
  - hybrid retrieval
  - regression suite
  - failure drills
  - cost/latency quality gates

Each module must explicitly state where complexity lives:

- data quality complexity
- chunking complexity
- retrieval/reranking complexity
- prompt/context complexity
- evaluation complexity
- operations complexity (latency/cost/index freshness)

---

## 7) Stage 7 Script Package Plan (`red-book/src/stage-7/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-optional.txt`
- `run_all_stage7.ps1`
- `run_ladder_stage7.ps1`
- `stage7_utils.py`

Core ladders (simple -> intermediate -> advanced):

0. PyTorch/CUDA in RAG systems
- `topic00a_pytorch_cuda_rag_simple.py`
- `topic00_pytorch_cuda_rag_intermediate.py`
- `topic00c_pytorch_cuda_rag_advanced.py`

1. Ingestion and chunking
- `topic01a_ingestion_chunking_simple.py`
- `topic01_ingestion_chunking_intermediate.py`
- `topic01c_chunk_quality_advanced.py`

2. Embeddings and indexing
- `topic02a_embeddings_index_simple.py`
- `topic02_embeddings_index_intermediate.py`
- `topic02c_index_diagnostics_advanced.py`
- `topic02d_qdrant_local_index.py`

3. Retrieval and reranking
- `topic03a_retrieval_simple.py`
- `topic03_retrieval_rerank_intermediate.py`
- `topic03c_hybrid_retrieval_advanced.py`
- `topic03d_qdrant_acl_search.py`

4. Prompt and grounding
- `topic04a_prompt_context_simple.py`
- `topic04_grounding_intermediate.py`
- `topic04c_citation_guardrails_advanced.py`

5. Evaluation and regression
- `topic05a_eval_basics_simple.py`
- `topic05_eval_metrics_intermediate.py`
- `topic05c_regression_suite_advanced.py`

6. Production operations and reliability
- `topic06a_index_freshness_simple.py`
- `topic06_ops_cost_latency_intermediate.py`
- `topic06c_acl_incident_advanced.py`

7. Labs
- `lab01_pdf_qa_rag.py`
- `lab02_policy_assistant_rag.py`
- `lab03_hybrid_retrieval_benchmark.py`
- `lab04_enterprise_rag_operations.py`
- `lab05_qdrant_end_to_end_rag.py`
- `lab06_project_baseline_to_production.py`

Script requirements:

- all scripts must include very detailed, clear, functional comments
- all scripts must print data/schema declarations
- all scripts must print metrics and interpretation text
- all scripts must include explicit failure-handling paths
- all scripts must support deterministic reruns (fixed seed / fixed eval IDs)

---

## 8) Operable Roadmap (Week 13-14)

### Week 13 (Core RAG Pipeline)

Day 1:
- ingestion baseline and data cleaning rules

Day 2:
- chunking strategy baseline and inspection

Day 3:
- embeddings/index creation and retrieval baseline

Day 4:
- prompt construction + citation formatting

Day 5:
- baseline evaluation and failure logging

### Week 14 (Quality and Reliability)

Day 1:
- reranking and metadata filtering

Day 2:
- hybrid retrieval and comparison

Day 3:
- grounding and unknown-answer policy hardening

Day 4:
- regression gate and quality thresholds

Day 5:
- final project run and postmortem

---

## 9) Notebook and Visuals Plan

Required visuals:

- ingestion -> chunk -> embed -> index -> retrieve -> generate diagram
- chunk quality examples (good vs bad)
- retrieval score distribution plot
- top-k retrieval error examples
- before/after benchmark table

Notebook requirement:

- optional `stage7_explainer.ipynb`
- no hidden steps; notebook must map directly to scripts

---

## 10) Practice Labs (Real, Operatable)

### Lab 1: PDF Q&A RAG

Goal:
- answer questions from PDF documents with citations.

Required outputs:
- `results/lab1_outputs.jsonl`
- `results/lab1_retrieval_metrics.csv`
- `results/lab1_grounding_audit.md`

### Lab 2: Policy Assistant RAG

Goal:
- retrieve internal policy chunks and generate rule-grounded responses.

Required outputs:
- `results/lab2_outputs.jsonl`
- `results/lab2_policy_violations.csv`
- `results/lab2_fix_log.md`

### Lab 3: Hybrid Retrieval Benchmark

Goal:
- compare vector vs lexical vs hybrid retrieval on fixed eval set.

Required outputs:
- `results/lab3_retrieval_comparison.csv`
- `results/lab3_error_cases.md`
- `results/lab3_before_after_summary.md`

### Lab 4: Enterprise RAG Operations Drill

Goal:
- run index freshness update, permission-aware retrieval checks, and latency/cost SLO verification.

Required outputs:
- `results/lab4_sync_log.md`
- `results/lab4_acl_validation.csv`
- `results/lab4_slo_report.csv`
- `results/lab4_incident_postmortem.md`

### Lab 5: Qdrant End-to-End RAG

Goal:
- compare baseline retrieval vs local Qdrant retrieval with ACL filtering and fixed metrics.

Required outputs:
- `results/lab5_qdrant_outputs.jsonl`
- `results/lab5_qdrant_metrics.csv`
- `results/lab5_qdrant_acl_validation.csv`
- `results/lab5_qdrant_runbook.md`

### Lab 6: Realistic Project Improvement (Beginning -> Production)

Goal:
- start from a baseline project, identify failures, compare solution options, implement one controlled improvement path, and verify production readiness.

Required outputs:
- `results/lab6_project_baseline_outputs.jsonl`
- `results/lab6_project_improved_outputs.jsonl`
- `results/lab6_project_solution_options.csv`
- `results/lab6_project_metrics_comparison.csv`
- `results/lab6_project_verification_report.md`
- `results/lab6_project_production_readiness.md`

Lab rules:

1. fixed dataset and fixed eval set
2. fixed prompt/version tags
3. at least one controlled improvement rerun
4. explicit before/after metric delta

### Industry Project Library Track (Mandatory)

Choose at least one track and complete it end-to-end:

Track A (Beginner): Internal Policy Assistant
- data scope: 50-300 documents with section/page metadata
- core requirement: grounded answers with strict citation formatting
- hard check: no answer without evidence

Track B (Intermediate): Customer Support RAG Triage
- data scope: product manuals + historical ticket notes
- core requirement: hybrid retrieval + reranker + metadata filters
- hard check: before/after quality delta on fixed eval set

Track C (Advanced): Permission-Aware Enterprise Search Assistant
- data scope: multi-team knowledge base with document ACL attributes
- core requirement: access-control-safe retrieval + SLO/cost reporting + incident drill
- hard check: retrieval must never return restricted chunks in ACL test cases

Project-library deliverables (all tracks):

- `results/project_track_selection.md`
- `results/project_data_declaration.md`
- `results/project_eval_set.jsonl`
- `results/project_metrics_before_after.csv`
- `results/project_failure_drills.md`
- `results/project_final_readme.md`

---

## 11) Troubleshooting and Realistic Problem Playbook

### 11.1 Stage-Specific Industry Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped lab |
|---|---|---|---|---|---|
| Ingestion and cleaning | Documents ingest but retrieval quality is poor | Broken OCR, noisy boilerplate, missing normalization | Add ingestion quality checks and normalized text pipeline before indexing | Ingestion defect report + clean/raw diff samples | `lab01_pdf_qa_rag.py` |
| Chunking strategy | Relevant facts split across chunks | Chunk size/overlap not aligned with document structure | Tune chunk size/overlap with fixed eval queries and compare recall | Recall@k delta by chunk policy | `lab03_hybrid_retrieval_benchmark.py` |
| Retrieval quality | Top-k results look plausible but miss key facts | Weak embeddings, no filter policy, stale index | Add metadata filters + re-index rules + query rewrite checks | Retrieval hit/miss audit and recall table | `lab05_qdrant_end_to_end_rag.py` |
| Grounding and citations | Fluent answers with unsupported claims | Context packing errors, missing citation rules | Enforce citation-required answer format and unknown-answer policy | Citation coverage and groundedness score | `lab01_pdf_qa_rag.py` |
| Hybrid retrieval | Hybrid setup increases complexity without gains | Poor weighting or duplicate result handling | Run weighted fusion experiments with duplicate suppression | Hybrid vs dense/lexical comparison report | `lab03_hybrid_retrieval_benchmark.py` |
| ACL-aware retrieval | User sees restricted chunks | Missing permission filters in retrieval layer | Apply ACL filter at query time and test with negative cases | ACL leak test (must be zero) | `lab05_qdrant_end_to_end_rag.py` |
| Index freshness ops | New documents not reflected in answers | No sync schedule, no freshness monitoring | Add incremental ingestion job + freshness SLO + stale-index alerts | Freshness lag report and sync logs | `lab04_enterprise_rag_operations_drill.py` |
| Latency/cost SLO | System works but exceeds budget | Large top-k, expensive reranking, no latency budget | Set latency budget per stage and optimize bottleneck step only | p95 latency/cost before-after report | `lab04_enterprise_rag_operations_drill.py` |
| GPU rerank path | CUDA path unstable across environments | Device mismatch, OOM, no fallback policy | Add device guards, batch ladder, and deterministic CPU fallback | GPU failure recovery log + parity check | `lab04_enterprise_rag_operations_drill.py` |

### 11.2 Required Troubleshooting Workflow

1. Reproduce failure with fixed query set and trace/run ID.
2. Classify failure: retrieval, grounding, citation, latency, ACL, or GPU path.
3. Compare at least 2 fixes with tradeoffs.
4. Apply exactly 1 targeted change.
5. Rerun same eval set and record metric deltas.
6. Decide promote/hold/rollback with explicit criteria.

### 11.3 Mandatory Artifacts

- `results/stage7/pain_point_matrix.md`
- `results/stage7/retrieval_grounding_before_after.csv`
- `results/stage7/ops_incident_postmortem.md`

---

## 12) Debugging and Quality Gates

Required debugging flow:

- weak answer -> inspect retrieval quality before changing prompts
- retrieval misses -> inspect chunking/indexing/metadata filters
- wrong citations -> inspect citation mapping and context assembly
- latency spikes -> inspect top-k and rerank batch size
- unstable outputs -> inspect prompt version drift

Quality gates:

- all Stage 7 scripts pass `run_all_stage7.ps1`
- ladders pass `run_ladder_stage7.ps1`
- expected outputs generated and validated
- benchmark table generated with before/after deltas
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 13) RAG Reliability Implementation Spec

Required content:

- chunking policy versioning (`chunk_v1`, `chunk_v2`)
- retrieval config versioning (`k`, filters, reranker)
- prompt template versioning (`prompt_v1`, `prompt_v2`)
- unknown-answer policy (abstain when evidence is weak)
- citation policy (all factual claims should map to sources)
- regression thresholds for retrieval and groundedness

Required runnable checks:

- print retrieval config per run
- print top-k scores and selected chunks
- print citation coverage rate
- print one failure sample and one corrected sample
- print before/after metric delta

---

## 14) Data and Schema Declaration Standard

Every example must include:

```text
Data: <name and source>
Documents: <count>
Chunking: <strategy, size, overlap>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed queries or split rule>
Type: <retrieval/generation/rerank/eval>
```

Synthetic data must declare generation method and purpose.

---

## 15) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Fix encoding artifacts in chapter text.
3. Add complexity scale and per-topic complexity notes.
4. Refactor each concept section to module template.
5. Add strict data/schema declaration blocks.
6. Create `red-book/src/stage-7/` ladders and runners.
7. Add retrieval/reranking/hybrid tutorials and scripts.
8. Add production operations section (freshness, ACL, SLO/cost, observability).
9. Upgrade project into fixed deliverable lab format.
10. Add debugging runbook and quality gates.
11. Add weighted self-test and remediation path.
12. Add resource catalog with verification policy.
13. Final QA pass (terminology, encoding, duplicate cleanup).

---

## 16) Acceptance Criteria (Definition of Done)

Stage 7 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script mapping
- all Stage 7 scripts include very detailed, clear comments
- data and schema declarations are present in all examples
- labs are real, operatable, and file-output based
- retrieval/reranking quality is measured with fixed metrics
- chapter includes strict grounding and citation policy
- PyTorch/CUDA section includes runnable examples and CPU fallback guidance
- chapter includes explicit production-RAG operations workflow (freshness, ACL, SLO/cost)
- chapter includes explicit video path and industry project library mapping
- chapter includes explicit local vector DB (Qdrant) setup and runnable workflow
- chapter includes explicit troubleshooting framework (identify -> compare -> verify)
- chapter includes one beginning-to-production improvement lab with fixed deliverables
- stage-7 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 17) Additional Improvement Items

### A. Glossary and Notation

- lock notation: `query`, `chunk`, `embedding`, `top_k`, `rerank_score`, `citation_id`
- add glossary for: grounding, chunk overlap, recall@k, mrr, hit@k, abstention

### B. Reproducibility

- fixed eval query set policy
- config snapshot policy (chunking/retrieval/prompt versions)
- environment/run-date logging policy

### C. Maintenance and QA

- link-check cadence (monthly)
- script smoke-test log template
- chapter changelog section

---

## 18) Priority Breakdown

P0 (must do):

- chapter restructure to operatable format
- Stage 7 script package + runners
- 5 real labs with fixed deliverables (including local Qdrant end-to-end lab)
- retrieval/reranking evaluation harness
- grounding/citation reliability policies
- detailed comment standard enforcement
- PyTorch/CUDA section with runnable ladder examples

P1 (should do):

- hybrid retrieval optimization track
- stronger failure-drill coverage
- optional framework adapters (LangChain/LlamaIndex/Haystack)

P2 (nice to have):

- optional cloud vector-db adapter track
- optional multilingual RAG extension

---

## 19) Chapter Simplification Blueprint (Mandatory)

Use this for every hard section:

1. Problem framing (what this solves)
2. Intuition (mental model)
3. Mechanics (step-by-step flow)
4. Operatable code (ladder examples)
5. Failure pattern and fix

Per-module must include:

- `why this is hard`
- one checkpoint question before moving forward
- one explicit reliability warning

---

## 20) Stage Transition Requirement

Handbook must end with `What Comes After Stage 7` and include:

- 2-3 sentence summary of Stage 8 focus
- mapping from Stage 7 skills to Stage 8 tasks
- readiness sentence before progression




---

## 21) Review-Driven Addendum (2026-04-04, Additive-Only)

This section incorporates external review feedback and is additive only. Existing sections, file names, and deliverables remain valid.

### 21.1) Local GPU Retrieval Optimization Benchmark (Mandatory)

Add an explicit benchmark track for local high-end hardware:

- compare `semantic search only` vs `semantic search + local GPU reranker`
- measure and report:
  - `NDCG@10`
  - `Recall@k`
  - `p95 latency (ms)`
  - `VRAM allocated (MB/GB)`
- require one fixed evaluation query set and fixed seed/config ID

Required artifact:

- `results/stage7/retrieval_latency_vs_vram.csv`

Recommended script mapping:

- `topic03e_local_rerank_benchmark.py`

### 21.2) Ontario/GIS Structure-Aware Chunking (Mandatory)

Add structure-aware chunking content for tabular/GIS sources:

- preserve GeoJSON `Feature` integrity (do not split geometry/properties across chunks)
- preserve row-level integrity for CSV/records with administrative identifiers
- compare against naive sentence/window chunking on fixed eval queries

Required artifact:

- `results/stage7/chunking_strategy_comparison.md`

Recommended script mapping:

- `topic01d_structure_aware_chunking.py`

### 21.3) RAG Triad + Grounding Attribution (Mandatory)

Evaluation must include all four dimensions:

- context relevance
- answer relevance
- faithfulness
- grounding attribution (claim-to-chunk/source mapping coverage)

Required artifact:

- `results/stage7/eval_triad_scores.jsonl`

Implementation rule:

- every evaluated answer must include source/chunk identifiers for factual claims

### 21.4) Small-to-Big Retrieval Pattern (Mandatory)

Add parent-document retrieval tutorial/lab path:

- retrieve with small chunks for precision
- expand to parent/broader context for completeness
- compare quality/latency against standard chunk-only retrieval

Recommended script mapping:

- `topic03f_small_to_big_retrieval.py`

### 21.5) Lost-in-the-Middle Failure Drill (Mandatory)

Add a dedicated positional-bias stress drill:

- construct long-context test where key evidence is in middle positions
- demonstrate baseline failure and improved strategy (rerank/context filtering/reordering)
- verify metric delta on same fixed eval set

Recommended script mapping:

- `topic05d_lost_in_middle_drill.py`

### 21.6) No-Regret Release Gate (Mandatory)

Before accepting new data-source ingestion or retrieval changes:

- run regression on existing fixed benchmark queries
- prove no unacceptable degradation on prior must-pass queries
- log promote/hold/rollback with evidence

Required artifact:

- `results/stage7/regression_report.md`

### 21.7) Stage 7 Acceptance Gate Extension

Stage 7 is only complete when all of the following are true:

- local reranker benchmark completed with quality/latency/VRAM evidence
- structure-aware chunking implemented and compared vs naive baseline
- RAG triad + grounding attribution results generated and reviewed
- small-to-big retrieval comparison completed
- lost-in-the-middle drill completed with verified mitigation
- no-regret regression report produced for data/index changes

### 21.8) Results Mapping Note

To preserve compatibility with existing plan outputs:

- keep all existing Stage 7 output filenames unchanged
- add this mapping file when needed:
  - `results/stage7/artifact_name_map.md`
- map existing output names to canonical names from Section C (Cross-Plan Consistency Addendum)

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



