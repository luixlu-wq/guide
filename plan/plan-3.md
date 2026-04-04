# Stage 3 Handbook Improvement Plan (v1)

Target file: `red-book/AI-study-handbook-3.md`  
Plan owner: You + Codex  
Version date: 2026-04-03

## 0) User Requirements (Locked)

These requirements are locked and must remain in scope:

- Improve `AI-study-handbook-3.md` to be:
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

Additional locked requirements requested later (must remain in scope):

- This chapter is complicated and hard to understand; do your best to find resources that help students understand better, collect more information, and consider the best improvement path.
- Add more example code for each topic, from simple to complicated.
- Add clear functional comments to all Stage 3 topic scripts.
- Add and enforce `Example Complexity Scale (Used In All Modules)` and explicit `where complexity is` explanation for each topic/module.
- Make the practice project section more clear and operatable.
- PyTorch and CUDA section is hard to understand; provide detailed guide and instructions, and include ladder-complexity examples (simple -> intermediate -> advanced).

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

- Clear Stage 3 goal: understand major ML algorithms and when to use them.
- Good high-level algorithm coverage (Linear/Logistic/Tree/RF/SVM/KMeans).
- Includes project and self-test.

### What still needs improvement

- Missing explicit “How to use this handbook” structure.
- No formal day-by-day roadmap with script mapping.
- No Stage 3 runnable script package (`red-book/src/stage-3/`) defined.
- No fail-fast runner for Stage 3 examples.
- No strict fair-comparison rules for model benchmarking.
- Data declaration blocks are not consistently enforced before examples.
- Expected output ranges are not standardized per script.
- No dedicated QA/maintenance framework (glossary, smoke-test log, link policy, UTF-8 checks).

---

## 2) Target Outcomes (Measurable)

Stage 3 rewrite is complete only when:

- A learner can compare classical ML algorithms fairly on the same task.
- Every algorithm module includes:
  - plain-language explanation
  - model assumptions
  - preprocessing needs
  - strengths/weaknesses
  - failure modes
  - runnable script mapping
  - demonstration checklist
  - quick check
  - common beginner mistake + fix
- Every worked example includes a data declaration block.
- Every runnable script includes expected output content and interpretation notes.
- Stage 3 supports a single-command fail-fast runner (`run_all_stage3.ps1`).
- Self-test includes weighted scoring and remediation actions.

---

## 3) Resource Upgrade (Complete Catalog)

Use this layered stack:

- Layer 1: core learning path (must complete)
- Layer 2: official docs (must use during implementation)
- Layer 3: books/articles (depth)
- Layer 4: practical GitHub resources

Link verification status:

- Last verified: 2026-04-03
- Policy: replace/remove links that fail two consecutive checks

### A. Core Learning Path (Must Complete)

- Google Machine Learning Crash Course
  - https://developers.google.com/machine-learning/crash-course
- scikit-learn supervised learning
  - https://scikit-learn.org/stable/supervised_learning.html
- scikit-learn unsupervised learning
  - https://scikit-learn.org/stable/unsupervised_learning.html
- scikit-learn model evaluation
  - https://scikit-learn.org/stable/model_evaluation.html
- scikit-learn cross-validation
  - https://scikit-learn.org/stable/modules/cross_validation.html
- scikit-learn common pitfalls
  - https://scikit-learn.org/stable/common_pitfalls.html
- Google MLCC Linear Regression module
  - https://developers.google.com/machine-learning/crash-course/linear-regression
- Google MLCC Logistic Regression module
  - https://developers.google.com/machine-learning/crash-course/logistic-regression
- Google Decision Forests course (for tree/forest intuition)
  - https://developers.google.com/machine-learning/decision-forests

### B. Official Documentation (Implementation-First)

- Linear models (sklearn)
  - https://scikit-learn.org/stable/modules/linear_model.html
- Decision trees
  - https://scikit-learn.org/stable/modules/tree.html
- Random forests
  - https://scikit-learn.org/stable/modules/ensemble.html
- SVM
  - https://scikit-learn.org/stable/modules/svm.html
- Clustering
  - https://scikit-learn.org/stable/modules/clustering.html
- Pipeline and preprocessing
  - https://scikit-learn.org/stable/modules/compose.html
- Classifier comparison example
  - https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
- Understanding the decision tree structure
  - https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
- Feature importances with a forest of trees
  - https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
- RBF SVM parameters
  - https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
- KMeans silhouette analysis
  - https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
- Visualizing cross-validation behavior
  - https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html
- Hyperparameter tuning guide
  - https://sklearn.org/stable/modules/grid_search.html

### C. Books (Priority Order)

- ISLP
  - https://www.statlearning.com/
- Hands-On Machine Learning (selected algorithm chapters)
  - https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/
- Python Data Science Handbook (modeling chapters)
  - https://jakevdp.github.io/PythonDataScienceHandbook/
- ISLP Labs (Python) - hands-on algorithm labs
  - https://islp.readthedocs.io/en/latest/labs.html

### D. Articles and Practical Reading

- A Few Useful Things to Know About Machine Learning
  - https://dl.acm.org/doi/10.1145/2347736.2347755
- Rules of Machine Learning
  - https://developers.google.com/machine-learning/guides/rules-of-ml/
- R2D3 Part 1: Visual Intro to Machine Learning (Decision Trees)
  - https://r2d3.us/visual-intro-to-machine-learning-part-1/
- R2D3 Part 2: Visual Intro to Machine Learning (Bias-Variance)
  - https://r2d3.us/visual-intro-to-machine-learning-part-2/
- Stanford CS229 Notes 1 (Supervised Learning)
  - https://cs229.stanford.edu/notes_archive/cs229-notes1.pdf
- Stanford CS229 Notes 3 (Generalized Linear Models / Logistic)
  - https://cs229.stanford.edu/notes_archive/cs229-notes3.pdf
- Stanford CS229 Notes 7A (K-means)
  - https://cs229.stanford.edu/notes_archive/cs229-notes7a.pdf
- 3Blue1Brown: Gradient Descent intuition
  - https://www.3blue1brown.com/lessons/gradient-descent

### E. Popular GitHub Resources

- scikit-learn examples repo
  - https://github.com/scikit-learn/scikit-learn
- handson-ml3
  - https://github.com/ageron/handson-ml3
- mlcourse.ai
  - https://github.com/Yorko/mlcourse.ai
- Microsoft ML for Beginners
  - https://github.com/microsoft/ML-For-Beginners
- INRIA scikit-learn MOOC notebooks and exercises
  - https://github.com/INRIA/scikit-learn-mooc

### F. Resource-to-Stage Mapping (How to Use in Stage 3)

- Week 1 algorithm foundations:
  - MLCC linear/logistic + R2D3 Part 1 + sklearn supervised docs
- Week 2 model comparison and evaluation:
  - sklearn model evaluation + CV visualizations + grid search + pitfalls + R2D3 Part 2
- Week 3 project and debugging:
  - sklearn examples + ISLP labs + handson-ml3 selected notebooks + CS229 notes

### H. Comprehension-First Learning Ladder (New)

For each algorithm, use a 3-step ladder:

1. Intuition first (R2D3 / visual explanation)
2. Official mechanics (scikit-learn user guide + example)
3. Operatable code (stage-3 script + project comparison)

Per-algorithm ladder:

- Linear Regression:
  - intuition: R2D3 + 3Blue1Brown gradient descent context
  - mechanics: sklearn linear models + MLCC linear regression
  - code: stage-3 linear regression script and residual plot
- Logistic Regression:
  - intuition: MLCC classification/thresholding + R2D3 boundaries
  - mechanics: sklearn logistic + MLCC logistic regression
  - code: stage-3 logistic script + confusion matrix
- Decision Tree / Random Forest:
  - intuition: Google Decision Forests + R2D3 Part 1/2
  - mechanics: sklearn tree/ensemble docs + tree structure example
  - code: stage-3 tree/forest comparison script
- SVM:
  - intuition: MLCC classification boundaries + margin concept notes
  - mechanics: sklearn SVM docs + RBF parameter example
  - code: stage-3 SVM tuning script
- KMeans:
  - intuition: CS229 Note 7A + sklearn clustering visuals
  - mechanics: sklearn clustering docs + silhouette analysis example
  - code: stage-3 KMeans evaluation script

### G. Priority and Time Budget (Must / Should / Optional)

Must:

- MLCC selected modules: 5-7h
- sklearn algorithm docs (linear/tree/forest/svm/kmeans): 6-8h
- evaluation + CV + pitfalls docs: 4-5h

Should:

- ISLP selected chapters: 4-6h
- handson-ml3 algorithm notebooks: 4-6h
- Domingos + Rules of ML: 2-3h

Optional:

- additional repos/articles deep dive: 3-6h

Recommended Stage 3 total budget:

- Minimum track: 28-36h
- Strong track: 40-55h

---

## 4) New Handbook Structure (Required)

1. How to Use This Handbook
2. Prerequisites and Environment Setup
3. Three-Week Roadmap (Week 4-6)
4. Learning Targets (with pass checks)
5. Operatable Examples (script mapping + expected outputs)
6. Key Knowledge Modules
7. Fair Model Comparison Rules
8. Debugging Checklist
9. Practice Project
10. Self-Test + weighted scoring rubric
11. What Comes After Stage 3

### Section Content Specifications

Section 1 must include:

- who this stage is for
- script-first study loop
- what to do when stuck
- expected weekly effort

Section 7 must include:

- same split policy across models
- same preprocessing policy across models
- same metric set per task
- same random seed strategy
- same CV fold strategy

Section 11 must include:

- 2-3 sentence Stage 4 preview
- skill mapping Stage 3 -> Stage 4
- readiness sentence before progressing

---

## 5) Concept Module Template (Mandatory)

Each module must include:

- What it is
- Why it matters
- Data declaration block
- Worked example
- Assumptions of the model
- Preprocessing requirements
- Strengths and weaknesses
- Common beginner mistake + fix
- Demonstration checklist
- Quick check
- When to use / when not to use

Core Stage 3 modules:

- Linear Regression
- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- KMeans Clustering
- Cross-validation and fair model comparison
- Metric selection by task
- Bias/variance behavior per algorithm
- Optional bridge: PyTorch implementation intuition for linear/logistic

Hard requirement: no module ships with missing fields.

---

## 6) Operable Roadmap (Week 4-6)

### Week 4 (Algorithm Basics)

- Day 1: Linear Regression + assumptions + residual thinking
- Day 2: Logistic Regression + probability interpretation
- Day 3: Decision Trees + overfitting behavior
- Day 4: Random Forest + variance reduction intuition
- Day 5: SVM + margin concept + scaling effects
- Day 6: KMeans + distance-based clustering intuition
- Day 7: recap and quick algorithm comparison notes

### Week 5 (Evaluation and Fair Comparison)

- Day 8: metric selection by task (classification vs regression)
- Day 9: cross-validation workflow
- Day 10: preprocessing pitfalls and leakage prevention
- Day 11: fair benchmark design
- Day 12: run benchmark scripts and interpret gaps
- Day 13-14: refine and document comparison table

### Week 6 (Project + Readiness)

- Day 15-17: build model comparison project
- Day 18: error analysis + failure mode diagnosis
- Day 19: feature importance and interpretation
- Day 20: final reporting
- Day 21: self-test and readiness check

---

## 7) Notebook and Visuals Plan

Notebook track:

- notebook01_linear_vs_logistic.ipynb
- notebook02_tree_forest_behavior.ipynb
- notebook03_svm_kmeans.ipynb
- notebook04_cv_and_fair_comparison.ipynb
- notebook05_model_comparison_lab.ipynb

Visual requirements:

- regression fit + residual plot
- confusion matrix per classifier
- ROC or PR curve for classification
- model comparison bar chart (same metric/split)
- tree depth vs train/test performance curve
- KMeans cluster scatter (2D projection)

---

## 8) Stage 3 Project Spec (Reproducible)

Required project layout:

- `project/README.md`
- `project/requirements.txt`
- `project/src/prepare_data.py`
- `project/src/train_models.py`
- `project/src/evaluate_models.py`
- `project/src/compare_models.py`
- `project/results/metrics.csv`
- `project/results/figures/`

Minimum run commands:

Windows:
- `python -m venv .venv`
- `.venv\Scripts\activate`
- `pip install -r requirements.txt`
- `powershell -ExecutionPolicy Bypass -File .\run_all_stage3.ps1`

Unix/macOS:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `pwsh -File ./run_all_stage3.ps1`

Required outputs:

- same-task multi-model comparison table
- per-model metrics with same split
- at least 3 analysis figures
- short model-selection rationale

---

## 9) Debugging and Quality Gates

Required debugging flow:

- suspiciously high performance -> leakage audit
- unstable CV scores -> investigate split randomness/data size
- model-specific failure:
  - linear/logistic underfit -> feature engineering/interaction terms
  - tree overfit -> depth/pruning/tuning
  - SVM poor results -> scaling/kernel/C tuning
  - KMeans poor clusters -> scaling/K selection/feature choice

Quality gates before completion:

- all Stage 3 scripts pass fail-fast runner
- fair comparison rules are followed and documented
- expected outputs match script runs
- weighted score meets threshold
- project artifacts complete and reproducible

---

## 10) Implementation Plan (Execution Order)

1. Add locked requirements to Stage 3 handbook front matter.
2. Add section structure + section content specs.
3. Add Week 4-6 roadmap.
4. Refactor algorithm sections into full module template.
5. Create `red-book/src/stage-3/` scripts + README + runner.
6. Add fair-comparison rules section.
7. Add data declaration blocks to all worked examples.
8. Add expected output documentation for every script.
9. Add weighted scoring rubric and remediation flow.
10. Add optional bridge module if needed.
11. Add glossary/notation consistency pass.
12. Add smoke-test log and reproducibility notes.
13. Final QA pass (grammar, UTF-8, link checks, duplicate cleanup).

---

## 11) Acceptance Criteria (Final Definition of Done)

Stage 3 is accepted only if:

- handbook is actionable without external planning
- each algorithm has detailed explanation + demonstration
- assumptions/preprocessing/failure modes are explicit
- learning targets are measurable and weighted
- data source and structure declared in each example
- Stage 3 scripts run end-to-end via `run_all_stage3.ps1`
- expected outputs documented and aligned with real script runs
- fair model comparison rules are enforced and evidenced
- debugging checklist maps to real model failure patterns
- stage transition section maps Stage 3 to Stage 4
- handbook passes UTF-8/encoding quality checks

---

## 12) Data Declaration Format Standard

Every example must include:

```
Data: <name and source>
Rows: <count>
Features: <columns and brief description>
Target: <name, type, unit if applicable>
Type: <Regression / Classification / Clustering / Comparison>
```

Synthetic data must still declare:

- generation method
- shape
- value range
- purpose

---

## 13) Stage Transition Requirement

Handbook must end with "What Comes After Stage 3" and include:

- 2-3 sentence summary of Stage 4
- explicit mapping from Stage 3 model knowledge to Stage 4 work
- readiness sentence before progression

---

## 14) Optional GPU/Advanced Bridge Spec

Optional and non-blocking for Stage 3 completion:

- one bridge script to show gradient-based training in PyTorch
- CUDA checks and CPU fallback behavior
- explicit statement: classical sklearn algorithms mostly run CPU path

---

## 15) Additional Improvement Items (New)

### A. Glossary and Notation Standard

- lock notation (`X`, `y`, `y_pred`, `X_train`, `X_test`)
- add glossary for decision boundary, margin, impurity, bias/variance, leakage

### B. Script Quality and Verification

- maintain smoke-test command list
- add validation log for script runs
- add troubleshooting notes per algorithm

### C. Reproducibility Policy

- pin dependency versions
- fixed random seeds where needed
- record OS and environment notes

### D. Learning Evidence and Progress Tracking

- learner log template:
  - script result
  - interpretation
  - mistake
  - correction
- weekly completion tracker

### E. Content QA and Maintenance

- pre-release checklist:
  - link checks
  - script-run checks
  - terminology consistency
  - UTF-8 checks
- add changelog and review cadence

### F. Priority Additions (Requested)

P0:

- add `run_all_stage3.ps1` fail-fast runner
- add weighted scoring per learning target
- enforce fair-comparison rule block
- add dead-link replacement rule (replace/remove after 2 failed checks)

P1:

- add link status table with last-check date
- add validation-log template
- add "algorithm learning ladder" table in handbook (intuition -> mechanics -> code)
- add "what this model gets wrong" subsection per algorithm

---

## 16) Priority Breakdown

P0 (must do):

- concept-module upgrade with full template
- Stage 3 runnable scripts + fail-fast runner
- fair-comparison rules and evidence
- data declaration enforcement
- expected output documentation for every script

P1 (should do):

- weighted target rubric
- glossary/notation standard
- reproducibility and validation log

P2 (nice to have):

- notebook variants per algorithm
- extra datasets and benchmark expansions

---

## 17) Chapter Simplification Blueprint (New)

This section is added specifically because Stage 3 is currently perceived as hard to understand.

### A. 4-Pass Teaching Flow (Mandatory)

Each algorithm section should be learned in this order:

1. Problem framing pass:
   - what task it solves
   - what input/output looks like
   - one concrete real example
2. Intuition pass:
   - geometric or visual intuition
   - how decision boundary or grouping changes
3. Mechanics pass:
   - objective/loss
   - optimization idea
   - key hyperparameters and their effect
4. Operatable pass:
   - runnable code
   - expected output
   - failure case + fix

### B. "Why This Is Hard" Blocks (Mandatory)

For each module, add a small block:

- why beginners get confused
- 2-3 symptoms of misunderstanding
- one checkpoint question before moving on

### C. Concept-to-Code Bridge Table (Mandatory)

For each algorithm, add:

- concept term
- where it appears in code
- what to print/plot to verify understanding

Example row format:

`margin` -> `SVC(C=..., kernel=...)` -> plot decision boundary + support vectors

### D. Minimum Math Pack (Must Have)

Keep math lightweight but explicit:

- Linear Regression: slope/intercept, MSE
- Logistic Regression: sigmoid, log loss
- Tree/Forest: impurity/information gain
- SVM: margin, C, kernel role
- KMeans: centroid update + inertia

### E. Link Reliability Policy

- Only keep links verified reachable at review time.
- For unstable resources, keep one backup in same topic category.
- Add `Last verified` date for external links.
- Replace/remove dead links after two failed checks.

### F. Resource Priority for Struggling Learners

Use in this strict order when learner is stuck:

1. R2D3 visual intuition page
2. sklearn official user guide + one official example
3. Stage-3 runnable script
4. CS229 notes / ISLP chapter for deeper theory

### G. Immediate P0 Additions Triggered by Complexity Feedback

- Add "How to use this chapter if you feel lost" section to handbook start.
- Add per-algorithm "what this model gets wrong" section.
- Add one minimum runnable script per algorithm in `red-book/src/stage-3/`.
- Add one fairness benchmark script comparing at least 4 classifiers on same split.
- Add one failure-mode script showing overfitting and leakage examples.





