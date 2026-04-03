# Stage 1 — AI and Machine Learning Fundamentals

*(Week 1–2)*

---

## 0. How to Use This Handbook

### Who This Is For

This handbook is designed for beginners who know basic Python (loops, functions, lists, dicts) but have no prior machine learning experience. If you can read and run a Python script, you have enough to start.

### Recommended Reading Order

Follow the handbook linearly on your first pass:

1. Complete Prerequisites and Environment Setup so your scripts can run.
2. Read the Two-Week Guided Roadmap to understand what each day targets.
3. For each day's topic: read the concept module, run the mapped script, interpret the output, and answer the quick check.
4. After Week 2, take the Self-Test to confirm readiness before Stage 2.

If you are revisiting a specific topic, jump directly to the concept module. Each module is self-contained.

### How to Use Scripts Alongside the Text

For every concept module:

1. Read the concept section completely.
2. Run the mapped script from `red-book/src/stage-1/`.
3. Compare the actual output against the expected output documented in this handbook.
4. Write 3–5 lines interpreting what you observed.
5. Answer the quick check question without looking at the answer first.

### What to Do If You Are Stuck

- First: re-read the concept explanation and beginner walkthrough.
- Second: check the "Common Beginner Mistake" box in the module.
- Third: consult the mapped resource in the Study Materials section.
- Fourth: run the script again and add `print()` statements to inspect intermediate values.

---

## 1. Prerequisites and Environment Setup

### Required Knowledge

- Basic Python: variables, loops, functions, lists, dicts
- Ability to run a `.py` file from the terminal
- No prior ML knowledge required

If you are not comfortable with Python basics, complete this first:
- https://docs.python.org/3/tutorial/ (sections 1–5 are sufficient)

### Required Software

- Python 3.10 or higher
- pip (comes with Python)
- A terminal (Command Prompt, PowerShell, or bash)

Check your Python version:

```bash
python --version
```

### Environment Setup

**Windows:**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Unix / macOS:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `requirements.txt` in `red-book/src/stage-1/` contains:

```
numpy>=1.24
pandas>=2.0
scikit-learn>=1.3
matplotlib>=3.7
```

Optional GPU track requirements:

```
pip install -r requirements-gpu.txt
```

The `requirements-gpu.txt` currently contains:

```
torch>=2.3
```

### GPU Track Setup (Optional)

Use this only if you have an NVIDIA GPU and want to run CUDA examples.

Check GPU visibility:

```bash
nvidia-smi
```

Check PyTorch CUDA:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
```

### Verify Setup

Run the first script to confirm everything works:

```
python topic01_supervised_learning.py
```

Expected: accuracy and metric values printed without errors.

For GPU track, run:

```
python topic12_pytorch_cuda.py
```

Expected: torch version, CUDA availability, autograd demo, and CPU/GPU timing (GPU timing only if CUDA is available).

---

## 2. Two-Week Guided Roadmap

Each day has a primary concept, a script to run, and a deliverable.

### Week 1 — Foundations + First Pipeline

| Day | Concept | Script | Deliverable |
|---|---|---|---|
| 1 | ML mental model, supervised vs unsupervised | topic01, topic02 | Write one paragraph: what ML is and is not |
| 2 | Features vs target, feature engineering | topic03, topic10 | List 3 features and explain why they help |
| 3 | Train/test split, validation set, data leakage | topic06, topic09 | Explain train/val/test in your own words |
| 4 | Loss functions, gradient descent | topic04, topic05 | Interpret the loss curve from topic05 |
| 5 | Overfitting, underfitting, bias, variance | topic07, topic08 | Identify underfit and overfit regions in topic08 output |
| 6 | Cross-validation, regularization | topic11 | Explain how regularization prevents overfitting |
| 7 | Build and evaluate baseline pipeline | topic01 + project step 1–5 | Working script with train and test metrics printed |

### Week 2 — Strengthening + Comparison + Reporting

| Day | Focus | Activity | Deliverable |
|---|---|---|---|
| 8 | Model comparison | Run DecisionTree and RandomForest on project data | Comparison table: model, train metric, test metric |
| 9 | Metrics interpretation | Re-read metrics modules, inspect topic01 output | For each metric: write what it measures and when it misleads |
| 10 | Debugging drills | Run all scripts, apply debugging decision flow | Complete debugging checklist per script |
| 11 | Feature improvement | Add 1–2 engineered features to your project | Show before/after metric improvement |
| 12 | Results and charts (+ optional GPU) | Build results table and plots; run topic12 if doing GPU track | results/metrics.json + at least one figure; optional CPU vs GPU notes |
| 13 | Self-test | Take the 30-question self-test | Score and identify weak areas |
| 14 | Final review | Fix gaps, re-run project, check quality gates | All quality gates passed |

### Daily Time Budget

- Focused study per day: 2–3 hours
- Week 1 total: ~16–20 hours
- Week 2 total: ~16–20 hours
- Stage 1 total (minimum track): 32–40 hours

---

## 3. Study Materials

### Must Complete in Stage 1

These are the core learning paths. Complete selected sections, not full courses.

| Resource | Sections | Time |
|---|---|---|
| DeepLearning.AI + Stanford ML Specialization | Beginner modules: supervised learning intro, cost function, gradient descent | 10–12h |
| Google Machine Learning Crash Course | Framing, Descending into ML, Reducing Loss, Generalization | 5–6h |
| scikit-learn User Guide | Supervised, Unsupervised, Model Evaluation | 4–5h |
| scikit-learn Common Pitfalls | Full guide | 1.5–2h |
| NumPy quickstart | Full guide | 1h |
| pandas getting started | Full guide | 1.5h |
| Matplotlib tutorials | Basic plotting only | 1–1.5h |
| Kaggle Intro to Machine Learning | Full micro-course | 3–4h |
| ISLP — An Introduction to Statistical Learning | Chapter 1 intro + Chapter 2 statistical learning | 4–6h |

Links:
- https://www.coursera.org/specializations/machine-learning-introduction
- https://developers.google.com/machine-learning/crash-course
- https://scikit-learn.org/stable/user_guide.html
- https://scikit-learn.org/stable/common_pitfalls.html
- https://numpy.org/doc/stable/user/quickstart.html
- https://pandas.pydata.org/docs/getting_started/index.html
- https://matplotlib.org/stable/tutorials/index.html
- https://www.kaggle.com/learn/intro-to-machine-learning
- https://www.statlearning.com/

### Should Complete (High Value, If Schedule Allows)

| Resource | Time |
|---|---|
| MIT OCW 6.036 — selected lectures | 4–6h |
| Stanford CS229 handouts | 3–4h |
| Rules of Machine Learning (Google) | 1–2h |
| A Few Useful Things to Know About ML (Domingos) | 1h |
| Microsoft ML for Beginners — selected lessons | 3–5h |
| handson-ml3 notebooks — selected chapters | 3–4h |
| homemade-machine-learning notebooks | 1–2h |

Links:
- https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/
- https://cs229.stanford.edu/materials.html-full
- https://developers.google.com/machine-learning/guides/rules-of-ml/
- https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf
- https://github.com/microsoft/ML-For-Beginners
- https://github.com/ageron/handson-ml3
- https://github.com/trekhleb/homemade-machine-learning

### Optional (Deeper or Broader)

| Resource | Time |
|---|---|
| Dive into Deep Learning (d2l.ai) — selected chapters | 3–5h |
| fast.ai Practical Deep Learning — Part 1 selected | 4–8h |
| Hands-On Machine Learning (O'Reilly) — selected | 8–15h |
| fastai book notebooks | 2–4h |
| Awesome Machine Learning curated list (browse) | 1–2h |

Links:
- https://d2l.ai/
- https://course.fast.ai/
- https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/
- https://github.com/fastai/fastbook
- https://github.com/josephmisiti/awesome-machine-learning

### GPU / PyTorch Track Resources (Optional)

Use these when working on `topic12_pytorch_cuda.py`:

- PyTorch Tutorials: https://pytorch.org/tutorials/
- PyTorch CUDA semantics: https://pytorch.org/docs/stable/notes/cuda.html
- PyTorch local install selector: https://pytorch.org/get-started/locally/

---

## 4. Learning Targets (With Demonstration Criteria)

Use these as required outcomes for Stage 1.

### Target 1: Explain the ML pipeline in plain language

- You must explain: data → model → prediction → error → update.
- Demonstration:
  - Run `topic05_gradient_descent.py`
  - Explain why loss decreases from initial to final value
- Pass check:
  - You can explain what `w`, `b`, and loss mean in the script output

### Target 2: Explain supervised learning with metrics

- You must explain: labels, train/test split, precision/recall/F1.
- Demonstration:
  - Run `topic01_supervised_learning.py`
  - Interpret confusion matrix and metric values
- Pass check:
  - You can explain what a false positive and false negative are

### Target 3: Explain unsupervised learning and clustering quality

- You must explain: no labels during training, cluster assignment, silhouette score.
- Demonstration:
  - Run `topic02_unsupervised_learning.py`
  - Explain silhouette score and cluster counts
- Pass check:
  - You can explain why scaling is applied before K-Means

### Target 4: Explain feature importance and feature engineering

- You must explain: why better features improve prediction, and what feature engineering means.
- Demonstration:
  - Run `topic03_features_vs_target.py` and `topic10_feature_engineering.py`
  - Compare accuracy with meaningful vs shuffled features; compare R² before and after engineering
- Pass check:
  - You can explain why shuffled features degrade performance and give one example of a derived feature

### Target 5: Explain cost functions clearly

- You must explain: MSE for regression and Log Loss for classification.
- Demonstration:
  - Run `topic04_cost_function.py`
  - Verify manual and sklearn losses match
- Pass check:
  - You can explain what each loss penalizes

### Target 6: Explain correct evaluation (train / validation / test)

- You must explain: train set, validation set, test set — and why mixing them is wrong.
- Demonstration:
  - Run `topic06_training_vs_testing.py` and `topic09_validation_set.py`
  - Compare proper split metrics vs same-data metrics; explain the three-way split workflow
- Pass check:
  - You can explain why same-data R² gives false confidence
  - You can explain the difference between validation set and test set

### Target 7: Explain overfitting and model complexity

- You must explain: underfit, good fit, overfit.
- Demonstration:
  - Run `topic07_overfitting.py`
  - Compare cross-validation MSE for degrees 1, 4, and 15
- Pass check:
  - You can explain why a high-degree model fails on validation

### Target 8: Explain bias-variance tradeoff

- You must explain: high bias vs high variance patterns.
- Demonstration:
  - Run `topic08_bias_variance.py`
  - Inspect train error vs validation error across tree depth
- Pass check:
  - You can identify roughly where model complexity is balanced

### Target 9: Explain regularization

- You must explain: what regularization is and how C controls it.
- Demonstration:
  - Run `topic11_regularization.py`
  - Identify the C value with best test accuracy and explain why very high/low C is worse
- Pass check:
  - You can explain the tradeoff in the table output

### Target 10: Explain PyTorch tensors, autograd, and CUDA device use

- You must explain:
  - what a tensor is
  - what autograd computes
  - how device placement (`cpu` vs `cuda`) changes execution
- Demonstration:
  - Run `topic12_pytorch_cuda.py`
  - Explain the autograd derivative output and the learned `w`/`b` values
  - Compare CPU and GPU timing output (if CUDA is available)
- Pass check:
  - You can explain why `.to("cuda")` is needed for GPU tensors
  - You can explain why small workloads may not always show GPU speedup

---

## 5. Operatable Examples for Each Learning Topic

All runnable files are in `red-book/src/stage-1/`.

### Quick Workflow

**Windows:**
```
cd red-book\src\stage-1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage1.ps1
```

Optional GPU track:
```
pip install -r requirements-gpu.txt
powershell -ExecutionPolicy Bypass -File .\run_all_stage1.ps1 -IncludeGpu
```

**Unix/macOS:**
```
cd red-book/src/stage-1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pwsh -File ./run_all_stage1.ps1
```

Optional GPU track:
```
pip install -r requirements-gpu.txt
pwsh -File ./run_all_stage1.ps1 -IncludeGpu
```

### Script Reference and Expected Outputs

| Script | Topic | Expected Output |
|---|---|---|
| `topic01_supervised_learning.py` | Supervised Learning | accuracy ~0.97–0.98, precision ~0.97–0.98, recall ~0.97–0.99, F1 ~0.97–0.98, confusion matrix 2×2 |
| `topic02_unsupervised_learning.py` | Unsupervised / Clustering | silhouette ~0.40–0.55, ARI ~0.55–0.75, cluster counts near [50, 50, 50] |
| `topic03_features_vs_target.py` | Features vs Target | meaningful accuracy ~0.97, shuffled accuracy ~0.50–0.55 |
| `topic04_cost_function.py` | Loss Functions | MSE manual = MSE sklearn = 0.375; LogLoss manual = LogLoss sklearn ≈ 0.254 |
| `topic05_gradient_descent.py` | Gradient Descent | learned w ≈ 3.0, learned b ≈ 5.0; initial loss ~200–400, final loss ~4–6; loss curve PNG saved |
| `topic06_training_vs_testing.py` | Training vs Testing | train R² ≈ 1.0; test R² ≈ 0.10–0.25; wrong evaluation R² ≈ 1.0 |
| `topic07_overfitting.py` | Overfitting | degree=1 has higher CV MSE, degree=4 much lower, degree=15 extremely high/unstable CV MSE (overfit) |
| `topic08_bias_variance.py` | Bias-Variance | best depth often around 6–10; shallow depth: both errors high; deep depth: train low, validation worse |
| `topic09_validation_set.py` | Validation Set | train ~341, val ~114, test ~114; best C in 0.1–1.0 range; final test accuracy ~0.95–0.98 |
| `topic10_feature_engineering.py` | Feature Engineering | baseline and engineered R² both typically high (~0.90+); compare whether engineered features improve, stay similar, or degrade slightly |
| `topic11_regularization.py` | Regularization | table with train/test accuracy per C value; best test at C=0.1–1.0; high C shows small gap growing |
| `topic12_pytorch_cuda.py` | PyTorch + CUDA | torch version and cuda availability printed; autograd derivative shown; learned w near 2.5 and b near 1.0; CPU timing always printed; GPU timing printed if CUDA available |

### Plot Output

`topic05_gradient_descent.py` saves a PNG file (`topic05_loss_curve.png`) in the same directory. The plot should show loss curving downward from a high value and flattening near the bottom. If the curve does not decrease, the learning rate may be too large.

### Reference Sources for Examples

- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn Common Pitfalls: https://scikit-learn.org/stable/common_pitfalls.html
- Google Machine Learning Crash Course: https://developers.google.com/machine-learning/crash-course
- TensorFlow tutorial on overfitting: https://www.tensorflow.org/tutorials/keras/overfit_and_underfit
- ISLP textbook: https://www.statlearning.com/
- D2L book: https://d2l.ai/
- PyTorch tutorials: https://pytorch.org/tutorials/
- PyTorch CUDA semantics: https://pytorch.org/docs/stable/notes/cuda.html

---

## 6. Key Knowledge — Concept Modules

Each module follows this template:
- What it is (plain English)
- Why it matters
- Worked example (with data declaration)
- Common beginner mistake + fix
- Code snippet
- Demonstration checklist
- Quick check
- When to use / when not to use (for algorithms)

---

### Module 1: ML Mental Model

#### What It Is

Machine Learning is learning a function from data.

Given examples of input → output, the model finds a pattern and uses it to predict output for new inputs.

```
input (features) → [model] → output (target)
```

It is NOT intelligence. It is math + optimization applied to data.

#### Why It Matters

Before writing any code, you need the correct mental model. Beginners who think ML is magic make mistakes at every step — they expect too much, debug in the wrong places, and misread results.

#### Worked Example

```
Data: house examples
Rows: 3
Features: house_size (sq ft)
Target: price ($)

| house_size | price  |
|-----------|--------|
| 1000      | 200000 |
| 1500      | 300000 |
| 2000      | 400000 |
```

The computer sees these examples and discovers:

```
price ≈ 200 × house_size
```

That learned relationship is the model. The model does not understand houses. It finds a pattern in numbers.

#### Common Beginner Mistake

**Mistake:** Thinking the model understands context or reasons about cause.

**Fix:** Always ask: What data did it learn from? What pattern is it exploiting? What happens outside that data range?

#### Demonstration Checklist

- [ ] Read the example above and explain the pattern in your own words
- [ ] State one thing a model trained on this data could NOT reliably predict and why
- [ ] State one way the training data could be misleading (e.g., all houses are in one city)

#### Quick Check

If a model predicts house prices using data from a single expensive city, what problem will it have on houses from a different city?

> Answer: It learned a pattern specific to that city's prices. It will likely overestimate or underestimate prices in a different city because the relationship between size and price differs.

---

### Module 2: Supervised vs Unsupervised Learning

#### What It Is

**Supervised learning:** You provide both input data (X) and correct answers (y). The model learns to map X to y.

**Unsupervised learning:** You provide only input data (X). No correct answers. The model discovers hidden structure.

#### Why It Matters

Choosing the wrong learning type leads to the wrong setup entirely. Most beginner ML problems are supervised.

#### Worked Example

```
Data: Supervised — email spam detection
Rows: 4 example emails
Features: email text (simplified)
Target: label (0 = not spam, 1 = spam)
Type: Binary Classification

| Email Text              | Label |
|------------------------|-------|
| "Win money now!"       | 1     |
| "Meeting at 3 PM"      | 0     |
| "Claim your prize"     | 1     |
| "Project update"       | 0     |
```

```
Data: Unsupervised — customer segmentation
Rows: customer behavior data
Features: purchase frequency, average spend
Target: none (labels not known)
Type: Clustering
```

#### Common Beginner Mistake

**Mistake:** Trying to use supervised learning when no labels exist (e.g., "cluster my customers" but then looking for a y column).

**Fix:** Ask first — do I have correct answers for each example? If yes → supervised. If no → unsupervised.

#### Code Snippet

```python
# Supervised: you supply both X and y
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)      # learns from labeled examples
preds = model.predict(X_test)    # predicts labels for new inputs

# Unsupervised: only X, no y
from sklearn.cluster import KMeans
model = KMeans(n_clusters=3)
labels = model.fit_predict(X)    # assigns cluster IDs, no y needed
```

#### Demonstration Checklist

- [ ] Run `topic01_supervised_learning.py` — confirm labels are used during training
- [ ] Run `topic02_unsupervised_learning.py` — confirm no labels are used during fit
- [ ] Explain the silhouette score: what it measures, what a higher value means

#### Quick Check

You have a dataset of medical records. Each record has patient features AND a diagnosis label. Should you use supervised or unsupervised learning?

> Answer: Supervised — you have correct labels (diagnosis), so you can train a model to predict diagnosis from features.

#### When to Use / When Not to Use

| | Supervised | Unsupervised |
|---|---|---|
| Use when | Labels exist; goal is prediction | No labels; goal is discovery |
| Not for | Exploration without labels | Predicting a specific target |

---

### Module 3: Features vs Target

#### What It Is

- **Features (X):** the inputs the model uses to make a prediction
- **Target (y):** the output the model is trying to predict

Bad features produce a bad model regardless of algorithm complexity.

#### Why It Matters

Features determine what information the model has access to. No algorithm can recover signal that is not present in the features.

#### Worked Example

```
Data: Breast Cancer Wisconsin (sklearn built-in)
Rows: 569
Features (X): 30 numeric cell measurements (mean radius, mean texture, ...)
Target (y): 0 = malignant, 1 = benign
Type: Binary Classification
```

```
Good features (real measurements) → model accuracy ~0.97
Shuffled features (randomized)    → model accuracy ~0.52 (near random)
```

The shuffled features destroy all signal. The model cannot learn any pattern.

#### Common Beginner Mistake

**Mistake:** Using a feature that encodes the answer (target leakage). For example: using "diagnosis_text" to predict diagnosis — the feature directly contains the answer.

**Fix:** For every feature ask: would this information be available at prediction time in the real world? If it contains or derives from the answer, remove it.

#### Code Snippet

```python
from sklearn.datasets import load_breast_cancer
X, y = load_breast_cancer(return_X_y=True)

# X = features: 30 cell measurements
# y = target:   0 (malignant) or 1 (benign)
print("feature shape:", X.shape)  # (569, 30)
print("target shape :", y.shape)  # (569,)
```

#### Demonstration Checklist

- [ ] Run `topic03_features_vs_target.py`
- [ ] Record the accuracy with meaningful features and with shuffled features
- [ ] Explain in one sentence why shuffled features produce near-random accuracy

#### Quick Check

You are predicting whether a loan will default. You have features: income, credit score, loan amount, and "days_since_default." What is wrong with "days_since_default"?

> Answer: It is target leakage. If a loan has already defaulted, days_since_default directly encodes the answer. That information would not exist for future loans you need to predict.

---

### Module 4: Feature Engineering

#### What It Is

Feature engineering is creating new input columns from existing raw data.

Instead of using only the columns you were given, you compute derived values that express relationships more clearly.

#### Why It Matters

Raw features do not always express the relationships a model needs. Feature engineering often produces more improvement than switching to a more complex algorithm.

#### Worked Example

```
Data: Synthetic house dataset (numpy-generated)
Rows: 300
Raw features: area (sq ft), rooms (count), age (years)
Target: price ($)
Type: Regression
```

Raw features: area=1200, rooms=3, age=20

Derived features:
- `area_per_room = area / rooms = 400` — captures spaciousness per room
- `log_age = log(1 + 20) = 3.04` — compresses effect of very old buildings

The model sees the same houses, but now has richer signal. R² improves from ~0.88 to ~0.95.

#### Common Beginner Mistake

**Mistake:** Creating features using test set information during preprocessing (e.g., computing mean of the full dataset before splitting).

**Fix:** Always split first. Compute derived statistics (means, encodings) on the training set only, then apply to test.

#### Code Snippet

```python
import numpy as np

# Given raw matrix: columns are [area, rooms, age]
area = X[:, 0]
rooms = X[:, 1]
age = X[:, 2]

area_per_room = area / rooms        # new feature: space per room
log_age = np.log1p(age)             # new feature: compressed age

X_engineered = np.column_stack([X, area_per_room, log_age])
```

#### Demonstration Checklist

- [ ] Run `topic10_feature_engineering.py`
- [ ] Record baseline R² and engineered R²
- [ ] Explain why `area_per_room` adds information that `area` alone does not carry

#### Quick Check

You have a dataset with `start_time` and `end_time` columns. What useful engineered feature could you create?

> Answer: `duration = end_time - start_time`. The raw timestamps are less directly useful than the duration between them, which may be the real signal for your target.

#### When to Use / When Not to Use

| Use | Not for |
|---|---|
| When raw features are indirect proxies for the signal | When features already directly express the target relationship |
| When domain knowledge suggests a ratio, log, or difference is meaningful | When you have very few examples — risk of noise amplification |

---

### Module 5: Train/Test Split and Data Leakage

#### What It Is

**Train/test split:** Divide your data into two parts. The model learns from the training set. Evaluation happens on the test set — data the model has never seen.

**Data leakage:** When the model accidentally sees information it should not have, making evaluation misleading.

#### Why It Matters

The real goal of ML is to predict well on new, future data — not on data the model already memorized. If you test on training data, you are measuring memory, not learning.

#### Worked Example

```
Data: Diabetes dataset (sklearn built-in)
Rows: 442
Features: 10 clinical measurements
Target: disease progression score (numeric)
Type: Regression
```

| Evaluation Method | R² |
|---|---|
| Correct (train on train, test on test) | ~0.13–0.25 |
| Wrong (train and test on same data) | ~1.0 (perfect, misleading) |

The model memorizes the training data. R² = 1.0 on same data looks perfect but means nothing about future predictions.

#### Common Beginner Mistake

**Mistake:** Fitting a scaler or encoder on the full dataset before splitting, then splitting. This leaks test statistics into the training preprocessing.

**Fix:** Always split first. Fit preprocessing only on training data. Transform test data using the same fitted object.

```python
# Wrong — leakage
scaler.fit(X_all)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Correct — no leakage
scaler.fit(X_train)            # fit only on training data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

#### Demonstration Checklist

- [ ] Run `topic06_training_vs_testing.py`
- [ ] Record train R², test R², and same-data R²
- [ ] Explain why same-data R² ≈ 1.0 but is not a good result

#### Quick Check

A model achieves R² = 0.99 on its evaluation set. Should you celebrate? What is the first thing you check?

> Answer: First check whether the evaluation was done on the training data or truly held-out data. R² = 0.99 on training data means the model memorized it. On a proper test set it is genuinely good.

---

### Module 6: Validation Set

#### What It Is

Three-way split: **train / validation / test**.

- **Train set:** model learns from this
- **Validation set:** use this to compare models and tune hyperparameters
- **Test set:** use this exactly ONCE at the very end for the final honest evaluation

The validation set is like a practice exam. The test set is the real exam. You never use the answers from the real exam while studying.

#### Why It Matters

If you use the test set to pick the best model, you are overfitting to the test set. Your test score becomes optimistic. You need a separate validation set so the test set remains untouched.

#### Worked Example

```
Data: Breast Cancer Wisconsin (sklearn built-in)
Rows: 569
Features: 30 numeric cell measurements
Target: 0 = malignant, 1 = benign
Type: Binary Classification

Split: 60% train (~341), 20% validation (~114), 20% test (~114)
```

Workflow:
1. Try C = 0.001, 0.01, 0.1, 1.0, 10.0 — evaluate each on validation set
2. Best validation accuracy at C = 0.1 → pick this model
3. Evaluate that model on test set → report final accuracy

The test set was never touched until step 3.

#### Common Beginner Mistake

**Mistake:** Using the test set multiple times to compare different models. Each time you check the test set, it leaks information back into your model selection process.

**Fix:** Treat the test set as locked. Compare all variants using only the validation set (or cross-validation). Open the test set once at the very end.

#### Code Snippet

```python
from sklearn.model_selection import train_test_split

# Step 1: lock away the test set
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# Step 2: split remaining into train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42
)
# Result: 60% train, 20% val, 20% test
```

#### Demonstration Checklist

- [ ] Run `topic09_validation_set.py`
- [ ] Record which C has the best validation accuracy
- [ ] Explain why the script does not use test accuracy to select C

#### Quick Check

You compare three models on the test set and pick the best one. Is this a valid procedure?

> Answer: No. You have used the test set to make a selection decision. The test score of the winner is now optimistic. You should use a validation set (or cross-validation) to compare models and reserve the test set for a single final evaluation.

---

### Module 7: Cross-Validation

#### What It Is

Cross-validation is a more robust way to evaluate a model when you do not have enough data for a dedicated validation set.

**k-Fold Cross-Validation:**
1. Split data into k equal folds (e.g., k=5)
2. Train on k-1 folds, evaluate on the remaining 1 fold
3. Repeat k times, rotating which fold is held out
4. Average the k evaluation scores

#### Why It Matters

A single train/validation split can give a noisy estimate — the result depends on which examples happened to land in each set. Cross-validation reduces this noise by averaging across multiple splits.

#### Worked Example

```
Data: Synthetic sinusoidal dataset (numpy-generated)
Rows: 40
Features: 1 numeric (X values)
Target: sin(2πX) + noise
Type: Regression — comparing polynomial complexity
```

| Degree | CV MSE (mean) | CV MSE (std) | Interpretation |
|---|---|---|---|
| 1 | ~0.22 | low | Underfit: line cannot capture the curve |
| 4 | ~0.04 | low | Good fit: captures the pattern |
| 15 | ~0.15+ | high | Overfit: memorizes noise, high variance |

High std means the score changes a lot depending on which fold is used — sign of instability.

#### Common Beginner Mistake

**Mistake:** Including preprocessing (e.g., scaling) outside the cross-validation loop. This leaks test fold statistics into the training process for every fold.

**Fix:** Use a Pipeline so that preprocessing is re-fitted inside each fold.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

model = Pipeline([
    ("scaler", StandardScaler()),    # re-fitted inside each fold
    ("clf", LogisticRegression()),
])
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(scores.mean(), scores.std())
```

#### Demonstration Checklist

- [ ] Run `topic07_overfitting.py` (uses 5-fold cross-validation internally)
- [ ] Compare mean CV MSE for degrees 1, 4, 15
- [ ] Identify which degree has both low mean and low std — that is the best fit

#### Quick Check

A model has cross-validation scores [0.91, 0.92, 0.93, 0.91, 0.92]. Another has [0.95, 0.75, 0.93, 0.60, 0.90]. Which is more reliable and why?

> Answer: The first model. Its scores are consistent across folds (~0.92 average, low variance). The second has high variance (0.60 to 0.95), meaning its performance is unstable and depends heavily on which examples are in each fold.

---

### Module 8: Loss Functions and Optimization

#### What It Is

A loss function measures how wrong the model's predictions are.

The model learns by minimizing the loss: it adjusts its parameters so predictions get closer to the truth.

```
Loss = difference between prediction and truth
```

#### Why It Matters

The loss function defines what the model is trying to optimize. Choosing the wrong loss for your problem produces a model that optimizes the wrong thing.

#### Worked Example

```
Data: Manual examples (4 regression values, 6 classification probabilities)
No file load — values are hard-coded in the script

Regression example:
  y_true = [3.0, -0.5, 2.0, 7.0]
  y_pred = [2.5,  0.0, 2.0, 8.0]
  MSE = mean((y_true - y_pred)^2) = (0.25 + 0.25 + 0.0 + 1.0) / 4 = 0.375... 
  (with the given values: MSE ≈ 0.8125)

Classification example:
  y_true = [1, 0, 1, 1, 0, 0]
  y_prob = [0.9, 0.1, 0.8, 0.7, 0.2, 0.4]
  LogLoss ≈ 0.264
```

#### Common Loss Functions

**Mean Squared Error (MSE) — for regression:**

```
MSE = (1/n) × Σ (y_pred - y_true)²
```

- Squares the error so negative and positive errors do not cancel
- Penalizes large errors more than small ones
- When it misleads: outliers inflate MSE because squaring amplifies large errors

**Log Loss / Cross-Entropy — for classification:**

```
LogLoss = -(1/n) × Σ [y × log(p) + (1-y) × log(1-p)]
```

- Penalizes confident wrong predictions very heavily
- A prediction of 0.99 that is wrong is penalized far more than a prediction of 0.51
- When it misleads: if probabilities are poorly calibrated, LogLoss can be misleading even when accuracy is high

#### Common Beginner Mistake

**Mistake:** Using MSE for a classification problem.

**Fix:** Regression problems → MSE or MAE. Binary classification → Log Loss or binary cross-entropy. Multi-class → categorical cross-entropy.

#### Code Snippet

```python
import numpy as np

y_true = np.array([3.0, -0.5, 2.0, 7.0])
y_pred = np.array([2.5,  0.0, 2.0, 8.0])

mse = np.mean((y_true - y_pred) ** 2)
print("MSE:", mse)   # 0.8125

mae = np.mean(np.abs(y_true - y_pred))
print("MAE:", mae)   # 0.5
```

#### Demonstration Checklist

- [ ] Run `topic04_cost_function.py`
- [ ] Confirm MSE manual ≈ MSE sklearn
- [ ] Confirm LogLoss manual ≈ LogLoss sklearn
- [ ] Explain why the manual and library values match (they compute the same formula)

#### Quick Check

MSE for model A is 4.0. MSE for model B is 1.0. Which is better and why?

> Answer: Model B. MSE measures average squared error. Lower MSE means predictions are closer to the true values on average.

---

### Module 9: Gradient Descent

#### What It Is

Gradient descent is the algorithm that updates model parameters to reduce loss step by step.

```
Data → Predict → Measure Loss → Compute Gradient → Update Parameters → Repeat
```

The gradient tells the model which direction to move to reduce loss. The learning rate controls how big each step is.

#### Why It Matters

Almost all ML models — including neural networks — learn by some form of gradient descent. Understanding it means you understand why models sometimes fail to train (learning rate too large) or train too slowly (learning rate too small).

#### Worked Example

```
Data: Synthetic linear dataset (numpy-generated)
Rows: 200
Features: X values uniformly sampled from [0, 10]
Target: y = 3.0 × X + 5.0 + Gaussian noise (σ=2)
Type: Regression (learning w and b)
```

Update rule for each epoch:
```
w ← w - lr × (dLoss/dw)
b ← b - lr × (dLoss/db)
```

After 3000 epochs with lr=0.001:
- learned w ≈ 3.0 (true value is 3.0)
- learned b ≈ 5.0 (true value is 5.0)
- initial loss ~200–400, final loss ~4–6

#### Common Beginner Mistake

**Mistake:** Setting the learning rate too high. The loss oscillates or increases instead of decreasing.

**Fix:** If loss is increasing or oscillating: reduce the learning rate by 10×. If loss decreases very slowly: try increasing the learning rate.

#### Code Snippet

```python
# One step of gradient descent for linear regression
def update(X, y, w, b, lr=0.001):
    n = len(X)
    err = (w * X + b) - y       # prediction error
    dw = (2/n) * np.sum(err * X)  # gradient w.r.t. w
    db = (2/n) * np.sum(err)      # gradient w.r.t. b
    w -= lr * dw
    b -= lr * db
    return w, b
```

#### Demonstration Checklist

- [ ] Run `topic05_gradient_descent.py`
- [ ] Record initial loss and final loss
- [ ] Open the saved `topic05_loss_curve.png` — confirm loss curves downward and flattens
- [ ] Explain what would happen if lr=0.1 instead of 0.001

#### Quick Check

A model's loss goes from 500 to 490 after 100 epochs. What does this suggest about the learning rate?

> Answer: The model is learning, but very slowly. The learning rate may be too small. Try increasing it (e.g., multiply by 10) and observe whether loss decreases faster without oscillating.

---

### Module 10: Regularization

#### What It Is

Regularization adds a penalty to the loss function for model complexity. It prevents the model from fitting the training data too closely.

```
Total Loss = Prediction Error + λ × Complexity Penalty
```

**L2 regularization** (Ridge): penalizes the sum of squared weights.
**L1 regularization** (Lasso): penalizes the sum of absolute weights — drives some weights to exactly zero.

In scikit-learn's LogisticRegression, `C = 1 / λ`. Higher C = weaker penalty.

#### Why It Matters

Without regularization, a flexible model can memorize training data (overfit). Regularization forces the model to learn more general patterns.

#### Worked Example

```
Data: Breast Cancer Wisconsin (sklearn built-in)
Rows: 569
Features: 30 numeric cell measurements
Target: 0 = malignant, 1 = benign
Type: Binary Classification
```

| C | Train Accuracy | Test Accuracy | Interpretation |
|---|---|---|---|
| 0.001 | ~0.93 | ~0.93 | Strong regularization — underfitting |
| 0.1 | ~0.98 | ~0.97 | Balanced — good generalization |
| 1.0 | ~0.99 | ~0.97 | Still good |
| 1000 | ~1.00 | ~0.97 | Weak regularization — model starts memorizing |

The gap between train and test accuracy grows as regularization weakens (C increases).

#### Common Beginner Mistake

**Mistake:** Turning off regularization entirely (setting C to a very large value) hoping the model "learns more freely."

**Fix:** Start with the default C=1.0. Only increase C if the model is clearly underfitting (both train and test accuracy are low).

#### Code Snippet

```python
from sklearn.linear_model import LogisticRegression

# L2 regularization (default), moderate strength
model = LogisticRegression(C=1.0, penalty="l2")

# Stronger regularization
model_strong = LogisticRegression(C=0.01, penalty="l2")

# L1 regularization (drives some weights to zero)
model_l1 = LogisticRegression(C=1.0, penalty="l1", solver="liblinear")
```

#### Demonstration Checklist

- [ ] Run `topic11_regularization.py`
- [ ] Find the C value with the best test accuracy
- [ ] Identify which C values show signs of overfitting (high train, lower test)
- [ ] Identify which C values show signs of underfitting (both train and test lower)

#### Quick Check

A logistic regression model has train accuracy = 0.99 and test accuracy = 0.84. What kind of regularization change would you try first?

> Answer: Increase regularization (decrease C). The large gap between train and test accuracy suggests overfitting. Stronger regularization will penalize complexity and encourage the model to generalize.

#### When to Use / When Not to Use

| Use | Not for |
|---|---|
| Whenever model overfits (high train, low test) | When model underfits (both errors are already high) |
| When feature space is large relative to data size | Not a substitute for collecting more data |

---

### Module 11: Overfitting, Underfitting, Bias, Variance

#### What It Is

**Overfitting:** model memorizes training data including noise. Works on training, fails on new data.

**Underfitting:** model is too simple to capture the pattern. Performs poorly on both training and test data.

**Bias:** error from being too simple (wrong assumptions).

**Variance:** error from being too sensitive to training data (instability).

#### Why It Matters

Every ML model lives on a spectrum from underfit to overfit. Diagnosing which side you are on tells you exactly what to do next.

#### Worked Example

```
Data: Synthetic sinusoidal dataset (numpy-generated)
Rows: 40
Feature: X values in [0, 1]
Target: sin(2πX) + Gaussian noise (σ=0.15)
Type: Regression — polynomial fitting
```

| Model | CV MSE | Behavior |
|---|---|---|
| Degree 1 (line) | ~0.22 | Underfit — too simple to capture the curve |
| Degree 4 | ~0.04 | Good fit — captures the pattern |
| Degree 15 | ~0.15+ | Overfit — memorizes training noise, high std |

Bias-variance example:

```
Data: make_classification (sklearn synthetic)
Rows: 1500, Features: 20
Target: binary class
```

| Tree Depth | Train Error | Val Error | Interpretation |
|---|---|---|---|
| 1–2 | High | High | High bias — underfitting |
| 4–7 | Low | Low | Balanced — good fit |
| 15–20 | Near 0 | Higher | High variance — overfitting |

#### Common Beginner Mistake

**Mistake:** Seeing poor test performance and immediately trying a more complex model.

**Fix:** Diagnose first. Check train performance. If train is also poor → underfitting (add complexity). If train is high but test is low → overfitting (reduce complexity or regularize).

#### Code Snippet

```python
# Detecting over/underfitting from train vs test performance
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

if train_score < 0.7 and test_score < 0.7:
    print("Underfitting: try more complexity or better features")
elif train_score > 0.95 and (train_score - test_score) > 0.15:
    print("Overfitting: try regularization, simpler model, or more data")
else:
    print("Reasonable fit")
```

#### Demonstration Checklist

- [ ] Run `topic07_overfitting.py` — identify best degree
- [ ] Run `topic08_bias_variance.py` — identify best tree depth
- [ ] For topic08: find the depth where val error is at minimum and both curves are close

#### Quick Check

A model has train accuracy = 0.72 and test accuracy = 0.70. Is this overfitting or underfitting?

> Answer: This is likely underfitting (high bias). Both train and test accuracy are low. The model is too simple to capture the pattern. The gap between train and test is small, which rules out overfitting.

#### When to Use Fixes

| Problem | Fix |
|---|---|
| Underfitting | More features, more complex model, less regularization |
| Overfitting | More data, simpler model, regularization, pruning, early stopping |

---

### Module 12: Metrics — Classification

Each metric below has: what it measures, a worked numeric example, and when it misleads.

#### Accuracy

**What it measures:** Fraction of correct predictions out of all predictions.

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

**Numeric example:**

```
Total: 100 predictions
Correct: 95
Accuracy = 95 / 100 = 0.95
```

**When it misleads:** On imbalanced datasets. If 95% of emails are not spam, a model that always predicts "not spam" gets 0.95 accuracy while detecting zero spam. Accuracy looks great but the model is useless.

---

#### Precision

**What it measures:** Of all predictions of class 1, how many were actually class 1?

```
Precision = TP / (TP + FP)
```

**Numeric example:**

```
Model predicted spam 20 times.
15 were truly spam (TP), 5 were not spam (FP).
Precision = 15 / (15 + 5) = 0.75
```

**When it misleads:** A model that only predicts "spam" for the most obvious cases gets high precision but misses many real spam emails. High precision does not mean good recall.

---

#### Recall (Sensitivity)

**What it measures:** Of all actual class 1 examples, how many did the model find?

```
Recall = TP / (TP + FN)
```

**Numeric example:**

```
There were 30 true spam emails.
Model found 20 of them (TP), missed 10 (FN).
Recall = 20 / (20 + 10) = 0.67
```

**When it misleads:** A model that predicts "spam" for every email gets perfect recall but zero precision. Use recall when missing a positive case is costly (e.g., medical screening).

---

#### F1 Score

**What it measures:** Harmonic mean of precision and recall. Balances both.

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Numeric example:**

```
Precision = 0.75, Recall = 0.67
F1 = 2 × (0.75 × 0.67) / (0.75 + 0.67) = 2 × 0.5025 / 1.42 ≈ 0.708
```

**When it misleads:** If your classes are highly imbalanced and you care much more about one class than the other, F1 treats them symmetrically. Consider weighted F1 instead.

---

#### Confusion Matrix

**What it measures:** A table of TP, TN, FP, FN — shows all four prediction outcomes simultaneously.

```
              Predicted 0    Predicted 1
Actual 0   [  TN          |  FP          ]
Actual 1   [  FN          |  TP          ]
```

**Numeric example:**

```
              Pred: Not Spam   Pred: Spam
Actual: Not    85               5
Actual: Spam   10               0

TN=85, FP=5, FN=10, TP=0
Accuracy=0.85, but zero spam detected!
```

**When it misleads:** Confusion matrix is clear, but always look at all four quadrants. A model with all predictions in one class can have high accuracy while one row or column is entirely zero.

---

### Module 13: Metrics — Regression

#### MSE (Mean Squared Error)

**What it measures:** Average squared difference between predictions and true values.

```
MSE = (1/n) × Σ (y_pred - y_true)²
```

**Numeric example:**

```
y_true = [3.0, -0.5, 2.0, 7.0]
y_pred = [2.5,  0.0, 2.0, 8.0]
errors = [-0.5, 0.5, 0.0, 1.0]
squared = [0.25, 0.25, 0.0, 1.0]
MSE = (0.25 + 0.25 + 0.0 + 1.0) / 4 = 0.375
```

**When it misleads:** Outliers inflate MSE disproportionately because squaring amplifies large errors. One very wrong prediction can dominate the metric.

---

#### MAE (Mean Absolute Error)

**What it measures:** Average absolute difference between predictions and true values.

```
MAE = (1/n) × Σ |y_pred - y_true|
```

**Numeric example:**

```
Using same values as above:
|errors| = [0.5, 0.5, 0.0, 1.0]
MAE = (0.5 + 0.5 + 0.0 + 1.0) / 4 = 0.5
```

**When it misleads:** MAE treats all errors equally, so a few very bad predictions are not highlighted. Use MSE when large errors are particularly costly.

---

#### R² (Coefficient of Determination)

**What it measures:** Fraction of variance in the target that the model explains. Range: −∞ to 1.0.

```
R² = 1 - (Σ(y_true - y_pred)²) / (Σ(y_true - mean(y_true))²)
```

**Numeric example:**

```
R² = 1.0  → model explains all variance (perfect, or overfitting on train)
R² = 0.75 → model explains 75% of variance
R² = 0.0  → model does no better than predicting the mean
R² < 0    → model is worse than predicting the mean
```

**When it misleads:** R² = 1.0 on training data usually means overfitting, not a genuinely perfect model. Always check R² on test data. Also, high R² does not mean the model is correct for causal reasoning.

---

### Module 14: PyTorch Tensors, Autograd, and CUDA

#### What It Is

- **Tensor:** PyTorch's core data structure (similar to NumPy arrays, but with autograd and GPU support).
- **Autograd:** automatic differentiation system that computes gradients for trainable parameters.
- **CUDA device placement:** moving tensors and models from CPU to GPU for accelerated computation.

#### Why It Matters

Modern ML training commonly uses PyTorch and GPU acceleration. Even in Stage 1, you should understand:

- how gradient computation can be automatic
- how device mismatch errors happen
- when GPU helps and when it does not

#### Worked Example

```
Data: synthetic tensor regression data (generated with torch.randn)
Rows: 20,000
Features: x (shape [N, 1], float32)
Target: y = 2.5*x + 1.0 + noise
Type: Regression
```

Script: `topic12_pytorch_cuda.py`

The script does four things:

1. Prints torch version and CUDA availability.
2. Runs an autograd derivative demo.
3. Trains a linear regression model with autograd (`w`, `b` parameters).
4. Compares CPU and GPU matrix multiplication timing (if CUDA exists).

#### Common Beginner Mistake

**Mistake:** mixing devices (for example, model on GPU but input tensor on CPU), causing runtime errors.

**Fix:** place all participating tensors and parameters on the same device (`cpu` or `cuda`) and verify with `.device`.

#### Code Snippet

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.randn(8, 1, device=device, requires_grad=True)
y = x.pow(2).sum()
y.backward()
print("device:", x.device, "grad shape:", x.grad.shape)
```

#### Demonstration Checklist

- [ ] Run `topic12_pytorch_cuda.py`
- [ ] Confirm `torch.cuda.is_available()` output
- [ ] Explain the autograd gradient output in plain language
- [ ] Explain why learned `w` is near 2.5 and `b` near 1.0
- [ ] If CUDA is available, compare CPU vs GPU timing and interpret result

#### Quick Check

If `torch.cuda.is_available()` is `True`, but your code still runs on CPU, what is the most likely issue?

> Answer: Tensors and/or model were not moved to CUDA (for example, missing `.to("cuda")`), so computation remains on CPU.

#### When to Use / When Not to Use

| | Use | Do not use |
|---|---|---|
| PyTorch + CUDA | training medium/large tensor workloads; autograd-based optimization | very small workloads where transfer/launch overhead dominates |
| CPU-only | lightweight demos and environments without CUDA | large training loops that benefit from GPU acceleration |

---

## 7. Difficulty Points

### 1. Thinking ML is "smart"

> It is NOT intelligence. It is math + optimization.

**Why beginners make this mistake:** Because model outputs can look impressive.

**Fix strategy:** Always ask:
- What data did it learn from?
- What pattern is it using?
- What are its limits?

### 2. Confusing correlation vs causation

> A model does NOT understand cause.

**Example:** Ice cream sales increase → drowning incidents increase. Both are caused by hot weather. The model may find them correlated, but not causal.

**Fix strategy:** Use domain knowledge. Do not assume the model discovered true cause.

### 3. Misunderstanding evaluation

> High accuracy ≠ good model.

**Example:** If 95% of emails are not spam, a model that always predicts "not spam" gets 95% accuracy — but it is useless.

**Fix strategy:** Use precision, recall, F1, confusion matrix. Choose the metric that matches the business problem.

### 4. Ignoring features

> Features determine everything.

**Real problem:** A bad model with good features can outperform a fancy model with bad features.

**Fix strategy:** Spend time on data quality, feature design, and preprocessing before switching to a more complex model.

### 5. Data leakage

> The model accidentally sees future or hidden information.

**Example:** Predict house prices using a feature computed after the sale.

**Why it is dangerous:** The model appears excellent during evaluation but fails completely in deployment.

**Fix strategy:** Split data first. Fit preprocessing only on training data. Avoid features that encode or derive from the target.

### 6. Validation set confusion

> Validation set ≠ test set.

**Why beginners confuse them:** Both are held-out data not used for training.

**Fix strategy:** Validation set is used for model selection and tuning. Test set is used exactly once for the final honest evaluation.

### 7. Copying code without understanding shape and columns

**Fix strategy:** Always inspect before running:

```python
print(X.shape)
print(df.info())
print(df.columns.tolist())
```

---

## 8. ML Workflow (Real World)

```
1. Define problem
2. Collect data
3. Clean data
4. Select and engineer features
5. Split data (train / val / test)
6. Train model
7. Evaluate on validation
8. Tune and compare
9. Final evaluation on test
10. Improve
```

### Beginner Explanation of Each Step

1. **Define problem** — Be specific.
   - Bad: "Predict the market"
   - Good: "Predict whether stock price will go up tomorrow based on last 5 days of indicators"

2. **Collect data** — Gather examples related to the problem.

3. **Clean data** — Fix missing values, errors, duplicates, bad formatting.

4. **Select and engineer features** — Choose what information the model should use. Create derived features that express relationships more clearly.

5. **Split data** — Train / validation / test. Lock the test set.

6. **Train model** — Let the algorithm learn patterns from training data.

7. **Evaluate on validation** — Check performance on held-out validation data.

8. **Tune and compare** — Adjust hyperparameters. Compare models on validation score.

9. **Final evaluation on test** — Report the honest score. Do this once.

10. **Improve** — Refine data, features, model choice based on findings.

---

## 9. Evaluation and Debugging Playbook

### Decision Flow: Diagnosing Model Problems

```
Step 1: Measure train error and test error.

train error HIGH  +  test error HIGH
  → Underfitting (high bias)
  → Actions: add more features, try more complex model, reduce regularization

train error LOW   +  test error HIGH
  → Overfitting (high variance)
  → Actions: add more data, simplify model, increase regularization,
             use pruning, apply cross-validation

test error UNEXPECTEDLY LOW (too good to be true)
  → Leakage suspected
  → Check: feature timestamps, preprocessing order, target encoding,
           whether test data was accidentally included in training
```

### Beginner Debugging Checklist

If performance is poor, check:

- [ ] Is the target correct (right column, right encoding)?
- [ ] Are there missing values that were not handled?
- [ ] Are features meaningful (not shuffled, not leaking the answer)?
- [ ] Is leakage present (preprocessing before split, future data)?
- [ ] Is the dataset too small for the model complexity?
- [ ] Is the model overfitting (check train vs test gap)?
- [ ] Is the evaluation metric appropriate for the problem type?
- [ ] Was the validation set used correctly (not the test set for tuning)?

### Hard Quality Gates Before Stage 1 Completion

All must pass before moving to Stage 2:

- [ ] Project runs reproducibly from a clean environment with only documented commands
- [ ] No leakage indicators (preprocessing fitted on training only; no future features)
- [ ] Metrics and narrative are consistent (a claim of "good performance" is backed by numbers)
- [ ] At least 2 model baselines compared on the same holdout set
- [ ] Self-test score ≥ 22 out of 30

---

## 10. Stage 1 Project Runbook

### Project: Mini Predictor

**Goal:** Build a complete, reproducible ML pipeline on a real dataset.

### Project Layout

```
project/
  README.md
  requirements.txt
  src/
    train.py
    evaluate.py
  notebooks/
  results/
    metrics.json
    figures/
```

### Setup Commands

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/train.py
python src/evaluate.py
```

**Unix/macOS:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/train.py
python src/evaluate.py
```

### Step-by-Step Runbook

**Step 1 — Get Data**

```
Data: California Housing (sklearn built-in, fetch_california_housing)
Rows: 20,640
Features: MedInc (median income), HouseAge, AveRooms, AveBedrms,
          Population, AveOccup, Latitude, Longitude
Target: MedHouseVal (median house value in $100k units)
Type: Regression
```

```python
from sklearn.datasets import fetch_california_housing
import pandas as pd

data = fetch_california_housing(as_frame=True)
df = data.frame
```

**Step 2 — Inspect**

```python
print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())
```

*Why this step matters: Understand what columns exist, their types, scale, and whether any values are missing.*

**Step 3 — Define X and y**

```python
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]
```

*Why this step matters: Separate inputs from output before any splitting or preprocessing.*

**Step 4 — Split**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

*Why this step matters: Lock away the test set before any preprocessing.*

**Step 5 — Train (Baseline)**

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

**Step 6 — Evaluate**

```python
from sklearn.metrics import mean_squared_error, r2_score

train_preds = model.predict(X_train)
test_preds = model.predict(X_test)

print("train MSE:", round(mean_squared_error(y_train, train_preds), 4))
print("test  MSE:", round(mean_squared_error(y_test, test_preds), 4))
print("train R2 :", round(r2_score(y_train, train_preds), 4))
print("test  R2 :", round(r2_score(y_test, test_preds), 4))
```

Expected test R² range for linear regression: ~0.60–0.65

**Step 7 — Compare a Second Model**

```python
from sklearn.tree import DecisionTreeRegressor

tree = DecisionTreeRegressor(max_depth=5, random_state=42)
tree.fit(X_train, y_train)
tree_test_r2 = r2_score(y_test, tree.predict(X_test))
print("Decision Tree test R2:", round(tree_test_r2, 4))
```

Expected test R² range for depth-5 tree: ~0.65–0.72

### Required Outputs

- `results/metrics.json` — train and test metrics for each model
- `results/figures/` — at least one visualization (predicted vs actual, or residual plot)
- Short written error analysis: where does the model make the largest errors?
- Feature summary: which features are most correlated with the target?
- Model comparison table: model name, train R², test R²

### Deliverables

- Code (train.py, evaluate.py)
- Dataset documentation (data declaration block)
- Metrics (metrics.json)
- README with setup instructions

### Experiment Tasks

**Experiment 1 — Train and test on the same data**

- Purpose: See how evaluation becomes misleading.
- Expected: R² ≈ 1.0 on training data (memorization).
- Lesson: Testing on training data is not evaluation.

**Experiment 2 — Remove some features**

- Purpose: Observe how feature removal affects model quality.
- Try removing: Latitude and Longitude.
- Lesson: Some features carry more signal than others.

**Experiment 3 — Add an engineered feature**

- Create `rooms_per_household = AveRooms / AveOccup`
- Compare test R² before and after.
- Lesson: Derived features can improve performance without changing the model.

**Experiment 4 — Try Random Forest**

```python
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
```

Expected test R²: ~0.78–0.83

Lesson: Ensemble models often outperform single trees on tabular data.

### Common Mistakes

1. **Target leakage** — Using a feature that encodes or derives from the answer. *Fix: Remove any feature that contains information unavailable at prediction time.*

2. **Testing on training data** — Gives fake confidence. *Fix: Always use a separate test set held out before training.*

3. **Ignoring missing values** — Can silently break models. *Fix: Inspect `df.isna().sum()` before training.*

4. **Using meaningless features** — Model cannot learn from noise. *Fix: Think carefully about which features logically relate to the target.*

5. **Believing one metric tells the whole story** — R² alone may hide large individual errors. *Fix: Use MSE and R² together, inspect the residual distribution.*

---

## 11. Self-Test + Scoring Rubric

### Scoring

| Score | Action |
|---|---|
| 27–30 | Proceed to Stage 2 |
| 22–26 | Review flagged concepts, re-run the corresponding scripts, then re-test |
| < 22 | Restart from Day 1 of the Two-Week Roadmap |

### Questions

1. What is Machine Learning?
2. What is a model?
3. What is supervised learning?
4. What is unsupervised learning?
5. What is the difference between regression and classification?
6. What are features?
7. What is the target?
8. Why do we split data into training and testing sets?
9. What is the difference between a validation set and a test set?
10. What is generalization?
11. What is overfitting?
12. What is underfitting?
13. What is bias?
14. What is variance?
15. What is a loss function?
16. Why does a model need a loss function?
17. What is MSE? When does it mislead?
18. What is R²? What does R² = 0.0 mean?
19. What is precision? What is recall? How do they differ?
20. What is F1 score?
21. What is the confusion matrix?
22. What is gradient descent?
23. What is the difference between batch gradient descent and SGD?
24. What is data leakage? Give one example.
25. What is feature engineering? Give one example of a derived feature.
26. What is regularization? What does increasing regularization do?
27. What is cross-validation? Why is it more reliable than a single split?
28. Why can high accuracy be misleading?
29. What pattern in train vs test error indicates overfitting?
30. What are the three things you check first when a model performs poorly?

### Answers

1. Machine Learning is a way for computers to learn patterns from data so they can make predictions or decisions on new data without being explicitly programmed with rules.

2. A model is a mathematical function or system that maps input features to output predictions by learning patterns from training data.

3. Supervised learning means training a model with labeled examples — both input data (X) and correct answers (y) are provided.

4. Unsupervised learning means training a model on unlabeled data so it can discover hidden patterns, groups, or structure without correct answers.

5. Regression predicts a continuous number (e.g., house price). Classification predicts a category or label (e.g., spam/not spam).

6. Features are the input variables used by the model to make predictions. They describe each example in the dataset.

7. The target is the output value the model is trying to predict.

8. To check whether the model can perform well on new, unseen data — not just memorize the examples it was trained on.

9. The validation set is used during training to compare models and tune hyperparameters. The test set is locked away and used only once at the very end for the final honest evaluation.

10. Generalization is the ability of a model to perform well on new data it has never seen before.

11. Overfitting happens when a model memorizes training data too closely, including noise, and performs poorly on new data.

12. Underfitting happens when a model is too simple and fails to capture important patterns in the data. Both train and test performance are poor.

13. Bias is error from a model being too simple or making overly strong assumptions. It leads to underfitting.

14. Variance is error from a model being too sensitive to the specific training data. It leads to overfitting.

15. A loss function measures how wrong the model's predictions are. It gives the model a signal to improve.

16. Because the loss function tells the model how bad its predictions are and provides a gradient to guide parameter updates.

17. MSE is the average squared difference between predictions and true values. It misleads when outliers are present because squaring amplifies large errors, making one bad prediction dominate the metric.

18. R² measures what fraction of variance in the target the model explains. R² = 0.0 means the model is no better than always predicting the mean value of y.

19. Precision = of all predicted positives, how many are truly positive. Recall = of all actual positives, how many did the model find. Precision matters when false positives are costly. Recall matters when missing a positive is costly.

20. F1 score is the harmonic mean of precision and recall. It balances both metrics into a single number. Useful when both false positives and false negatives matter.

21. The confusion matrix is a table showing TP, TN, FP, FN — the four possible prediction outcomes for a binary classifier. It reveals what kinds of errors the model makes.

22. Gradient descent is an optimization algorithm that repeatedly updates model parameters in the direction that reduces loss, using the gradient of the loss to determine which way to move.

23. Batch gradient descent uses the entire training set to compute one update. SGD uses one sample or a small mini-batch, which is faster but noisier.

24. Data leakage happens when the model accidentally uses information that would not be available in real-world prediction. Example: fitting a scaler on the full dataset before splitting, then using test data statistics in training preprocessing.

25. Feature engineering is creating new input columns from existing raw data. Example: from start_time and end_time, derive duration = end_time - start_time.

26. Regularization adds a penalty to the loss for large model weights. Increasing regularization forces the model to be simpler and reduces overfitting — but if too strong, it causes underfitting.

27. Cross-validation splits data into k folds and evaluates the model k times, each time using a different fold as the holdout. It is more reliable because it averages results across multiple splits rather than depending on one particular split.

28. Because on imbalanced data, a model that always predicts the majority class achieves high accuracy while being completely useless for the minority class.

29. Overfitting pattern: training error is very low and test error is significantly higher. The gap between train and test is large.

30. Check: (1) data quality and missing values, (2) features — are they meaningful? is there leakage? (3) the train vs test error gap — is it underfitting or overfitting? Do NOT change the model until you have checked these three.

---

## 12. Stage Completion Checklist

### What You Must Be Able To Do After Stage 1

- [ ] Explain ML in plain English
- [ ] Explain the difference between supervised and unsupervised learning
- [ ] Explain regression vs classification
- [ ] Explain features and target, and why feature quality matters
- [ ] Explain what feature engineering is and give one example
- [ ] Explain training vs testing and why they must be separate
- [ ] Explain the difference between a validation set and a test set
- [ ] Explain cross-validation and why it is more reliable than a single split
- [ ] Explain overfitting vs generalization
- [ ] Explain underfitting and how to diagnose it
- [ ] Explain what a loss function is and name one for regression and one for classification
- [ ] Explain how gradient descent improves a model
- [ ] Explain what regularization is and what the C parameter does in logistic regression
- [ ] Explain precision, recall, and F1 — and when each one matters
- [ ] Interpret a confusion matrix
- [ ] Interpret MSE, MAE, and R² on regression output
- [ ] Build a simple ML pipeline and evaluate it on a held-out test set
- [ ] Identify data leakage in a pipeline
- [ ] Pass the self-test with a score of 22 or higher

---

## 13. What Comes After Stage 1

Stage 2 covers the Python tools you need for real AI engineering work: NumPy for numerical computation, Pandas for structured data handling, Matplotlib for visualization, and Scikit-learn as a unified ML toolkit. Stage 1 is required first because every Stage 2 task assumes you already know what you are building and why.

The Stage 1 concepts that Stage 2 directly builds on:

- **Train/test split** → used in every scikit-learn pipeline via `train_test_split`
- **Features and target (X and y)** → directly mapped to Pandas DataFrames and NumPy arrays
- **Loss and evaluation metrics** → computed and interpreted using scikit-learn model evaluation tools
- **Overfitting** → reinforced through scikit-learn's preprocessing pitfalls and pipeline discipline
- **Feature engineering** → extended in Stage 2 using Pandas column operations

Before moving to Stage 2, you must be able to explain supervised learning, build a simple pipeline end-to-end, and evaluate a model correctly on held-out data.

