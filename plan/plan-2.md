# Stage 2 Handbook Improvement Plan (v2)

Target file: `red-book/AI-study-handbook-2.md`  
Plan owner: You + Codex  
Version date: 2026-04-03

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-2.md` to be:
  - more detailed
  - more guidable
  - more operatable
  - more understandable
- Add detailed explanation and demonstration for concepts.
- Add more instructions on learning targets.
- Add detailed tutorials for key topics.
- Add examples for each learning topic.
- Examples must be complete and operatable:
  - include data
  - include functions
  - include full workflow
  - runnable end-to-end with expected outputs
- Declare the data resource and data structure used in examples.
- Include high-quality resources (tutorials, books, articles, official docs, GitHub).
- Key request: all example code must be commented in very detail and clear, so learners can understand functionality line by line.

- Mandatory request: include PyTorch and CUDA conceptual/tutorial content in the chapter.
- Mandatory request: include runnable PyTorch/CUDA example code (simple -> intermediate -> advanced) with very detailed and clear functional comments.

This section is a scope guard: future edits should not remove these requirements.

---

## 1) Review Summary

### What is already strong

- Clear stage goal: Python tools for AI data workflow.
- Strong beginner-friendly concept coverage (NumPy, Pandas, Matplotlib, scikit-learn).
- Includes project and self-test.

### What still needs improvement

- No explicit Stage 2 runnable script package (`red-book/src/stage-2/`).
- No single-command fail-fast execution for Stage 2 scripts.
- Tutorial sequence is not strict enough for day-by-day execution.
- Learning targets are not weighted and not fully measurable.
- Data declaration format is not enforced in all worked examples.
- Expected output ranges are not documented for each script.
- No dedicated Stage 2 GPU/PyTorch implementation spec section.
- No explicit QA/maintenance framework (glossary, smoke-test log, link policy, encoding checks).

---

## 2) Target Outcomes (Measurable)

Stage 2 rewrite is complete only when:

- A beginner can execute Stage 2 using a fixed day-by-day sequence.
- Every key concept module includes:
  - plain-language definition
  - worked example
  - runnable script mapping
  - demonstration checklist
  - quick check question
  - common beginner mistake + fix
- Every example includes a data declaration block.
- Every runnable script includes expected output content and interpretation notes.
- Stage 2 supports a single-command fail-fast runner (`run_all_stage2.ps1`).
- Self-test includes weighted scoring and remediation actions.

---

## 3) Resource Upgrade (Complete Catalog)

Use this layered stack:

- Layer 1: core learning path (must complete)
- Layer 2: official docs (must use during implementation)
- Layer 3: books/articles (depth)
- Layer 4: practical GitHub resources

### A. Core Learning Path (Must Complete)

- NumPy quickstart
  - https://numpy.org/doc/stable/user/quickstart.html
- Pandas getting started
  - https://pandas.pydata.org/docs/getting_started/index.html
- Matplotlib tutorials
  - https://matplotlib.org/stable/tutorials/index.html
- scikit-learn user guide
  - https://scikit-learn.org/stable/user_guide.html
- scikit-learn common pitfalls
  - https://scikit-learn.org/stable/common_pitfalls.html
- Kaggle Intro to Machine Learning
  - https://www.kaggle.com/learn/intro-to-machine-learning
- Kaggle Pandas
  - https://www.kaggle.com/learn/pandas
- Kaggle Data Visualization
  - https://www.kaggle.com/learn/data-visualization

### B. Official Documentation (Implementation-First)

- NumPy reference
  - https://numpy.org/doc/stable/reference/index.html
- Pandas user guide
  - https://pandas.pydata.org/docs/user_guide/index.html
- Matplotlib gallery
  - https://matplotlib.org/stable/gallery/index.html
- scikit-learn examples
  - https://scikit-learn.org/stable/auto_examples/index.html
- Python datetime docs
  - https://docs.python.org/3/library/datetime.html

### C. Books (Priority Order)

- Python Data Science Handbook
  - https://jakevdp.github.io/PythonDataScienceHandbook/
- ISLP
  - https://www.statlearning.com/
- Dive into Deep Learning
  - https://d2l.ai/
- Hands-On Machine Learning (selected sections)
  - https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/

### D. Articles and Practical Reading

- Rules of Machine Learning
  - https://developers.google.com/machine-learning/guides/rules-of-ml/
- A Few Useful Things to Know About Machine Learning
  - https://homes.cs.washington.edu/~pedrod/papers/cacm12.pdf

### E. Popular GitHub Resources

- pandas
  - https://github.com/pandas-dev/pandas
- matplotlib
  - https://github.com/matplotlib/matplotlib
- scikit-learn
  - https://github.com/scikit-learn/scikit-learn
- handson-ml3
  - https://github.com/ageron/handson-ml3
- mlcourse.ai
  - https://github.com/Yorko/mlcourse.ai

### F. Resource-to-Stage Mapping (How to Use in Stage 2)

- Week 1 core:
  - NumPy quickstart, Pandas getting started, Matplotlib tutorials
- Week 1 ML toolkit usage:
  - scikit-learn user guide, common pitfalls
- Project and applied practice:
  - Kaggle Pandas + Data Visualization + Intro ML
- Optional deepening:
  - Python Data Science Handbook, handson-ml3, ISLP

### G. Priority and Time Budget (Must / Should / Optional)

Must (complete in Stage 2):

- NumPy quickstart: 2-3h
- Pandas getting started + user guide basics: 4-6h
- Matplotlib basics + gallery examples: 2-3h
- scikit-learn user guide (split/preprocess/evaluation): 4-5h
- scikit-learn common pitfalls: 1.5-2h
- Kaggle Pandas + Data Visualization + Intro ML: 6-8h

Should (high value):

- Python Data Science Handbook (selected chapters): 4-6h
- handson-ml3 selected notebooks: 3-5h
- Rules of ML + Domingos paper: 2-3h

Optional:

- ISLP and D2L selected sections: 4-8h
- GitHub source exploration (pandas/sklearn/matplotlib): 2-4h

Recommended Stage 2 total budget:

- Minimum track: 28-36h
- Strong track: 40-55h

---

## 4) New Handbook Structure (Required)

1. How to Use This Handbook
2. Prerequisites and Environment Setup (CPU + optional GPU bridge)
3. One-Week Core Roadmap (+ optional extension week)
4. Learning Targets (with pass checks)
5. Operatable Examples (script mapping + expected outputs)
6. Key Knowledge Modules
7. Debugging Checklist
8. Practice Project
9. Self-Test + weighted scoring rubric
10. What Comes After Stage 2

### Section Content Specifications

Section 1 must include:

- who this stage is for
- reading/running order
- script-first workflow
- what to do when stuck

Section 2 must include:

- Python version target
- OS-specific commands (Windows + Unix)
- requirements install commands
- optional GPU bridge setup and verification

Section 10 must include:

- 2-3 sentence Stage 3 preview
- explicit mapping from Stage 2 skills to Stage 3 needs
- readiness sentence before progressing

---

## 5) Concept Module Template (Mandatory)

Each module must include:

- What it is
- Why it matters
- Data declaration block
- Worked example
- Common beginner mistake + fix
- Code snippet
- Demonstration checklist
- Quick check
- When to use / when not to use

Core Stage 2 modules:

- NumPy vectorization
- NumPy shapes and broadcasting
- Pandas load/inspect/clean
- Pandas joins/groupby/rolling
- Feature engineering for tabular/time-series data
- Matplotlib as a debugging tool
- Train/validation/test preparation in scikit-learn
- Preprocessing + leakage prevention
- Pipeline pattern in scikit-learn
- Optional bridge: tensors/autograd/CUDA basics

Hard requirement: no module ships with missing fields.

---

## 6) Operable Roadmap

### Week 1 (Core Stage 2)

- Day 1: NumPy arrays, vectorization, broadcasting
- Day 2: Pandas load/inspect/clean basics
- Day 3: Pandas transform/groupby/rolling features
- Day 4: Matplotlib visualization for data debugging
- Day 5: scikit-learn split/preprocess/pipeline basics
- Day 6: leakage pitfalls + debugging checklist drills
- Day 7: Stage 2 project baseline pipeline + report draft

### Optional Extension Week

- Day 8-9: improve feature engineering and plots
- Day 10: add model comparison and error analysis
- Day 11: optional PyTorch/CUDA bridge script
- Day 12: finalize reproducibility and output artifacts
- Day 13: self-test + gap repair
- Day 14: final review and Stage 3 readiness check

---

## 7) Notebook and Visuals Plan

Notebook track:

- notebook01_numpy_pandas_basics.ipynb
- notebook02_data_cleaning_transform.ipynb
- notebook03_visual_debugging.ipynb
- notebook04_sklearn_pipeline.ipynb
- notebook05_stage2_project.ipynb

Visual requirements:

- one missing-values heatmap or table summary
- one time-series line chart with moving averages
- one distribution chart (histogram)
- one scatter plot for relationship checking
- one pipeline flowchart (load -> clean -> transform -> features -> split -> train -> evaluate)

---

## 8) Stage 2 Project Spec (Reproducible)

Required project layout:

- `project/README.md`
- `project/requirements.txt`
- `project/requirements-gpu.txt` (optional bridge)
- `project/src/load_data.py`
- `project/src/clean_transform.py`
- `project/src/features.py`
- `project/src/plot.py`
- `project/src/train_eval.py`
- `project/results/metrics.json`
- `project/results/figures/`

Minimum run commands:

Windows:
- `python -m venv .venv`
- `.venv\Scripts\activate`
- `pip install -r requirements.txt`
- `powershell -ExecutionPolicy Bypass -File .\run_all_stage2.ps1`

Unix/macOS:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `pwsh -File ./run_all_stage2.ps1`

Required outputs:

- cleaned dataset summary
- feature engineering summary
- plots with interpretation notes
- train/validation/test metrics
- leakage checks and findings

---

## 9) Debugging and Quality Gates

Required debugging flow:

- file/column mismatch -> verify load path, `df.columns`, `df.dtypes`
- datetime issues -> convert with `pd.to_datetime`, then sort by date
- NaN propagation -> inspect `df.isna().sum()` before/after transforms
- shape mismatch -> print shapes before NumPy/scikit-learn operations
- suspiciously high metrics -> leakage checks (split order, fit/transform boundaries)

Quality gates before completion:

- all Stage 2 scripts pass fail-fast runner
- expected outputs match documented patterns
- no unresolved leakage risks
- weighted score meets threshold
- project artifacts complete and reproducible

---

## 10) Implementation Plan (Execution Order)

1. Add locked requirements to Stage 2 handbook front matter.
2. Add section structure + section content specs.
3. Add Week 1 roadmap and optional extension week.
4. Refactor concepts into full module template.
5. Create `red-book/src/stage-2/` scripts and README.
6. Create `run_all_stage2.ps1` fail-fast runner.
7. Add data declaration blocks to all worked examples.
8. Add expected output documentation for every script.
9. Add weighted scoring rubric and remediation paths.
10. Add optional GPU bridge module and script.
11. Add glossary/notation and consistency pass.
12. Add smoke-test log and reproducibility notes.
13. Run final QA pass (grammar, UTF-8 cleanup, link checks, duplicate cleanup).

---

## 11) Acceptance Criteria (Final Definition of Done)

Stage 2 is accepted only if:

- handbook is actionable without external planning
- key topics include detailed explanation + demonstration
- learning targets are measurable and weighted
- data source and structure are declared in each example
- Stage 2 scripts run end-to-end via `run_all_stage2.ps1`
- expected outputs are documented and aligned with real script runs
- debugging checklist maps to real failure patterns
- optional GPU bridge is present and clearly marked optional
- stage transition section clearly maps Stage 2 to Stage 3
- handbook passes UTF-8/encoding quality checks

---

## 12) Data Declaration Format Standard

Every example must include:

```
Data: <name and source>
Rows: <count>
Features: <columns and brief description>
Target: <name, type, unit if applicable>
Type: <Tabular prep / Regression / Classification / Visualization / etc.>
```

Synthetic data must still declare:

- generation method
- shape
- value range
- purpose

---

## 13) Stage Transition Requirement

Handbook must end with "What Comes After Stage 2" and include:

- 2-3 sentence summary of Stage 3
- explicit mapping from Stage 2 skills to Stage 3 tasks
- readiness sentence before progression

---

## 14) GPU Track Implementation Spec

This section defines the optional Stage 2 GPU bridge.

Required items:

- environment checks:
  - `nvidia-smi`
  - `torch.cuda.is_available()`
- installation commands for Windows and Unix
- CPU fallback path
- validation script output must include:
  - torch version
  - CUDA availability
  - device name if CUDA exists
  - simple CPU/GPU timing comparison note
- integration:
  - one concept module
  - one runnable script
  - one learning target entry

---

## 15) Additional Improvement Items (New)

### A. Glossary and Notation Standard

- add glossary for DataFrame, array, tensor, feature, target, leakage
- lock notation style (`X`, `y`, `df`, `y_pred`)
- add "do not mix terms" notes

### B. Script Quality and Verification

- maintain smoke-test command list for all stage-2 scripts
- capture validation outputs in a log file
- include troubleshooting notes per common runtime issue

### C. Reproducibility Policy

- pin dependencies in `requirements.txt`
- set fixed seeds where stochastic behavior exists
- document OS command differences

### D. Learning Evidence and Progress Tracking

- add learner log template:
  - run result
  - interpretation
  - mistake
  - correction
- add daily completion tracker

### E. Content QA and Maintenance

- pre-release checklist:
  - link checks
  - script-run checks
  - terminology consistency
  - UTF-8 encoding checks
- add handbook changelog section
- define review cadence

### F. Priority Additions (Requested)

P0:

- add UTF-8 cleanup task
- add `run_all_stage2.ps1` fail-fast runner
- add weighted learning-target scoring
- add dead-link replacement rule (replace/remove after 2 failed checks)

P1:

- add link status table with last-check date
- add validation-log template for script runs

---

## 16) Priority Breakdown

P0 (must do):

- learning target upgrade with pass checks
- complete stage-2 runnable scripts + fail-fast runner
- data declaration enforcement
- expected output documentation for every script
- debugging and quality-gate enforcement

P1 (should do):

- weighted target rubric
- optional GPU bridge module + script
- glossary and notation standard
- link maintenance table

P2 (nice to have):

- notebook variants for each topic
- extra domain datasets
- optional benchmark/performance mini-study

