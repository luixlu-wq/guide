# Stage 3 Runnable Examples

This folder contains complete runnable examples for Stage 3: classical ML algorithms, fair comparison, and failure-mode debugging.

## Setup (CPU Path)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup (Recommended GPU Bridge If CUDA Is Available)

```bash
pip install -r requirements-gpu.txt
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## Run

Fail-fast run (CPU topics):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage3.ps1
```

This runner now validates key artifacts and basic sanity bounds (for example, model-comparison row counts and minimum metric thresholds), not only exit codes.

Fail-fast run including GPU bridge:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage3.ps1 -IncludeGpu
```

Run progressive ladders (simple -> intermediate -> advanced):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage3.ps1
```

Run ladders plus PyTorch/CUDA ladder:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage3.ps1 -IncludeGpuBridge
```

## Topics

- Linear Regression ladder:
  - `topic01a_linear_regression_simple.py`
  - `topic01_linear_regression.py` (intermediate baseline)
  - `topic01c_linear_regression_advanced.py`
- Logistic Regression ladder:
  - `topic02a_logistic_regression_simple.py`
  - `topic02_logistic_regression.py` (intermediate baseline)
  - `topic02c_logistic_regression_advanced.py`
- Decision Tree ladder:
  - `topic03a_decision_tree_simple.py`
  - `topic03_decision_tree_depth.py` (intermediate baseline)
  - `topic03c_decision_tree_advanced.py`
- Random Forest ladder:
  - `topic04a_random_forest_simple.py`
  - `topic04_random_forest_baseline.py` (intermediate baseline)
  - `topic04c_random_forest_advanced.py`
- SVM ladder:
  - `topic05a_svm_simple.py`
  - `topic05_svm_tuning.py` (intermediate baseline)
  - `topic05c_svm_advanced.py`
- KMeans ladder:
  - `topic06a_kmeans_simple.py`
  - `topic06_kmeans_silhouette.py` (intermediate baseline)
  - `topic06c_kmeans_advanced.py`
- `topic07_fair_model_comparison.py`: same-split benchmark across multiple models
- `topic08_failure_modes_overfit_leakage.py`: overfitting and leakage demos
- PyTorch/CUDA bridge ladder:
  - `topic09a_pytorch_cuda_simple.py`
  - `topic09_pytorch_cuda_bridge.py` (intermediate)
  - `topic09c_pytorch_cuda_advanced.py`
- `run_ladder_stage3.ps1`: executes all six topic ladders end-to-end

## Outputs Created by Scripts

- `results/topic07_fair_comparison.csv`
- `results/topic07_fair_comparison.json`
- `results/topic07_fair_comparison_seed_stats.csv`
- `results/topic07_fair_comparison_seed_stats.json`
- `results/stage3/topic05_svm_summary.csv`
- `results/stage3/topic05_svm_summary.json`
- `results/stage3/topic06_kmeans_k_scan.csv`
- `results/stage3/topic06_kmeans_k_scan.json`
- `results/stage3/topic05c_svm_top5_cv.csv`
- `results/stage3/topic05c_svm_summary.json`
- `results/stage3/topic06c_kmeans_advanced_metrics.csv`
- `results/stage3/topic06c_kmeans_advanced_metrics.json`
- `results/stage3/model_compare_before_after.csv`
- `results/stage3/model_compare_seed_stability.csv`
- `results/stage3/fair_comparison_checklist.md`
- `results/stage3/failure_class_before_after.csv`
- `results/stage3/failure_class_before_after.json`
- `results/stage3/pain_point_matrix.md`
- `results/stage3/failure_diagnosis.md`
- `results/stage3/cpu_gpu_latency_transfer.csv`
- `results/stage3/cpu_gpu_latency_transfer.json`
- `results/stage3/decision_and_risk.md`
- `results/stage3/cpu_gpu_parity_report.json`

## Data Source and Structure Summary

All datasets are built-in `scikit-learn` datasets or synthetic data generated in code.

### `load_diabetes` (topic01, topic01c)

- Task type: regression
- Size: 442 rows, 10 numeric features
- Target: disease progression score (continuous)

### `load_breast_cancer` (topics 02, 03, 04, 07, topic03c, topic04c)

- Task type: binary classification
- Size: 569 rows, 30 numeric features
- Target: `0=malignant`, `1=benign`

### `load_iris` (topics 03a, 04a, 05, 06, 05a)

- Task type: multiclass classification / clustering demo
- Size: 150 rows, 4 numeric features
- Target: species label (used in topic05, ignored in topic06 training)

### `make_classification` and synthetic random data (topic02a, topic02c, topic08)

- Overfitting demo: controlled synthetic classification data
- Leakage demo: random features + random labels to reveal leakage inflation

### `make_blobs` synthetic clustering data (topic06a, topic06c)

- Controlled cluster data for simple and advanced KMeans practice

### PyTorch synthetic tensor data (topic09a, topic09, topic09c)

- topic09a: tiny 4-row tensor example for one training step anatomy
- topic09: 25,000-row tensor regression `y = 2.2*x - 0.4 + noise`
- topic09c: 30,000-row, 8-feature mini-batch training with validation
