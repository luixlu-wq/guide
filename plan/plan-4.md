# Stage 4 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-4.md`  
Plan owner: You + Codex  
Version date: 2026-04-03

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-4.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Chapter 4 is hard to understand; collect more high-quality information and design the best practical improvement path.
- Add detailed explanation and demonstration for core deep learning concepts.
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

Carry-over quality requirements from successful Stage 3 pattern (apply to Stage 4):

- Add more example code for each topic, from simple to complicated.
- Add clear functional comments to all Stage 4 topic scripts.
- Add and enforce `Example Complexity Scale (Used In All Modules)` and explicit `where complexity is` explanation per topic.
- Make practice project section clear and operatable with exact workflow and deliverables.
- PyTorch and CUDA content must include detailed step-by-step instruction and ladder-complexity examples.

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

## 1) Review Summary (Chapter 4 Current State)

### What is already strong

- Good topic coverage: neural nets, forward/loss/backprop/optimizer, CNN, RNN, Transformer.
- Includes a project and self-test.
- Motivation and beginner framing are present.

### What still needs improvement

- Chapter is concept-heavy and still hard to operate as a study system.
- No explicit complexity ladder (simple -> intermediate -> advanced) for most topics.
- No Stage 4 runnable script package (`red-book/src/stage-4/`) yet.
- Practice project is still broad and can be made more executable with stricter outputs.
- Missing explicit concept-to-code mapping for tensor shapes, gradients, and training loop errors.
- Missing strict debugging flow for deep learning failure modes (shape mismatch, no-grad, exploding/vanishing gradients, LR instability).
- GPU/CUDA section needs stronger instruction depth and verification flow.
- Encoding artifacts exist in chapter text (mojibake), reducing readability.

---

## 2) Target Outcomes (Measurable)

Stage 4 rewrite is complete only when:

- Learner can explain and execute the 5-step deep learning loop:
  - device placement
  - forward pass
  - loss computation
  - backward pass
  - optimizer step
- Every core topic has simple/intermediate/advanced runnable examples.
- Every Stage 4 script has:
  - data declaration
  - clear workflow comments
  - expected output notes
- Chapter includes explicit tensor-shape checkpoints for all model families.
- Practice project has fixed workflow, fixed outputs, and reproducibility notes.
- Stage 4 scripts run with fail-fast runner and optional GPU bridge runner.
- Self-test has weighted scoring and remediation path.

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

- FastAI Practical Deep Learning for Coders
  - https://course.fast.ai/
- Google ML Crash Course - Neural Networks module
  - https://developers.google.com/machine-learning/crash-course/neural-networks
- PyTorch Learn the Basics index
  - https://docs.pytorch.org/tutorials/beginner/basics/index.html
- PyTorch Quickstart
  - https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
- PyTorch Build Model tutorial
  - https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
- PyTorch Autograd tutorial
  - https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html
- PyTorch Optimization tutorial
  - https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
- PyTorch Data tutorial
  - https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html
- Stanford CS231n (deep learning for vision)
  - https://cs231n.stanford.edu/
- Dive into Deep Learning
  - https://d2l.ai/

### B. Official Docs (Implementation-First)

- PyTorch CUDA semantics
  - https://docs.pytorch.org/docs/stable/notes/cuda.html
- `torch.cuda.is_available`
  - https://docs.pytorch.org/docs/stable/generated/torch.cuda.is_available.html
- `torch.utils.data` reference
  - https://docs.pytorch.org/docs/stable/data.html
- `torch.nn.CrossEntropyLoss`
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
- `torch.optim.Adam`
  - https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html
- `torch.nn.Transformer`
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html
- PyTorch AMP examples
  - https://docs.pytorch.org/docs/stable/notes/amp_examples.html
- PyTorch AMP recipe
  - https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- PyTorch performance tuning guide
  - https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html
- Google Deep Learning Tuning Playbook
  - https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook

### C. Books and Papers (Priority Order)

- Deep Learning (Goodfellow, Bengio, Courville)
  - https://www.deeplearningbook.org/
- D2L (book + notebooks)
  - https://d2l.ai/
- Attention Is All You Need
  - https://arxiv.org/abs/1706.03762
- Deep Residual Learning (ResNet)
  - https://arxiv.org/abs/1512.03385
- Adam: A Method for Stochastic Optimization
  - https://arxiv.org/abs/1412.6980
- Batch Normalization
  - https://arxiv.org/abs/1502.03167
- Dropout
  - https://arxiv.org/abs/1207.0580
- Sequence to Sequence Learning with Neural Networks
  - https://arxiv.org/abs/1409.3215
- Long Short-Term Memory (original paper PDF)
  - https://www.bioinf.jku.at/publications/older/2604.pdf

### D. Practical Repos and Ecosystem Resources

- PyTorch examples
  - https://github.com/pytorch/examples
- PyTorch tutorials repo
  - https://github.com/pytorch/tutorials
- Hugging Face Transformers docs
  - https://huggingface.co/docs/transformers/index
- Hugging Face Transformers repo
  - https://github.com/huggingface/transformers
- nanoGPT (educational transformer training)
  - https://github.com/karpathy/nanoGPT
- Karpathy training recipe
  - https://karpathy.github.io/2019/04/25/recipe/

### E. Resource-to-Stage Mapping (Week 7-9)

- Week 7 foundations:
  - MLCC neural nets + PyTorch basics (quickstart/build/autograd/optimization)
- Week 8 architectures:
  - CS231n + D2L architecture chapters + `nn.Transformer` docs
- Week 9 tuning/debug/project:
  - Google DL tuning playbook + PyTorch AMP/tuning guides + practical repos

### F. Time Budget (Must / Should / Optional)

Must:

- PyTorch basics path + coding: 10-14h
- MLCC neural networks + DL tuning playbook: 4-6h
- Core architecture modules (MLP/CNN/RNN/Transformer) with scripts: 10-14h

Should:

- CS231n + D2L selected chapters: 8-12h
- Papers (Attention/ResNet/Adam/BatchNorm/Dropout): 5-8h

Optional:

- Hugging Face + nanoGPT deep dive: 6-10h

Recommended Stage 4 budget:

- Minimum track: 36-48h
- Strong track: 50-70h

---

## 4) New Handbook Structure (Required)

1. How to Use This Chapter (if you feel lost)
2. Prerequisites and Environment Setup (CPU + optional CUDA)
3. Deep Learning Foundations (neuron, forward, loss, backprop, optimizer)
4. Example Complexity Scale + Where Complexity Is
5. Model Family Modules (MLP, CNN, RNN/GRU/LSTM, Transformer)
6. Deep Learning Debugging Playbook
7. Practice Project Lab (operatable workflow + deliverables)
8. Self-Test + weighted scoring rubric
9. What Comes After Stage 4

Section requirements:

- Section 1 must include a 4-pass learning flow (problem -> intuition -> mechanics -> code).
- Section 4 must explicitly define `simple/intermediate/advanced` and complexity dimensions.
- Section 7 must include exact outputs and acceptance checks.

### Stage 4 Complexity Scale Extension (Hardware-Aware, Mandatory)

Use the existing `simple -> intermediate -> advanced` ladder and add this compute dimension:

- `Simple (CPU-friendly)`:
  - NumPy-only backprop walkthrough or tiny MLP
  - objective is concept correctness, not throughput
- `Intermediate (single-GPU baseline)`:
  - standard PyTorch `nn.Module` training loop
  - CUDA optional, CPU fallback required
- `Advanced (RTX 5090 optimized)`:
  - AMP + gradient accumulation + profiler-driven tuning
  - includes memory/latency evidence and throughput comparison

For every topic, include:

- where complexity is in `model`, `data`, `optimization`, and `compute path`
- one explicit statement of when CPU is still preferable
- one explicit statement of when GPU acceleration is justified

---

## 5) Concept Module Template (Mandatory)

Every module must include:

- What it is
- Why it matters
- Data declaration block
- Shape declaration block
- Worked example
- Assumptions and limits
- Common beginner mistake + fix
- Demonstration checklist
- Quick check
- When to use / when not to use

Core Stage 4 modules:

- Neural network basics (layers, activation, parameters)
- 5-step training loop (device/forward/loss/backward/step)
- Backprop intuition + autograd mechanics
- Optimizers and learning rate behavior
- CNN basics + pooling + feature maps
- RNN/GRU/LSTM sequence intuition
- Transformer basics (QKV, attention, positional encoding)
- GPU/CUDA/AMP basics and pitfalls
- computation graph tracing (forward graph -> backward gradients)
- activation comparison (Sigmoid/Tanh/ReLU) and vanishing-gradient intuition
- Overfitting/underfitting in deep learning
- Train vs eval mode and checkpointing

Hard requirement: no module ships with missing fields.

---

## 6) Operable Roadmap (Week 7-9)

### Week 7 (Foundations and Loop Control)

- Day 1: tensors/devices/shapes
- Day 2: forward/loss/backward/optimizer anatomy
- Day 3: autograd and gradient checks
- Day 4: optimizer and learning rate experiments
- Day 5: train/eval mode and checkpoint basics
- Day 6: failure drills (shape mismatch, no-grad)
- Day 7: recap and written concept checks

### Week 8 (Model Families)

- Day 8: MLP on tabular or FashionMNIST
- Day 9: CNN for image classification
- Day 10: RNN/GRU/LSTM for sequence classification
- Day 11: Transformer encoder basics
- Day 12: compare model families on one controlled task
- Day 13-14: architecture summary and error analysis

### Week 9 (Project and Performance)

- Day 15-17: implement project baseline
- Day 18: add one architecture variant
- Day 19: add one optimization/tuning variant
- Day 20: final report and reproducibility notes
- Day 21: self-test and readiness decision

---

## 7) Stage 4 Script Package Plan (`red-book/src/stage-4/`)

Required files:

- `README.md`
- `requirements.txt`
- `requirements-gpu.txt`
- `run_all_stage4.ps1`
- `run_ladder_stage4.ps1`

Core ladders (simple -> intermediate -> advanced):

1. Training loop anatomy
- `topic01a_loop_anatomy_simple.py`
- `topic01_loop_anatomy.py`
- `topic01c_loop_anatomy_advanced.py`

2. MLP ladder
- `topic02a_mlp_simple.py`
- `topic02_mlp_intermediate.py`
- `topic02c_mlp_advanced.py`

3. CNN ladder
- `topic03a_cnn_simple.py`
- `topic03_cnn_intermediate.py`
- `topic03c_cnn_advanced.py`

4. RNN/GRU/LSTM ladder
- `topic04a_rnn_simple.py`
- `topic04_rnn_intermediate.py`
- `topic04c_rnn_advanced.py`

5. Transformer ladder
- `topic05a_transformer_simple.py`
- `topic05_transformer_intermediate.py`
- `topic05c_transformer_advanced.py`

6. CUDA/AMP ladder (optional)
- `topic06a_cuda_simple.py`
- `topic06_cuda_intermediate.py`
- `topic06c_cuda_amp_advanced.py`

7. Diagnostics and project support
- `topic07_failure_modes.py`
- `topic08_project_baseline.py`

8. Data pipeline and hardware profiling support
- `topic09_dataset_dataloader_pipeline.py`
- `topic10_vram_math_and_profiler.py`

Script requirements:

- All scripts must include clear `# Workflow:` comments.
- All scripts must print data/shape declarations.
- All scripts must print expected metrics and short interpretation text.
- All scripts must include schema-contract headers:
  - `Data Source`
  - `Schema`
  - `Preprocessing`
  - `Null Handling`
- All baseline scripts must output one diagnosis line (for example: `underfit`, `overfit`, `unstable gradients`, `data pipeline bottleneck`).

---

## 8) Practice Project Spec (Clear and Operatable)

Project goal:

- Train and compare at least 2 deep architectures on one defined task and justify final choice.

Recommended default track:

- Dataset: FashionMNIST
- Task: multi-class image classification
- Models: MLP baseline + CNN baseline (+ optional transformer-style baseline)

Required workflow:

1. Declare dataset and shape (`N, C, H, W`, number of classes).
2. Use fixed split strategy and fixed random seeds.
3. Define one baseline model and one improved model.
4. Train both with same epoch budget and comparable settings.
5. Log train/validation loss and accuracy per epoch.
6. Add one controlled improvement (augmentation, regularization, lr schedule, architecture change).
7. Rerun and compare before/after.
8. Write final model selection rationale with tradeoffs.
9. Include one hardware-awareness experiment:
   - compare CPU vs CUDA path for at least one training or tensor workload
   - record transfer time, compute time, total time, and peak memory
10. Include one optimization experiment:
   - before: standard FP32 or untuned LR
   - after: AMP and/or scheduler and/or gradient accumulation
   - report before/after delta with same evaluation protocol

Required deliverables:

- `results/metrics_before.csv`
- `results/metrics_after.csv`
- `results/learning_curves.png`
- `results/error_analysis.md`
- `results/final_choice.md`
- `results/reproducibility.md`
- `results/hardware_profile.csv`
- `results/hardware_decision.md`
- `results/evidence_schema_metrics.csv`

Minimum acceptance checks:

- Same split/seed policy across compared runs
- At least 2 models compared
- Before/after improvement evidence exists
- One concrete failure diagnosis + fix is documented
- Evidence schema fields include `run_id`, `before_value`, `after_value`, `delta`
- Hardware profile includes memory and timing evidence

### 8.1 Stage-Specific Industry Pain-Point Matrix (Mandatory)

| Topic | Typical industry pain point | Common root causes | Resolution strategy (operatable) | Verification evidence | Mapped script/lab |
|---|---|---|---|---|---|
| Training loop anatomy | Model runs but gradients are wrong | Incorrect zero_grad/backward/step ordering | Enforce 5-step loop checklist and gradient sanity checks | Gradient norm and loss trend report | `topic01_loop_anatomy.py` |
| MLP baseline | Accuracy stalls early | Weak normalization/learning-rate setup | Tune LR and normalization with fixed epochs | Learning-curve comparison | `topic02_mlp_intermediate.py` |
| CNN module | CNN performs worse than MLP on images | Bad shape handling and augment mismatch | Add shape assertions and augmentation audit | Shape trace + augmentation effect table | `topic03_cnn_intermediate.py` |
| RNN/sequence modeling | Sequence model unstable or slow | Long dependency issues and batching problems | Apply sequence-length policy + gradient clipping | Sequence loss stability report | `topic04_rnn_intermediate.py` |
| Transformer basics | Attention code works but predictions unstable | Mask/position handling errors | Add mask/position validation tests | Attention mask validity report | `topic05_transformer_intermediate.py` |
| CUDA/AMP | GPU path faster but numerically unstable | AMP misuse and overflow handling gaps | Add AMP guardrails and fallback execution path | CPU/GPU/AMP comparison report | `topic06_cuda_intermediate.py` |
| Activation dynamics | Deep network stops learning | Dying ReLU or saturated Sigmoid/Tanh | Add activation audit + initialization/LR review | Activation output histogram + gradient norm report | `topic02c_mlp_advanced.py`, `topic07_failure_modes.py` |
| Gradient stability | Loss spikes or diverges | Exploding gradients and LR instability | Add gradient clipping + LR schedule comparison | Before/after loss stability and gradient norms | `topic07_failure_modes.py` |
| Data pipeline throughput | GPU utilization low despite large model | DataLoader bottleneck and host-device transfer inefficiency | Tune `num_workers`, `pin_memory`, `non_blocking=True`, batch sizing | Loader throughput + step-time table | `topic09_dataset_dataloader_pipeline.py` |
| VRAM planning | OOM in local training despite large VRAM | Incorrect parameter/activation/optimizer-state memory assumptions | Add VRAM math script + validate with runtime memory stats | Estimated vs observed VRAM report | `topic10_vram_math_and_profiler.py` |
| Failure modes | Team cannot localize deep learning failures | No failure taxonomy | Use structured failure drill and one-change rerun | Failure diagnosis and fix log | `topic07_failure_modes.py` |
| Project baseline to improvement | Final model chosen without evidence | Missing baseline-vs-improved protocol | Enforce fixed baseline, one controlled improvement, and decision gate | Before/after metrics + final rationale | `topic08_project_baseline.py` |

### 8.2 Required Matrix Usage Workflow

1. Reproduce issue with fixed seed/data split and run ID.
2. Capture loss/metric/shape/device evidence.
3. Compare 2 fix options and apply one change.
4. Rerun same training budget and evaluation.
5. Record release/hold decision and rollback trigger.

### 8.3 Mandatory Artifacts

- `results/stage4/pain_point_matrix.md`
- `results/stage4/training_before_after.csv`
- `results/stage4/model_selection_decision.md`

---

## 9) Debugging and Quality Gates

Required debugging flow:

- model not learning -> check data/labels -> check output/loss pairing -> check gradients -> check LR
- exploding/vanishing gradients -> inspect gradient norms -> clipping/init/lr adjustments
- dying ReLU -> inspect activation distributions and dead-neuron ratio -> adjust init/LR/activation
- suspicious validation behavior -> leakage and split audit
- CUDA failures -> device mismatch and memory checks
- throughput collapse -> profile DataLoader and host/device transfer path before changing model

Quality gates:

- all Stage 4 scripts pass `run_all_stage4.ps1`
- ladders pass `run_ladder_stage4.ps1`
- optional GPU ladder passes with CPU fallback behavior
- expected outputs documented and validated
- chapter passes UTF-8 cleanup check (no mojibake)

---

## 10) Implementation Plan (Execution Order)

1. Add locked requirements and simplification front matter.
2. Fix encoding artifacts in `AI-study-handbook-4.md`.
3. Add complexity scale and per-topic complexity explanation.
4. Refactor concept sections to mandatory module template.
5. Add deep training-loop detailed guide (step-by-step + debug checks).
6. Create `red-book/src/stage-4/` ladders and runners.
7. Add explicit data/shape declaration blocks to all examples.
8. Upgrade practice project to operatable spec and file outputs.
9. Add weighted self-test rubric and remediation flow.
10. Add resource catalog + link policy + verification date.
11. Add deep-learning intuition visuals:
   - computation graph trace
   - activation comparison plots (Sigmoid/Tanh/ReLU)
   - residual/loss-curve diagnostics where applicable
12. Add RTX 5090 optimization track:
   - AMP + gradient accumulation tutorial
   - PyTorch profiler tutorial
   - VRAM estimate vs observed memory validation
13. Add final QA pass (terminology, encoding, duplicate cleanup).

---

## 11) Acceptance Criteria (Definition of Done)

Stage 4 is accepted only if:

- chapter is actionable without extra interpretation
- each core module includes detailed explanation + demonstration
- each module has simple/intermediate/advanced script links
- all Stage 4 scripts include functional workflow comments
- data and shape declarations are present in all worked examples
- practice project is clear, operatable, and file-output based
- PyTorch/CUDA section has detailed guide + ladder examples
- stage-4 runners execute successfully with fail-fast behavior
- chapter passes UTF-8 quality check

---

## 12) Data and Shape Declaration Standard

Every example must include:

```
Data: <name and source>
Rows/Samples: <count>
Input shape: <tensor shape>
Target: <name/type/classes>
Split: <train/valid/test or CV rule>
Type: <classification/regression/sequence/vision>
```

Synthetic data must also declare generation method and purpose.

---

## 13) Stage Transition Requirement

Handbook must end with `What Comes After Stage 4` and include:

- 2-3 sentence summary of Stage 5 focus
- mapping from Stage 4 skills to Stage 5 tasks
- readiness sentence before progression

---

## 14) GPU/CUDA/AMP Implementation Spec

Required content:

- device selection and verification (`torch.cuda.is_available`)
- tensor/model device consistency rules
- AMP usage (`autocast` + `GradScaler`) and fallback behavior
- memory and performance basics (batch size, pin_memory, timing sync)
- CPU fallback in all GPU scripts
- `non_blocking=True` transfer guidance and caveats
- `torch.backends.cudnn.benchmark = True` usage guidance and caveats
- gradient accumulation guidance for memory-constrained runs
- profiler basics (`torch.profiler`) for locating bottlenecks
- VRAM math walkthrough:
  - parameter memory
  - gradient memory
  - optimizer-state memory
  - activation memory estimate

Required runnable checks:

- print selected device
- run one CUDA path when available
- show CPU fallback message when CUDA unavailable
- optional benchmark output with clear caveat on hardware dependence
- print peak CUDA memory and compare to VRAM estimate
- produce a short decision note: `CPU better` vs `GPU better` for the tested workload

---

## 15) Additional Improvement Items

### A. Glossary and Notation

- lock notation: `x`, `y`, `y_pred`, `logits`, `loss`, `grad`
- add glossary for: epoch, batch, step, overfit, underfit, exploding gradient, vanishing gradient

### B. Reproducibility

- fixed seed policy in scripts
- dependency pinning policy
- run-date and environment logging in project outputs

### C. Maintenance and QA

- link-check cadence
- script smoke-test log template
- changelog section in handbook

---

## 16) Priority Breakdown

P0 (must do):

- chapter simplification rewrite with module template
- Stage 4 runnable script ladders + fail-fast runners
- practice project operatable rewrite
- detailed PyTorch/CUDA/AMP guide
- complexity scale + where-complexity-is blocks
- encoding cleanup

P1 (should do):

- weighted rubric improvements
- diagnostics extensions (gradient norms, LR sweeps)
- additional architecture variants

P2 (nice to have):

- optional Hugging Face integration example
- optional mini language-model notebook track

---

## 17) Chapter Simplification Blueprint (Mandatory)

Use this for every hard section:

1. Problem framing (what task this solves)
2. Intuition (visual/mental model)
3. Mechanics (math and algorithm steps)
4. Operatable code (ladder examples)
5. Failure pattern and fix

Per-module must include `why this is hard` and one checkpoint question before moving forward.





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

## Stage 4 Review Integration Addendum (2026-04-04, Additive-Only)

This addendum applies the latest Stage 4 review comments without removing existing requirements.

1. Deep-learning complexity must include compute-path maturity:
   - CPU-friendly concept path
   - single-GPU baseline
   - RTX 5090 optimized path with AMP/profiler/accumulation
2. Add mandatory intuition visuals for hard concepts:
   - computation graph tracing
   - activation function comparison and vanishing-gradient behavior
3. Extend troubleshooting to DL-specific failures:
   - dying ReLU
   - exploding gradients
   - deep overfitting controls (dropout, batch norm, early stopping)
4. Add sovereign-hardware tutorials:
   - VRAM math vs observed memory from runtime tools
   - explicit CUDA transfer/throughput optimization guidance
5. Enforce data-pipeline excellence:
   - method-chaining-based tabular prep before tensor conversion
   - custom `Dataset` + efficient `DataLoader` configuration tutorials
6. Enforce evidence-schema compliance in stage outputs:
   - `run_id`, `before_value`, `after_value`, `delta` are mandatory in metric tables.



