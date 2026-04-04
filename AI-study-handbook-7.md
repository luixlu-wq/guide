# Stage 7 - RAG Systems

(Week 13-14)

## 0) If This Chapter Feels Hard

Use this 3-pass learning strategy:

1. Pass 1 (Concept pass): read only `What it is` and `Why it matters` in each module.
2. Pass 2 (Mechanics pass): run `simple` scripts first, then `intermediate`.
3. Pass 3 (Reliability pass): run `advanced` scripts, failure drills, and lab outputs.

Do not skip pass order. Stage 7 becomes easier when you learn pipeline order, not isolated concepts.

---

## 1) Learning Targets (Must Achieve)

By the end of Stage 7, you must be able to:

- build an end-to-end RAG pipeline with fixed data and fixed eval set
- compare vector vs reranked vs hybrid retrieval with metric deltas
- enforce grounded answers with citation policy
- debug failures using retrieval logs and trace ids
- run a full troubleshooting loop:
  - identify problem class from evidence
  - compare candidate fixes with tradeoffs
  - verify selected fix with controlled before/after rerun
- run one production-style operations drill:
  - index freshness/re-ingestion
  - permission filtering (ACL)
  - latency/cost checks
- explain where PyTorch/CUDA helps in RAG (local embedding/rerank acceleration)
- run one local GPU reranking benchmark and report quality/latency/VRAM deltas
- implement structure-aware chunking for structured Ontario-style records (for example GeoJSON or subdivision tables)
- execute a no-regret regression check before promoting retrieval/indexing changes

---

## 2) Prerequisites and Environment

Minimum:

- Python 3.10+
- `pip install -r red-book/src/stage-7/requirements.txt`
- CPU path works first; GPU path is optional and must support fallback

Recommended optional:

- `pip install -r red-book/src/stage-7/requirements-optional.txt`
- CUDA-enabled PyTorch for local rerank acceleration
- Local Qdrant vector DB (if installed on your machine)

Local Qdrant check:

1. Ensure service is running on `localhost:6333`.
2. Open `http://localhost:6333/collections` in browser (or `curl`) and confirm response.
3. Run:
   - `python red-book/src/stage-7/topic02d_qdrant_local_index.py`
   - `python red-book/src/stage-7/topic03d_qdrant_acl_search.py`

If Qdrant is not running, all non-Qdrant scripts still work (offline fallback path).

Run order:

1. `red-book/src/stage-7/run_ladder_stage7.ps1`
2. `red-book/src/stage-7/run_all_stage7.ps1`

---

## 3) RAG Architecture (Mental Model)

RAG is not one model. It is a pipeline.

```text
query
 -> retrieval preparation (embed + filters)
 -> retrieve top-k chunks
 -> rerank/hybrid merge (optional but high impact)
 -> construct grounded prompt
 -> generate answer with citations
 -> evaluate and log metrics
```

If answer quality is poor, debug in this order:

1. data quality
2. chunking
3. retrieval/rerank
4. prompt/context packing
5. generation

---

## 3.1) Theory Foundation (Detailed, Mandatory)

This section explains why RAG works and why it fails.

### A. Core RAG objective

RAG tries to maximize:

1. Evidence relevance: retrieved chunks should contain true support for the query.
2. Evidence sufficiency: enough coverage to answer fully.
3. Evidence efficiency: minimal irrelevant context (noise).

If relevance is low, generation quality cannot recover reliably.

### B. Similarity and ranking theory

Dense retrieval usually computes similarity between query vector `q` and chunk vector `d`.

- cosine similarity:
  - `sim(q, d) = (q · d) / (||q|| ||d||)`
- higher similarity means closer semantic meaning

But dense similarity is not enough for exact identifiers (IDs, names, policy codes), so hybrid retrieval adds lexical evidence.

### C. Top-k tradeoff theory

- Low `k` risk:
  - miss necessary evidence (low recall)
- High `k` risk:
  - add irrelevant chunks (low precision, high prompt noise)

So RAG tuning is a precision-recall tradeoff problem, not a single “best k” value.

### D. Two-stage retrieval theory

A common production architecture:

1. Stage 1 retriever:
  - fast candidate generation (high recall)
2. Stage 2 reranker:
  - slower, stronger relevance model (high precision)

This is equivalent to:
- retrieve broadly, then filter aggressively.

### E. Error propagation theory (why small upstream issues become large)

RAG is a chained system. Upstream errors multiply downstream:

1. bad ingestion -> wrong chunks
2. wrong chunks -> wrong retrieval
3. wrong retrieval -> wrong context
4. wrong context -> hallucinated or weak answer

Practical implication:
- fix earliest failing stage first; late-stage prompt tweaks often hide root causes.

### F. Grounding and abstention theory

A grounded answer requires evidence alignment:

- each key claim should map to retrieved text
- if evidence score is weak, system should abstain

Safe RAG is not “always answer.” It is “answer when supported, abstain when unsupported.”

### G. What this means for improvement work

When RAG quality is poor:

1. optimize retrieval quality before changing generator
2. treat metrics as system signals, not isolated numbers
3. require before/after verification on fixed eval set

---

## 3.2) Failure Mode Theory (Why RAG Breaks)

RAG quality failures usually come from one of four theory-level gaps:

1. Representation gap:
   - embedding space does not preserve task-relevant similarity
   - symptom: semantically close but task-wrong chunks rank high
2. Segmentation gap:
   - chunk boundaries split evidence that should stay together
   - symptom: each retrieved chunk has partial facts, answer becomes generic
3. Ranking gap:
   - candidate recall exists, but order is poor
   - symptom: correct chunk appears in top-20 but not top-5 context window
4. Grounding gap:
   - generator follows language prior more than retrieved evidence
   - symptom: fluent answer with weak or incorrect citations

Theory-backed correction principle:

1. first optimize recall at candidate stage
2. then optimize precision via rerank/filter
3. then tighten grounding policy
4. only then tune generation style

If you reverse this order, quality gains are unstable and usually non-transferable.

---

## 4) Data and Schema Declaration Standard (Mandatory)

Every example and lab must declare:

```text
Data: <name and source>
Documents: <count>
Chunking: <strategy, size, overlap>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed queries or split rule>
Type: <retrieval/generation/rerank/eval>
```

If synthetic data is used, also declare generation method and purpose.

---

## 5) Example Complexity Scale (Used in All Modules)

- Simple:
  - one dataset
  - one retriever
  - no reranker
- Intermediate:
  - metadata filtering
  - reranking
  - query rewrite/expansion
- Advanced:
  - hybrid retrieval
  - reliability regression gates
  - production operations checks (freshness/ACL/SLO)

Where complexity is:

- data quality complexity
- chunk boundary complexity
- retrieval ranking complexity
- prompt context packing complexity
- evaluation complexity
- operations complexity (cost/latency/freshness/security)

---

## 6) Concept Modules

## 6.1 Ingestion and Cleaning

What it is:
- Convert raw docs (PDF/text/wiki/export) into clean, traceable records.

Why it matters:
- Broken extraction causes broken chunks, retrieval misses, and wrong citations.

Input schema:
- `doc_id: str`, `source: str`, `text: str`, `updated_at: str`, `acl_tags: list[str]`

Output schema:
- `chunk_id: str`, `doc_id: str`, `chunk_text: str`, `meta: dict`

Common mistake and fix:
- Mistake: drop page/section metadata.
- Fix: always keep source/page/section/chunk id and version.

When to use / not use:
- Use always for document-grounded systems.
- Do not skip ingestion validation even for small demos.

---

## 6.2 Chunking

What it is:
- Split docs into retrievable units.

Why it matters:
- Chunking quality strongly controls retrieval quality.

Practical baseline:
- token-aware chunk size: 300-700 tokens
- overlap: 50-120 tokens
- keep section headers when available

Common mistake and fix:
- Mistake: fixed-size split without manual chunk inspection.
- Fix: inspect at least 20 random chunks before indexing.

Checklist:
- chunk has complete local meaning
- no major sentence break in key facts
- metadata points back to exact source

Structure-aware chunking for Ontario/GIS-style data (mandatory):

- Do not split one logical record across multiple chunks when the record should stay atomic.
- For GeoJSON-like sources:
  - chunk by `Feature` object (or by stable administrative boundary key), not by arbitrary sentence window.
- For tabular administrative sources:
  - chunk by row/record group using stable keys (`division_id`, `subdivision_id`, `source_file`).
- Always preserve record identifiers in payload metadata so retrieval can be audited.

Operational log requirement:

- write `results/stage7/ontario_data_chunking_log.md` with:
  - chunking strategy version
  - record-preservation checks
  - at least 10 sampled chunk inspections
  - failure cases and fixes

---

## 6.3 Embeddings and Indexing

What it is:
- Encode chunks and queries into vectors; store searchable index.

Why it matters:
- Good embedding-index pair improves recall and semantic matching.

Core choices:
- embedding model
- index type
- top-k and search params

Vector DB implementation track (mandatory in this chapter):
- baseline index path: local TF-IDF/array index (for concept clarity)
- production-style path: local Qdrant collection with metadata payload and filters

Qdrant workflow (operatable):
1. Create collection with explicit vector size and cosine distance.
2. Upsert points with payload fields: `chunk_id`, `source`, `section`, `acl_tag`, `updated_at`.
3. Query top-k vectors with ACL filter.
4. Compare retrieval metrics vs non-DB baseline.

Common mistake and fix:
- Mistake: changing prompt/model first when retrieval is weak.
- Fix: measure retrieval metrics first (recall@k, hit@k, MRR).

---

## 6.4 Retrieval, Reranking, and Hybrid Search

What it is:
- Retrieval selects candidate chunks.
- Reranker reorders candidates with stronger relevance signal.
- Hybrid combines dense + lexical strengths.

Why it matters:
- Many RAG failures are retrieval failures, not generation failures.

Decision guide:
- start with dense top-k baseline
- add metadata filters for domain restrictions
- add reranker when top-k has many near-miss chunks
- add hybrid when exact terms/ids are critical

Common mistake and fix:
- Mistake: using large top-k to hide poor ranking.
- Fix: improve candidate quality before increasing k.

Industry pattern: Small-to-Big retrieval (mandatory)

- Step 1: index small child chunks for precise matching.
- Step 2: retrieve top child chunks.
- Step 3: expand to parent section/document before generation.
- Step 4: rerank final context pack for precision.

Why this matters:

- It solves a common production issue: retrieval finds the right sentence but misses surrounding constraints needed for correct final answer.

---

## 6.5 Prompt Construction, Grounding, and Citations

What it is:
- Build final context and instructions so answer is evidence-constrained.

Why it matters:
- Good retrieval can still fail if context packing is noisy.

Minimum grounding policy:
- answer only from provided evidence
- cite source for each factual claim
- abstain when evidence is insufficient

Common mistake and fix:
- Mistake: no abstention rule.
- Fix: enforce "insufficient evidence" response path.

---

## 6.6 Evaluation and Regression Gates

What it is:
- Fixed eval set + repeated measurement after each controlled change.

Why it matters:
- Without fixed evaluation, you cannot tell if system improved.

Required metrics:

- retrieval:
  - `hit@k`
  - `recall@k`
  - `MRR`
  - `nDCG` (optional if available)
- answer quality:
  - correctness/usefulness score
  - groundedness score
  - citation coverage/precision
- operations:
  - latency p50/p95
  - cost per query
  - failure rate

Metric definitions (operatable):

1. `hit@k`:
   - proportion of queries where at least one relevant chunk appears in top-k
2. `recall@k`:
   - relevant chunks retrieved in top-k / all relevant chunks
3. `MRR`:
   - mean of reciprocal rank of first relevant chunk (`1/rank`)
4. groundedness:
   - proportion of answer claims supported by cited evidence
5. citation precision:
   - proportion of citations that actually support mapped claims

Minimum evaluation protocol:

1. Use fixed eval set and stable labels.
2. Compute all metrics for baseline.
3. Apply one controlled change.
4. Recompute on same eval set.
5. Report absolute delta and percentage delta.

Regression gate example:
- block merge if `hit@5` drops > 3% or groundedness drops > 2%.

RAG triad + grounding attribution (mandatory):

- Evaluate these dimensions together:
  - context relevance (retrieval-side)
  - answer relevance (response usefulness/correctness)
  - faithfulness (answer stays aligned with evidence)
  - grounding attribution (claims map to specific chunk/source ids)

Required output artifact:

- `results/stage7/eval_triad_scores.jsonl`

No-regret release gate (mandatory):

- Stage 7 change is not promotable unless this check passes:
  - increasing `top_k` from `3` to `10` improves or maintains hit rate
  - and p95 latency remains within your defined latency budget on the local target machine
- If quality improves but latency exceeds budget:
  - decision must be `hold` or `rollback` unless optimization evidence is provided

---

## 6.7 Production RAG Operations (Mandatory)

This chapter includes mandatory production operations topics:

- index freshness and re-ingestion policy
- document-level ACL filtering
- cost/latency/SLO controls
- observability and incident response

Minimum operations checks per run:

- retrieval config version id
- prompt version id
- top-k scores and chosen chunks
- latency and cost summary
- citation ids in final output
- failure class (if any)

---

## 6.8 PyTorch and CUDA in RAG (Mandatory)

### Conceptual guide

PyTorch/CUDA is not required for every RAG system, but it is highly useful when you run local models for:

- embedding generation
- reranking (cross-encoder or scoring model)
- batched retrieval-side scoring

How training/inference loop relates to RAG scoring:

1. Move tensors to `cpu` or `cuda`.
2. Forward pass computes relevance logits/scores.
3. Loss compares predicted relevance vs labels (training path).
4. Backward computes gradients (training path).
5. Optimizer updates parameters (training path).

In production inference path, usually step 3-5 are skipped (no training), but steps 1-2 still matter for fast reranking.

Cross-encoder reranking acceleration (review-driven, mandatory):

- Use local GPU when available for reranking pass (especially larger cross-encoders).
- Compare CPU vs GPU latency on identical candidate sets and query batches.
- Track VRAM usage during rerank runs.

Operatable benchmark workflow:

1. Run intermediate rerank baseline:
   - `python red-book/src/stage-7/topic03_retrieval_rerank_intermediate.py`
2. Run advanced CUDA path:
   - `python red-book/src/stage-7/topic00c_pytorch_cuda_rag_advanced.py`
3. Record:
   - rerank latency
   - total query latency
   - VRAM allocated
4. Save benchmark table:
   - `results/stage7/retrieval_vram_usage.csv`
   - `results/stage7/retrieval_latency_vs_vram.csv`

### Device policy

- Always detect GPU availability.
- Always keep CPU fallback.
- Log selected device in every run.

Code moved to runnable examples:
- `red-book/src/stage-7/topic00a_pytorch_cuda_rag_simple.py`
- `red-book/src/stage-7/topic00_pytorch_cuda_rag_intermediate.py`

Run:
- `python red-book/src/stage-7/topic00a_pytorch_cuda_rag_simple.py`
- `python red-book/src/stage-7/topic00_pytorch_cuda_rag_intermediate.py`

Interpretation:
- simple example shows device handling and scoring mechanics.
- intermediate example shows how rerank models are trained and then used for ranking.
- advanced example shows hardware-aware optimization and memory-aware execution patterns.

---

## 7) Stage 7 Script Mapping (`red-book/src/stage-7`)

Core ladders (simple -> intermediate -> advanced):

0. PyTorch/CUDA in RAG
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

6. Production operations
- `topic06a_index_freshness_simple.py`
- `topic06_ops_cost_latency_intermediate.py`
- `topic06c_acl_incident_advanced.py`

7. Labs
- `lab01_pdf_qa_rag.py`
- `lab02_policy_assistant_rag.py`
- `lab03_hybrid_retrieval_benchmark.py`
- `lab04_enterprise_rag_operations.py`
- `lab05_qdrant_end_to_end_rag.py` (local Qdrant track)
- `lab06_project_baseline_to_production.py` (realistic project improvement track)

Hard requirement:
- all scripts must include very detailed functional comments
- all scripts must print data/schema declarations
- all scripts must print expected metrics and interpretation

---

## 8) Practice Labs (Clear and Operatable)

Common execution protocol (all labs):

1. Run environment check:
   - `python --version`
   - `python -c "import torch; print(torch.__version__)"` (optional GPU path)
2. Print run metadata at script start:
   - `dataset_version`, `eval_set_version`, `retrieval_config_version`, `prompt_version`
3. Run baseline first, then one controlled improvement.
4. Save all required output files exactly with required names.
5. Write one conclusion paragraph:
   - what changed
   - which metric improved
   - what tradeoff appeared

## Lab 1: PDF Q&A RAG

Goal:
- answer from PDF corpus with citations.

Required workflow:

1. Parse at least 20 pages from one PDF source folder.
2. Chunk with fixed settings:
   - `chunk_size=500`, `chunk_overlap=80`
3. Build baseline retriever and run fixed eval queries.
4. Add one improvement:
   - metadata filter OR reranker OR chunking change
5. Rerun same eval queries and compare before/after.

Required outputs:
- `results/lab1_outputs.jsonl`
- `results/lab1_retrieval_metrics.csv`
- `results/lab1_grounding_audit.md`
- `results/stage7/grounding_report.md` (canonical alias mapped from grounding audit)

Acceptance checks:
- each answer has at least 1 citation id
- `hit@5 >= 0.70` on your fixed eval set
- grounding audit records at least 10 manual checks

## Lab 2: Policy Assistant RAG

Goal:
- retrieve policy chunks and generate rule-grounded answers.

Required workflow:

1. Create policy schema fields:
   - `policy_id`, `effective_date`, `owner_team`, `acl_tag`
2. Run baseline retrieval with no ACL filter (for comparison only).
3. Run ACL-safe retrieval with explicit filter.
4. Verify non-authorized documents are never returned.
5. Add abstention path for unsupported questions.

Required outputs:
- `results/lab2_outputs.jsonl`
- `results/lab2_policy_violations.csv`
- `results/lab2_fix_log.md`

Acceptance checks:
- zero ACL leak in validation file
- zero unsupported answers without abstention
- all violation rows include root cause + fix id

## Lab 3: Hybrid Retrieval Benchmark

Goal:
- compare vector vs lexical vs hybrid on fixed eval set.

Required workflow:

1. Freeze eval set with at least 50 labeled queries.
2. Run dense-only retrieval and save metrics.
3. Run lexical-only retrieval and save metrics.
4. Run hybrid retrieval and save metrics.
5. Add reranker on hybrid candidates and rerun.

Required outputs:
- `results/lab3_retrieval_comparison.csv`
- `results/lab3_error_cases.md`
- `results/lab3_before_after_summary.md`

Acceptance checks:
- include per-query winner (`dense`, `lexical`, `hybrid`, `hybrid+rerank`)
- include at least 10 failure-case analyses
- include metric deltas for `hit@k`, `MRR`, and latency

Additional drill (lost-in-the-middle, mandatory):

1. Build a 20-chunk context where the correct evidence is in chunk #10.
2. Run baseline packing and record miss/failure behavior.
3. Apply one mitigation:
   - stronger reranker OR context filtering OR smaller final top-k pack.
4. Rerun same cases and record delta.

Required outputs:
- `results/stage7/lost_in_middle_drill.jsonl`
- `results/stage7/lost_in_middle_fix_report.md`

## Lab 4: Enterprise RAG Operations Drill

Goal:
- run freshness update, ACL validation, and SLO checks.

Required workflow:

1. Simulate document updates:
   - add 5 docs, modify 5 docs, delete 2 docs
2. Run re-ingestion job and capture sync logs.
3. Run ACL validation on multiple user roles.
4. Run load test for latency p50/p95 and error rate.
5. Create postmortem for one simulated incident.

Required outputs:
- `results/lab4_sync_log.md`
- `results/lab4_acl_validation.csv`
- `results/lab4_slo_report.csv`
- `results/lab4_incident_postmortem.md`

Acceptance checks:
- sync log includes update timestamps and doc versions
- ACL validation includes at least 3 roles
- SLO report includes p50, p95, timeout rate, and cost per 100 queries

## Lab 5: Qdrant End-to-End RAG

Goal:
- run baseline retrieval vs local Qdrant vector-DB retrieval, with ACL filter checks.

Required workflow:

1. Confirm local Qdrant is healthy (`localhost:6333`).
2. Create collection with explicit vector settings.
3. Upsert points with payload:
   - `chunk_id`, `source`, `section`, `acl_tag`, `updated_at`
4. Run baseline non-Qdrant path and save metrics.
5. Run Qdrant path with ACL filter and save metrics.
6. Compare quality and latency/cost.

Required outputs:
- `results/lab5_qdrant_outputs.jsonl`
- `results/lab5_qdrant_metrics.csv`
- `results/lab5_qdrant_acl_validation.csv`
- `results/lab5_qdrant_runbook.md`

Acceptance checks:
- include collection config snapshot
- include top-5 retrieval example with payload evidence
- zero ACL leak in validation report

## Lab 6: Realistic Project Improvement (Beginning -> Production)

Goal:
- improve a realistic RAG project from baseline to production readiness with evidence-based troubleshooting.

Required workflow:

1. Baseline phase:
   - run baseline pipeline on fixed eval set
   - collect metrics and top failure classes
2. Diagnosis phase:
   - choose top 3 failure classes
   - write evidence for each class
3. Solution comparison phase:
   - define at least 2 candidate fixes per failure class
   - estimate risk, expected impact, and implementation cost
4. Controlled improvement phase:
   - apply one fix at a time
   - rerun same eval set after each fix
5. Production readiness phase:
   - add monitoring checks
   - add rollback condition
   - add incident response checklist

Required outputs:
- `results/lab6_project_baseline_outputs.jsonl`
- `results/lab6_project_improved_outputs.jsonl`
- `results/lab6_project_solution_options.csv`
- `results/lab6_project_metrics_comparison.csv`
- `results/lab6_project_verification_report.md`
- `results/lab6_project_production_readiness.md`

Lab rules:

1. fixed dataset and fixed eval ids
2. fixed prompt/retrieval version tags
3. one controlled change per rerun
4. explicit before/after metric deltas

Required `lab6_project_solution_options.csv` columns:
- `problem_class`
- `option_name`
- `change_scope`
- `expected_quality_delta`
- `expected_latency_delta`
- `risk_level`
- `chosen_flag`

Required `lab6_project_verification_report.md` sections:
- baseline summary
- controlled changes
- metric delta table
- regression gate checks
- final promote/hold/rollback decision

---

## 9) Industry Project Library Track (Mandatory)

Complete at least one track end-to-end:

Track A (Beginner): Internal Policy Assistant
- data: 50-300 docs with metadata
- check: no answer without evidence

Track B (Intermediate): Customer Support RAG Triage
- data: manuals + ticket notes
- check: hybrid + reranker + measured delta

Track C (Advanced): Permission-Aware Enterprise Search
- data: multi-team docs with ACL attributes
- check: no restricted chunks retrieved in ACL tests

Project deliverables:
- `results/project_track_selection.md`
- `results/project_data_declaration.md`
- `results/project_eval_set.jsonl`
- `results/project_metrics_before_after.csv`
- `results/project_failure_drills.md`
- `results/project_final_readme.md`

---

## 10) Troubleshooting and Failure Playbook

Required failure drills:

- bad chunk boundaries
- irrelevant top-k chunks
- wrong citations
- stale index after doc updates
- ACL retrieval leak
- latency spike and budget overrun
- unknown-answer policy missing
- prompt injection in retrieved docs
- PyTorch/CUDA device mismatch or CUDA OOM
- lost-in-the-middle (correct evidence present but ignored due to context position)

Required workflow:

1. reproduce with fixed query and trace id
2. inspect retrieved chunks + scores
3. inspect metadata + ACL filters
4. inspect prompt context assembly
5. apply one targeted fix only
6. rerun same case and record delta

Operational evidence checklist (collect before fixing):

1. query id, trace id, and timestamp
2. retrieved chunk ids and raw scores
3. metadata payload (`source`, `section`, `acl_tag`, `updated_at`)
4. final prompt context (sanitized)
5. model output + citation ids
6. latency split:
   - retrieval latency
   - rerank latency
   - generation latency
7. cost estimate per query

RAG failure diagnosis decision tree (use in order):

1. Are citations missing or wrong?
   - yes -> inspect grounding policy and citation mapper first
2. Are retrieved chunks off-topic?
   - yes -> inspect chunking and retrieval/rerank settings
3. Are chunks relevant but answer still wrong?
   - yes -> inspect context packing and instruction policy
4. Is answer unstable between runs?
   - yes -> inspect config/version drift and non-determinism
5. Is quality acceptable but latency/cost too high?
   - yes -> optimize top-k, rerank depth, batching, caching
6. Any ACL/privacy violation?
   - yes -> stop release and run ACL incident playbook immediately
7. Correct evidence present but final answer still wrong?
   - yes -> test for lost-in-the-middle and rerank/context-pack strategy

Problem identification matrix (operatable):

1. Symptom: good-looking answer, wrong facts
   - check first: retrieved chunk relevance and citation mapping
   - likely root cause: retrieval miss or citation mismatch
2. Symptom: unstable answers between reruns
   - check first: prompt/version drift and non-fixed eval set
   - likely root cause: uncontrolled configuration changes
3. Symptom: answer too generic
   - check first: context specificity and top-k noise
   - likely root cause: weak retrieval precision
4. Symptom: frequent “insufficient evidence”
   - check first: chunk coverage and retriever recall
   - likely root cause: under-retrieval or poor chunking
5. Symptom: high latency/high cost
   - check first: top-k, rerank batch size, repeated context
   - likely root cause: oversized context path
6. Symptom: security/privacy incident
   - check first: ACL filter, metadata tags, audit logs
   - likely root cause: missing permission gate

Improvement strategy ladder (from low-risk to high-impact):

1. Data fixes:
   - clean extraction errors
   - repair metadata/source links
2. Chunking fixes:
   - adjust chunk size/overlap
   - preserve section boundaries
3. Retrieval fixes:
   - tune top-k
   - add metadata filters
   - add hybrid retrieval
4. Ranking fixes:
   - add reranker
   - calibrate rerank threshold
5. Grounding fixes:
   - stricter citation policy
   - stricter abstention threshold
6. Operations fixes:
   - enforce SLO/cost gates
   - enforce ACL and incident playbooks

RAG-not-working root cause map (practical):

1. Root cause: bad documents/chunks
   - evidence:
     - frequent irrelevant retrieval
     - broken sentence boundaries
   - fixes:
     - clean extraction
     - re-chunk with semantic boundaries
2. Root cause: retrieval recall too low
   - evidence:
     - low `hit@k` / low `recall@k`
   - fixes:
     - adjust embedding model
     - tune top-k
     - add query rewrite
3. Root cause: retrieval precision too low
   - evidence:
     - many near-miss chunks in top-k
   - fixes:
     - add reranker
     - add metadata filters
     - reduce context noise
4. Root cause: grounding policy weak
   - evidence:
     - unsupported claims with no strong citation
   - fixes:
     - strict citation requirement
     - abstention threshold
5. Root cause: ops bottleneck
   - evidence:
     - high p95 latency, high timeout/cost
   - fixes:
     - cache frequent retrieval
     - reduce rerank depth
     - batch embeddings/rerank
6. Root cause: positional context failure (lost-in-the-middle)
   - evidence:
     - answer ignores mid-context evidence while citing earlier/later noisy chunks
   - fixes:
     - rerank context before final packing
     - reduce context window to high-confidence chunks
     - apply small-to-big expansion only for top-ranked evidence

Verification process (must follow in order):

1. Freeze baseline:
   - lock dataset, eval ids, prompt version, retrieval config
2. Define one change:
   - only one controlled change per experiment
3. Run paired evaluation:
   - baseline and improved on same eval set
4. Compare core metrics:
   - retrieval (`hit@k`, `recall@k`, `MRR`)
   - grounding/citation
   - latency/cost
5. Check regression gates:
   - no critical metric drop beyond threshold
6. Record decision:
   - promote, hold, or rollback with reasons

Minimum acceptance thresholds before promotion:

1. quality:
   - groundedness >= baseline
   - citation precision >= baseline
2. retrieval:
   - `hit@5` and `MRR` must not regress beyond gate
3. security:
   - zero ACL leak in validation set
4. operations:
   - p95 latency within SLO
   - cost/query within budget
5. reliability:
   - rerun variance within allowed band
6. no-regret gate:
   - `top_k=10` must improve/maintain hit rate vs `top_k=3`
   - p95 latency must remain within defined budget

Troubleshooting capability framework (mandatory):

1. Identify the problem from evidence:
   - classify failure type (retrieval miss, grounding failure, citation failure, ACL leak, SLO violation)
   - collect trace id, query id, retrieved ids, scores, latency, and output text
2. Compare solution options:
   - define at least 2 candidate fixes
   - estimate expected impact and risk for each option
   - choose one option as controlled experiment
3. Verify solution correctness:
   - rerun the same fixed eval set
   - compare before/after metrics
   - confirm no regression on grounding/citation/ACL/SLO checks
4. Decide production action:
   - promote only when acceptance thresholds pass
   - otherwise rollback and test next option

Solution comparison template:

```text
Problem class:
Evidence:
Option A (low risk):
Option B (higher impact):
Expected tradeoff:
Chosen option:
Verification metrics:
Production decision:
```

Incident severity model (for realistic operations):

- Sev1:
  - ACL leak, sensitive citation exposure, critical compliance risk
  - action: immediate rollback + access block + incident owner assignment
- Sev2:
  - major quality failure on core user flows
  - action: freeze deploy + hotfix experiment + daily status updates
- Sev3:
  - minor quality/latency degradation
  - action: backlog with measured fix window

---

## 11) Minimal Runnable RAG Baseline (Complete, Local)

This example is fully operable and does not require API keys.

Data declaration:

```text
Data: inline synthetic policy docs
Documents: 4
Chunking: one chunk per document section (manual)
Input schema: query:str
Output schema: answer:str, citations:list[str], retrieved_ids:list[str]
Eval policy: fixed query list of 3 items
Type: retrieval + grounded generation (template)
```

Code moved to runnable example:
- `red-book/src/stage-7/stage7_minimal_local_rag.py`

Run:
- `python red-book/src/stage-7/stage7_minimal_local_rag.py`

Expected output behavior:
- each query prints retrieved chunk ids and citations
- answer text is grounded in retrieved chunk content

Review-driven mandatory artifact set (additive):

- `results/stage7/retrieval_vram_usage.csv`
- `results/stage7/retrieval_latency_vs_vram.csv`
- `results/stage7/eval_triad_scores.jsonl`
- `results/stage7/ontario_data_chunking_log.md`

Artifact mapping rule:

- Keep existing script output names.
- Add canonical aliases/mappings in:
  - `red-book/src/stage-7/artifact_name_map.md`

---

## 12) Resource Library (High Priority)

How to use this library:

1. Start with `Core theory` and `Official docs`.
2. Use `Tutorial/courses` for implementation path.
3. Use `Eval and reliability` for verification design.
4. Use `Industry projects` for production architecture patterns.

Core theory and papers:

- https://arxiv.org/abs/2005.11401 (RAG paper)
- https://arxiv.org/abs/1706.03762 (Attention Is All You Need, transformer foundation)
- https://arxiv.org/abs/2112.01488 (ColBERTv2 reranking/late interaction)
- https://arxiv.org/abs/2104.08663 (BEIR retrieval benchmark)
- https://arxiv.org/abs/2405.07437 (RAG evaluation survey)

Books (deep understanding track):

- https://www.oreilly.com/library/view/natural-language-processing/9781098136789/
- https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- https://www.oreilly.com/library/view/build-a-large/9781633437166/
- https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/

Official implementation docs:

- https://cookbook.openai.com/examples/file_search_responses
- https://platform.openai.com/docs/guides/tools-file-search
- https://python.langchain.com/docs/tutorials/rag/
- https://docs.llamaindex.ai/en/stable/understanding/rag/
- https://docs.haystack.deepset.ai/docs/intro
- https://faiss.ai/
- https://qdrant.tech/documentation/
- https://docs.trychroma.com/
- https://docs.weaviate.io/

Qdrant-focused tutorials (matches your local setup):

- https://qdrant.tech/documentation/quick-start/
- https://qdrant.tech/documentation/concepts/filtering/
- https://qdrant.tech/documentation/concepts/hybrid-queries/
- https://qdrant.tech/documentation/tutorials-search-engineering/hybrid-search-fastembed/
- https://qdrant.tech/documentation/advanced-tutorials/reranking-hybrid-search/
- https://qdrant.tech/documentation/fastembed/fastembed-rerankers/

Evaluation and reliability references:

- https://docs.ragas.io/
- https://docs.langchain.com/langsmith/evaluate-rag-tutorial
- https://docs.llamaindex.ai/en/stable/examples/evaluation/retrieval/retriever_eval/
- https://github.com/beir-cellar/beir
- https://microsoft.github.io/msmarco/Datasets.html

Tutorials and guided courses:

- https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/
- https://www.deeplearning.ai/short-courses/knowledge-graphs-rag/
- https://www.coursera.org/projects/building-agentic-rag-with-llamaindex
- https://fullstackretrieval.com/

Production/cloud references:

- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html
- https://learn.microsoft.com/en-us/azure/search/search-get-started-rag
- https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview

Industry/open-source project references:

- https://docs.onyx.app/
- https://github.com/zylon-ai/private-gpt
- https://github.com/Mintplex-Labs/anything-llm
- https://github.com/deepset-ai/haystack
- https://github.com/langchain-ai/rag-from-scratch

---

## 13) Self-Test (Weighted)

Scoring:

- retrieval understanding: 30%
- grounding/citation correctness: 30%
- operations and reliability: 25%
- debugging discipline: 15%

Questions:

1. Why can improving retrieval help more than switching to a larger LLM?
2. What chunking signals tell you boundaries are bad?
3. What metrics do you use to evaluate retrieval quality?
4. How do you enforce abstention when evidence is weak?
5. What is the difference between dense, lexical, and hybrid retrieval?
6. How do you test ACL safety in RAG retrieval?
7. What run logs are mandatory for incident debugging?
8. Where does PyTorch/CUDA help in a RAG pipeline?

Pass rule:
- at least 75/100 and no critical miss on ACL or grounding questions.

---

## 14) What Comes After Stage 7

Stage 8 focuses on deployment and lifecycle management of AI systems.

Stage 7 skills map to Stage 8 tasks as follows:
- retrieval/grounding -> production quality monitoring
- evaluation gates -> CI/CD quality control
- operations drills -> incident response and reliability engineering

Readiness check:
- if you can run one full lab with fixed outputs and explain metric deltas, move to Stage 8.
