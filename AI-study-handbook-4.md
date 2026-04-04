# Stage 4 - Deep Learning

*(Week 7-9)*

## 0) If This Chapter Feels Hard

Do not read this chapter in one long pass.
Use this 4-pass loop for each module:

1. Problem framing: what prediction task is being solved.
2. Intuition: what the model learns at a high level.
3. Mechanics: tensor shapes first, then loss, gradients, optimizer behavior.
4. Operatable practice: run code, inspect outputs, explain one failure, and verify hardware utilization.

If you are stuck, answer these before changing model architecture:

- What is the input shape and target shape?
- Is the task regression, classification, or next-token prediction?
- Is the output layer paired with the correct loss?
- Is the issue from data, optimization, or model capacity?

Mandatory hardware-awareness check for local training:

```powershell
nvidia-smi
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.memory_allocated() if torch.cuda.is_available() else 0)"
```

If CUDA is available but memory usage is always zero during training, you are likely still on CPU path.

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

Hardware check (recommended before every deep-learning lab run):

```powershell
nvidia-smi
python -c "import torch; print('cuda', torch.cuda.is_available()); print('device_count', torch.cuda.device_count())"
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

Pipeline quality standard (method chaining -> tensor conversion):

```python
# Example pattern before Dataset/DataLoader creation.
df_clean = (
    raw_df
    .dropna(subset=["f1", "f2", "target"])
    .assign(
        f1_z=lambda d: (d["f1"] - d["f1"].mean()) / d["f1"].std(),
        f2_z=lambda d: (d["f2"] - d["f2"].mean()) / d["f2"].std(),
    )
    .loc[:, ["f1_z", "f2_z", "target"]]
)

X = torch.tensor(df_clean[["f1_z", "f2_z"]].to_numpy(), dtype=torch.float32)
y = torch.tensor(df_clean["target"].to_numpy(), dtype=torch.long)
```

Mandatory dtype/device declaration in examples:

- `input_dtype` (for example `torch.float32`)
- `target_dtype` (for example `torch.long` for class labels)
- `device` (for example `cpu` or `cuda`)

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
- hardware complexity: CPU-only -> single-GPU device-safe -> AMP + throughput/profiler optimization

Where complexity is in Stage 4 topics:

- Topic 1: one-step loop -> full loop -> gradient diagnostics + scheduler
- Topic 2: binary MLP -> multiclass split discipline -> regularization tradeoff
- Topic 3: minimal CNN -> validation-controlled CNN -> augmentation comparison
- Topic 4: basic RNN -> GRU with validation -> RNN/GRU/LSTM comparison
- Topic 5: attention mechanics -> transformer classifier -> causal next-token modeling
- Topic 6: device move basics -> CPU/GPU bridge -> AMP path with fallback

---

### Visual Intuition Prompts (Mandatory in Teaching Flow)

Use these visuals when concepts feel abstract:

1. Gradient descent landscape:
   - compare too-small LR vs stable LR vs too-large LR
   - show convergence vs oscillation/divergence behavior
2. Vanishing gradient comparison:
   - Sigmoid chain vs ReLU chain in deep stack
   - show why gradients can collapse toward zero with saturated activations

These visuals are required in notebook or script-generated figures for Stage 4 study sessions.

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

- Run simple NumPy script and confirm manual gradient-update steps move parameters.
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
- Section suite simple: [topic05a_mlp_simple.py](src/stage-4/topic05a_mlp_simple.py)
- Section-focused baseline: [topic05b_mlp_pytorch.py](src/stage-4/topic05b_mlp_pytorch.py)
- Section suite advanced: [topic05c_mlp_optimized.py](src/stage-4/topic05c_mlp_optimized.py)

Industry mapping note:
- Your proposed suite `topic05a/topic05b/topic05c` maps here to the Stage 4 MLP ladder (`topic02a/topic02/topic02c`) in this repository.

### Section 5 Alignment (MLP Foundation)

5.1 What it is and why it matters:
- MLP is a universal approximator for dense/tabular feature spaces.
- In practice it is also used as the final classifier/regressor head in larger models.

5.2 Mechanics and tensor contract:
- Input: `[Batch_Size, Input_Features]`
- Hidden: `H = Activation(XW + b)`
- Output logits: `[Batch_Size, Output_Classes]` (classification) or `[Batch_Size, 1]` (regression)

5.3 Operatable practice scripts:
- `topic05a_mlp_simple.py`: NumPy math-first MLP (no autograd magic).
- `topic05b_mlp_pytorch.py`: PyTorch baseline with `CrossEntropyLoss`.
- `topic05c_mlp_optimized.py`: BN + Dropout + Scheduler + AMP-ready path.

5.4 Failure-lab focus:
- Vanishing gradients: loss barely changes -> use ReLU-family activations and inspect gradient norms.
- Dying ReLU: hidden outputs collapse to zero -> lower LR or use LeakyReLU.
- Shape mismatch: verify shapes before every linear layer.

### What it is

MLP is the foundational deep model for dense/tabular feature spaces and classification heads.
It is a universal function approximator composed of:

- input layer
- one or more hidden layers with nonlinear activation
- output layer mapped to task-specific loss

### Why it matters

In industry, MLP is used for:

- tabular deep learning baselines
- projection heads in larger vision/NLP systems
- fast controlled experiments before architecture escalation

### Data and shape declaration

- Digits flat input: `(N,64)`
- Target: class labels `(N,)`, classes `0..9`

### Shape-first tensor contract (mandatory)

- Input `X`: `[batch_size, input_features]`
- Hidden layer: `H = activation(XW + b)`
- Output logits: `[batch_size, output_classes]`
- Classification loss pair: logits + `CrossEntropyLoss`

If this contract is broken, assume shape/pairing bug first.

### Worked tutorial

1. Simple (`topic02a`): binary MLP on digits subset.
2. Baseline (`topic02`): multiclass train/val/test with split discipline.
3. Advanced (`topic02c`): dropout + weight decay + comparison deltas.
4. Hardware check (all runs): print device and memory profile.

Method-chaining ingestion pattern (required before tensor conversion):

```python
df_clean = (
    raw_df
    .dropna(subset=["f1", "f2", "target"])
    .assign(
        f1_z=lambda d: (d["f1"] - d["f1"].mean()) / d["f1"].std(),
        f2_z=lambda d: (d["f2"] - d["f2"].mean()) / d["f2"].std(),
    )
)
```

### Assumptions and limits

- Ignores spatial locality unless features encode it.
- Can overfit quickly without regularization.

### Common beginner mistake and fix

- Mistake: using accuracy only.
- Fix: inspect train/val gap and test accuracy together.

### Architecture failure taxonomy (MLP)

- Failure mode: `Dying ReLU` (hidden outputs collapse to near-zero for many samples).
- Red flag: accuracy plateaus early while loss changes minimally.
- First fix: reduce LR, use better initialization, or test LeakyReLU.
- Verification: compare hidden-activation distribution before/after the fix.
- Failure mode: vanishing gradients in deeper MLP with saturating activations.
- Red flag: loss barely moves over many epochs.
- First fix: prefer ReLU-family activations, normalize inputs, and inspect gradient norms.

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
- Section suite simple: [topic06a_cnn_anatomy.py](src/stage-4/topic06a_cnn_anatomy.py)
- Section suite baseline: [topic06b_cnn_cifar10.py](src/stage-4/topic06b_cnn_cifar10.py)
- Section-focused performance lab: [topic06c_cnn_performance.py](src/stage-4/topic06c_cnn_performance.py)

Industry mapping note:
- Your proposed suite `topic06a/topic06b/topic06c` maps here to the Stage 4 CNN ladder (`topic03a/topic03/topic03c`) in this repository.

### Section 6 Alignment (CNN Spatial Intelligence)

6.1 Intuition:
- CNN kernels slide across local neighborhoods to detect edges, textures, and higher-level patterns.

6.2 Mechanics and tensor contract:
- Input format: `[N, C, H, W]`
- Pooling reduces `(H, W)` while preserving strong activations.
- Flatten bridges convolutional feature maps to dense layers.

6.3 Operatable practice scripts:
- `topic06a_cnn_anatomy.py`: manual Sobel filter anatomy.
- `topic06b_cnn_cifar10.py`: baseline CNN (CIFAR-10 local, digits fallback).
- `topic06c_cnn_performance.py`: hardware/performance comparison with AMP path.

6.4 Failure-lab focus:
- Over-pooling: feature map too small too early.
- Channel explosion: memory pressure from aggressive channel growth.
- Overfitting: high train vs lower validation/test behavior.

### What it is

Convolutional model that learns local patterns and hierarchical image features.

### Why it matters

CNNs usually outperform plain MLPs on image-like inputs.

### Data and shape declaration

- Digits image input: `(N,1,8,8)`
- Target: class labels `(N,)`

### Shape-first CNN contract (mandatory)

- Input format: `[N, C, H, W]` (industry standard)
- Convolution keeps/changes channels and spatial sizes by kernel/stride/padding policy
- Pooling reduces spatial dimensions
- Flatten bridges feature maps to dense classifier head

Track shape transitions explicitly for each block:

- `Conv -> Act -> Pool -> Conv -> Act -> Flatten -> Linear`

### Worked tutorial

1. Simple (`topic03a`): minimal Conv pipeline, inspect feature-map outputs.
2. Baseline (`topic03`): train/val/test with deeper stack and stable logging.
3. Advanced (`topic03c`): controlled augmentation + regularization delta analysis.
4. Hardware profile: compare throughput path and memory behavior on CPU/CUDA.

### Assumptions and limits

- Best for grid-like data.
- May still overfit without regularization.

### Common beginner mistake and fix

- Mistake: flattening too early and losing local structure.
- Fix: keep convolutional feature extraction before dense head.

### Architecture failure taxonomy (CNN)

- Failure mode: information bottleneck from overly aggressive pooling/stride.
- Red flag: train and validation accuracy both low despite stable training.
- First fix: reduce pooling aggressiveness or adjust feature-map width.
- Verification: compare feature-map size progression and before/after validation accuracy.
- Failure mode: channel explosion and memory pressure.
- Red flag: OOM or heavy step-time growth when channels increase too fast.
- First fix: moderate channel growth and monitor peak memory.

### Demonstration checklist

- [ ] Input shape includes channel dimension.
- [ ] Reports train-val behavior by epoch.
- [ ] Explains impact of controlled augmentation.
- [ ] Verifies final feature-map size is not over-compressed.

### Quick check

Q: Why is weight sharing useful in CNN?
A: Same feature detector can be reused across positions.

### When to use / not use

- Use: image and spatial signals.
- Not use: purely tabular tasks without spatial structure.

### Sovereign AI Hardware Check (MLP/CNN Labs)

Include this profiling block in each MLP/CNN script run:

```python
import torch

if torch.cuda.is_available():
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Max VRAM Allocated: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")
    torch.backends.cudnn.benchmark = True
else:
    print("Device: CPU fallback path")
```

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

### Architecture failure taxonomy (RNN/GRU/LSTM)

- Failure mode: exploding gradients.
- Red flag: loss spikes, unstable updates, or `NaN` loss.
- First fix: gradient clipping + lower LR.
- Verification: gradient-norm trace shows controlled values and stable loss.

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

### Architecture failure taxonomy (Transformer)

- Failure mode A: attention collapse (nearly uniform or degenerate attention patterns).
- Failure mode B: positional encoding misuse (token order not represented correctly).
- Red flag: model trains but sequence reasoning quality remains weak.
- First fix: validate mask/position pipeline and inspect attention diagnostics.
- Verification: attention-map sanity checks and sequence-quality delta after fix.

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
- If CUDA is available, print peak GPU memory usage.

### AMP conceptual note

- AMP reduces memory and can increase throughput on supported GPUs.
- AMP does not replace correct optimization; it changes numeric precision policy.

### Throughput optimization tutorial (local GPU track)

Use this workflow when moving from \"script works\" to \"system performs\":

1. Start with stable FP32 baseline and record step time.
2. Enable AMP (`autocast` + `GradScaler`) and compare throughput.
3. Tune input pipeline:
   - `DataLoader(..., pin_memory=True, num_workers=<tuned value>)`
   - `.to(device, non_blocking=True)` for batch transfer
4. Enable backend tuning when shapes are stable:
   - `torch.backends.cudnn.benchmark = True`
5. Re-measure:
   - transfer time
   - compute time
   - total step time
   - peak memory

Decision rule:

- Keep optimized path only if quality stays stable and throughput or memory meaningfully improves.

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
| MLP dead activations | dying ReLU from optimizer/init setup | lower LR, test LeakyReLU, inspect activations |
| CNN weak representation | pooling/stride too aggressive | reduce downsampling, inspect feature-map sizes |
| RNN training blows up | exploding gradients | clip gradients and reduce LR |
| Transformer sequence confusion | positional encoding or mask misuse | validate mask/position pipeline and attention diagnostics |

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
- Day 12: architecture comparison on fixed setup + failure taxonomy drill
- Day 13-14: error analysis and summary notes

### Week 9 - Project and performance

- Day 15-17: project baseline and before metrics
- Day 18: feature engineering change and after metrics
- Day 19: throughput optimization pass (AMP, DataLoader tuning, memory checks)
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
9. Add one hardware-profile run (CPU vs CUDA if available) with memory/timing evidence.

### Required deliverables (file-based)

The script must generate these files in `src/stage-4/results/`:

- `metrics_before.csv`
- `metrics_after.csv`
- `learning_curves.csv`
- `learning_curves.png`
- `error_analysis.md`
- `final_choice.md`
- `reproducibility.md`
- `evidence_schema_metrics.csv`
- `hardware_profile.csv`
- `hardware_decision.md`

### Minimum acceptance checks

- At least two models compared in before and after tables.
- Same split/seed policy across compared runs.
- Explicit feature engineering change is declared and applied.
- Final choice is justified with metric evidence.
- `evidence_schema_metrics.csv` contains: `run_id`, `before_value`, `after_value`, `delta`.

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
- NVIDIA CUDA Refresher (Getting Started): https://developer.nvidia.com/blog/even-easier-introduction-cuda/
- NVIDIA CUDA Refresher (Programming Model): https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/

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
