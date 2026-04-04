# Stage 1 Handbook Improvement Plan (v2)

Target file: `red-book/AI-study-handbook-1.md`  
Plan owner: You + Codex  
Version date: 2026-04-03

## 0) User Requirements (Locked)

These requirements come directly from user instructions and must remain in scope:

- Improve `AI-study-handbook-1.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Keep and expand high-quality learning resources in this plan:
  - tutorials
  - books
  - articles
  - official documentation
  - popular GitHub resources
- Include all listed resources in `plan-1.md` with clear prioritization and estimated time.
- Add examples for each learning topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare the data resource and data structure used in examples.
- Add detailed explanation and demonstration for concepts.
- Add more instructions for learning targets.
- Add detailed tutorials for key topics.
- Examples can be sourced/adapted from websites, tutorials, books, docs, and articles.
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.

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

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary

### What is already strong

- Coverage is broad and beginner-friendly.
- Explanations are practical and concrete.
- Includes project, checklist, and self-test.

### What still needs improvement

- The handbook reads like notes, not a guided study system.
- There is no strict daily execution flow (what to do first, next, last).
- Some concepts overlap across sections and increase cognitive load.
- Operational details are incomplete (setup, run order, expected outputs).
- Self-test has no scoring policy or remediation path.
- Resource section is too short and not prioritized.
- One edited line in the prior plan is unclear:
  - `how diagramsand images` should be rewritten as `how to use diagrams and images`.
- The plan references "Section 14 GPU spec" but does not define that section yet.
- No explicit quality assurance loop is defined for script execution after handbook edits.
- No terminology glossary standard is defined, which can cause wording drift.

---

## 2) Target Outcomes (Measurable)

After rewrite, Stage 1 must satisfy all checks:

- A beginner can follow a day-by-day sequence without external planning.
- Each key concept includes:
  - plain-language definition
  - small numeric example
  - one runnable snippet (exception: ML mental model — use a demonstration walkthrough instead)
  - one quick check question
  - one demonstration task with output interpretation
  - one common beginner mistake + fix (hard requirement — no concept module ships without this)
- Project can run from clean environment with only documented commands.
- Evaluation section includes leakage checks and metric interpretation rules.
  - Each metric must have its own: plain-language interpretation, worked numeric example, and a note on when it misleads.
  - Required metrics for Stage 1: precision, recall, F1, accuracy, MSE, MAE, R², confusion matrix.
- Self-test includes score bands and clear next actions.
  - 27–30 correct → proceed to Stage 2
  - 22–26 → review flagged concepts, re-run corresponding scripts
  - < 22 → restart from Day 1

---

## 3) Resource Upgrade (Complete Catalog)

Use this as a layered resource stack:

- Layer 1: core learning path (must complete)
- Layer 2: official docs (must use during implementation)
- Layer 3: books and classic articles (depth)
- Layer 4: popular GitHub resources (practice and reference)

### A. Core Learning Path (Must Complete)

- DeepLearning.AI + Stanford: Machine Learning Specialization (Coursera)
  - https://www.coursera.org/specializations/machine-learning-introduction
- Google Machine Learning Crash Course
  - https://developers.google.com/machine-learning/crash-course
- scikit-learn User Guide
  - https://scikit-learn.org/stable/user_guide.html
- scikit-learn Common Pitfalls
  - https://scikit-learn.org/stable/common_pitfalls.html
- MIT OCW 6.036 Introduction to Machine Learning
  - https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/
- fast.ai Practical Deep Learning for Coders
  - https://course.fast.ai/
- TensorFlow Tutorials
  - https://www.tensorflow.org/tutorials
- Stanford CS229 Handouts and Notes
  - https://cs229.stanford.edu/materials.html-full

### B. Official Documentation (Implementation-First)

- NumPy quickstart
  - https://numpy.org/doc/stable/user/quickstart.html
- pandas getting started
  - https://pandas.pydata.org/docs/getting_started/index.html
- Matplotlib tutorials
  - https://matplotlib.org/stable/tutorials/index.html
- PyTorch tutorials (beginner path: tensors, autograd, training loop)
  - https://pytorch.org/tutorials/
- PyTorch CUDA semantics (required for GPU usage)
  - https://pytorch.org/docs/stable/notes/cuda.html
- PyTorch install selector (choose CUDA version correctly)
  - https://pytorch.org/get-started/locally/
- Jupyter try-online environment
  - https://jupyter.org/try
- Kaggle micro-course: Intro to Machine Learning
  - https://www.kaggle.com/learn/intro-to-machine-learning

### C. Books (Priority Order)

Free/core:

- Dive into Deep Learning (interactive, free)
  - https://d2l.ai/
- An Introduction to Statistical Learning (ISLP)
  - https://www.statlearning.com/

Applied/paid:

- Hands-On Machine Learning (latest edition page)
  - https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/

Advanced optional:

- Probabilistic Machine Learning
  - https://mitpress.mit.edu/9780262048439/probabilistic-machine-learning/

### D. Articles and Practical Reading

- Rules of Machine Learning (engineering mindset)
  - https://developers.google.com/machine-learning/guides/rules-of-ml/
- A Few Useful Things to Know About Machine Learning
  - https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf
- The Unreasonable Effectiveness of Data
  - https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35179.pdf

### E. Popular GitHub Resources (Hands-On and Community)

- Microsoft ML for Beginners
  - https://github.com/microsoft/ML-For-Beginners
- Aurelien Geron notebook repo for Hands-On ML
  - https://github.com/ageron/handson-ml3
- Awesome Machine Learning curated list
  - https://github.com/josephmisiti/awesome-machine-learning
- Homemade Machine Learning (algorithm intuition notebooks)
  - https://github.com/trekhleb/homemade-machine-learning
- Machine Learning with PyTorch and Scikit-Learn code repo
  - https://github.com/rasbt/machine-learning-book
- fastai book notebooks
  - https://github.com/fastai/fastbook
- scikit-learn source and examples
  - https://github.com/scikit-learn/scikit-learn

### F. Resource-to-Stage Mapping (How to Use in Stage 1)

- Week 1 concepts:
  - ML Specialization, Google MLCC, ISLP, scikit-learn User Guide
- Week 1 coding fundamentals:
  - NumPy, pandas, Matplotlib, Jupyter, Kaggle Intro ML
- Week 2 model comparison and debugging:
  - scikit-learn Common Pitfalls, CS229 notes, Rules of ML
- Week 2 GPU and PyTorch intro:
  - PyTorch tutorials (beginner path), PyTorch CUDA semantics doc
- Project and notebooks:
  - handson-ml3, ML-For-Beginners, homemade-machine-learning, rasbt repo
- Optional deepening:
  - D2L, fast.ai, TensorFlow tutorials, Probabilistic ML

### G. Priority and Time Budget (Must / Should / Optional)

Time labels are estimates for Stage 1 use, not full-course completion.

Must (complete in Stage 1):

- DeepLearning.AI + Stanford: Machine Learning Specialization (selected beginner modules) - 10-12h
  - https://www.coursera.org/specializations/machine-learning-introduction
- Google Machine Learning Crash Course (core sections) - 5-6h
  - https://developers.google.com/machine-learning/crash-course
- scikit-learn User Guide (supervised/unsupervised/model evaluation sections) - 4-5h
  - https://scikit-learn.org/stable/user_guide.html
- scikit-learn Common Pitfalls - 1.5-2h
  - https://scikit-learn.org/stable/common_pitfalls.html
- NumPy quickstart - 1h
  - https://numpy.org/doc/stable/user/quickstart.html
- pandas getting started - 1.5h
  - https://pandas.pydata.org/docs/getting_started/index.html
- Matplotlib tutorials (basic plotting only) - 1-1.5h
  - https://matplotlib.org/stable/tutorials/index.html
- Jupyter try-online environment - 0.5h
  - https://jupyter.org/try
- Kaggle Intro to Machine Learning - 3-4h
  - https://www.kaggle.com/learn/intro-to-machine-learning
- ISLP (selected intro and supervised chapters) - 4-6h
  - https://www.statlearning.com/

Should (high value, if schedule allows):

- MIT OCW 6.036 (selected lectures) - 4-6h
  - https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/
- Stanford CS229 handouts and notes (selected reading) - 3-4h
  - https://cs229.stanford.edu/materials.html-full
- Dive into Deep Learning (selected notebook chapters) - 3-5h
  - https://d2l.ai/
- Rules of Machine Learning - 1-2h
  - https://developers.google.com/machine-learning/guides/rules-of-ml/
- A Few Useful Things to Know About Machine Learning - 1h
  - https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf
- The Unreasonable Effectiveness of Data - 0.5-1h
  - https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35179.pdf
- Microsoft ML for Beginners (selected lessons) - 3-5h
  - https://github.com/microsoft/ML-For-Beginners
- handson-ml3 notebooks (selected chapters aligned to project) - 3-4h
  - https://github.com/ageron/handson-ml3
- homemade-machine-learning (algorithm intuition notebooks) - 1-2h
  - https://github.com/trekhleb/homemade-machine-learning
- rasbt machine-learning-book repository (selected code) - 2-3h
  - https://github.com/rasbt/machine-learning-book

Optional (deeper or broader than Stage 1 needs):

- fast.ai Practical Deep Learning for Coders - 4-8h (selected) / 20h+ (full part)
  - https://course.fast.ai/
- TensorFlow tutorials beyond basics - 2-6h
  - https://www.tensorflow.org/tutorials
- PyTorch tutorials (beginner path) - 2-5h
  - https://pytorch.org/tutorials/
- fastai book notebooks - 2-4h
  - https://github.com/fastai/fastbook
- Awesome Machine Learning curated list (browse and pick) - 1-2h
  - https://github.com/josephmisiti/awesome-machine-learning
- scikit-learn source and examples (reference use) - 1-2h
  - https://github.com/scikit-learn/scikit-learn
- Hands-On Machine Learning book - 8-15h (selected) / 30h+ (broad pass)
  - https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/
- Probabilistic Machine Learning - 6-10h (selected) / 40h+ (deep study)
  - https://mitpress.mit.edu/9780262048439/probabilistic-machine-learning/

Recommended Stage 1 total study budget:

- Minimum track: 32-40h
- Strong track: 45-60h

---

## 4) New Handbook Structure (Required)

1. How to Use This Handbook
2. Prerequisites and Environment Setup (CPU + GPU tracks)
3. Two-Week Guided Roadmap
4. Concept Modules (standard template)
5. Evaluation and Debugging Playbook
6. Stage 1 Project Runbook
7. Self-Test + Scoring Rubric
8. Stage Completion Checklist
9. What Comes After Stage 1 (Stage Transition)

### Section Content Specifications

**Section 1 — How to Use This Handbook**

Must include:
- recommended reading order (linear vs. topic-first)
- how to use the scripts alongside the text (read concept → run script → interpret output → answer self-check)
- what to do if stuck (which resource to consult first)
- who this stage is designed for (assumed knowledge: basic Python, loops, functions)

**Section 2 — Prerequisites and Environment Setup**

Must include:
- required Python version (3.10+)
- supported OS (Windows and Unix — show commands for both)
- assumed prior knowledge: basic Python syntax, loops, functions, lists, dicts
- what to do if prerequisites are not met (link to a Python beginner resource)
- environment setup commands end-to-end (venv creation, activation, pip install)
- GPU track setup — separate subsection (see Section 14 for full GPU spec)
  - CUDA version check command
  - PyTorch GPU install command
  - GPU verification snippet

**Section 9 — What Comes After Stage 1**

Must include:
- a 2–3 sentence summary of what Stage 2 covers and why Stage 1 is required first
- the foundational concepts from Stage 1 that Stage 2 directly builds on
- one sentence confirming what a learner should be able to do before moving on

---

## 5) Concept Module Template (Apply to Every Core Topic)

For each module:

- What it is (plain English)
- Why it matters
- Tiny worked example
- Common beginner mistake
- One code snippet
- Demonstration checklist (what to run and what to explain)
- One quick check
- When to use / when not to use (for algorithms)

Core modules:

- ML mental model (no code snippet required — use demonstration walkthrough instead)
- supervised vs unsupervised learning
- features and target
- feature engineering (what it is, why it matters, one worked example, when it happens in the workflow)
- train/test split and data leakage
- validation set (treat as a distinct module from test set — beginners confuse the two)
- cross-validation
- loss functions and optimization
- regularization (connects loss function + overfitting + model selection — deserves its own module)
- overfitting, underfitting, bias, variance
- metrics (classification + regression)
  - each metric gets its own entry: definition, numeric example, when it misleads
- PyTorch tensors and autograd (GPU track)
  - what a tensor is vs a NumPy array
  - how autograd computes gradients automatically
  - how to move tensors to GPU with `.to("cuda")`
  - reimplement gradient descent from topic05 using PyTorch autograd on GPU
  - CPU vs GPU timing comparison

Hard requirement: every module must have all template fields filled. No module ships with a missing common beginner mistake, missing quick check, or missing worked example.

GPU track modules are required if the learner has a CUDA-capable GPU. They are optional otherwise.

---

## 6) Two-Week Operable Roadmap

### Week 1 (Foundations + First Pipeline)

- Day 1: ML mental model, supervised vs unsupervised
- Day 2: features, target, preprocessing basics
- Day 3: train/test split, validation, leakage
- Day 4: loss, gradient descent, learning dynamics
- Day 5: overfitting, underfitting, bias/variance
- Day 6: build baseline pipeline (linear regression)
- Day 7: evaluate baseline and write findings

### Week 2 (Strengthening + Comparison + Reporting)

- Day 8: model comparison (tree + random forest)
- Day 9: metrics interpretation and error analysis
- Day 10: debugging drills using decision flow
- Day 11: improve features and retrain
- Day 12: create final results table + charts
- Day 13: self-test and gap repair
- Day 14: final report and readiness check

---

## 7) Notebook and Visuals Plan

Add a notebook-driven learning track:

- Notebook 1: full baseline pipeline
- Notebook 2: overfitting demo (train vs test behavior)
- Notebook 3: gradient descent intuition with plot
- Notebook 4: feature ablation and model comparison

Visual requirements:

- one flowchart for ML workflow
- one decision tree for debugging
- one plot showing underfit vs good fit vs overfit
- one confusion matrix example

Language fix for prior edit:

- Replace `how diagramsand images` with `how to use diagrams and images`.

---

## 8) Stage 1 Project Spec (Reproducible)

Required project layout:

- `project/README.md`
- `project/requirements.txt`        (CPU-only dependencies)
- `project/requirements-gpu.txt`    (PyTorch + CUDA, installed separately)
- `project/src/train.py`
- `project/src/evaluate.py`
- `project/notebooks/`
- `project/results/metrics.json`
- `project/results/figures/`

Minimum run commands to document (show both OS variants):

Windows:
- `python -m venv .venv`
- `.venv\Scripts\activate`
- `pip install -r requirements.txt`
- `python src/train.py`
- `python src/evaluate.py`

Unix/macOS:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `python src/train.py`
- `python src/evaluate.py`

Required outputs:

- train metric(s)
- test metric(s)
- short error analysis
- feature summary
- model comparison table

Expected output documentation (required for every script):

- Each script in `red-book/src/stage-1/` must have documented expected output in the handbook.
- Format: state what the output should contain, a representative numeric range, and what it means.
- Example format:
  - `topic01_supervised_learning.py` → expected: accuracy > 0.85, confusion matrix 2×2, precision/recall/F1 printed
  - `topic05_gradient_descent.py` → expected: loss decreases from ~X to ~Y over N iterations, final w and b printed
- If a script produces a plot, state what the plot should look like (e.g., "loss should curve downward and flatten").

---

## 9) Debugging and Quality Gates

Add a decision flow:

- low train + low test -> underfitting actions (simplify model, check features, gather more data)
- high train + low test -> overfitting actions (regularize, reduce complexity, add data, prune)
- unexpectedly high test -> leakage checks (check feature timestamps, preprocessing order, target encoding)

Add hard quality gates before Stage 1 completion:

- reproducible run from clean env
- no leakage indicators
- metrics match narrative
- at least 2 model baselines compared
- self-test score >= 22 out of 30 (see scoring rubric in section 2)

---

## 10) Implementation Plan (Execution Order)

1. Add front matter: usage guide, prerequisites (CPU + GPU tracks), roadmap, stage transition.
2. Refactor concept sections into module template.
3. Add missing concept modules: validation set, feature engineering, regularization.
4. Add PyTorch + autograd + GPU concept module (Section 14 spec).
5. Merge evaluation/generalization/overfitting into one coherent block.
6. Add per-metric interpretation entries (precision, recall, F1, MSE, MAE, R², confusion matrix).
7. Add setup/runbook with OS-specific commands (Windows + Unix) and GPU install track.
8. Add notebook and visual requirements.
9. Upgrade project section to reproducible spec with requirements-gpu.txt and expected outputs per script.
10. Add self-test scoring + remediation actions (lock thresholds: 27–30 / 22–26 / <22).
11. Add data declaration block to every example (format defined in section 12).
12. Write topic12_pytorch_cuda.py (gradient descent on GPU with autograd, CPU vs GPU timing).
13. Add glossary + notation standard and apply consistently across all concept sections.
14. Add script smoke-test command set and capture outputs in a validation log.
15. Add dependency pinning and reproducibility policy (requirements, random seeds, OS notes).
16. Add content QA pass (grammar + UTF-8 encoding cleanup + duplicate removal).
17. Add a single-command runner (`run_all_stage1.ps1`) to execute all Stage 1 scripts with fail-fast behavior.
18. Add weighted scoring rubric per learning target (not only total self-test score).
19. Add resource link maintenance policy (dead-link replacement/removal workflow).
20. Validate and remove mojibake/encoding artifacts in handbook text before final release.

---

## 11) Acceptance Criteria (Final Definition of Done)

The revised handbook is accepted only if:

- It is actionable for a beginner without extra interpretation.
- It includes a resource stack with primary and backup options.
- It includes reproducible commands and expected artifacts.
- It explicitly declares data resource and data structure for each example (format: section 12).
- It includes detailed concept explanation and demonstration instructions.
- It includes clear learning-target instructions for each topic.
- It includes detailed tutorial flow for each key topic.
- It includes score-based readiness criteria with locked thresholds.
- It uses consistent terminology across all sections.
- It removes major redundancy while preserving conceptual depth.
- Every concept module has all template fields filled (no missing mistake, snippet, or quick check).
- Validation set and test set are treated as distinct concepts.
- Feature engineering and regularization each have their own concept module.
- Every runnable script has documented expected output in the handbook.
- All Stage 1 scripts can be executed via a single fail-fast command runner.
- Stage transition section explains what Stage 2 builds on from Stage 1.
- Learning assessment includes weighted scoring by target, not only raw question count.
- Resource section includes dead-link replacement/removal policy.
- Handbook passes UTF-8 quality check with no mojibake artifacts.
- GPU track: prerequisites section has verified CUDA setup steps for RTX 5090.
- GPU track: PyTorch + autograd concept module is present and complete.
- GPU track: topic12_pytorch_cuda.py runs without error and prints GPU device name.

---

## 12) Data Declaration Format Standard

Every example in the handbook that uses a dataset must include this block immediately before the code:

```
Data: <name and source>
Rows: <count>
Features: <column names and brief description>
Target: <column name, unit, type>
Type: <Regression / Classification / Clustering>
```

Example:

```
Data: California Housing (sklearn built-in, fetch_california_housing)
Rows: 20,640
Features: MedInc (median income), HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
Target: MedHouseVal (median house value in $100k units)
Type: Regression
```

This block is required for every worked example, project step, and demonstration task.
Synthetic data (e.g., `np.random`) must still declare shape, range, and purpose.

---

## 13) Stage Transition Requirement

The handbook must end with a section titled "What Comes After Stage 1" that includes:

- A 2–3 sentence summary of what Stage 2 covers (Python tools for AI: NumPy, Pandas, Matplotlib, Scikit-learn).
- The specific Stage 1 concepts that Stage 2 directly builds on:
  - train/test split → used in every scikit-learn pipeline
  - features and target (X and y) → directly mapped to Pandas DataFrames
  - loss and evaluation metrics → used in scikit-learn model evaluation
  - overfitting → reinforced in scikit-learn preprocessing pitfalls
- One sentence confirming minimum readiness: "Before moving to Stage 2, you must be able to explain supervised learning, build a simple pipeline, and evaluate a model on held-out data."

---

## 14) GPU Track Implementation Spec

This section closes the existing plan reference gap and defines the exact GPU-track requirements.

Required items:

- Environment checks:
  - Python version check command
  - CUDA driver/toolkit check command (`nvidia-smi`)
  - PyTorch CUDA availability check (`torch.cuda.is_available()`)
- Installation:
  - Windows and Unix installation commands for PyTorch with CUDA
  - explicit fallback to CPU-only install path
- Validation:
  - print GPU device name
  - run one tensor operation on GPU and one on CPU
  - report timing comparison with a warning that small operations may not show GPU speedup
- Handbook integration:
  - one dedicated subsection in setup
  - one dedicated concept module for tensors + autograd + device placement
  - one runnable script (`topic12_pytorch_cuda.py`) referenced from learning targets

---

## 15) Additional Improvement Items (New)

These items are recommended to make the plan stronger and easier to maintain.

### A. Glossary and Notation Standard

- Add a short glossary for recurring terms: feature, target, label, loss, metric, validation set, test set.
- Lock notation style (`X`, `y`, `y_pred`) and apply it everywhere.
- Add one "do not mix these terms" note (validation vs test, error vs loss).

### B. Script Quality and Verification

- Add a mandatory smoke-test command list for all scripts in `red-book/src/stage-1/`.
- Add expected runtime and expected output pattern for each script.
- Add a troubleshooting subsection for common runtime issues (package import failure, plotting backend, OS path issues).

### C. Reproducibility Policy

- Pin dependency versions in `requirements.txt` and document update policy.
- Require fixed random seeds in all tutorial scripts where stochastic behavior exists.
- Add OS-specific notes for command differences and known caveats.

### D. Learning Evidence and Progress Tracking

- Add a learner log template:
  - script run result
  - interpretation summary
  - mistake found
  - correction applied
- Add a daily completion tracker tied to Week 1/Week 2 roadmap.

### E. Content QA and Maintenance

- Add a pre-release checklist:
  - link check
  - script run check
  - terminology consistency check
  - UTF-8 encoding check
- Add a lightweight changelog section in the handbook with date and change summary.
- Define review cadence (for example: monthly quick review, quarterly full review).

### F. Priority Additions (Requested)

P0 (must include):

- Add explicit UTF-8 cleanup task for `AI-study-handbook-1.md` (remove mojibake characters).
- Add a single-command Stage 1 script runner (`run_all_stage1.ps1`) with fail-fast behavior.
- Add weighted scoring rubric per learning target.
- Add resource review rule: replace/remove dead links after 2 failed checks.

P1 (should include):

- Add a tiny "link status table" with last-check date for each primary resource.
- Add a validation log file template for smoke-test outputs.




