# Stage 1 Runnable Examples

This folder contains complete, runnable examples for Stage 1 topics.

## Setup (CPU Path)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup (Optional GPU Path: PyTorch + CUDA)

```bash
pip install -r requirements-gpu.txt
```

`requirements-gpu.txt` is pinned to the PyTorch CUDA wheel index (`cu121`).
If your local CUDA/PyTorch combo is different, update the index URL accordingly.

Verify PyTorch/CUDA:

```bash
python -c "import torch; print('torch', torch.__version__); print('cuda', torch.cuda.is_available())"
```

## Run

Single command (fail-fast, CPU topics):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage1.ps1
```

Single command including optional GPU topic:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage1.ps1 -IncludeGpu
```

Or run scripts one by one:

```bash
python topic01_supervised_learning.py
python topic02_unsupervised_learning.py
python topic03_features_vs_target.py
python topic04_cost_function.py
python topic05_gradient_descent.py
python topic06_training_vs_testing.py
python topic07_overfitting.py
python topic08_bias_variance.py
python topic09_validation_set.py
python topic10_feature_engineering.py
python topic11_regularization.py
python topic12_pytorch_cuda.py
```

## Topics

- `topic01_supervised_learning.py`: classification pipeline with metrics
- `topic02_unsupervised_learning.py`: K-Means clustering + silhouette/ARI
- `topic03_features_vs_target.py`: feature quality impact demo
- `topic04_cost_function.py`: manual vs library MSE and Log Loss
- `topic05_gradient_descent.py`: gradient descent from scratch + loss plot
- `topic06_training_vs_testing.py`: proper split vs wrong same-data evaluation
- `topic07_overfitting.py`: model complexity and cross-validation MSE
- `topic08_bias_variance.py`: depth sweep to observe bias-variance behavior
- `topic09_validation_set.py`: train/validation/test split for model selection
- `topic10_feature_engineering.py`: feature engineering impact on model quality
- `topic11_regularization.py`: regularization tradeoffs
- `topic12_pytorch_cuda.py`: tensors, autograd, device placement, CPU/GPU timing

## Engineering Artifacts

Each script now writes:

- console + file logs: `results/topicXX_*.log`
- structured metrics: `results/topicXX_*_metrics.json`
- topic-specific figures (where applicable), for example:
  - `results/topic03_feature_importance.png`
  - `results/topic05_regression_line_evolution.png`

Shared helpers are in `common/`:

- `common/runtime.py`: logging, JSON artifact writing, hardware metadata
- `common/ml_utils.py`: reusable data split and baseline model builders

## Dataset Explanations

All datasets are built-in `scikit-learn` datasets or synthetic data generated in code.
The Stage 1 project runbook in Chapter 1 also uses a local finance CSV:

### `data/stock_5m_sample.csv` (used by Stage 1 project runbook)

- Task type: regression
- Structure: OHLCV bars at 5-minute granularity
- Columns: `timestamp, open, high, low, close, volume, symbol`
- Suggested target: `next_5m_volatility = abs(log(close_t+1 / close_t))`
- Why used here: aligns the Stage 1 pipeline with realistic trading-system style tabular workflows

### `load_breast_cancer` (used in `topic01`, `topic03`, `topic09`, `topic11`)

- Task type: binary classification
- Size: 569 samples, 30 numeric features
- Target (`y`): `0 = malignant`, `1 = benign`
- Why used here: clean numeric benchmark suitable for metrics, validation split, and regularization demos

### `load_iris` (used in `topic02`)

- Task type: clustering/classification benchmark
- Size: 150 samples, 4 numeric features
- Target (`y_true`): species labels (`setosa`, `versicolor`, `virginica`)
- Why used here: small interpretable dataset for K-Means and cluster quality scores

### `load_diabetes` (used in `topic06`)

- Task type: regression
- Size: 442 samples, 10 numeric features
- Target (`y`): quantitative disease progression measure
- Why used here: train/test evaluation and overfitting behavior in regression

### `make_classification` (used in `topic08`)

- Task type: synthetic binary classification
- Size in script: 1500 samples, 20 features
- Target (`y`): generated class label (`0/1`)
- Why used here: controlled dataset for bias-variance visualization

### Synthetic data generated in scripts

- `topic05_gradient_descent.py`: `y = 3x + 5 + noise`
- `topic07_overfitting.py`: `y = sin(2*pi*x) + noise`
- `topic10_feature_engineering.py`: synthetic house-price data from area, rooms, age
- `topic12_pytorch_cuda.py`: tensor regression data `y = 2.5x + 1.0 + noise`

### Small manual arrays

- `topic04_cost_function.py`: tiny hardcoded arrays for manual loss verification
