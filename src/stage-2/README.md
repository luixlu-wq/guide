# Stage 2 Runnable Examples

This folder contains complete runnable examples for Stage 2: Python tools for AI data work.

## Setup (CPU Path)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup (Optional GPU Bridge)

```bash
pip install -r requirements-gpu.txt
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## Run

Fail-fast run (CPU topics):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1
```

Fail-fast run including optional GPU bridge:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1 -IncludeGpu
```

## Topics

- `topic01_numpy_vectorization.py`: vectorization vs loop performance
- `topic02_numpy_shape_broadcasting.py`: shape handling and broadcasting
- `topic03_pandas_load_inspect.py`: CSV load + inspect pattern
- `topic04_pandas_clean_transform.py`: cleaning and transformation workflow
- `topic05_feature_engineering_time_series.py`: derived features for time-series
- `topic06_matplotlib_data_debugging.py`: visual debugging and anomaly visibility
- `topic07_sklearn_split_preprocess.py`: train/test split + preprocessing
- `topic08_sklearn_pipeline_leakage.py`: wrong vs correct preprocessing order
- `topic09_stage2_end_to_end_pipeline.py`: full tabular pipeline + metrics artifact
- `topic10_pytorch_cuda_bridge.py` (optional): tensors/autograd/CUDA bridge

## Outputs Created by Scripts

- `topic03_data.csv`
- `topic06_line.png`
- `topic06_hist.png`
- `results/topic09_metrics.json`

## Data Source Summary

- Built-in / generated synthetic data only.
- No external download is required for these scripts.
