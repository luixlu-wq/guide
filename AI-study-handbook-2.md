# Stage 2 - Python for AI Data Workflows

*(Week 3 core + optional extension week)*

---

## 0. How to Use This Handbook

### Who This Stage Is For

This stage is for learners who completed Stage 1 and can run basic Python scripts.

You are not learning "all Python."
You are learning the Python data stack used in real AI work:

- NumPy
- Pandas
- Matplotlib
- scikit-learn
- PyTorch/CUDA bridge (mandatory in this handbook track; CPU fallback allowed when CUDA is unavailable)

### Recommended Order

1. Complete setup and verify scripts run.
2. Follow the roadmap day by day.
3. For each topic:
   - read concept
   - run script
   - compare output to expected range
   - write short interpretation
   - answer quick check
4. Complete project and self-test before moving on.

### Stage 2 Pipeline Mental Model (ETL)

Treat Stage 2 as one engineering pipeline, not isolated tools:

- Extract: Pandas `read_csv` / `read_sql` and schema inspection
- Transform: NumPy vectorization + Pandas feature engineering
- Load: Convert to model-ready arrays/tensors and place on CPU/GPU device correctly

This pipeline view helps you debug by stage: data ingest issues, transformation issues, and device/runtime issues.

### If You Get Stuck

- Check script input shapes and column names first.
- Re-run from a clean terminal session.
- Use the debugging checklist in Section 7.
- Revisit the mapped official docs in Study Materials.

---

## 1. Prerequisites and Environment Setup

### Required Knowledge

- Basic Python (variables, loops, functions, lists, dicts)
- Ability to run `.py` scripts from terminal

### Required Software

- Python 3.10+
- pip
- PowerShell/bash terminal

Check version:

```bash
python --version
```

### Setup (CPU Path)

**Windows**

```bash
cd red-book\src\stage-2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Unix/macOS**

```bash
cd red-book/src/stage-2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### PyTorch/CUDA Bridge Setup (Mandatory Module for This Track)

```bash
pip install -r requirements-gpu.txt
```

Verify CUDA:

```bash
nvidia-smi
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
```

### Verify Stage 2 Setup

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1
```

GPU acceleration run (if CUDA is available on this machine):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1 -IncludeGpu
```

---

## 2. One-Week Core Roadmap (+ Optional Extension)

### Week 1 Core

| Day | Focus | Script(s) | Deliverable |
|---|---|---|---|
| 1 | NumPy vectorization and broadcasting | topic01, topic02 | Explain shape and vectorization speedup |
| 2 | Pandas load and inspect | topic03 | Data inspection note (columns, dtypes, missing) |
| 3 | Pandas clean and transform | topic04 | Before/after cleaning summary |
| 4 | Feature engineering for time series | topic05 | Explain each engineered column |
| 5 | Visualization for debugging | topic06 | Interpret line plot and histogram |
| 6 | scikit-learn split, preprocessing, leakage | topic07, topic08 | Explain wrong vs correct workflow |
| 7 | End-to-end tabular pipeline + bridge basics | topic09, topic10, topic11 | Save metrics artifact + explain CPU fallback and VRAM checks |

### Optional Extension Week

| Day | Focus | Script(s) | Deliverable |
|---|---|---|---|
| 8 | Project expansion and additional features | topic05, topic09 | Updated feature list with rationale |
| 9 | Error analysis and leakage audit | topic08, topic09 | Leakage prevention checklist |
| 10 | GPU bridge deepening and troubleshooting | topic10, topic11 | CPU vs GPU + memory management note |
| 11 | Documentation and reproducibility | run_all_stage2 | Run log and environment note |
| 12 | Self-test and weak-topic review | handbook self-test | Score + remediation plan |
| 13-14 | Final polish and handoff | all | Stage completion checklist |

---

## 3. Study Materials

### Must Complete

- NumPy Quickstart: https://numpy.org/doc/stable/user/quickstart.html
- Pandas Getting Started: https://pandas.pydata.org/docs/getting_started/index.html
- Python for Data Analysis (Wes McKinney): https://wesmckinney.com/book/
- Matplotlib Tutorials: https://matplotlib.org/stable/tutorials/index.html
- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn Common Pitfalls: https://scikit-learn.org/stable/common_pitfalls.html
- Kaggle Pandas: https://www.kaggle.com/learn/pandas
- Kaggle Data Visualization: https://www.kaggle.com/learn/data-visualization

### Should Complete

- Python Data Science Handbook: https://jakevdp.github.io/PythonDataScienceHandbook/
- Kaggle Intro to ML: https://www.kaggle.com/learn/intro-to-machine-learning
- handson-ml3 examples: https://github.com/ageron/handson-ml3
- Effective Pandas (Matt Harrison): https://books.google.com/books/about/Effective_Pandas.html?id=bYP0zgEACAAJ
- Modern Pandas (method chaining): https://tomaugspurger.net/posts/method-chaining/

### Optional Deepening

- ISLP: https://www.statlearning.com/
- D2L: https://d2l.ai/
- PyTorch Tutorials: https://pytorch.org/tutorials/
- PyTorch CUDA semantics: https://pytorch.org/docs/stable/notes/cuda.html
- NVIDIA CUDA Refresher (Getting Started): https://developer.nvidia.com/blog/cuda-refresher-getting-started-with-cuda/
- NVIDIA CUDA Refresher (Programming Model): https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/

---

## 4. Learning Targets (With Pass Checks)

### Target 1: NumPy vectorized computation

- Run `topic01_numpy_vectorization.py`
- Explain loop vs vectorized timing difference
- Pass check: you can explain why vectorization is usually faster

### Target 2: NumPy shapes and broadcasting

- Run `topic02_numpy_shape_broadcasting.py`
- Explain how row and column broadcasting works
- Pass check: you can predict output shape before running

### Target 3: Pandas load and inspect

- Run `topic03_pandas_load_inspect.py`
- Report shape, dtypes, missing values, column names
- Pass check: you can identify at least one potential data issue

### Target 4: Pandas cleaning and transformation

- Run `topic04_pandas_clean_transform.py`
- Explain all cleaning steps and why each is needed
- Pass check: before/after missing values and row count are clearly interpreted

### Target 5: Feature engineering

- Run `topic05_feature_engineering_time_series.py`
- Explain `return_1d`, `ma_5`, `ma_20`, `volatility_5`
- Pass check: you can describe why rolling features create NaN rows

### Target 6: Visualization as debugging

- Run `topic06_matplotlib_data_debugging.py`
- Explain what anomaly and distribution chart reveal
- Pass check: saved plot files exist and are interpreted

### Target 7: Proper split and preprocessing

- Run `topic07_sklearn_split_preprocess.py`
- Explain split order and scaler usage
- Pass check: you can explain what happens if you fit scaler on all data

### Target 8: Leakage prevention with pipeline

- Run `topic08_sklearn_pipeline_leakage.py`
- Compare wrong and correct workflow scores
- Pass check: you can explain leakage risk in one sentence

### Target 9: End-to-end pipeline

- Run `topic09_stage2_end_to_end_pipeline.py`
- Inspect saved metrics JSON
- Pass check: you can explain R2, MAE, and MSE from output

### Target 10: PyTorch/CUDA bridge (mandatory module, CPU fallback accepted)

- Run `topic10_pytorch_cuda_bridge.py`
- Run `topic11_linear_gradient_example.py`
- Explain tensor/autograd/device concepts
- Pass check: you can explain CPU fallback when CUDA is unavailable, and how to monitor memory when CUDA is available

---

## 5. Operatable Examples for Stage 2

All runnable files are in:

- `red-book/src/stage-2/`

### Quick Workflow

**Windows**

```bash
cd red-book\src\stage-2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1
```

GPU acceleration run (if CUDA is available on this machine):

```bash
pip install -r requirements-gpu.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1 -IncludeGpu
```

**Unix/macOS**

```bash
cd red-book/src/stage-2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pwsh -File ./run_all_stage2.ps1
```

### Script Reference and Expected Outputs

| Script | Topic | Expected Output |
|---|---|---|
| `topic01_numpy_vectorization.py` | NumPy vectorization | vectorized time lower than loop time; equal outputs = True |
| `topic02_numpy_shape_broadcasting.py` | Broadcasting | prints shapes and resulting matrices from row/column broadcast |
| `topic03_pandas_load_inspect.py` | Load/inspect | shape `(120, 4)`, column list, info, missing-value summary |
| `topic04_pandas_clean_transform.py` | Clean/transform | missing values reduce to zero; duplicates removed; cleaned head printed |
| `topic05_feature_engineering_time_series.py` | Feature engineering | new feature columns created; post-dropna shape and summary stats printed |
| `topic06_matplotlib_data_debugging.py` | Visualization | saves `topic06_line.png` and `topic06_hist.png` |
| `topic07_sklearn_split_preprocess.py` | Split+preprocess | train/test shapes and strong test metrics printed |
| `topic08_sklearn_pipeline_leakage.py` | Leakage | wrong vs correct accuracy with small but visible delta |
| `topic09_stage2_end_to_end_pipeline.py` | End-to-end pipeline | prints `r2`, `mae`, `mse`; saves `results/topic09_metrics.json` |
| `topic10_pytorch_cuda_bridge.py` | PyTorch/CUDA bridge | prints torch/cuda status, autograd demo, learned params near expected values; CPU/GPU timing note |
| `topic11_linear_gradient_example.py` | Gradient verification | compares manual gradient and autograd gradient; shows parameter updates clearly |

### Data Resource and Data Structure Declarations

All Stage 2 scripts explicitly declare:

- data source (built-in or synthetic)
- row count
- feature structure
- target definition (if present)
- task type

Recommended canonical Stage 2 project dataset:

- `red-book/src/stage-2/data/ohlcv_5m_sample.csv` (or equivalent user-provided OHLCV time-series table)

---

## 6. Key Knowledge - Concept Modules

Each module includes:

- what it is
- why it matters
- data declaration
- worked example
- common beginner mistake + fix
- demonstration checklist
- quick check

### How to Execute Each Module (Detailed Tutorial Loop)

For every module in this section, use this exact loop:

1. Read `What it is` and `Why it matters`.
2. Copy the data declaration into your notes.
3. Run the mapped script from `red-book/src/stage-2/`.
4. Compare actual output with the expected behavior in Section 5.
5. Write:
   - what worked
   - one confusion point
   - one concrete takeaway
6. Answer the quick check without looking at references.

Use this note template:

```
Module:
Script:
Observed output:
Interpretation:
Common mistake to avoid:
Quick-check answer:
```

### Module 1: NumPy Vectorization

What it is:
- Operating on full arrays without Python loops.
- NumPy arrays are contiguous typed memory blocks managed by optimized native code (C-level loops), not Python object-by-object containers.

Why it matters:
- Faster and cleaner numeric computation.
- This is the memory layer of AI data processing: contiguous memory layout + SIMD-friendly operations are the main reason vectorized code is fast.

Data declaration:
```
Data: synthetic random float array
Rows: 1,000,000
Features: one numeric vector
Target: none
Type: numerical computation
```

Common mistake:
- Writing loops for simple element-wise operations.

Fix:
- Use array expressions first (`x * 2 + 1`).

Demo:
- `topic01_numpy_vectorization.py`

Quick check:
- Why can vectorized code outperform loops even when operation is the same?

Developer note:
- Think of NumPy as "C arrays with Python ergonomics."
- Python loop version: Python interpreter controls each element step.
- Vectorized version: native kernels operate on whole memory blocks.

Detailed tutorial instructions:

1. Run:
   - `python topic01_numpy_vectorization.py`
2. Record:
   - loop time
   - vectorized time
   - speedup
3. Verify:
   - `outputs equal` is `True`
4. Interpret:
   - explain why "same math, different implementation" changes runtime.
5. Troubleshoot:
   - if speedup seems small, increase data size and re-test.

---

### Module 2: NumPy Shapes and Broadcasting

What it is:
- Shape-aware arithmetic between arrays of compatible dimensions.

Why it matters:
- Prevents shape bugs and reduces boilerplate code.
- Broadcasting is the highest-frequency source of silent logic bugs when moving from loop-based code to tensor math.

Data declaration:
```
Data: synthetic matrix and vectors
Rows: matrix 3x4
Features: numeric matrix values
Target: none
Type: array operations
```

Common mistake:
- Ignoring shape before operation.

Fix:
- Print `.shape` and reason about broadcast alignment.

Demo:
- `topic02_numpy_shape_broadcasting.py`

Quick check:
- What is output shape of `(3,4) + (4,)`?

Broadcasting rules (must memorize):

1. NumPy compares dimensions from right to left.
2. Two dimensions are compatible if:
   - they are equal, or
   - one of them is `1`.
3. If neither condition is true, broadcasting fails.

Right-aligned shape examples:

```
(3,4) + (4,)   -> (3,4)   # row vector across rows
(3,4) + (3,1)  -> (3,4)   # column vector across columns
(3,4) + (3,)   -> error    # trailing dims 4 vs 3 are incompatible
```

Detailed tutorial instructions:

1. Run:
   - `python topic02_numpy_shape_broadcasting.py`
2. Before reading output:
   - predict output shape for each operation.
3. Compare predictions with actual printed results.
4. Interpret:
   - explain why row vector broadcasts across rows.
5. Troubleshoot:
   - if output shape surprises you, draw dimensions on paper before rerunning.

---

### Module 3: Pandas Load and Inspect

What it is:
- Read CSV and inspect structure before transforming.
- Use Pandas Index to turn a plain table into a label-aligned data engine for selection, joins, and time-based operations.

Why it matters:
- Prevents downstream bugs from wrong dtypes/columns.
- Index quality directly impacts correctness and speed of lookup, alignment, and rolling-window computation.

Data declaration:
```
Data: synthetic CSV table created by script
Rows: 120
Features: date, close, volume, sector
Target: none
Type: tabular inspection
```

Common mistake:
- Start cleaning/modeling before checking `info()` and missing values.

Fix:
- Always inspect `shape`, `columns`, `dtypes`, `isna().sum()` first.

Demo:
- `topic03_pandas_load_inspect.py`

Quick check:
- Why is `date` initially `object` after CSV load?

Pandas Index engineering note:

- `RangeIndex` is default integer indexing.
- `DatetimeIndex` enables fast time slicing, rolling windows, and aligned joins.
- Conceptually, index labels act like keys in a high-performance lookup/alignment layer.

Quant-oriented operation examples:

```python
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").set_index("date")

# Daily return-style change
df["ret_1"] = df["close"].pct_change()

# 20-period rolling average (classic quant baseline)
df["ma_20"] = df["close"].rolling(window=20, min_periods=20).mean()
```

Large-data memory note (operational):

If CSV size can exceed RAM, use chunked extraction:

```python
import pandas as pd

for chunk in pd.read_csv("big_ohlcv.csv", chunksize=200_000):
    # transform per chunk, then append/save intermediate results
    ...
```

Use chunking on CPU-side ingest and batching on model-side tensor loading.

Detailed tutorial instructions:

1. Run:
   - `python topic03_pandas_load_inspect.py`
2. Verify:
   - generated CSV exists (`topic03_data.csv`)
   - column list and dtypes are printed
3. Interpret:
   - identify which columns should later be type-converted and why.
4. Execute quant-style index operations in a scratch cell/script:
   - convert date to datetime
   - set datetime index
   - run `pct_change()` and `rolling(window=20).mean()`
   - explain why early rolling rows are NaN by design
5. Troubleshoot:
   - if file path errors occur, run from `red-book/src/stage-2/`.

---

### Module 4: Pandas Clean and Transform

What it is:
- Normalize column names, parse dates, sort, deduplicate, fill missing values.

Why it matters:
- Dirty data causes hidden failures in plots/features/models.

Data declaration:
```
Data: synthetic dirty table
Rows: 12
Features: Date, Close Price, Volume
Target: none
Type: tabular cleaning
```

Common mistake:
- Filling missing values without understanding source pattern.

Fix:
- Print before/after missing summaries and explain chosen fill logic.

Demo:
- `topic04_pandas_clean_transform.py`

Quick check:
- Why sort by date before creating rolling features?

Detailed tutorial instructions:

1. Run:
   - `python topic04_pandas_clean_transform.py`
2. Verify:
   - missing-value counts before and after cleaning
   - row count change after deduplication
3. Interpret:
   - explain each transformation step and its purpose.
4. Troubleshoot:
   - if missing values remain, inspect fill strategy and column dtypes.

---

### Module 5: Feature Engineering

What it is:
- Deriving informative columns from raw data.

Why it matters:
- Better features often improve model quality more than changing model type.

Data declaration:
```
Data: synthetic close-price time series
Rows: 180
Features: close plus engineered return/MA/volatility columns
Target: direction_up
Type: feature engineering
```

Common mistake:
- Forgetting rolling operations create NaN at start of series.

Fix:
- Explicitly drop or handle NaN rows after feature creation.

Demo:
- `topic05_feature_engineering_time_series.py`

Quick check:
- Why can MA20 not be computed for early rows?

Detailed tutorial instructions:

1. Run:
   - `python topic05_feature_engineering_time_series.py`
2. Verify:
   - engineered columns exist
   - shape decreases after `dropna()`
3. Interpret:
   - explain what each feature expresses (trend, momentum, variability).
4. Troubleshoot:
   - if NaN handling seems wrong, print first 25 rows before dropping.

---

### Module 6: Matplotlib for Data Debugging

What it is:
- Use charts to detect anomalies and distribution shifts.

Why it matters:
- Visual inspection catches pipeline problems quickly.

Data declaration:
```
Data: synthetic time series with injected anomaly
Rows: 160
Features: date, close, ma_10, return_1d
Target: none
Type: visualization/debugging
```

Common mistake:
- Treat plots as decoration, not validation.

Fix:
- Every plot should answer a concrete question.

Demo:
- `topic06_matplotlib_data_debugging.py`

Quick check:
- What does a sudden spike in line plot suggest you should inspect?

Detailed tutorial instructions:

1. Run:
   - `python topic06_matplotlib_data_debugging.py`
2. Verify:
   - `topic06_line.png` and `topic06_hist.png` are created
3. Inspect plots manually:
   - point out anomaly location and distribution characteristics.
4. Interpret:
   - explain what checks you would run next in a real pipeline.
5. Troubleshoot:
   - if plots do not save, confirm write permission in the script directory.

---

### Module 7: Split and Preprocess in scikit-learn

What it is:
- Split data first, then fit preprocessing and model on training data.

Why it matters:
- Prevents leakage and preserves honest evaluation.

Data declaration:
```
Data: Breast Cancer Wisconsin (sklearn built-in)
Rows: 569
Features: 30 numeric columns
Target: diagnosis (binary)
Type: classification
```

Common mistake:
- Fitting scaler using full dataset before split.

Fix:
- Use pipeline with split-first workflow.

Demo:
- `topic07_sklearn_split_preprocess.py`

Quick check:
- Why is test set excluded from scaler fit?

Detailed tutorial instructions:

1. Run:
   - `python topic07_sklearn_split_preprocess.py`
2. Verify:
   - train/test shapes and metrics are printed.
3. Interpret:
   - explain why split happens before preprocessing.
4. Troubleshoot:
   - if model fails to converge, increase `max_iter` and rerun.

---

### Module 8: Leakage and Pipeline Pattern

What it is:
- Compare wrong preprocessing order with proper pipeline execution.

Why it matters:
- Leakage can make metrics look better than true generalization.

Data declaration:
```
Data: synthetic high-dimensional classification data
Rows: 900
Features: 2000
Target: binary label
Type: leakage demonstration
```

Common mistake:
- Selecting features before train/test split.

Fix:
- Wrap feature selection + scaling + model in one pipeline and fit only on train.

Demo:
- `topic08_sklearn_pipeline_leakage.py`

Quick check:
- Why can "wrong workflow" score be inflated?

Detailed tutorial instructions:

1. Run:
   - `python topic08_sklearn_pipeline_leakage.py`
2. Verify:
   - both wrong and correct workflow scores are printed.
3. Interpret:
   - explain why preprocessing on full data before split leaks information.
4. Troubleshoot:
   - if delta is small, rerun with different random seeds and compare trend.

---

### Module 9: End-to-End Tabular Pipeline

What it is:
- Full workflow from synthetic data generation to saved metrics artifact.

Why it matters:
- Integrates all Stage 2 skills into one reproducible script.

Data declaration:
```
Data: synthetic house dataset with numeric + categorical features
Rows: 500
Features: area, rooms, age, zone
Target: price
Type: end-to-end regression pipeline
```

Common mistake:
- Mixing preprocessing steps outside pipeline and losing reproducibility.

Fix:
- Use `ColumnTransformer` + `Pipeline` and save metrics to file.

Demo:
- `topic09_stage2_end_to_end_pipeline.py`

Quick check:
- Why is one-hot encoding required for `zone`?

Detailed tutorial instructions:

1. Run:
   - `python topic09_stage2_end_to_end_pipeline.py`
2. Verify:
   - `results/topic09_metrics.json` is generated.
3. Inspect:
   - open JSON and explain R2, MAE, MSE in plain language.
4. Interpret:
   - explain why numeric and categorical preprocessing are separated.
5. Troubleshoot:
   - if JSON missing, verify `results/` path and script permissions.

---

### Module 10: PyTorch/CUDA Bridge (Mandatory for This Track, CPU Fallback Allowed)

What it is:
- Intro to tensors, autograd, and device placement.

Why it matters:
- Bridges tabular Python workflows to model-training frameworks.
- This module is required because real AI pipelines eventually move from DataFrame operations to tensor compute and device/runtime constraints.

Conceptual and theory guide:

- **Tensor (PyTorch core object)**:
  - A tensor is a multi-dimensional numeric container (generalization of scalar/vector/matrix).
  - In training, tensors hold:
    - model parameters (weights/bias)
    - input batches
    - model outputs
    - gradients
- **Computational graph**:
  - During forward pass, PyTorch records operations as a graph when `requires_grad=True`.
  - Each node represents an operation; edges represent data flow.
- **Autograd (automatic differentiation)**:
  - Uses chain rule to compute `d(loss)/d(parameter)` for each trainable parameter.
  - Calling `loss.backward()` traverses graph in reverse and accumulates gradients in `.grad`.
- **CUDA device model**:
  - CPU and GPU have separate memory spaces.
  - Tensors must be moved to same device as model parameters (`.to("cuda")`).
  - GPU acceleration helps mostly for larger batch/matrix workloads due to transfer + kernel overhead.

DataFrame -> NumPy -> Tensor bridge (zero-copy boundary tutorial):

```python
import pandas as pd
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_csv("topic03_data.csv")
df["close"] = df["close"].astype("float32")

# Zero-copy (when possible) from pandas-managed memory to NumPy view.
arr = df[["close"]].to_numpy(dtype="float32", copy=False)

# Zero-copy CPU tensor view over NumPy memory.
x_cpu = torch.from_numpy(arr)

# Required memory transfer to device if CUDA is used.
x_dev = x_cpu.to(device)
```

Important:
- `from_numpy` shares CPU memory (no copy).
- Moving to CUDA always performs a device transfer (not zero-copy across CPU->GPU boundary).
- Goal is to avoid unnecessary extra copies before the device transfer.

VRAM management (required operational checks):

```python
if torch.cuda.is_available():
    torch.cuda.reset_peak_memory_stats()
    before_mb = torch.cuda.memory_allocated() / (1024 ** 2)
    # ... run batch/tensor operations ...
    after_mb = torch.cuda.memory_allocated() / (1024 ** 2)
    peak_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)
    print("vram_before_mb:", round(before_mb, 2))
    print("vram_after_mb :", round(after_mb, 2))
    print("vram_peak_mb  :", round(peak_mb, 2))
    torch.cuda.empty_cache()  # release cached blocks back to allocator pool
```

For RTX 5090-class hardware (32GB VRAM), record these values per run to build a memory budget baseline before scaling batch sizes.

How model training works (theory -> execution):

Training repeats this loop:

1. **Forward pass**:
   - Compute predictions from inputs and current parameters.
   - Example linear model: `y_hat = XW + b`.
2. **Loss computation**:
   - Measure prediction error (e.g., MSE).
3. **Backward pass**:
   - `loss.backward()` computes gradients:
   - `grad_W = d(loss)/dW`, `grad_b = d(loss)/db`.
4. **Parameter update**:
   - Gradient descent step:
   - `W = W - lr * grad_W`, `b = b - lr * grad_b`.
5. **Gradient reset**:
   - Clear old gradients (`zero_grad`) before next iteration.

Why this converges:

- If learning rate is reasonable, updates move parameters toward lower loss.
- Over many iterations, predictions align better with target patterns.

Minimal training pseudo-structure:

```python
for batch_x, batch_y in data_loader:
    pred = model(batch_x)           # forward
    loss = loss_fn(pred, batch_y)   # objective
    loss.backward()                 # backward (autograd)
    optimizer.step()                # update params
    optimizer.zero_grad()           # clear grads
```

Concrete gradient example (linear regression):

Model:

```
y_hat = w*x + b
loss  = (1/n) * Σ (y_hat - y)^2
```

Parameter gradients:

```
d(loss)/dw = (2/n) * Σ (y_hat - y) * x
d(loss)/db = (2/n) * Σ (y_hat - y)
```

Update step:

```
w_new = w_old - lr * d(loss)/dw
b_new = b_old - lr * d(loss)/db
```

Tiny numeric intuition:

- If prediction is too high (`y_hat > y`), error term is positive.
- Then `d(loss)/dw` and/or `d(loss)/db` often become positive.
- Subtracting a positive gradient moves parameters downward.
- This usually lowers future predictions and reduces loss.

In PyTorch autograd terms:

- You define forward and loss.
- `loss.backward()` computes these gradients automatically.
- Optimizer step applies the same update rule without manual derivative coding.

Runnable concrete script for this section:

- `topic11_linear_gradient_example.py`

CPU vs GPU in training:

- **CPU**:
  - Lower startup overhead, good for small models/datasets.
- **GPU (CUDA)**:
  - Massive parallelism for matrix-heavy operations.
  - Usually faster for larger batch sizes and deeper models.
  - Can be slower on tiny workloads due to transfer and launch overhead.

Data declaration:
```
Data: synthetic tensor regression data
Rows: 30,000
Features: x tensor [N,1]
Target: y tensor [N,1]
Type: PyTorch/CUDA bridge
```

Common mistake:
- Mixing CPU and CUDA tensors in one operation.

Fix:
- Keep all tensors/model on same device.

Demo:
- `topic10_pytorch_cuda_bridge.py`
- `topic11_linear_gradient_example.py`

Quick check:
- What should your script do if CUDA is unavailable?

Theory check:
- Why do we call `optimizer.zero_grad()` every iteration?
- What does `loss.backward()` compute conceptually?
- Why can GPU show little or no speedup for very small matrices?

Detailed tutorial instructions:

1. Run:
   - `python topic10_pytorch_cuda_bridge.py`
   - `python topic11_linear_gradient_example.py`
2. Verify:
   - torch version, CUDA availability, and autograd outputs are printed.
   - manual and autograd gradients match in topic11 output
3. Interpret:
   - if CUDA is `False`, explain why CPU fallback is still correct behavior.
4. If CUDA is available:
   - compare CPU and GPU timing and write one sentence about workload size effects.
5. Troubleshoot:
   - if CUDA expected but unavailable, re-check PyTorch install build and `nvidia-smi`.

Training-logic walkthrough (with this module's script):

1. Identify trainable parameters:
   - `w`, `b` tensors with `requires_grad=True`.
2. Follow one epoch mentally:
   - compute `pred = x @ w + b`
   - compute MSE loss
   - call backward to populate gradients
   - update `w`, `b` with learning rate
3. Validate learning:
   - `w` should approach ~1.8 and `b` should approach ~-0.7.
4. Relate output to theory:
   - decreasing loss indicates gradients point in useful descent direction.
5. Device reasoning:
   - explain why both `x` and parameters must be on same device.

---

## 7. Debugging Checklist (Stage 2)

If scripts fail or outputs look wrong:

- [ ] Did file load succeed and path match?
- [ ] Are columns exactly what your code expects?
- [ ] Are datetime columns parsed and sorted?
- [ ] Did cleaning reduce missing values as intended?
- [ ] Are feature shapes compatible for model input?
- [ ] Did preprocessing fit only on training data?
- [ ] Are expected artifacts (png/json/csv) created?
- [ ] Did you rerun from clean environment after dependency changes?

### Shape Mismatch Checklist (High Priority)

Use this checklist whenever you see matrix/tensor errors or suspicious outputs:

- [ ] Print all operand shapes right before the failing line.
- [ ] Verify matrix multiplication rule:
  - `(a, b) @ (b, c) -> (a, c)`
- [ ] Check for common mismatch pattern:
  - `(64, 10) @ (1, 10)` is invalid; second tensor should be `(10, c)` for matrix multiply.
- [ ] Verify you did not accidentally keep singleton dimensions (`(n, 1)` vs `(n,)`).
- [ ] For broadcasting ops, compare trailing dimensions from right to left.
- [ ] In pandas-to-NumPy conversion, verify final feature matrix shape is `(rows, features)`.
- [ ] In PyTorch, verify input tensor and model parameters are on the same device.

Quick shape debug snippet:

```python
print("X shape:", X.shape)
print("W shape:", W.shape)
print("b shape:", b.shape)
print("device X:", getattr(X, "device", "cpu"))
```

---

## 8. Practice Project

Project goal:
- Build a reproducible data pipeline from raw-like tabular data to evaluated model metrics.
- Default project context: OHLCV-style time-series data (for example `ohlcv_5m_sample.csv`) with chronological split rules.
- Starter file in this repo: `red-book/src/stage-2/data/ohlcv_5m_sample.csv`.

Required pipeline framing (ETL):

- Extract: load data, validate schema, inspect dtypes/missing values.
- Transform: clean data, engineer features, enforce time-aware ordering/splits.
- Load: prepare model/tensor inputs, run evaluation, save reproducible artifacts.

Required outputs:
- cleaned and transformed data summary
- engineered feature summary
- at least two plots
- metrics JSON artifact
- short interpretation note (what worked, what failed, what to improve)
- vectorized vs loop runtime comparison for one transformation step
- explicit train/validation/test split policy for time-series (no random future leakage)

Quality gates:
- script runs end-to-end from clean environment
- no leakage pattern in pipeline
- expected output artifacts are generated

---

## 9. Self-Test and Scoring Rubric

Weighted rubric:

- Data handling (NumPy + Pandas): 35%
- Visualization and interpretation: 20%
- scikit-learn preprocessing/evaluation: 30%
- Debugging and leakage awareness: 15%

Score bands:

- >= 85: ready for next stage
- 70-84: proceed with focused review
- < 70: rerun weak-topic scripts and retake test

### Code Review Checklist (Efficiency + Operability)

Apply this checklist to your Stage 2 scripts and project notebook:

- [ ] Uses vectorized NumPy/Pandas operations for column/array math where possible.
- [ ] Avoids unnecessary row-wise `.apply()` for operations that can be vectorized.
- [ ] Declares data source, shape, feature columns, and target clearly.
- [ ] Uses split-first then fit-transform on train-only to avoid leakage.
- [ ] Logs or saves key metrics/artifacts for reproducibility.
- [ ] Documents shape checks at critical boundaries (pre-model and pre-tensor).
- [ ] Handles CUDA unavailable case safely (CPU fallback path).

Suggested deduction guide (for peer/self review):

- `-10` points: uses row-wise `.apply()` where a clear vectorized expression exists.
- `-10` points: missing or unclear data declaration.
- `-15` points: leakage risk (fit on full dataset before split).
- `-10` points: no saved artifacts/metrics for reproducibility.
- `-10` points: no shape/device checks at model or tensor boundaries.

---

## 10. What Comes After Stage 2

Stage 3 builds on Stage 2 by moving from "tool usage" to "system building."
You will use these foundations to construct larger AI workflows, stronger model experiments, and reproducible project structures.

Before moving on, you must be able to:
- clean and inspect data confidently
- engineer and validate features
- run split/preprocess/train/evaluate workflow without leakage
