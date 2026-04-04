# Stage 4 Runnable Examples

This folder contains complete runnable examples for Stage 4: deep learning foundations, architecture ladders, CUDA/AMP bridge, failure diagnostics, and a practice project baseline.

## Setup (CPU Path)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup (Optional CUDA Path)

```bash
pip install -r requirements-gpu.txt
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## Run

Preset modes:

- `full` (default): stronger training quality, longer runtime
- `quick`: reduced training/data budget for faster iteration

Fail-fast run (core intermediate scripts):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage4.ps1
```

Fail-fast run including CUDA bridge module:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage4.ps1 -IncludeGpu
```

Quick fail-fast run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage4.ps1 -Preset quick
```

Run progressive ladders (simple -> intermediate -> advanced):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage4.ps1
```

Run ladders plus optional CUDA/AMP ladder:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage4.ps1 -IncludeGpuBridge
```

Quick ladder run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage4.ps1 -Preset quick
```

## Topic Mapping

- Topic 1 (training loop anatomy):
  - `topic01a_loop_anatomy_simple.py` (NumPy math-first neural anatomy)
  - `topic01_loop_anatomy.py` (PyTorch baseline neural anatomy)
  - `topic01c_loop_anatomy_advanced.py`
- Topic 2 (MLP ladder):
  - `topic02a_mlp_simple.py`
  - `topic02_mlp_intermediate.py`
  - `topic02c_mlp_advanced.py`
- Topic 3 (CNN ladder):
  - `topic03a_cnn_simple.py`
  - `topic03_cnn_intermediate.py`
  - `topic03c_cnn_advanced.py`
- Topic 4 (RNN/GRU/LSTM ladder):
  - `topic04a_rnn_simple.py`
  - `topic04_rnn_intermediate.py`
  - `topic04c_rnn_advanced.py`
- Topic 5 (Transformer ladder):
  - `topic05a_transformer_simple.py`
  - `topic05_transformer_intermediate.py`
  - `topic05c_transformer_advanced.py`
- Topic 6 (PyTorch/CUDA/AMP ladder, optional):
  - `topic06a_cuda_simple.py`
  - `topic06_cuda_intermediate.py`
  - `topic06c_cuda_amp_advanced.py`
- Diagnostics and project:
  - `topic07_failure_modes.py`
  - `topic08_project_baseline.py`

Section-focused supplemental scripts (industry-style chapter aliases):

- `topic05a_mlp_simple.py` (NumPy MLP math-first simple lab)
- `topic05b_mlp_pytorch.py` (shape-first MLP baseline with failure-lab diagnostics)
- `topic05c_mlp_optimized.py` (MLP optimized with BN/Dropout/Scheduler/AMP path)
- `topic06a_cnn_anatomy.py` (manual Sobel filter anatomy demo)
- `topic06b_cnn_cifar10.py` (CNN baseline with CIFAR10-local preference and digits fallback)
- `topic06c_cnn_performance.py` (CNN performance lab with AMP/pin-memory profiling)

## Outputs

`topic08_project_baseline.py` creates:

- `results/metrics_before.csv`
- `results/metrics_after.csv`
- `results/learning_curves.csv`
- `results/learning_curves.png`
- `results/error_analysis.md`
- `results/final_choice.md`
- `results/reproducibility.md`

Topic 01 scripts create:

- `results/stage4/topic01a_numpy_loss_trace.csv`
- `results/stage4/topic01a_before_after_metrics.csv`
- `results/stage4/topic01_loop_training_trace.csv`
- `results/stage4/topic01_before_after_metrics.csv`
- `results/stage4/topic01_before_after_metrics.json`
- `results/stage4/topic05b_before_after_metrics.csv`
- `results/stage4/topic05b_before_after_metrics.json`
- `results/stage4/topic05a_numpy_trace.csv`
- `results/stage4/topic05a_before_after_metrics.csv`
- `results/stage4/topic05c_optimized_metrics.csv`
- `results/stage4/topic05c_optimized_metrics.json`
- `results/stage4/topic06a_sobel_demo.png`
- `results/stage4/topic06a_sobel_summary.csv`
- `results/stage4/topic06b_cnn_baseline_metrics.csv`
- `results/stage4/topic06b_cnn_baseline_metrics.json`
- `results/stage4/topic06c_performance_metrics.csv`
- `results/stage4/topic06c_performance_metrics.json`

## Data Source and Structure Summary

### sklearn digits (`load_digits`)

Used in Topic 2, Topic 3, Topic 6C, Topic 7, Topic 8.

- Source: `sklearn.datasets.load_digits`
- Rows: 1,797
- Input (flat): `(n_samples, 64)` with pixel values scaled to `[0, 1]`
- Input (image): `(n_samples, 1, 8, 8)`
- Target: digit class label `(n_samples,)`, values `0..9`
- Task: multiclass classification

### Synthetic regression tensors

Used in Topic 1 and Topic 6 intermediate.

- Source: generated in-script with fixed random seed
- Input: `(n_samples, n_features)`
- Target: `(n_samples, 1)` continuous values
- Task: regression

### Synthetic sequence tensors

Used in Topic 4 and Topic 5.

- Source: generated in-script with fixed random seed
- Input: sequence tensors `(n_samples, seq_len, feature_dim)` or token ids `(n_samples, seq_len)`
- Target: class labels or next-token ids
- Task: sequence classification / autoregressive modeling
