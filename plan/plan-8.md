# Stage 8 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-8.md`  
Plan owner: You + Codex  
Version date: 2026-04-04

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-8.md` to be:
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
  - industry platform implementation guides
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.
- Mandatory request: include PyTorch and CUDA conceptual/tutorial content in the chapter.
- Mandatory request: include runnable PyTorch/CUDA example code (simple -> intermediate -> advanced) with very detailed and clear functional comments.

Carry-over key requirements from prior plans (must remain active):

- Key request: collect the best tutorials, books, videos, official documentation, guides, instructions, and industry project references to build chapter content.
- Key request: chapter content must be detailed, easy to understand, and operatable from both theory and realistic project perspectives.
- Key request: create a learning library/track that leads students to real, industry-level projects.
- Key request: add more theory instruction in each chapter so learners understand principles, not only steps.
- Key request: explicitly teach troubleshooting capability as a core skill:
  - how to identify and classify problems from evidence/logs/metrics
  - how to compare possible solutions with clear tradeoff analysis
  - how to verify fixes using controlled reruns and before/after metrics
- Key request: include a new realistic lab that improves a project from beginning to production, with fixed deliverables and production-quality acceptance checks.

Stage-8-specific locked requirements:

- Teach fine-tuning as both theory and engineering workflow, not only definitions.
- Make `fine-tuning vs prompting vs RAG` a strict decision module with measurable decision criteria.
- Make instruction tuning, LoRA, QLoRA, and distillation fully operatable with runnable examples.
- Add explicit data quality and dataset governance guidance for tuning datasets.
- Add strict evaluation framework (baseline vs tuned, fixed eval set, regression gates).
- Add resource-backed industry implementation guidance (OpenAI, Hugging Face, cloud platforms).
- For each Stage 8 topic, document industry pain points, root causes, practical resolution strategies, and at least one related runnable lab practice example.
- Add at least one lab that compares:
  - base model
  - prompt-only baseline
  - tuned model
  - tuned + retrieval hybrid path (optional local Qdrant track)

- Key request: for each chapter topic, list industry-project pain points, root causes, and practical resolution strategies, and provide related lab practice examples so learners can understand and operate solutions more easily.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary (Current Chapter 8 State)

### What is already strong

- Core topics are present: instruction tuning, LoRA, QLoRA, distillation.
- Includes practical motivation and common mistakes.
- Includes a beginner-friendly project narrative and self-test.

### What still needs improvement

- Chapter is still mostly concept text; operation workflow is not strict enough.
- No clear script package mapping (`red-book/src/stage-8/`) exists yet.
- No fail-fast runner and ladder runner for Stage 8 examples.
- No formal example complexity ladder (simple -> intermediate -> advanced).
- No strict metrics framework for tuning success and regression control.
- No fixed data declaration and schema declaration standard before all examples.
- No production lifecycle section:
  - experiment tracking
  - model registry
  - promotion/rollback criteria
  - cost/latency controls
- PyTorch/CUDA content is not yet fully operationalized for stage scripts.
- No explicit beginning-to-production fine-tuning lab with fixed artifacts.

---

## 2) Target Outcomes (Measurable)

Stage 8 rewrite is complete only when:

- Learner can explain and execute end-to-end model adaptation workflow:
  - problem framing
  - data design
  - method selection
  - training
  - evaluation
  - deployment decision
- Learner can decide correctly among:
  - prompt-only optimization
  - RAG
  - fine-tuning
  - hybrid strategy
- Every Stage 8 module has simple/intermediate/advanced runnable examples.
- Every Stage 8 script includes:
  - very detailed functional comments
  - data/schema declarations
  - expected output and interpretation notes
- Stage 8 includes strict baseline-vs-tuned evaluation with regression gates.
- Stage 8 includes one beginning-to-production improvement lab with fixed deliverables.
- Stage 8 scripts run via fail-fast and ladder runners.
- Learner can execute PyTorch/CUDA fine-tuning path with CPU fallback behavior.

---

## 3) Resource Upgrade (High-Quality Catalog)

Link verification status:

- Last verified: 2026-04-04
- Policy: replace/remove links after 2 failed checks

### A. Core Learning Path (Must Complete)

- OpenAI model optimization and fine-tuning guide
  - https://platform.openai.com/docs/guides/fine-tuning
- Hugging Face Transformers fine-tuning docs
  - https://huggingface.co/docs/transformers/training
- Hugging Face PEFT quicktour (LoRA)
  - https://huggingface.co/docs/peft/quicktour
- Hugging Face TRL SFT Trainer docs
  - https://huggingface.co/docs/trl/sft_trainer
- Hugging Face bitsandbytes quantization docs (QLoRA path)
  - https://huggingface.co/docs/transformers/quantization/bitsandbytes

### B. Official Docs (Implementation-First)

- OpenAI fine-tuning API reference
  - https://platform.openai.com/docs/api-reference/fine-tuning
- OpenAI direct preference optimization guide
  - https://platform.openai.com/docs/guides/direct-preference-optimization
- OpenAI evals guide
  - https://platform.openai.com/docs/guides/evals
- PyTorch CUDA semantics
  - https://docs.pytorch.org/docs/stable/notes/cuda.html
- PyTorch AMP recipe
  - https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- PyTorch FSDP docs
  - https://docs.pytorch.org/docs/stable/fsdp.html
- Hugging Face Accelerate docs
  - https://huggingface.co/docs/accelerate/index
- TorchTune overview (PyTorch LLM tuning)
  - https://docs.pytorch.org/torchtune/0.1/overview.html

### C. Papers and Theory Foundations

- LoRA: Low-Rank Adaptation of Large Language Models
  - https://arxiv.org/abs/2106.09685
- QLoRA: Efficient Finetuning of Quantized LLMs
  - https://arxiv.org/abs/2305.14314
- InstructGPT
  - https://arxiv.org/abs/2203.02155
- Self-Instruct
  - https://arxiv.org/abs/2212.10560
- Scaling Instruction-Finetuned Language Models (FLAN)
  - https://arxiv.org/abs/2210.11416
- DPO: Direct Preference Optimization
  - https://arxiv.org/abs/2305.18290
- Distilling the Knowledge in a Neural Network
  - https://arxiv.org/abs/1503.02531
- Model Cards for Model Reporting
  - https://arxiv.org/abs/1810.03993

### D. Books and Structured Courses

- Build a Large Language Model (From Scratch)
  - https://www.oreilly.com/library/view/build-a-large/9781633437166/
- NLP with Transformers (O'Reilly)
  - https://www.oreilly.com/library/view/natural-language-processing/9781098136789/
- Hands-On Large Language Models
  - https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/
- Hugging Face NLP Course
  - https://huggingface.co/learn/nlp-course
- DeepLearning.AI short course: Finetuning Large Language Models
  - https://www.deeplearning.ai/short-courses/finetuning-large-language-models/

### E. Practical Repos and Framework References

- PEFT repository
  - https://github.com/huggingface/peft
- TRL repository
  - https://github.com/huggingface/trl
- Transformers repository
  - https://github.com/huggingface/transformers
- Accelerate repository
  - https://github.com/huggingface/accelerate
- TorchTune repository
  - https://github.com/pytorch/torchtune
- Llama Recipes
  - https://github.com/meta-llama/llama-recipes
- LLMs-from-scratch repo
  - https://github.com/rasbt/LLMs-from-scratch
- lm-evaluation-harness
  - https://github.com/EleutherAI/lm-evaluation-harness

### F. Industry Platform Implementation Guides

- Amazon Bedrock fine-tuning
  - https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.html
- Amazon Bedrock model customization jobs
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-submit.html
- SageMaker JumpStart fine-tuning
  - https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-fine-tune.html
- Azure AI Foundry fine-tuning overview
  - https://learn.microsoft.com/en-us/azure/ai-studio/concepts/fine-tuning-overview
- Azure OpenAI / Foundry fine-tuning guide
  - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning
- Vertex AI tuning overview
  - https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models
- Vertex AI open model tuning
  - https://cloud.google.com/vertex-ai/generative-ai/docs/models/open-model-tuning
- Gemma model fine-tuning docs
  - https://ai.google.dev/gemma/docs/tune

### G. Operations, Governance, and Reliability References

- MLflow model registry
  - https://mlflow.org/docs/latest/ml/model-registry/
- MLflow evaluation docs
  - https://mlflow.org/docs/latest/ml/evaluation/
- Weights and Biases registry
  - https://docs.wandb.ai/models/registry
- DVC data/model versioning
  - https://dvc.org/doc/use-cases/versioning-data-and-models
- Great Expectations data docs
  - https://docs.greatexpectations.io/docs/oss/guides/setup/configuring_data_docs/host_and_share_data_docs
- OpenTelemetry docs
  - https://opentelemetry.io/docs/
- NIST AI RMF 1.0
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10

---

## 4) New Handbook Structure (Required)

1. If this chapter feels hard (3-pass learning strategy)
2. Prerequisites and environment setup (CPU + optional CUDA)
3. Fine-tuning mental model and decision boundaries
4. Fine-tuning vs prompting vs RAG (operational decision framework)
5. Data design for tuning (quality, schema, and splits)
6. Instruction tuning module
7. LoRA module
8. QLoRA module
9. Distillation module
10. PyTorch/CUDA tuning loop module
11. Evaluation and regression gates
12. Industry operations and deployment workflow
13. Example complexity scale + where complexity is
14. Stage 8 script mapping (`src/stage-8`)
15. Practice labs with fixed deliverables
16. Troubleshooting and failure playbook
17. Self-test with weighted rubric
18. What comes after Stage 8

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
- Cost/latency note
- Very detailed code-comment expectation for mapped scripts

Hard requirement: no module ships with missing fields.

---

## 6) Example Complexity Scale (Use in All Modules)

- Simple:
  - tiny dataset
  - single method run
  - one metric family
- Intermediate:
  - method comparison (base vs tuned)
  - hyperparameter sweeps
  - fixed eval set with error analysis
- Advanced:
  - multi-method decision (prompt vs RAG vs tune)
  - cost/latency and quality gates
  - production promotion/rollback decision

Each module must explicitly state where complexity lives:

- data quality complexity
- objective and method complexity
- memory/compute complexity
- evaluation complexity
- operations complexity (cost, latency, rollback)

---

## 7) Stage 8 Script Package Plan (`red-book/src/stage-8/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-optional.txt`
- `run_all_stage8.ps1`
- `run_ladder_stage8.ps1`
- `stage8_utils.py`

Core ladders (simple -> intermediate -> advanced):

0. PyTorch/CUDA tuning fundamentals
- `topic00a_pytorch_cuda_tuning_simple.py`
- `topic00_pytorch_cuda_tuning_intermediate.py`
- `topic00c_pytorch_cuda_tuning_advanced.py`

1. Dataset design and formatting
- `topic01a_dataset_schema_simple.py`
- `topic01_dataset_quality_intermediate.py`
- `topic01c_data_governance_advanced.py`

2. Instruction tuning baseline
- `topic02a_sft_baseline_simple.py`
- `topic02_sft_intermediate.py`
- `topic02c_sft_eval_advanced.py`

3. LoRA ladder
- `topic03a_lora_simple.py`
- `topic03_lora_intermediate.py`
- `topic03c_lora_rank_sweep_advanced.py`

4. QLoRA ladder
- `topic04a_qlora_simple.py`
- `topic04_qlora_intermediate.py`
- `topic04c_qlora_memory_tradeoff_advanced.py`

5. Distillation ladder
- `topic05a_distill_simple.py`
- `topic05_distill_intermediate.py`
- `topic05c_distill_eval_advanced.py`

6. Decision and system comparison ladder
- `topic06a_prompt_vs_tune_simple.py`
- `topic06_tune_vs_rag_intermediate.py`
- `topic06c_hybrid_strategy_advanced.py`

7. Evaluation and regression ladder
- `topic07a_eval_basics_simple.py`
- `topic07_eval_regression_intermediate.py`
- `topic07c_promotion_gate_advanced.py`

8. Industry operations ladder
- `topic08a_model_registry_simple.py`
- `topic08_ops_observability_intermediate.py`
- `topic08c_canary_rollback_advanced.py`

9. Labs
- `lab01_instruction_tuning_baseline.py`
- `lab02_lora_qlora_comparison.py`
- `lab03_distillation_tradeoff_lab.py`
- `lab04_finetune_project_baseline_to_production.py`
- `lab05_finetune_vs_rag_vs_hybrid_qdrant.py` (optional local Qdrant track)

Script requirements:

- all scripts must include very detailed, clear, functional comments
- all scripts must print data/schema declarations
- all scripts must print metrics and interpretation text
- all scripts must include explicit failure-handling paths
- all scripts must support deterministic reruns (fixed seed / fixed eval IDs)

---

## 8) Operable Roadmap (Week 15-16)

### Week 15 (Method Foundations)

Day 1:
- decision framework: prompt vs RAG vs fine-tuning

Day 2:
- dataset schema design and quality checks

Day 3:
- SFT baseline run (base vs tuned)

Day 4:
- LoRA path and rank/target-module understanding

Day 5:
- QLoRA path and memory tradeoff analysis

Day 6:
- PyTorch/CUDA performance and stability checks

Day 7:
- baseline evaluation summary

### Week 16 (Reliability and Productionization)

Day 8:
- distillation basics and teacher-student comparison

Day 9:
- fixed eval harness and regression gates

Day 10:
- error analysis and failure classification

Day 11:
- operations setup (tracking, registry, promotion policy)

Day 12:
- controlled improvement rerun (one change only)

Day 13:
- production readiness checklist and rollback drill

Day 14:
- final report and readiness decision

---

## 9) Notebook and Visuals Plan

Required visuals:

- adaptation decision flowchart (prompt vs RAG vs tune)
- LoRA/QLoRA architecture overlays
- memory usage comparison chart
- quality/cost/latency comparison table
- before/after metric delta plots

Notebook requirement:

- optional `stage8_explainer.ipynb`
- no hidden steps; notebook must map directly to scripts

---

## 10) Practice Labs (Real, Operatable)

### Lab 1: Instruction Tuning Baseline

Goal:
- run base vs SFT-tuned comparison on one fixed task.

Required outputs:
- `results/lab1_base_outputs.jsonl`
- `results/lab1_tuned_outputs.jsonl`
- `results/lab1_metrics_comparison.csv`
- `results/lab1_error_cases.md`

### Lab 2: LoRA vs QLoRA Comparison

Goal:
- compare adaptation quality and memory/cost tradeoffs.

Required outputs:
- `results/lab2_lora_metrics.csv`
- `results/lab2_qlora_metrics.csv`
- `results/lab2_memory_latency_report.md`

### Lab 3: Distillation Tradeoff Lab

Goal:
- train/evaluate student model from teacher outputs and compare cost-quality profile.

Required outputs:
- `results/lab3_teacher_outputs.jsonl`
- `results/lab3_student_outputs.jsonl`
- `results/lab3_distillation_report.md`

### Lab 4: Realistic Project Improvement (Beginning -> Production)

Goal:
- improve one tuning project from baseline to production readiness with evidence-based troubleshooting.

Required outputs:
- `results/lab4_project_baseline_outputs.jsonl`
- `results/lab4_project_improved_outputs.jsonl`
- `results/lab4_solution_options.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_verification_report.md`
- `results/lab4_production_readiness.md`

### Lab 5: Fine-Tuning vs RAG vs Hybrid (Optional Qdrant Track)

Goal:
- compare tuned-only, RAG-only, and hybrid pipelines on the same fixed eval set.

Required outputs:
- `results/lab5_compare_prompt_rag_tune.csv`
- `results/lab5_qdrant_retrieval_metrics.csv`
- `results/lab5_final_decision.md`

Lab rules:

1. fixed dataset and fixed eval set
2. fixed prompt/model/dataset version tags
3. at least one controlled improvement rerun
4. explicit before/after metric deltas

---

## 11) Industry Pain-Point Matrix (Topic -> Cause -> Solution -> Lab)

This section is mandatory and must be reflected in the final chapter content.

### 11.1 Stage-Specific Industry Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped lab |
|---|---|---|---|---|---|
| Fine-tuning decision boundary | Team fine-tunes too early and spends budget with weak gain | No baseline, no decision rubric, mixing behavior and knowledge gaps | Enforce decision order: prompt baseline -> RAG baseline -> tune only if measurable gap remains | Decision matrix with baseline metrics | `lab05_finetune_vs_rag_vs_hybrid_qdrant.py` |
| Dataset design/governance | Tuned model is inconsistent or unsafe | Label noise, split contamination, weak schema checks | Add dataset contracts, validation, dedupe, contamination checks | Data quality audit and contamination report | `topic01_dataset_quality_intermediate.py` |
| Instruction tuning (SFT) | Better on demos, weak on unseen prompts | Narrow prompt coverage, overfitting, template mismatch | Expand prompt diversity and enforce template parity tests | Seen vs unseen performance delta | `lab01_instruction_tuning_baseline.py` |
| LoRA | Adapter quality unstable across tasks | Wrong target modules, weak rank choice | Rank/module sweep with cost-quality tradeoff table | Rank sweep results and chosen config rationale | `topic03c_lora_rank_sweep_advanced.py` |
| QLoRA | Memory improves but quality regresses | Aggressive quantization and unstable optimizer settings | Stabilize with validated config, clipping, and baseline parity checks | LoRA vs QLoRA quality/memory comparison | `lab02_lora_qlora_comparison.py` |
| Distillation | Student model fast but brittle at edges | Weak teacher outputs, no hard-example focus | Build failure-focused distillation set and segment eval | Segment-level quality and latency report | `lab03_distillation_tradeoff_lab.py` |
| PyTorch/CUDA tuning | Training crashes or underutilizes GPU | OOM, mixed device tensors, no AMP policy | Device checks, AMP policy, batch ladder, fallback path | GPU util/memory timeline + crash recovery log | `topic00c_pytorch_cuda_tuning_advanced.py` |
| Evaluation/regression gates | Subjective promotion decisions | No fixed eval harness, no threshold gates | Lock eval set and enforce promotion/rollback thresholds | Gate report with pass/fail decisions | `topic07c_promotion_gate_advanced.py` |
| Ops deployment | Good offline metrics but production incidents | Missing canary, weak traceability, no rollback drill | Add model registry + canary + rollback runbook | Canary metrics + rollback drill evidence | `topic08c_canary_rollback_advanced.py` |
| Tune + retrieval hybrid | Team treats tune and retrieval as mutually exclusive | No failure ownership model | Define hybrid policy: tune for behavior, retrieve for freshness | Failure ownership map + hybrid benchmark | `topic06c_hybrid_strategy_advanced.py` |

### 11.2 Required Matrix Usage Workflow

1. Reproduce issue with fixed run ID and fixed eval split.
2. Capture evidence before proposing any fix.
3. Compare at least 2 options; apply 1 change.
4. Rerun identical eval and compare deltas.
5. Record promotion/hold/rollback decision.

### 11.3 Mandatory Artifacts

- `results/stage8/pain_point_matrix.md`
- `results/stage8/method_compare_before_after.csv`
- `results/stage8/promotion_gate_decision.md`

---

## 12) Troubleshooting and Realistic Failure Playbook

Required failure scenarios:

- malformed training dataset records
- prompt-template drift between train and eval
- overfitting on small tuning sets
- no measurable gain over base model
- regression in format validity
- catastrophic forgetting symptoms
- unstable training loss
- CUDA OOM and device mismatch
- quantization instability in QLoRA
- misleading success due to weak eval set
- cost/latency increase beyond budget

Required troubleshooting workflow:

1. reproduce with fixed eval IDs and run ID
2. classify failure type from evidence
3. inspect data/schema consistency
4. inspect training config and method settings
5. inspect eval outputs and metric deltas
6. compare at least two fix options with tradeoffs
7. apply one targeted fix only
8. rerun same eval set and record deltas
9. promote/hold/rollback decision with reason

Required logs per run:

- run id and config version ids
- dataset version and split IDs
- method (`SFT/LoRA/QLoRA/distill`)
- training and validation metrics
- memory/latency/cost summary
- failure class and selected fix

---

## 13) Debugging and Quality Gates

Required debugging flow:

- weak improvement -> verify baseline/eval design first
- unstable training -> inspect lr/batch/gradient settings
- format errors -> inspect output schema and parser checks
- poor generalization -> inspect data diversity and leakage
- high cost/latency -> inspect model size, context, batch policy

Quality gates:

- all Stage 8 scripts pass `run_all_stage8.ps1`
- ladders pass `run_ladder_stage8.ps1`
- expected outputs generated and validated
- benchmark table generated with before/after deltas
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 14) Fine-Tuning Reliability Implementation Spec

Required content:

- dataset versioning policy (`data_v1`, `data_v2`)
- method/config versioning policy (`lora_v1`, `qlora_v1`)
- prompt/template versioning policy (`prompt_v1`, `prompt_v2`)
- evaluation gate policy (quality/cost/latency thresholds)
- promotion/rollback policy for tuned models

Required runnable checks:

- print config versions in every run
- print base vs tuned delta metrics
- print one failure sample and one corrected sample
- print memory/cost summary for each method
- print final decision (`promote`, `hold`, `rollback`)

---

## 15) Data and Schema Declaration Standard

Every example must include:

```text
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Split/Eval policy: <fixed cases or split rule>
Type: <SFT/LoRA/QLoRA/distill/comparison>
```

Synthetic data must declare generation method and purpose.

---

## 16) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Refactor chapter structure to Stage 7 pattern.
3. Add complexity scale and per-topic complexity notes.
4. Refactor each concept section to module template.
5. Add strict data/schema declaration blocks.
6. Create `red-book/src/stage-8/` ladders and runners.
7. Add SFT/LoRA/QLoRA/distillation operatable tutorials and scripts.
8. Add fine-tuning vs RAG decision and comparison section.
9. Add topic-by-topic industry pain-point matrix with causes, fix strategies, and mapped lab drills.
10. Add evaluation/regression gate section.
11. Upgrade project into fixed deliverable lab format.
12. Add troubleshooting runbook and quality gates.
13. Add weighted self-test and remediation path.
14. Add resource catalog with verification policy.
15. Final QA pass (terminology, encoding, duplicate cleanup).

---

## 17) Acceptance Criteria (Definition of Done)

Stage 8 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script mapping
- all Stage 8 scripts include very detailed, clear comments
- data and schema declarations are present in all examples
- labs are real, operatable, and file-output based
- tuning methods are compared with fixed metrics and fair baselines
- each topic has explicit industry pain points, root causes, and resolution strategy with related lab drill
- chapter includes strict decision framework for prompt vs RAG vs tune
- chapter includes explicit PyTorch/CUDA tuning guidance with CPU fallback
- chapter includes beginning-to-production improvement lab with fixed deliverables
- stage-8 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 18) Additional Improvement Items

### A. Glossary and Notation

- lock notation: `base_model`, `adapter`, `rank`, `prompt_v`, `data_v`, `eval_set`
- add glossary for: SFT, DPO, RFT, LoRA rank, quantization, catastrophic forgetting, regression gate

### B. Reproducibility

- fixed seed policy where randomness exists
- config snapshot policy for every run
- run-date and environment logging policy

### C. Maintenance and QA

- link-check cadence (monthly)
- script smoke-test log template
- chapter changelog section

---

## 19) Priority Breakdown

P0 (must do):

- chapter restructure to operatable format
- Stage 8 script package + runners
- 4+ real labs with fixed deliverables
- strict evaluation and regression gates
- detailed comment standard enforcement
- PyTorch/CUDA section with runnable ladder examples

P1 (should do):

- optional Qdrant comparison lab
- stronger model registry and rollback workflow
- deeper distillation and preference-optimization track

P2 (nice to have):

- distributed training extension (FSDP/DeepSpeed)
- additional cloud adapter examples

---

## 20) Chapter Simplification Blueprint (Mandatory)

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

## 21) Stage Transition Requirement

Handbook must end with `What Comes After Stage 8` and include:

- 2-3 sentence summary of Stage 9 focus
- mapping from Stage 8 skills to Stage 9 tasks
- readiness sentence before progression

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



