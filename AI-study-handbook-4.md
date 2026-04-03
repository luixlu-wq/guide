# Stage 4 - Deep Learning

*(Week 7-9)*

## 0) If This Chapter Feels Hard

Do not read this chapter in one long pass.
Use this 4-pass loop for each module:

1. Problem framing: what prediction task is being solved.
2. Intuition: what the model learns at a high level.
3. Mechanics: tensor shapes, loss, gradients, optimizer behavior.
4. Operatable practice: run code, inspect outputs, explain one failure.

If you are stuck, answer these before changing model architecture:

- What is the input shape and target shape?
- Is the task regression, classification, or next-token prediction?
- Is the output layer paired with the correct loss?
- Is the issue from data, optimization, or model capacity?

---

## 1) Stage Goal

Understand deep learning as a trainable system, not a black box.

You are not only learning `model(x)`.
You are learning:

- how forward and backward passes work together
- how gradients update parameters
- how tensor shapes control correctness
- how to debug unstable training
- when MLP, CNN, RNN, or Transformer is the right choice

By the end of Stage 4, you should move from:

> "I can run a PyTorch tutorial"

to:

> "I can explain and debug a full training loop, compare architectures fairly, and justify improvements with evidence."

---

## 2) How To Use This Handbook

### Script-first study loop (recommended)

For each module:

1. Read "What it is" and "Why it matters".
2. Read data and shape declaration blocks.
3. Run the simple -> intermediate -> advanced scripts.
4. Record:
   - data source + shape
   - train/validation behavior
   - one failure and one fix

### Time guide

- One concept module: 60-100 minutes
- One architecture ladder: 90-150 minutes
- Weekly commitment: 8-12 hours

### If outputs look wrong

- Use Section 9 (Debugging Playbook).
- Change one variable at a time.
- Keep split, metric, and seed fixed while debugging.

---

## 3) Prerequisites And Environment Setup

### Knowledge prerequisites

- Stage 1-3 concepts
- Python functions/loops
- NumPy basics
- Train/test split and metrics basics

### Environment setup

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install -r src/stage-4/requirements.txt
```

Optional CUDA bridge:

```powershell
pip install -r src/stage-4/requirements-gpu.txt
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

### Runtime presets (recommended)

Stage 4 runners support two presets:

- `full` (default): longer runtime, stronger training results
- `quick`: shorter runtime for iteration and debugging

Examples:

```powershell
powershell -ExecutionPolicy Bypass -File .\src\stage-4\run_all_stage4.ps1 -Preset quick
powershell -ExecutionPolicy Bypass -File .\src\stage-4\run_all_stage4.ps1 -Preset full
powershell -ExecutionPolicy Bypass -File .\src\stage-4\run_ladder_stage4.ps1 -Preset quick
```

### Reproducibility rules

- Use fixed random seeds.
- Keep split strategy fixed when comparing models.
- Keep epoch budget and metric set fixed in before/after comparisons.

---

## 4) Learning Targets (Weighted Rubric)

| Target | Evidence | Weight |
|---|---|---:|
| Explain 5-step training loop | Written explanation + runnable demo | 15 |
| Declare data source and tensor shapes | Present in each module log | 10 |
| Run all architecture ladders | Scripts run with expected outputs | 20 |
| Compare train/validation/test behavior | Gap interpretation per module | 15 |
| Diagnose and fix failure modes | One failure + one fix evidence | 15 |
| Execute project workflow with deliverables | Required files in `results/` | 15 |
| Explain PyTorch/CUDA/AMP flow | Device-safe training explanation | 10 |

Total: 100

Pass levels:

- 85-100: Ready for Stage 5
- 70-84: Continue with targeted remediation
- <70: Repeat modules 1, 2, 6, 9, and project lab

---

## 5) Data Resources And Data Structure Declarations

Stage 4 examples use these data sources.

| Dataset | Source | Rows | Input shape | Target shape | Task |
|---|---|---:|---|---|---|
| Digits | `sklearn.datasets.load_digits` | 1,797 | `(N, 64)` or `(N, 1, 8, 8)` | `(N,)` class 0..9 | Multiclass classification |
| Synthetic regression | generated in script | configurable | `(N, d)` | `(N, 1)` | Regression |
| Synthetic sequence | generated in script | configurable | `(N, T, F)` or `(N, T)` | `(N,)` or `(N, T)` | Sequence classification / next-token |

Data declaration standard for every module and script:

```text
Data: <name and source>
Rows/Samples: <count>
Input shape: <tensor shape>
Target: <name/type/classes>
Split: <train/val/test or CV>
Type: <task type>
```

---

## 6) Example Complexity Scale (Used In All Modules)

- `Simple`: one concept focus, tiny or clean data, minimal moving parts.
- `Intermediate`: full train/validation workflow, mini-batching, split discipline, metric tracking.
- `Advanced`: controlled model/optimization changes, stronger diagnostics, and tradeoff reasoning.

Complexity dimensions:

- data complexity: noise, sequence length, dimensionality
- pipeline complexity: batching, split policy, feature change policy
- model complexity: depth, regularization, architecture variants
- optimization complexity: LR schedule, clipping, AMP
- evaluation complexity: train/val/test comparison and gap analysis

Where complexity is in Stage 4 topics:

- Topic 1: one-step loop -> full loop -> gradient diagnostics + scheduler
- Topic 2: binary MLP -> multiclass split discipline -> regularization tradeoff
- Topic 3: minimal CNN -> validation-controlled CNN -> augmentation comparison
- Topic 4: basic RNN -> GRU with validation -> RNN/GRU/LSTM comparison
- Topic 5: attention mechanics -> transformer classifier -> causal next-token modeling
- Topic 6: device move basics -> CPU/GPU bridge -> AMP path with fallback

---

## 7) Concept Modules With Operatable Examples

## Module 1 - 5-Step Training Loop Anatomy

Runnable scripts:
- Simple: [topic01a_loop_anatomy_simple.py](src/stage-4/topic01a_loop_anatomy_simple.py)
- Intermediate: [topic01_loop_anatomy.py](src/stage-4/topic01_loop_anatomy.py)
- Advanced: [topic01c_loop_anatomy_advanced.py](src/stage-4/topic01c_loop_anatomy_advanced.py)

### What it is

A fixed learning loop:

1. Move data/model to device.
2. Forward pass computes prediction.
3. Loss computes error signal.
4. Backward pass computes gradients.
5. Optimizer updates parameters.

### Why it matters

Every deep model uses this loop. If any step is wrong, training fails.

### Data and shape declaration

- Simple: synthetic regression, `(4,1) -> (4,1)`
- Intermediate/advanced: synthetic tabular regression `(N,d) -> (N,1)`

### Worked tutorial

- Run simple script and confirm parameter values change after `optimizer.step()`.
- Run intermediate and verify validation MSE decreases over epochs.
- Run advanced and inspect gradient norm + scheduler behavior.

### Assumptions and limits

- Loss must match task type.
- Data and model must be on the same device.

### Common beginner mistake and fix

- Mistake: forgetting `optimizer.zero_grad()`.
- Fix: clear gradients each step before `loss.backward()`.

### Demonstration checklist

- [ ] Can explain each of the 5 steps in one sentence.
- [ ] Can print and verify tensor shapes and devices.
- [ ] Can explain why loss decreases or fails to decrease.

### Quick check

Q: What is the minimum signal required for learning?
A: A valid loss and its gradients.

### When to use / not use

- Use: every trainable deep model.
- Not use: pure rule-based inference without training.

---

## Module 2 - MLP (Tabular or Flattened Features)

Runnable scripts:
- Simple: [topic02a_mlp_simple.py](src/stage-4/topic02a_mlp_simple.py)
- Intermediate: [topic02_mlp_intermediate.py](src/stage-4/topic02_mlp_intermediate.py)
- Advanced: [topic02c_mlp_advanced.py](src/stage-4/topic02c_mlp_advanced.py)

### What it is

A feedforward network using fully connected layers.

### Why it matters

Strong baseline for tabular data and flattened features.

### Data and shape declaration

- Digits flat input: `(N,64)`
- Target: class labels `(N,)`, classes `0..9`

### Worked tutorial

- Start with binary subset (0 vs 1).
- Upgrade to full 10-class workflow with train/val/test.
- Add dropout + weight decay and compare train-val gap.

### Assumptions and limits

- Ignores spatial locality unless features encode it.
- Can overfit quickly without regularization.

### Common beginner mistake and fix

- Mistake: using accuracy only.
- Fix: inspect train/val gap and test accuracy together.

### Demonstration checklist

- [ ] Uses fixed split and seed.
- [ ] Reports train, val, and test metrics.
- [ ] Compares baseline vs improved configuration.

### Quick check

Q: Why does dropout usually lower train accuracy but improve generalization?
A: It regularizes co-adaptation and can reduce overfitting.

### When to use / not use

- Use: tabular features, baseline classification.
- Not use: tasks where spatial or sequential structure is dominant.

---

## Module 3 - CNN (Image Structure)

Runnable scripts:
- Simple: [topic03a_cnn_simple.py](src/stage-4/topic03a_cnn_simple.py)
- Intermediate: [topic03_cnn_intermediate.py](src/stage-4/topic03_cnn_intermediate.py)
- Advanced: [topic03c_cnn_advanced.py](src/stage-4/topic03c_cnn_advanced.py)

### What it is

Convolutional model that learns local patterns and hierarchical image features.

### Why it matters

CNNs usually outperform plain MLPs on image-like inputs.

### Data and shape declaration

- Digits image input: `(N,1,8,8)`
- Target: class labels `(N,)`

### Worked tutorial

- Simple: one Conv + pooling path.
- Intermediate: BatchNorm + deeper conv stack with validation tracking.
- Advanced: controlled augmentation and regularization comparison.

### Assumptions and limits

- Best for grid-like data.
- May still overfit without regularization.

### Common beginner mistake and fix

- Mistake: flattening too early and losing local structure.
- Fix: keep convolutional feature extraction before dense head.

### Demonstration checklist

- [ ] Input shape includes channel dimension.
- [ ] Reports train-val behavior by epoch.
- [ ] Explains impact of controlled augmentation.

### Quick check

Q: Why is weight sharing useful in CNN?
A: Same feature detector can be reused across positions.

### When to use / not use

- Use: image and spatial signals.
- Not use: purely tabular tasks without spatial structure.

---

## Module 4 - RNN/GRU/LSTM (Sequence Learning)

Runnable scripts:
- Simple: [topic04a_rnn_simple.py](src/stage-4/topic04a_rnn_simple.py)
- Intermediate: [topic04_rnn_intermediate.py](src/stage-4/topic04_rnn_intermediate.py)
- Advanced: [topic04c_rnn_advanced.py](src/stage-4/topic04c_rnn_advanced.py)

### What it is

Sequence models that summarize time-ordered inputs into hidden states.

### Why it matters

Introduces temporal dependency modeling before transformers.

### Data and shape declaration

- Synthetic sequence input: `(N,T,F)`
- Target: sequence-level class `(N,)`

### Worked tutorial

- Start with simple binary sequence rule.
- Train GRU with validation checkpoints.
- Compare RNN vs GRU vs LSTM under fixed conditions.

### Assumptions and limits

- Long dependencies can still be difficult for vanilla RNN.
- Sequence length impacts optimization stability.

### Common beginner mistake and fix

- Mistake: wrong input shape ordering.
- Fix: keep `(batch, time, feature)` when using `batch_first=True`.

### Demonstration checklist

- [ ] Confirms `(N,T,F)` input shape.
- [ ] Uses fixed split and same epoch budget for architecture comparison.
- [ ] Explains train-val gap and architecture tradeoff.

### Quick check

Q: Why add gradient clipping in recurrent models?
A: It reduces exploding-gradient instability.

### When to use / not use

- Use: compact sequential tasks and recurrent baselines.
- Not use: long-context tasks where transformer attention is preferred.

---

## Module 5 - Transformer Basics To Causal Modeling

Runnable scripts:
- Simple: [topic05a_transformer_simple.py](src/stage-4/topic05a_transformer_simple.py)
- Intermediate: [topic05_transformer_intermediate.py](src/stage-4/topic05_transformer_intermediate.py)
- Advanced: [topic05c_transformer_advanced.py](src/stage-4/topic05c_transformer_advanced.py)

### What it is

Attention-first sequence architecture using token interaction instead of recurrence.

### Why it matters

Core architecture behind modern language and multimodal models.

### Data and shape declaration

- Simple mechanics: tiny embedding tensor `(1,4,4)`
- Intermediate: token ids `(N,T)` -> class labels `(N,)`
- Advanced: token ids `(N,T)` -> next-token targets `(N,T)`

### Worked tutorial

- Simple: compute scaled dot-product attention weights.
- Intermediate: train transformer encoder classifier.
- Advanced: causal mask and next-token prediction with perplexity.

### Assumptions and limits

- Requires positional information.
- Attention cost can grow with sequence length.

### Common beginner mistake and fix

- Mistake: forgetting causal mask in autoregressive setup.
- Fix: use upper-triangular mask to block future tokens.

### Demonstration checklist

- [ ] Can explain query/key/value at concept level.
- [ ] Can describe why positional encoding is required.
- [ ] Can explain token accuracy and perplexity meaning.

### Quick check

Q: What is the effect of missing causal mask in next-token training?
A: Data leakage from future tokens, producing invalid learning behavior.

### When to use / not use

- Use: sequence modeling with long-range dependencies.
- Not use: tiny tabular problems where simpler models are enough.

---

## Module 6 - PyTorch + CUDA + AMP (Detailed Guide)

Runnable scripts:
- Simple: [topic06a_cuda_simple.py](src/stage-4/topic06a_cuda_simple.py)
- Intermediate: [topic06_cuda_intermediate.py](src/stage-4/topic06_cuda_intermediate.py)
- Advanced: [topic06c_cuda_amp_advanced.py](src/stage-4/topic06c_cuda_amp_advanced.py)

### Why this module is hard

Beginners often mix up:

- device placement
- autograd steps
- optimizer updates
- mixed precision conditions

### Step-by-step instruction

1. Select device:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

2. Move both model and tensors to same device.
3. Run forward pass and compute task-appropriate loss.
4. Clear grads, run backward, then optimizer step.
5. If using CUDA AMP:
   - wrap forward/loss in `autocast`
   - use `GradScaler` for scaled backward + step

### Required debug checks

- Print selected device.
- Print tensor and model device to confirm match.
- Print loss trend over epochs.
- Verify CPU fallback path message if CUDA unavailable.

### AMP conceptual note

- AMP reduces memory and can increase throughput on supported GPUs.
- AMP does not replace correct optimization; it changes numeric precision policy.

### Ladder complexity in this module

- `Simple`: one-step CPU/CUDA consistency check.
- `Intermediate`: full device-aware training loop + timing.
- `Advanced`: mixed precision path + fallback-safe training.

---

## 8) Deep Learning Failure Modes And Fix Playbook

Runnable script:
- [topic07_failure_modes.py](src/stage-4/topic07_failure_modes.py)

| Symptom | Likely cause | First fix |
|---|---|---|
| Loss unstable or diverges | learning rate too high | lower LR, retry fixed seed |
| Accuracy unexpectedly weak | wrong output-loss pairing | verify logits/loss compatibility |
| Validation unstable with dropout | forgot `model.eval()` | switch modes correctly |
| Runtime device error | tensor/model on different devices | move both to same device |
| No learning signal | missing backward/step order | verify `zero_grad -> backward -> step` |

---

## 9) Debugging Checklist (Run In Order)

- [ ] Data source, shape, and target are declared.
- [ ] Output layer and loss are correctly paired.
- [ ] Model and data are on same device.
- [ ] Training order is correct: forward -> loss -> zero_grad -> backward -> step.
- [ ] Train/validation metrics are logged per epoch.
- [ ] `model.train()` and `model.eval()` are used in correct phases.
- [ ] Learning rate is in a stable range.
- [ ] Model can overfit a tiny subset (sanity test).

---

## 10) Three-Week Operable Roadmap (Week 7-9)

### Week 7 - Foundations and loop control

- Day 1: tensors, devices, shapes
- Day 2: 5-step loop anatomy
- Day 3: autograd and gradient interpretation
- Day 4: optimizer and LR behavior
- Day 5: train/eval mode and metrics logging
- Day 6: failure-mode drills
- Day 7: recap + written checks

### Week 8 - Architecture ladders

- Day 8: MLP ladder
- Day 9: CNN ladder
- Day 10: RNN/GRU/LSTM ladder
- Day 11: Transformer ladder
- Day 12: architecture comparison on fixed setup
- Day 13-14: error analysis and summary notes

### Week 9 - Project and performance

- Day 15-17: project baseline and before metrics
- Day 18: feature engineering change and after metrics
- Day 19: analysis docs and model selection rationale
- Day 20: reproducibility and final cleanup
- Day 21: self-test and Stage 5 readiness decision

---

## 11) Stage 4 Script Mapping (`src/stage-4`)

Core runners:
- [run_all_stage4.ps1](src/stage-4/run_all_stage4.ps1)
- [run_ladder_stage4.ps1](src/stage-4/run_ladder_stage4.ps1)
- [README.md](src/stage-4/README.md)
- [requirements.txt](src/stage-4/requirements.txt)
- [requirements-gpu.txt](src/stage-4/requirements-gpu.txt)

Topic ladders:
- Topic 1: [topic01a_loop_anatomy_simple.py](src/stage-4/topic01a_loop_anatomy_simple.py), [topic01_loop_anatomy.py](src/stage-4/topic01_loop_anatomy.py), [topic01c_loop_anatomy_advanced.py](src/stage-4/topic01c_loop_anatomy_advanced.py)
- Topic 2: [topic02a_mlp_simple.py](src/stage-4/topic02a_mlp_simple.py), [topic02_mlp_intermediate.py](src/stage-4/topic02_mlp_intermediate.py), [topic02c_mlp_advanced.py](src/stage-4/topic02c_mlp_advanced.py)
- Topic 3: [topic03a_cnn_simple.py](src/stage-4/topic03a_cnn_simple.py), [topic03_cnn_intermediate.py](src/stage-4/topic03_cnn_intermediate.py), [topic03c_cnn_advanced.py](src/stage-4/topic03c_cnn_advanced.py)
- Topic 4: [topic04a_rnn_simple.py](src/stage-4/topic04a_rnn_simple.py), [topic04_rnn_intermediate.py](src/stage-4/topic04_rnn_intermediate.py), [topic04c_rnn_advanced.py](src/stage-4/topic04c_rnn_advanced.py)
- Topic 5: [topic05a_transformer_simple.py](src/stage-4/topic05a_transformer_simple.py), [topic05_transformer_intermediate.py](src/stage-4/topic05_transformer_intermediate.py), [topic05c_transformer_advanced.py](src/stage-4/topic05c_transformer_advanced.py)
- Topic 6 (optional GPU bridge): [topic06a_cuda_simple.py](src/stage-4/topic06a_cuda_simple.py), [topic06_cuda_intermediate.py](src/stage-4/topic06_cuda_intermediate.py), [topic06c_cuda_amp_advanced.py](src/stage-4/topic06c_cuda_amp_advanced.py)
- Diagnostics: [topic07_failure_modes.py](src/stage-4/topic07_failure_modes.py)
- Practice project baseline: [topic08_project_baseline.py](src/stage-4/topic08_project_baseline.py)

Expected output style for each script:

- Print data declaration summary
- Print key metrics
- Print short interpretation (1-2 lines)

---

## 12) Practice Project Lab (Clear, Operatable)

Runnable baseline:
- [topic08_project_baseline.py](src/stage-4/topic08_project_baseline.py)

### Project goal

Train and compare at least two deep models on one fixed dataset and justify the final model with evidence.

### Required workflow

1. Use fixed dataset and split policy from the baseline script.
2. Declare data source and structure before training:
   - source
   - rows
   - input shape
   - target shape/classes
3. Train two models under same epoch budget:
   - `ShallowMLP`
   - `DeepMLP`
4. Record before-change metrics (`train`, `val`, `test`, and `train_val_gap`).
5. Apply one explicit feature engineering change:
   - append squared features `x^2`
6. Retrain both models with same split and epoch budget.
7. Record after-change metrics.
8. Compare before vs after and write final model choice rationale.

### Required deliverables (file-based)

The script must generate these files in `src/stage-4/results/`:

- `metrics_before.csv`
- `metrics_after.csv`
- `learning_curves.csv`
- `learning_curves.png`
- `error_analysis.md`
- `final_choice.md`
- `reproducibility.md`

### Minimum acceptance checks

- At least two models compared in before and after tables.
- Same split/seed policy across compared runs.
- Explicit feature engineering change is declared and applied.
- Final choice is justified with metric evidence.

---

## 13) Self-Test (Quick)

1. Why must model and tensors be on the same device?
2. What exactly happens between `loss.backward()` and `optimizer.step()`?
3. How do you recognize overfitting from train/validation behavior?
4. Why can a wrong loss-output pairing damage training?
5. Where does complexity increase from simple to advanced in CNN modules?
6. Why is gradient clipping used in recurrent and transformer advanced scripts?
7. What does a causal mask prevent?
8. When should you use AMP?
9. Why keep split and epoch budget fixed during comparisons?
10. What evidence is required to justify a final model choice?

Scoring suggestion:

- 8-10 correct: strong
- 6-7 correct: acceptable, review weak modules
- <=5 correct: rerun Module 1, 6, 8, and project lab

---

## 14) High-Quality Resources (Use In This Order)

### Core path

- FastAI course: https://course.fast.ai/
- Google ML Crash Course (Neural Networks): https://developers.google.com/machine-learning/crash-course/neural-networks
- PyTorch basics index: https://docs.pytorch.org/tutorials/beginner/basics/index.html
- PyTorch quickstart: https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
- PyTorch autograd tutorial: https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html
- PyTorch optimization tutorial: https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html

### Official implementation references

- CUDA semantics: https://docs.pytorch.org/docs/stable/notes/cuda.html
- AMP recipe: https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html
- Performance tuning guide: https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html
- Deep Learning tuning playbook: https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook

### Deeper theory and architecture

- Dive into Deep Learning: https://d2l.ai/
- CS231n: https://cs231n.stanford.edu/
- Attention Is All You Need: https://arxiv.org/abs/1706.03762
- Adam paper: https://arxiv.org/abs/1412.6980
- BatchNorm paper: https://arxiv.org/abs/1502.03167
- Dropout paper: https://arxiv.org/abs/1207.0580

---

## 15) What You Must Be Able To Do After Stage 4

- [ ] Explain and run the 5-step training loop clearly.
- [ ] Declare data source and tensor shapes for every experiment.
- [ ] Train and compare MLP, CNN, RNN-family, and Transformer examples.
- [ ] Diagnose at least three common training failures.
- [ ] Use CPU/CUDA path safely and explain AMP conditions.
- [ ] Complete the project workflow and produce all required deliverables.

---

## 16) What Comes After Stage 4

Stage 5 should focus on robust experiment design, larger-scale data pipelines, and production-quality training/evaluation loops.
The architecture and debugging skills from Stage 4 become the base for hyperparameter strategy, model governance, and deployment-oriented workflows.
Move to Stage 5 only when you can explain model behavior using evidence, not guesses.
