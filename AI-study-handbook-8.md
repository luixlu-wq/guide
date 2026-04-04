# Stage 8 - Fine-Tuning Models

(Week 15-16)

## 0) If This Chapter Feels Hard

Use this strict 3-pass learning strategy:

1. Pass 1 (Decision pass)
   - Study Sections 1, 3, and 7 only.
   - Goal: decide when to use prompting, RAG, fine-tuning, or hybrid.
2. Pass 2 (Method pass)
   - Run one method at a time: SFT -> LoRA -> QLoRA -> Distillation.
   - Goal: understand tradeoffs by evidence, not by preference.
3. Pass 3 (Production pass)
   - Run labs and complete promotion/rollback decision.
   - Goal: move from concept to production-like operation.

Do not start from QLoRA. Start from baseline and SFT so comparisons are meaningful.

---

## 1) Learning Targets (Must Achieve)

By the end of Stage 8, you must be able to:

- explain fine-tuning as continued optimization on task-specific distribution
- decide correctly between prompting, RAG, fine-tuning, and hybrid strategy
- design and validate instruction-tuning datasets with schema checks
- run baseline vs tuned comparisons on fixed eval set and fixed config
- explain and apply LoRA/QLoRA tradeoffs in memory, cost, and quality
- explain distillation and evaluate teacher-student tradeoffs
- run PyTorch/CUDA training loops with deterministic CPU fallback
- use regression gates and make promote/hold/rollback decisions
- identify failure type from evidence, compare fixes, and verify before/after deltas

Readiness checkpoint:

- if you cannot explain why a model was promoted (with metrics + thresholds), you are not done.

---

## 2) Prerequisites and Environment (Operatable)

Minimum:

- Python 3.10+
- `pip install -r red-book/src/stage-8/requirements.txt`
- CPU path must work first

Optional GPU path:

- `pip install -r red-book/src/stage-8/requirements-optional.txt`
- CUDA-compatible PyTorch
- `python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`

Run from:

- `red-book/src/stage-8`

Recommended execution order:

1. `powershell -ExecutionPolicy Bypass -File .\run_all_stage8.ps1`
2. `powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1`
3. `powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1 -IncludeLabs`
4. Optional Qdrant comparison:
   - `powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1 -IncludeLabs -IncludeQdrant`

Validation commands:

- core deliverables:
  - `powershell -ExecutionPolicy Bypass -File .\verify_stage8_outputs.ps1`
- include optional Qdrant outputs:
  - `powershell -ExecutionPolicy Bypass -File .\verify_stage8_outputs.ps1 -IncludeQdrant`

---

## 3) Adaptation Decision Framework (Prompt vs RAG vs Tune)

Use this strict decision order:

1. Prompt/system design first.
2. If knowledge freshness/private-doc grounding is missing, add RAG.
3. If behavior/format/style consistency is still weak, apply fine-tuning.
4. If you need both behavior alignment and fresh knowledge, use hybrid.

### Decision Matrix

| Problem pattern | Primary choice | Why |
|---|---|---|
| Format inconsistency | Fine-tuning (SFT/LoRA) | Parameter-level behavior alignment |
| Missing latest knowledge | RAG | External updatable memory |
| Style inconsistency | Fine-tuning | Stable output behavior |
| Unsupported factual claims | RAG + grounding policy | Evidence constraints |
| Inference too expensive | Distillation/quantization | Lower runtime cost |

### Quantitative Trigger Rules (Recommended)

Use these default triggers before starting fine-tuning:

- If prompt-only format-validity < 0.90 and task requires strict schema -> fine-tuning candidate.
- If factual failures come from missing documents/updates -> RAG first (not fine-tuning).
- If prompt-only quality is close to target but cost/latency too high -> distillation candidate.

### Decision Flywheel (Expert Placeholder)

Use this flywheel to avoid over-engineering:

```text
Axes:
- X: data freshness pressure (low -> high)
- Y: task complexity/behavior strictness (low -> high)

Heuristic:
- low freshness + low complexity -> prompt optimization first
- high freshness + low/medium complexity -> RAG first
- low freshness + high behavior strictness -> fine-tuning first
- high freshness + high behavior strictness -> hybrid (RAG + fine-tuning)
```

Operational rule:

- Do not promote an expensive fine-tuning path if the flywheel indicates prompt/RAG can solve target gaps with lower risk.

---

## 3.1) Theory Foundation (Detailed, Mandatory)

Fine-tuning is continued gradient-based optimization on new objective distribution.

Core objective:

- improve target-task behavior while controlling regressions in general behavior and operations.

Why this is difficult:

- data quality dominates results
- optimization can improve train loss while harming real-world generalization
- evaluation can be invalid if baseline and tuned runs are not controlled

Key theory points:

1. SFT: supervised conditional mapping from instruction/input to target output.
2. LoRA:
   - update form: `W' = W + BA`
   - where `B` and `A` are low-rank trainable matrices.
3. QLoRA:
   - base model quantized (often 4-bit variants)
   - adapters remain trainable.
4. Distillation:
   - teacher model supervision for student model tradeoff.
5. Fine-tuning changes behavior patterns more than knowledge freshness.

Practical implication:

- if your core issue is freshness or private evidence, retrieval layer is mandatory.

---

## 4) Data and Schema Declaration Standard (Mandatory)

Every example and lab must declare:

```text
Data: <name and source>
Records: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Split/Eval policy: <fixed split or fixed eval IDs>
Type: <SFT/LoRA/QLoRA/distill/comparison>
```

Synthetic-data note:

- always declare generation method, seed, and purpose.

### Required Dataset Quality Checklist

1. Schema-valid rows only.
2. No duplicate near-identical outputs dominating one class/style.
3. Coverage includes easy, medium, hard, and ambiguous cases.
4. Train/val/test separation is fixed and logged.
5. Label policy is documented in one paragraph.

---

## 5) Example Complexity Scale (Used in All Modules)

- Simple:
  - one method
  - tiny dataset
  - one metric family
- Intermediate:
  - baseline vs tuned
  - controlled hyperparameter changes
  - error analysis
- Advanced:
  - prompt vs RAG vs tune vs hybrid
  - quality/cost/latency tradeoffs
  - promotion and rollback decision

Where complexity lives:

- data quality complexity
- optimization stability complexity
- memory/compute complexity
- evaluation/regression complexity
- operations and release complexity

---

## 6) Detailed Concept Modules (Theory + Operation)

## 6.1 Dataset Design and Governance

What it is:
- Build reliable, representative, schema-valid tuning data.

Why it matters:
- weak data quality causes weak tuning regardless of algorithm.

Industry pain point:
- tuned model works in demo but fails in production traffic.

Root causes:
- narrow scenario coverage
- inconsistent label policy
- hidden contamination between train and eval

Step-by-step workflow:

1. Define task scope and output contract.
2. Create schema validator.
3. Run duplicate and class-balance checks.
4. Freeze split IDs and save snapshot.
5. Audit 30 random records manually.

Expected outputs:

- data declaration printed
- metrics CSV for baseline/tuned
- sample outputs JSONL

Related script:

- `topic01_dataset_quality_intermediate.py`

Worked example (actual run metrics from `red-book/src/stage-8/results`):

- `topic01a_dataset_schema_simple_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated latency: `45.0 ms`
- `topic01_dataset_quality_intermediate_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated latency: `50.0 ms`
- `topic01c_data_governance_advanced_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated latency: `60.0 ms`

How to interpret:

1. This module teaches quality and governance controls, so the main check is delta stability across complexity levels.
2. In this deterministic teaching dataset, tuned performance reaches `1.000`, while baseline stays around `0.625`.
3. If your tuned score is not better than baseline, inspect schema consistency and split contamination first.

---

## 6.2 Instruction Tuning (SFT)

What it is:
- supervised instruction-following adaptation.

Why it matters:
- improves consistency in requested format and style.

Industry pain point:
- quality gain appears on seen prompts but collapses on rephrased prompts.

Root causes:
- template overfitting
- low instruction diversity
- poor hold-out evaluation

Step-by-step workflow:

1. Build baseline output snapshot.
2. Train SFT path on fixed train split.
3. Evaluate on fixed test split.
4. Compare base vs tuned on exact same items.
5. Inspect failure cases and classify errors.

Expected outputs:

- baseline outputs JSONL
- tuned outputs JSONL
- metrics comparison CSV
- error case report markdown

Related script/lab:

- `topic02_sft_intermediate.py`
- `lab01_instruction_tuning_baseline.py`

Worked example (actual run metrics):

- `topic02a_sft_baseline_simple_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `1980 MB`
- `topic02_sft_intermediate_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `2200 MB`
- `topic02c_sft_eval_advanced_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `2640 MB`
- `lab1_metrics_comparison.csv`
  - accuracy delta: `+0.375`
  - f1_macro delta: `+0.4762`
  - format-validity delta: `0.0`

How to interpret:

1. SFT should improve behavior metrics first (accuracy/f1 for this task), not only style impressions.
2. Format-validity already starts at `1.0` in this lab, so quality deltas come from label correctness.
3. If memory budget is constrained, compare SFT with LoRA/QLoRA before final method choice.

---

## 6.3 LoRA

What it is:
- train low-rank adapters instead of full model weights.

Why it matters:
- major reduction in trainable parameters and cost.

Industry pain point:
- unstable results across domains and tasks.

Root causes:
- wrong target modules
- rank too low/high
- no controlled rank sweep

Step-by-step workflow:

1. Select target modules and initial rank.
2. Run rank sweep (`r=4,8,16` minimum).
3. Track quality + memory + latency together.
4. Choose smallest passing configuration.

Expected outputs:

- per-rank metrics rows
- comparison summary
- selected rank rationale

Related script:

- `topic03c_lora_rank_sweep_advanced.py`

Worked example (actual run metrics):

- `topic03a_lora_simple_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `810 MB`
- `topic03_lora_intermediate_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `900 MB`
- `topic03c_lora_rank_sweep_advanced_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `1080 MB`

How to interpret:

1. LoRA path in this stage shows lower memory footprint than SFT path for the same quality target.
2. Treat rank/module sweep as mandatory, even when one configuration already looks strong.
3. Choose the smallest memory configuration that still passes quality gates.

---

## 6.4 QLoRA

What it is:
- quantized base model plus trainable low-rank adapters.

Why it matters:
- enables larger-model adaptation on constrained hardware.

Industry pain point:
- lower memory but quality instability.

Root causes:
- unsafe quantization/runtime settings
- no baseline LoRA comparison
- insufficient stability checks

Step-by-step workflow:

1. Run LoRA baseline first.
2. Run QLoRA with controlled config.
3. Compare quality and operations metrics.
4. Accept QLoRA only if quality gate passes.

Expected outputs:

- LoRA metrics CSV
- QLoRA metrics CSV
- memory/latency report markdown

Related script/lab:

- `topic04_qlora_intermediate.py`
- `lab02_lora_qlora_comparison.py`

Worked example (actual run metrics):

- `topic04a_qlora_simple_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `558 MB`
- `topic04_qlora_intermediate_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `620 MB`
- `topic04c_qlora_memory_tradeoff_advanced_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `744 MB`
- `lab2_lora_metrics.csv` vs `lab2_qlora_metrics.csv`
  - both show accuracy/f1_macro/format-validity at `1.000` in current run

How to interpret:

1. In this controlled setup, QLoRA keeps quality while lowering memory vs LoRA.
2. In real projects, expect some quality risk and validate with the same fixed eval set.
3. Never pick QLoRA only by memory gain; apply regression gates first.

VRAM budgeting for WSL/Windows local training (mandatory):

| Parameter family | Higher value impact | Typical risk | Control action |
|---|---|---|---|
| LoRA rank `r` | increases adapter memory/compute | OOM during backward | start low (`r=4/8`) and sweep upward |
| LoRA `alpha` | can amplify unstable updates | unstable convergence | keep tied to rank policy and validate on fixed eval |
| batch size | major VRAM driver | CUDA OOM/fragmentation | batch ladder + gradient accumulation |
| sequence length | major attention memory driver | silent throughput collapse | cap max length for training stage |

WSL/Windows memory-fragmentation guardrails:

1. Use deterministic batch ladder (`64 -> 32 -> 16 -> 8`) before changing optimizer policy.
2. Log peak VRAM each run and compare by config ID.
3. Prefer one change per rerun; avoid changing rank + batch + sequence simultaneously.

Required telemetry artifact:

- `results/stage8/vram_telemetry_5090.csv`

Required columns:

- `run_id`
- `config_id`
- `device_name`
- `peak_vram_mb`
- `batch_size`
- `rank`
- `alpha`
- `decision`

---

## 6.5 Distillation

What it is:
- transfer behavior from teacher model to smaller student model.

Why it matters:
- reduces inference cost while retaining acceptable quality.

Industry pain point:
- student loses quality on difficult segments.

Root causes:
- weak teacher supervision
- no hard-case coverage
- only aggregate metric tracking

Step-by-step workflow:

1. Generate teacher outputs.
2. Build student training signal.
3. Evaluate teacher and student on fixed eval set.
4. Compare by segment (not only overall score).

Expected outputs:

- teacher outputs JSONL
- student outputs JSONL
- distillation report markdown

Related script/lab:

- `topic05_distill_intermediate.py`
- `lab03_distillation_tradeoff_lab.py`

Worked example (actual run metrics):

- `topic05a_distill_simple_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `432 MB`
- `topic05_distill_intermediate_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `480 MB`
- `topic05c_distill_eval_advanced_metrics.csv`
  - baseline accuracy: `0.625`
  - tuned accuracy: `1.000`
  - simulated memory: `576 MB`
- `lab3_distillation_report.md`
  - teacher accuracy/f1_macro: `1.0 / 1.0`
  - student accuracy/f1_macro: `1.0 / 1.0`

How to interpret:

1. Distillation is acceptable when student quality remains within your tolerance band.
2. Student wins are usually operational (cost/latency), not always quality gains.
3. Always include hard-case segment checks to avoid hidden regressions.

On-device distillation patterns (RTX 5090 advantage):

Goal:

- run teacher-guided supervision and student adaptation with reproducible evidence.

Pattern:

1. Teacher path:
   - large or stronger model generates supervised reasoning targets.
2. Student path:
   - smaller model is adapted on fixed distilled dataset.
3. Verification path:
   - run reasoning-focused eval set before/after student adaptation.

Mandatory metric:

- `reasoning_pass_rate`
  - percentage of reasoning test cases that meet expected output criteria.

Required comparison:

- student baseline `reasoning_pass_rate`
- student distilled `reasoning_pass_rate`
- delta and decision (`promote`/`hold`/`rollback`)

Required artifact:

- `results/stage8/forgetting_test_results.jsonl`

---

## 6.6 PyTorch and CUDA in Fine-Tuning (Mandatory)

Conceptual loop:

1. Move tensors/model to `cpu` or `cuda`.
2. Forward pass -> logits.
3. Loss calculation.
4. Backward pass -> gradients.
5. Optimizer step.

Industry pain point:
- CUDA OOM/device mismatch interrupts training.

Root causes:
- mixed-device tensors
- excessive batch size
- missing memory strategy

Resolution workflow:

1. print selected device at run start
2. assert tensor-device consistency
3. use batch-size ladder and accumulation
4. enable AMP only after baseline stability
5. keep CPU fallback for all scripts

Related scripts:

- `topic00a_pytorch_cuda_tuning_simple.py`
- `topic00_pytorch_cuda_tuning_intermediate.py`
- `topic00c_pytorch_cuda_tuning_advanced.py`

Worked example (actual run metrics):

- `topic00a_pytorch_cuda_tuning_simple_metrics.csv`
  - device: `cpu`
  - final_loss: `0.327534`
  - duration: `9.72 ms`
- `topic00_pytorch_cuda_tuning_intermediate_metrics.csv`
  - device: `cpu`
  - final_loss: `0.109524`
  - duration: `17.87 ms`
- `topic00c_pytorch_cuda_tuning_advanced_metrics.csv`
  - device: `cpu`
  - final_loss: `0.062524`
  - duration: `31.33 ms`

How to interpret:

1. As loop complexity increases, final_loss should decrease on this synthetic task.
2. Runtime increases with complexity; compare only within same hardware/device.
3. If CUDA is available on your machine, device may show `cuda` and timing profile will differ.

---

## 6.7 Evaluation and Regression Gates

Minimum metrics:

- quality:
  - accuracy or task correctness
  - format-validity rate
  - consistency indicator
  - perplexity
  - training_loss_vs_val_loss gap
- retrieval path (if hybrid):
  - hit@k
  - recall@k
  - citation support rate
- operations:
  - latency p50/p95
  - cost per query
  - failure rate
  - vram_peak

Recommended promotion thresholds (starter policy):

1. quality:
   - no drop in primary quality metric
2. format:
   - format-validity >= baseline
3. operations:
   - p95 latency increase <= 20%
   - cost/query increase <= 20%
4. reliability:
   - failure rate not worse than baseline

Knowledge-retention gate (mandatory for domain tuning):

- After domain-specific tuning (for example Ontario GIS vocabulary), run a general-capability holdout test.
- Fail gate if general-capability accuracy drops by more than `3%` from baseline.

Retention gate rule:

1. Compute `general_accuracy_baseline`.
2. Compute `general_accuracy_tuned`.
3. If `(baseline - tuned) > 0.03`, decision must be `hold` or `rollback`.

Industry pain point:
- model promoted because outputs look better in manual spot checks.

Resolution workflow:

1. freeze eval set and versions
2. run baseline and candidate
3. compute deltas
4. apply thresholds
5. decision: promote / hold / rollback

Related script:

- `topic07c_promotion_gate_advanced.py`
- `topic07d_forgetting_gate_advanced.py` (planned extension)

Worked example (actual run metrics):

- `topic07a_eval_basics_simple_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
- `topic07_eval_regression_intermediate_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
- `topic07c_promotion_gate_advanced_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
- `lab4_metrics_comparison.csv`
  - accuracy delta: `+0.3667`
  - f1_macro delta: `+0.4516`
  - format-validity delta: `0.0`

How to interpret:

1. Promotion decision should reference explicit deltas, not subjective review.
2. In this run, quality and format gates pass, enabling promotion.
3. If one critical metric regresses, hold or rollback by policy.

---

## 6.8 Local Alignment Bridge (DPO vs PPO)

What it is:
- preference-based post-training to improve helpfulness/safety/style alignment.

Why it matters:
- fine-tuning knowledge/format is not sufficient when human preference alignment is weak.

2026 practical recommendation:
- start with DPO for local alignment because it is simpler to operate than PPO in most small-team workflows.

DPO vs PPO operational comparison:

| Method | Strength | Typical cost/complexity | Best use |
|---|---|---|---|
| DPO | simpler implementation with preference pairs | lower pipeline complexity | local alignment improvement loops |
| PPO | flexible policy optimization | higher system complexity | advanced RLHF pipelines with mature infra |

Preference data contract:

- `prompt`
- `chosen_response`
- `rejected_response`
- `policy_tags` (optional)

Required output artifact:

- `results/stage8/dpo_preference_eval.csv`

---

## 6.9 Adapter Merging and Task Arithmetic

What it is:
- combine multiple task-specific adapters into one deployable artifact.

Why it matters:
- real projects often need multi-capability behavior (for example domain formatting + translation/localization) without retraining from scratch.

Operational workflow:

1. train/prepare adapter A and adapter B.
2. merge adapters with one reproducible strategy.
3. evaluate merged model on both task sets.
4. block promotion if either task regresses beyond threshold.

Required output artifact:

- `results/stage8/adapter_merge_matrix.csv`

---

## 6.10 Synthetic Data Curation (Self-Instruct Pattern)

What it is:
- use model-generated instruction/response pairs as supervised training data after quality curation.

Why it matters:
- high-quality human labels are expensive; synthetic-data pipelines are now common in local enterprise workflows.

Curation workflow:

1. generate synthetic pairs with fixed prompt templates.
2. dedupe and remove near-duplicates.
3. apply schema and safety filters.
4. score quality and keep only passing records.
5. freeze synthetic dataset version for reproducible tuning.

Required output artifact:

- `results/stage8/synthetic_data_curation_report.md`

---

## 6.11 Advanced Memory Management (Flash Attention 3 + Checkpointing)

What it is:
- memory-efficiency controls for larger context windows and stable local training runs.

Why it matters:
- high-end GPUs still hit OOM under long context and large batch combinations, especially in multi-process local workflows.

Required techniques in this chapter:

1. flash-attention optimized path (when runtime/platform supports it).
2. gradient checkpointing to trade compute for memory.
3. batch ladder (`64 -> 32 -> 16 -> 8`) before changing optimizer policy.
4. deterministic OOM fallback policy with rerun logging.

Required output artifact:

- `results/stage8/flashattn_checkpointing_benchmark.csv`

---

## 6.12 Industry Operations and Lifecycle Management

What it is:
- deploy tuned models with controlled risk.

Key controls:

- experiment/version tracking
- canary release
- rollback path
- continuous monitoring

Industry pain point:
- offline gains, production regressions.

Root causes:
- no canary or rollback strategy
- weak observability and alert thresholds

Resolution workflow:

1. register model + config versions
2. deploy to small traffic slice
3. monitor quality/cost/latency/failure
4. rollback on gate violation

Related script/lab:

- `topic08c_canary_rollback_advanced.py`
- `lab04_finetune_project_baseline_to_production.py`

Worked example (actual run metrics):

- `topic08a_model_registry_simple_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
  - simulated latency: `48.0 ms`
- `topic08_ops_observability_intermediate_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
  - simulated latency: `53.33 ms`
- `topic08c_canary_rollback_advanced_metrics.csv`
  - baseline accuracy/f1: `0.625 / 0.5238`
  - tuned accuracy/f1: `1.000 / 1.000`
  - simulated latency: `64.0 ms`
- `lab4_verification_report.md`
  - quality gate pass: `True`
  - format gate pass: `True`
  - decision: `promote`

How to interpret:

1. Operations module combines quality and runtime behavior for release readiness.
2. Canary and rollback controls are required even when offline quality is strong.
3. Production decision must be traceable to gate outputs in report files.

---

## 7) Industry Pain-Point Playbooks (Detailed)

## 7.1 Fine-Tuning Too Early

- Symptom: tuning project starts before baseline diagnosis.
- Causes: no decision rubric, subjective urgency.
- Fix: enforce prompt -> RAG -> tune sequence with metrics at each stage.
- Lab: `topic06a_prompt_vs_tune_simple.py`

## 7.2 Data Leakage in Tuning Evaluation

- Symptom: tuned score looks excellent but production behavior is weak.
- Causes: overlap across train/test, duplicated templates.
- Fix: split by scenario IDs and run leakage checks.
- Lab: `topic01_dataset_quality_intermediate.py`

## 7.3 LoRA Rank Instability

- Symptom: performance swings across runs.
- Causes: arbitrary rank/module choices.
- Fix: rank sweep with gate-based selection.
- Lab: `topic03c_lora_rank_sweep_advanced.py`

## 7.4 QLoRA Quality Regressions

- Symptom: lower memory but weaker outputs.
- Causes: aggressive quantization without baseline controls.
- Fix: direct LoRA vs QLoRA comparison on same eval IDs.
- Lab: `lab02_lora_qlora_comparison.py`

## 7.5 Student Collapse in Distillation

- Symptom: fast model but poor edge-case behavior.
- Causes: weak teacher labels or missing hard cases.
- Fix: hard-case segments and segment-wise metrics.
- Lab: `lab03_distillation_tradeoff_lab.py`

## 7.6 Production Release Risk

- Symptom: promoted model causes cost spike or quality drop.
- Causes: no release gates, no rollback criteria.
- Fix: canary + monitoring + rollback playbook.
- Lab: `lab04_finetune_project_baseline_to_production.py`

---

## 8) Stage 8 Script Mapping (`red-book/src/stage-8`)

Core ladders (simple -> intermediate -> advanced):

0. PyTorch/CUDA tuning
- `topic00a_pytorch_cuda_tuning_simple.py`
- `topic00_pytorch_cuda_tuning_intermediate.py`
- `topic00c_pytorch_cuda_tuning_advanced.py`

1. Data and governance
- `topic01a_dataset_schema_simple.py`
- `topic01_dataset_quality_intermediate.py`
- `topic01c_data_governance_advanced.py`

2. SFT
- `topic02a_sft_baseline_simple.py`
- `topic02_sft_intermediate.py`
- `topic02c_sft_eval_advanced.py`

3. LoRA
- `topic03a_lora_simple.py`
- `topic03_lora_intermediate.py`
- `topic03c_lora_rank_sweep_advanced.py`

4. QLoRA
- `topic04a_qlora_simple.py`
- `topic04_qlora_intermediate.py`
- `topic04c_qlora_memory_tradeoff_advanced.py`

5. Distillation
- `topic05a_distill_simple.py`
- `topic05_distill_intermediate.py`
- `topic05c_distill_eval_advanced.py`

6. Strategy comparison
- `topic06a_prompt_vs_tune_simple.py`
- `topic06_tune_vs_rag_intermediate.py`
- `topic06c_hybrid_strategy_advanced.py`

7. Evaluation and regression
- `topic07a_eval_basics_simple.py`
- `topic07_eval_regression_intermediate.py`
- `topic07c_promotion_gate_advanced.py`

8. Operations
- `topic08a_model_registry_simple.py`
- `topic08_ops_observability_intermediate.py`
- `topic08c_canary_rollback_advanced.py`

9. Alignment and merging
- `topic09a_dpo_foundations_simple.py`
- `topic09_dpo_intermediate.py`
- `topic09c_dpo_eval_advanced.py`
- `topic10a_adapter_merge_simple.py`
- `topic10_adapter_merge_intermediate.py`
- `topic10c_task_arithmetic_advanced.py`

10. Synthetic-data and memory
- `topic11a_synthetic_data_simple.py`
- `topic11_synthetic_data_curation_intermediate.py`
- `topic11c_synthetic_data_governance_advanced.py`
- `topic12a_memory_basics_simple.py`
- `topic12_memory_optimization_intermediate.py`
- `topic12c_flashattn_checkpointing_advanced.py`

9. Labs
- `lab01_instruction_tuning_baseline.py`
- `lab02_lora_qlora_comparison.py`
- `lab03_distillation_tradeoff_lab.py`
- `lab04_finetune_project_baseline_to_production.py`
- `lab05_finetune_vs_rag_vs_hybrid_qdrant.py` (optional local Qdrant track)

Hard requirements:

- all scripts include very detailed functional comments
- all scripts print data/schema declarations
- all scripts print metrics and interpretation text
- all scripts include deterministic rerun settings

---

## 9) Practice Labs (Detailed and Operatable)

## Lab 1: Instruction Tuning Baseline

Goal:
- compare base model vs tuned model on fixed task.

Required workflow:

1. freeze dataset and eval IDs
2. run baseline snapshot
3. run tuned path
4. compare metrics
5. inspect error cases

Required outputs:

- `results/lab1_base_outputs.jsonl`
- `results/lab1_tuned_outputs.jsonl`
- `results/lab1_metrics_comparison.csv`
- `results/lab1_error_cases.md`

## Lab 2: LoRA vs QLoRA

Goal:
- compare quality/memory/latency tradeoffs.

Required workflow:

1. run LoRA path
2. run QLoRA path
3. compare quality first
4. compare memory/latency next
5. choose preferred method by gate policy

Required outputs:

- `results/lab2_lora_metrics.csv`
- `results/lab2_qlora_metrics.csv`
- `results/lab2_memory_latency_report.md`
- `results/stage8/vram_telemetry_5090.csv`
- `results/stage8/sft_vs_qlora_delta.md`

## Lab 3: Distillation Tradeoff

Goal:
- compare teacher vs student quality and cost profile.

Required workflow:

1. generate teacher outputs
2. train student with distillation signal
3. evaluate both on fixed set
4. inspect hard-case segment behavior

Required outputs:

- `results/lab3_teacher_outputs.jsonl`
- `results/lab3_student_outputs.jsonl`
- `results/lab3_distillation_report.md`
- `results/stage8/forgetting_test_results.jsonl`
- `results/stage8/dpo_preference_eval.csv` (extension track)

## Lab 4: Baseline to Production Improvement

Goal:
- improve a realistic tuning project with controlled fixes and promotion decision.

Required workflow:

1. baseline measurement
2. failure classification
3. option comparison (at least 2)
4. one controlled improvement
5. gate check and decision

Required outputs:

- `results/lab4_project_baseline_outputs.jsonl`
- `results/lab4_project_improved_outputs.jsonl`
- `results/lab4_solution_options.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_verification_report.md`
- `results/lab4_production_readiness.md`
- `results/stage8/model_promotion_report.md`
- `results/stage8/adapter_merge_matrix.csv` (extension track)
- `results/stage8/synthetic_data_curation_report.md` (extension track)
- `results/stage8/flashattn_checkpointing_benchmark.csv` (extension track)

## Lab 5: Fine-Tuning vs RAG vs Hybrid (Optional Qdrant)

Goal:
- compare tuned-only, RAG-only, and hybrid pipelines.

Required workflow:

1. run prompt-only baseline
2. run RAG path
3. run tuned path
4. run hybrid path
5. choose deployment strategy by evidence

Required outputs:

- `results/lab5_compare_prompt_rag_tune.csv`
- `results/lab5_qdrant_retrieval_metrics.csv`
- `results/lab5_final_decision.md`

Lab rules:

1. fixed dataset and fixed eval IDs
2. fixed config versions (`data_v`, `prompt_v`, `method_v`)
3. one controlled change per rerun
4. explicit before/after deltas

---

## 10) Troubleshooting and Failure Playbook

Required failure drills:

- malformed dataset rows
- prompt-template mismatch (train vs eval)
- overfitting on small data
- no measurable gain vs baseline
- format-validity regression
- catastrophic forgetting indicators
- unstable loss
- CUDA OOM/device mismatch
- QLoRA instability
- cost/latency regression
- ghost-loss pattern (loss decreases while output quality/format collapses)
- alignment drift (model becomes overly safe/rigid or loses desired style)
- mode collapse (model repeats patterns/tokens due to unstable or repetitive training data)

Required incident workflow:

1. reproduce with fixed eval IDs and run ID
2. classify failure type from evidence
3. inspect data/schema and split integrity
4. inspect method config and optimization settings
5. inspect metric deltas and failure examples
6. compare at least 2 fix options and tradeoffs
7. apply one fix only
8. rerun and capture before/after deltas
9. decision: promote / hold / rollback

Ghost-loss troubleshooting drill (mandatory):

Symptom:

- training/validation loss looks healthy, but generated text degrades (repetition, broken format, unstable structure).

Common causes:

1. objective mismatch (loss does not reflect deployment output constraints)
2. template drift between train and eval/prompt runtime
3. insufficient periodic qualitative validation

Fix protocol:

1. Every 50 steps, run fixed validation samples and save outputs.
2. Compare output format-validity and semantic correctness against baseline.
3. If loss improves but output quality degrades, hold training promotion and inspect data/template consistency first.

Required logs per run:

- run/config version IDs
- dataset split/version IDs
- method (`SFT/LoRA/QLoRA/distill/hybrid`)
- quality metrics
- memory/latency/cost
- perplexity
- training_loss_vs_val_loss
- vram_peak
- failure class and chosen fix

---

## 11) Regression Gates and Promotion Policy

Starter gate policy (adjust by task):

- Primary quality metric: no regression allowed.
- Format-validity: no regression allowed.
- Cost/query: increase <= 20% unless explicitly approved.
- p95 latency: increase <= 20% unless explicitly approved.
- Failure rate: must not worsen.
- General capability retention: drop must be <= 3%.

Decision outcomes:

- `promote`: all gates pass.
- `hold`: mixed results, needs another controlled experiment.
- `rollback`: critical gates fail.

Mandatory promotion deliverable:

- `results/stage8/model_promotion_report.md`

Required sections:

1. baseline model vs tuned model (same fixed eval set)
2. primary quality metrics and deltas
3. retention gate results (including forgetting check)
4. cost/latency comparison
5. final decision with rationale and rollback condition

---

## 12) Minimal Operatable Baseline Workflow

Use this as first executable path:

1. Build fixed dataset (`train.jsonl`, `val.jsonl`, `test.jsonl`).
2. Run base model and save outputs.
3. Run one SFT path.
4. Evaluate on fixed test set.
5. Compare metrics and decide if gain is real.

Mandatory comparison outputs:

- format-validity delta
- task-quality delta
- latency/cost delta
- one failure case before/after

---

## 13) Resource Library (High Priority)

Core implementation docs:

- https://platform.openai.com/docs/guides/fine-tuning
- https://platform.openai.com/docs/api-reference/fine-tuning
- https://huggingface.co/docs/transformers/training
- https://huggingface.co/docs/peft/quicktour
- https://huggingface.co/docs/trl/sft_trainer
- https://huggingface.co/docs/transformers/quantization/bitsandbytes
- https://docs.pytorch.org/docs/stable/notes/cuda.html
- https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- https://huggingface.co/docs/accelerate/index

Theory and papers:

- https://arxiv.org/abs/2106.09685
- https://arxiv.org/abs/2305.14314
- https://arxiv.org/abs/2203.02155
- https://arxiv.org/abs/2212.10560
- https://arxiv.org/abs/2210.11416
- https://arxiv.org/abs/2305.18290
- https://arxiv.org/abs/1503.02531

Industry and operations references:

- https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-fine-tune.html
- https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning
- https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models
- https://mlflow.org/docs/latest/ml/model-registry/
- https://docs.wandb.ai/models/registry
- https://opentelemetry.io/docs/

Books and structured courses:

- https://www.oreilly.com/library/view/build-a-large/9781633437166/
- https://www.oreilly.com/library/view/natural-language-processing/9781098136789/
- https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/
- https://huggingface.co/learn/nlp-course
- https://www.deeplearning.ai/short-courses/finetuning-large-language-models/

---

## 14) Self-Test (Weighted)

Scoring:

- decision framework accuracy: 25%
- method understanding (SFT/LoRA/QLoRA/distill): 30%
- evaluation/regression discipline: 25%
- operations and troubleshooting: 20%

Questions:

1. When should you choose fine-tuning over RAG?
2. Why can LoRA improve cost-efficiency vs full fine-tuning?
3. What does QLoRA change compared with LoRA?
4. Why can tuned models fail despite lower training loss?
5. What fixed artifacts are required for fair baseline vs tuned comparison?
6. Which metrics are mandatory before model promotion?
7. What signals suggest catastrophic forgetting?
8. How do you handle CUDA OOM without invalidating fairness?

Pass rule:

- at least 75/100
- no critical miss on decision framework and regression-gate questions

---

## 15) What Comes After Stage 8

Stage 9 focuses on model serving, deployment patterns, and production reliability engineering.

Stage 8 to Stage 9 mapping:

- adaptation decisions -> service architecture decisions
- regression gates -> deployment gates
- troubleshooting drills -> incident response readiness

Readiness check:

- if you can run one full tuning lab and justify promotion/rollback with evidence, move to Stage 9.
