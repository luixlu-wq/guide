# Stage 3 - Machine Learning Algorithms

*(Week 4-6)*

## 0) If This Chapter Feels Hard

Do not read this chapter in one long pass.
Use this 4-pass loop for each algorithm:

1. Problem framing: what problem it solves and what output it predicts.
2. Intuition: what shape/boundary/rule the model is trying to learn.
3. Mechanics: loss function, optimization idea, and key hyperparameters.
4. Operatable practice: run code, inspect metrics/plots, and explain one failure mode.

If you are stuck, answer these first before changing algorithms:

- What is the target type (number, class label, or no label)?
- Which metric should decide success?
- Which preprocessing is required for this model?
- Is failure from underfitting, overfitting, leakage, or bad features?

---

## 1) Stage Goal

Understand major classical ML algorithms and how they behave on real data.

You are not only learning `.fit()` and `.predict()`.
You are learning:

- how models "think"
- when to use each model
- when a model is a bad choice
- how to compare models fairly

By the end of Stage 3, you should move from:

> "I can run a model"

to:

> "I can justify model choice, detect failure patterns, and improve the pipeline."

---

## 2) How To Use This Handbook

### Script-first study loop (recommended)

For each module:

1. Read "What it is" and "Why it matters".
2. Read assumptions and preprocessing requirements.
3. Run the complete example.
4. Record your result in a small learner log:
   - dataset used
   - metric value
   - one mistake you made
   - one fix you applied

### Time guide

- One algorithm module: 60-90 minutes
- One evaluation module: 60 minutes
- Weekly commitment: 8-12 hours

### What to do when results look strange

- Use the Debugging Checklist in Section 12.
- Do not change many things at once.
- Change one variable, rerun, compare.

---

## 3) Prerequisites And Environment Setup

### Knowledge prerequisites

- Python basics (functions, loops, lists, dicts)
- NumPy / pandas basics
- Stage 1 and Stage 2 concepts

### Environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install numpy pandas scikit-learn matplotlib seaborn
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pandas scikit-learn matplotlib seaborn
```

Optional (bridge module only):

```bash
pip install torch
```

### Reproducibility rules

- Use fixed `random_state` whenever supported.
- Keep train/test split constant for fair comparison.
- Keep preprocessing policy constant across compared models.

---

## 4) Learning Targets (Weighted Rubric)

| Target | Evidence | Weight |
|---|---|---|
| Distinguish regression/classification/clustering | Correct task type for each example | 10 |
| Explain 6 core algorithms at concept level | Short written explanation per module | 15 |
| Run complete workflow per module | Code runs end-to-end with outputs | 20 |
| Apply correct preprocessing per model | Pipeline uses scaling/encoding correctly | 10 |
| Compare models fairly | Same split, same metric, same folds | 15 |
| Diagnose underfit/overfit/leakage | Correct failure diagnosis and fix | 15 |
| Produce model comparison report | Table + rationale + tradeoff discussion | 15 |

Total: 100

Pass levels:

- 85-100: Ready for Stage 4
- 70-84: Continue with targeted remediation
- <70: Repeat core modules and fair-comparison workflow

---

## 5) Data Resources And Data Structure Declarations

Use these datasets for Stage 3 examples.

| Dataset | Source | Rows | Features | Target | Task |
|---|---|---:|---:|---|---|
| Diabetes | `sklearn.datasets.load_diabetes` | 442 | 10 numeric | disease progression score | Regression |
| Breast Cancer Wisconsin | `sklearn.datasets.load_breast_cancer` | 569 | 30 numeric | malignant/benign (0/1) | Classification |
| Iris | `sklearn.datasets.load_iris` | 150 | 4 numeric | species (0/1/2) | Classification / Clustering demo |
| Synthetic blobs | `sklearn.datasets.make_blobs` | configurable | configurable | optional label for validation | Clustering |

Common structure in scikit-learn examples:

- `X`: feature matrix, shape `(n_samples, n_features)`
- `y`: target vector, shape `(n_samples,)`

Reusable dataset inspection helper:

```python
from sklearn.datasets import load_breast_cancer


def inspect_dataset(loader):
    data = loader(as_frame=True)
    X = data.data
    y = data.target
    print("Dataset:", loader.__name__)
    print("Rows:", X.shape[0])
    print("Features:", X.shape[1])
    print("Feature columns:", list(X.columns)[:5], "...")
    print("Target name:", data.target_names if hasattr(data, "target_names") else "n/a")


if __name__ == "__main__":
    inspect_dataset(load_breast_cancer)
```

---

## 6) Fair Model Comparison Rules (Must Follow)

When comparing models, use all rules below:

1. Same task and same dataset.
2. Same train/test split (or same CV folds).
3. Same preprocessing policy where applicable.
4. Same evaluation metric set.
5. Same random seed strategy.
6. Compare both train and test metrics.
7. Record runtime and model complexity when relevant.

Do not compare models on different splits and call it "better".

---

## 7) Concept Modules With Complete Operatable Examples

### Example Complexity Scale (Used In All Modules)

- `Simple`: one clear objective, small/clean data, minimal preprocessing, one main metric.
- `Intermediate`: real benchmark dataset, proper split strategy, full metric set, stronger workflow discipline.
- `Advanced`: model comparison or deeper tuning, extra validation logic, tradeoff analysis, and failure-aware decisions.

Complexity dimensions you should watch:

- data complexity: noise, imbalance, nonlinearity, dimensionality
- pipeline complexity: preprocessing, feature engineering, leakage prevention
- model complexity: hyperparameter search, regularization, ensembling, kernel choice
- evaluation complexity: cross-validation, threshold tuning, multi-metric tradeoffs
- debugging complexity: overfitting/underfitting diagnosis and correction

## Module 1 - Linear Regression

Runnable script: [topic01_linear_regression.py](src/stage-3/topic01_linear_regression.py)

Progressive examples:
- Simple: [topic01a_linear_regression_simple.py](src/stage-3/topic01a_linear_regression_simple.py)
- Intermediate: [topic01_linear_regression.py](src/stage-3/topic01_linear_regression.py)
- Advanced: [topic01c_linear_regression_advanced.py](src/stage-3/topic01c_linear_regression_advanced.py)

Where complexity is in Topic 1:

- `Simple`: complexity is only parameter fitting (`slope`, `intercept`) on one feature.
- `Intermediate`: complexity comes from train/test split, scaling pipeline, and multiple regression metrics.
- `Advanced`: complexity comes from nonlinear feature expansion, regularization, and model-tradeoff comparison.

### What it is

Linear Regression predicts a continuous number by learning a weighted linear combination of features.

### Why it matters

It is a strong baseline and teaches core ideas: residuals, error minimization, and interpretability.

### Data declaration

- Data: Diabetes dataset (`load_diabetes`)
- Rows: 442
- Features: 10 numeric standardized features
- Target: disease progression score (continuous)
- Type: Regression

### Assumptions

- Relationship is approximately linear in parameters.
- Errors are not dominated by extreme outliers.
- Features carry predictive signal.

### Preprocessing requirements

- Scaling is often helpful but not always mandatory.
- Remove/handle extreme outliers when needed.

### Complete example (data + functions + workflow)

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def load_data():
    data = load_diabetes(as_frame=True)
    return data.data, data.target


def build_model():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ])


def evaluate(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    print("Train MSE:", round(mean_squared_error(y_train, train_pred), 3))
    print("Test MSE:", round(mean_squared_error(y_test, test_pred), 3))
    print("Test MAE:", round(mean_absolute_error(y_test, test_pred), 3))
    print("Test R^2:", round(r2_score(y_test, test_pred), 3))


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = build_model()
    evaluate(model, X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Nonlinear relationships if features are not transformed.
- Datasets with strong outliers and heavy noise.

### Common beginner mistake and fix

- Mistake: judging only by train score.
- Fix: always compare train vs test metrics.

### Demonstration checklist

- [ ] Dataset and target type are declared.
- [ ] MSE, MAE, R^2 are reported.
- [ ] Train and test metrics are compared.

### Quick check

Q: When should you avoid plain linear regression?
A: When relationship is strongly nonlinear and feature engineering cannot linearize it.

### When to use / not use

- Use: interpretable numeric prediction baseline.
- Not use: highly nonlinear pattern without engineered features.

---

## Module 2 - Logistic Regression

Runnable script: [topic02_logistic_regression.py](src/stage-3/topic02_logistic_regression.py)

Progressive examples:
- Simple: [topic02a_logistic_regression_simple.py](src/stage-3/topic02a_logistic_regression_simple.py)
- Intermediate: [topic02_logistic_regression.py](src/stage-3/topic02_logistic_regression.py)
- Advanced: [topic02c_logistic_regression_advanced.py](src/stage-3/topic02c_logistic_regression_advanced.py)

Where complexity is in Topic 2:

- `Simple`: complexity is binary decision boundary learning with one core metric.
- `Intermediate`: complexity comes from stratified split, scaling, and multi-metric evaluation.
- `Advanced`: complexity comes from imbalanced data handling and threshold-dependent precision/recall tradeoffs.

### What it is

Logistic Regression predicts class probability (0 to 1) and then class label.

### Why it matters

It is one of the best first baselines for classification.

### Data declaration

- Data: Breast Cancer Wisconsin (`load_breast_cancer`)
- Rows: 569
- Features: 30 numeric features
- Target: malignant/benign (binary)
- Type: Classification

### Assumptions

- Decision boundary is approximately linear in transformed feature space.
- Labels are reliable.

### Preprocessing requirements

- Scaling usually helps a lot.

### Complete example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def main():
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=3000, random_state=42)),
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]

    print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
    print("Precision:", round(precision_score(y_test, y_pred), 3))
    print("Recall:", round(recall_score(y_test, y_pred), 3))
    print("F1:", round(f1_score(y_test, y_pred), 3))
    print("ROC-AUC:", round(roc_auc_score(y_test, y_proba), 3))


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Complex nonlinear boundaries without engineered features.

### Common beginner mistake and fix

- Mistake: using accuracy only on imbalanced classes.
- Fix: include precision, recall, F1, and ROC-AUC.

### Demonstration checklist

- [ ] Uses scaling.
- [ ] Reports probability-based metric (ROC-AUC).
- [ ] Uses stratified split for classification.

### Quick check

Q: Why is logistic regression still a classification model?
A: It models class probability using sigmoid/logistic link and predicts labels via threshold.

### When to use / not use

- Use: fast, interpretable classification baseline.
- Not use: highly nonlinear boundary with weak feature engineering.

---

## Module 3 - Decision Tree

Runnable script: [topic03_decision_tree_depth.py](src/stage-3/topic03_decision_tree_depth.py)

Progressive examples:
- Simple: [topic03a_decision_tree_simple.py](src/stage-3/topic03a_decision_tree_simple.py)
- Intermediate: [topic03_decision_tree_depth.py](src/stage-3/topic03_decision_tree_depth.py)
- Advanced: [topic03c_decision_tree_advanced.py](src/stage-3/topic03c_decision_tree_advanced.py)

Where complexity is in Topic 3:

- `Simple`: complexity is basic rule-based splitting and reading tree size.
- `Intermediate`: complexity comes from depth sweep and overfitting gap interpretation.
- `Advanced`: complexity comes from pruning-path search, cross-validation, and alpha selection logic.

### What it is

A Decision Tree recursively splits features into rule-based branches.

### Why it matters

Very interpretable and naturally handles nonlinear patterns.

### Data declaration

- Data: Breast Cancer Wisconsin (`load_breast_cancer`)
- Rows: 569
- Features: 30 numeric features
- Target: binary class
- Type: Classification

### Assumptions

- Useful split rules exist in current feature space.

### Preprocessing requirements

- Usually no scaling requirement.

### Complete example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def train_and_eval(max_depth):
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, clf.predict(X_train))
    test_acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"max_depth={max_depth}, train={train_acc:.3f}, test={test_acc:.3f}")


def main():
    for d in [2, 4, 8, None]:
        train_and_eval(d)


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Overfits easily with deep trees.
- Unstable: small data changes can produce different trees.

### Common beginner mistake and fix

- Mistake: training unrestricted deep tree first.
- Fix: tune `max_depth`, `min_samples_leaf`, and compare train/test gap.

### Demonstration checklist

- [ ] Evaluates multiple depths.
- [ ] Reports train and test metrics.
- [ ] Detects overfitting pattern.

### Quick check

Q: What indicates tree overfitting?
A: Very high train score with much lower test score.

### When to use / not use

- Use: interpretable rule-based baseline.
- Not use: when stability and smooth generalization are critical without ensembling.

---

## Module 4 - Random Forest

Runnable script: [topic04_random_forest_baseline.py](src/stage-3/topic04_random_forest_baseline.py)

Progressive examples:
- Simple: [topic04a_random_forest_simple.py](src/stage-3/topic04a_random_forest_simple.py)
- Intermediate: [topic04_random_forest_baseline.py](src/stage-3/topic04_random_forest_baseline.py)
- Advanced: [topic04c_random_forest_advanced.py](src/stage-3/topic04c_random_forest_advanced.py)

Where complexity is in Topic 4:

- `Simple`: complexity is only ensemble training and one holdout metric.
- `Intermediate`: complexity comes from train/test generalization checks plus feature-importance interpretation.
- `Advanced`: complexity comes from OOB validation and permutation-importance diagnostics.

### What it is

Random Forest combines many decision trees and aggregates predictions.

### Why it matters

Strong tabular-data baseline with reduced overfitting compared to one tree.

### Data declaration

- Data: Breast Cancer Wisconsin (`load_breast_cancer`)
- Rows: 569
- Features: 30 numeric features
- Target: binary class
- Type: Classification

### Assumptions

- Ensemble diversity improves generalization.

### Preprocessing requirements

- Usually robust without strict scaling.

### Complete example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd


def main():
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    train_acc = accuracy_score(y_train, rf.predict(X_train))
    test_acc = accuracy_score(y_test, rf.predict(X_test))
    print("Train accuracy:", round(train_acc, 3))
    print("Test accuracy:", round(test_acc, 3))

    importances = pd.Series(rf.feature_importances_, index=X.columns)
    print("Top 5 features:")
    print(importances.sort_values(ascending=False).head(5))


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Can hide interpretability.
- May still fail with poor features or data leakage.

### Common beginner mistake and fix

- Mistake: assuming Random Forest removes need for feature quality.
- Fix: audit data quality and leakage first.

### Demonstration checklist

- [ ] Reports train/test accuracy.
- [ ] Reports top feature importances.
- [ ] Compares to single-tree baseline.

### Quick check

Q: Why does Random Forest usually generalize better than one tree?
A: Bagging and random feature subsampling reduce variance.

### When to use / not use

- Use: strong baseline on tabular data.
- Not use: when strict interpretability is the top requirement.

---

## Module 5 - SVM

Runnable script: [topic05_svm_tuning.py](src/stage-3/topic05_svm_tuning.py)

Progressive examples:
- Simple: [topic05a_svm_simple.py](src/stage-3/topic05a_svm_simple.py)
- Intermediate: [topic05_svm_tuning.py](src/stage-3/topic05_svm_tuning.py)
- Advanced: [topic05c_svm_advanced.py](src/stage-3/topic05c_svm_advanced.py)

Where complexity is in Topic 5:

- `Simple`: complexity is basic margin classifier with scaling.
- `Intermediate`: complexity comes from `C/gamma` tuning and CV-vs-test consistency.
- `Advanced`: complexity comes from multi-kernel search space and interpreting competing CV configurations.

### What it is

Support Vector Machine finds a margin-maximizing decision boundary.

### Why it matters

Can perform very well on medium-size datasets with clear margin structure.

### Data declaration

- Data: Iris (`load_iris`)
- Rows: 150
- Features: 4 numeric features
- Target: 3 classes
- Type: Classification

### Assumptions

- Classes can be separated in current or kernel-transformed space.

### Preprocessing requirements

- Scaling is usually required.

### Complete example

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def main():
    data = load_iris(as_frame=True)
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", random_state=42)),
    ])

    grid = GridSearchCV(
        pipe,
        param_grid={
            "svm__C": [0.1, 1, 10, 100],
            "svm__gamma": [0.01, 0.1, 1],
        },
        cv=5,
        n_jobs=-1,
    )

    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)

    print("Best params:", grid.best_params_)
    print("CV score:", round(grid.best_score_, 3))
    print("Test accuracy:", round(accuracy_score(y_test, y_pred), 3))


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Can be sensitive to scale and hyperparameters (`C`, `gamma`).
- Can be slower on large datasets.

### Common beginner mistake and fix

- Mistake: running SVM without scaling.
- Fix: always use pipeline with `StandardScaler`.

### Demonstration checklist

- [ ] Uses scaling pipeline.
- [ ] Tunes `C` and `gamma`.
- [ ] Reports CV and test metrics.

### Quick check

Q: What does a larger `C` usually do?
A: Penalizes misclassification more strongly and can reduce margin (risk overfit).

### When to use / not use

- Use: medium-size data with meaningful boundary geometry.
- Not use: very large datasets requiring fast training.

---

## Module 6 - KMeans Clustering

Runnable script: [topic06_kmeans_silhouette.py](src/stage-3/topic06_kmeans_silhouette.py)

Progressive examples:
- Simple: [topic06a_kmeans_simple.py](src/stage-3/topic06a_kmeans_simple.py)
- Intermediate: [topic06_kmeans_silhouette.py](src/stage-3/topic06_kmeans_silhouette.py)
- Advanced: [topic06c_kmeans_advanced.py](src/stage-3/topic06c_kmeans_advanced.py)

Where complexity is in Topic 6:

- `Simple`: complexity is fixed-`K` clustering and centroid interpretation.
- `Intermediate`: complexity comes from selecting `K` via silhouette after proper scaling.
- `Advanced`: complexity comes from multi-metric cluster validation (inertia/silhouette/ARI) and metric disagreement analysis.

### What it is

KMeans groups similar points into `K` clusters without labels.

### Why it matters

A practical first unsupervised method for segmentation tasks.

### Data declaration

- Data: Iris features only (`load_iris`)
- Rows: 150
- Features: 4 numeric features
- Target: not used for training (unsupervised)
- Type: Clustering

### Assumptions

- Cluster structure is roughly compact/spherical in feature space.

### Preprocessing requirements

- Scaling is recommended for distance-based methods.

### Complete example

```python
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np


def main():
    data = load_iris(as_frame=True)
    X = data.data

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_k = None
    best_score = -1.0

    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = km.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"k={k}, silhouette={score:.3f}")

        if score > best_score:
            best_score = score
            best_k = k

    final = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    final_labels = final.fit_predict(X_scaled)
    counts = np.bincount(final_labels)

    print("Best k:", best_k)
    print("Cluster sizes:", counts)


if __name__ == "__main__":
    main()
```

### What this model gets wrong

- Irregular cluster shapes.
- Sensitive to initialization and scaling.

### Common beginner mistake and fix

- Mistake: using cluster IDs as if they are true class labels.
- Fix: treat clusters as discovered structure, not ground truth categories.

### Demonstration checklist

- [ ] Tests multiple `k` values.
- [ ] Uses silhouette score.
- [ ] Uses scaling before distance-based clustering.

### Quick check

Q: Why does KMeans need `k` in advance?
A: The objective optimizes assignment for a fixed number of centroids.

### When to use / not use

- Use: quick segmentation baseline with numeric features.
- Not use: highly irregular/non-convex cluster structures.

---

## 8) Model Failure Patterns And Fix Playbook

Runnable scripts:
- [topic07_fair_model_comparison.py](src/stage-3/topic07_fair_model_comparison.py)
- [topic08_failure_modes_overfit_leakage.py](src/stage-3/topic08_failure_modes_overfit_leakage.py)

| Symptom | Likely cause | Fix |
|---|---|---|
| Train high, test low | Overfitting | regularization, simpler model, more data |
| Train and test both low | Underfitting | richer features, less bias, tune hyperparameters |
| Very high score unexpectedly | Leakage | audit preprocessing and target leakage |
| SVM unstable | no scaling / bad `C,gamma` | pipeline scaling + CV search |
| KMeans poor clusters | wrong scale / wrong `k` | scale features, silhouette analysis |

---

## 9) Three-Week Operable Roadmap (Week 4-6)

### Week 4 - Algorithm foundations

- Day 1: Linear Regression + residual thinking
- Day 2: Logistic Regression + threshold/probability
- Day 3: Decision Tree + depth control
- Day 4: Random Forest + variance reduction intuition
- Day 5: SVM + margin and scaling
- Day 6: KMeans + cluster quality
- Day 7: recap and concept checks

### Week 5 - Evaluation and fairness

- Day 8: metric selection
- Day 9: cross-validation workflow
- Day 10: leakage pitfalls
- Day 11: fair benchmark setup
- Day 12: compare models on same split
- Day 13-14: write model comparison report

### Week 6 - Project and readiness

- Day 15-17: build model comparison lab
- Day 18: error analysis
- Day 19: feature iteration
- Day 20: final report
- Day 21: self-test and readiness scoring

---

## 10) Stage 3 Script Mapping (for `/red-book/src/stage-3`)

Use this runnable script set:

- Topic 1 ladder:
  - [topic01a_linear_regression_simple.py](src/stage-3/topic01a_linear_regression_simple.py)
  - [topic01_linear_regression.py](src/stage-3/topic01_linear_regression.py)
  - [topic01c_linear_regression_advanced.py](src/stage-3/topic01c_linear_regression_advanced.py)
- Topic 2 ladder:
  - [topic02a_logistic_regression_simple.py](src/stage-3/topic02a_logistic_regression_simple.py)
  - [topic02_logistic_regression.py](src/stage-3/topic02_logistic_regression.py)
  - [topic02c_logistic_regression_advanced.py](src/stage-3/topic02c_logistic_regression_advanced.py)
- Topic 3 ladder:
  - [topic03a_decision_tree_simple.py](src/stage-3/topic03a_decision_tree_simple.py)
  - [topic03_decision_tree_depth.py](src/stage-3/topic03_decision_tree_depth.py)
  - [topic03c_decision_tree_advanced.py](src/stage-3/topic03c_decision_tree_advanced.py)
- Topic 4 ladder:
  - [topic04a_random_forest_simple.py](src/stage-3/topic04a_random_forest_simple.py)
  - [topic04_random_forest_baseline.py](src/stage-3/topic04_random_forest_baseline.py)
  - [topic04c_random_forest_advanced.py](src/stage-3/topic04c_random_forest_advanced.py)
- Topic 5 ladder:
  - [topic05a_svm_simple.py](src/stage-3/topic05a_svm_simple.py)
  - [topic05_svm_tuning.py](src/stage-3/topic05_svm_tuning.py)
  - [topic05c_svm_advanced.py](src/stage-3/topic05c_svm_advanced.py)
- Topic 6 ladder:
  - [topic06a_kmeans_simple.py](src/stage-3/topic06a_kmeans_simple.py)
  - [topic06_kmeans_silhouette.py](src/stage-3/topic06_kmeans_silhouette.py)
  - [topic06c_kmeans_advanced.py](src/stage-3/topic06c_kmeans_advanced.py)
- [topic07_fair_model_comparison.py](src/stage-3/topic07_fair_model_comparison.py)
- [topic08_failure_modes_overfit_leakage.py](src/stage-3/topic08_failure_modes_overfit_leakage.py)
- [topic09a_pytorch_cuda_simple.py](src/stage-3/topic09a_pytorch_cuda_simple.py) (optional bridge simple)
- [topic09_pytorch_cuda_bridge.py](src/stage-3/topic09_pytorch_cuda_bridge.py) (optional bridge intermediate)
- [topic09c_pytorch_cuda_advanced.py](src/stage-3/topic09c_pytorch_cuda_advanced.py) (optional bridge advanced)
- [run_all_stage3.ps1](src/stage-3/run_all_stage3.ps1)
- [run_ladder_stage3.ps1](src/stage-3/run_ladder_stage3.ps1) (`-IncludeGpuBridge` for topic09 ladder)
- [README.md](src/stage-3/README.md)
- [requirements.txt](src/stage-3/requirements.txt)
- [requirements-gpu.txt](src/stage-3/requirements-gpu.txt) (optional)

Expected output style for each script:

- Print data declaration summary
- Print key metrics
- Print short interpretation (1-2 lines)

---

## 11) Practice Project - Model Comparison Lab

### Goal

Compare multiple algorithms fairly and explain tradeoffs.

### Required workflow

1. Choose one project track and keep it fixed for the full lab.
2. If you want the recommended track, use classification with `load_breast_cancer`.
3. Declare dataset with this exact template before training: `source`, `rows`, `features`, `target`, `task type`.
4. Fix one evaluation strategy for all models:
5. Option A (recommended): `train_test_split(test_size=0.2, random_state=42, stratify=y)`.
6. Option B: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
7. Train at least 4 models on the same data conditions:
8. Recommended set for classification: LogisticRegression (scaled), DecisionTreeClassifier, RandomForestClassifier, SVC (scaled, `probability=True`).
9. Use one shared evaluation function and mandatory metric set:
10. Classification metrics: `accuracy`, `precision`, `recall`, `f1`, `roc_auc`.
11. Regression metrics (if you choose regression track): `mse`, `mae`, `r2`.
12. Record both train and test metrics for each model and compute a train-test gap.
13. Add one explicit feature engineering change with formula (example: `radius_texture_ratio = mean radius / mean texture`).
14. Rerun all models with the same split/CV and same metrics after feature engineering.
15. Create a before-vs-after delta table and explain which model improved, degraded, and why.
16. Choose one final model and write a short justification using performance + stability + interpretability tradeoffs.

### Required deliverables

- `results/model_comparison_before.csv`: one row per model with train/test metrics and train-test gap.
- `results/model_comparison_after.csv`: same schema as before table, after feature engineering change.
- `results/model_delta.csv`: per-model metric deltas (`after - before`) for the primary metric and at least one secondary metric.
- `results/failure_diagnosis.md`: one concrete failure case (overfit, underfit, or leakage risk), evidence, and fix.
- `results/feature_change.md`: exact feature formula, why it was added, and expected impact.
- `results/final_model_selection.md`: chosen model, rejected models, and final rationale in 5-10 sentences.
- `results/reproducibility.md`: dataset used, split/CV policy, random seed values, and run date.

Minimum acceptance checks:

- At least 4 models are compared in both before/after tables.
- The split/CV strategy and random seed are identical across all models.
- Before/after tables use the same metric set and same column names.
- Feature engineering step is explicit and rerun evidence is present.

---

## 12) Debugging Checklist

If results look wrong, check:

- [ ] Task type is correct (regression/classification/clustering)
- [ ] Target column is correct
- [ ] No data leakage in preprocessing
- [ ] Same split used across models
- [ ] Metric choice matches problem
- [ ] Train vs test gap inspected
- [ ] Scaling applied where needed
- [ ] Categorical encoding handled correctly
- [ ] Dataset size and class balance reviewed

---

## 13) Optional Bridge - PyTorch And CUDA (Concept + Training Flow)

Progressive examples:
- Simple: [topic09a_pytorch_cuda_simple.py](src/stage-3/topic09a_pytorch_cuda_simple.py)
- Intermediate: [topic09_pytorch_cuda_bridge.py](src/stage-3/topic09_pytorch_cuda_bridge.py)
- Advanced: [topic09c_pytorch_cuda_advanced.py](src/stage-3/topic09c_pytorch_cuda_advanced.py)

Classical scikit-learn algorithms in this chapter are mostly CPU path.
This bridge helps connect classical ML training concepts to deep learning training loops.

### Why This Section Feels Hard

Beginners often mix up three things:

- device placement (CPU/GPU)
- autograd gradient calculation
- optimizer parameter updates

If these are mixed up, training appears \"mysterious\".  
Use the 5-step loop below and verify each step with prints.

### 5-Step Training Loop (Detailed Guide And Instructions)

1. Move tensors to device (`cpu` or `cuda`).
2. Forward pass computes prediction.
3. Loss compares prediction vs target.
4. Backward pass computes gradients.
5. Optimizer updates parameters.

#### Step 1 - Move tensors to device

What to do:
- select `device = torch.device(\"cuda\" if torch.cuda.is_available() else \"cpu\")`
- move both data and model: `x = x.to(device)`, `model = model.to(device)`

Why it matters:
- model parameters and tensors must be on the same device

Debug check:
- print `x.device` and first parameter device

Common error:
- `Expected all tensors to be on the same device`

#### Step 2 - Forward pass

What to do:
- call model with input: `pred = model(x)`

Why it matters:
- this computes predicted values using current parameters

Debug check:
- print `pred.shape` and sample values

Common error:
- wrong input shape, especially missing batch dimension

#### Step 3 - Compute loss

What to do:
- choose loss by task: `MSELoss` (regression), `CrossEntropyLoss` (classification)
- `loss = loss_fn(pred, target)`

Why it matters:
- loss is the numeric training signal for optimization

Debug check:
- print initial loss; it should usually decrease over epochs

Common error:
- wrong target dtype/shape (for classification especially)

#### Step 4 - Backward pass

What to do:
- `optimizer.zero_grad()`
- `loss.backward()`

Why it matters:
- autograd computes `d(loss)/d(parameter)` and stores it in `parameter.grad`

Debug check:
- print gradient norm after backward

Common error:
- forgetting `zero_grad()` leads to gradient accumulation across steps

#### Step 5 - Optimizer step

What to do:
- `optimizer.step()`

Why it matters:
- updates model weights to reduce loss

Debug check:
- print parameter values before/after one step

Common error:
- calling `step()` before `backward()`

### Complexity Scale For This Bridge

- `Simple`:
  - one tiny tensor dataset
  - one forward/backward/update step
  - focus: understand parameter change
- `Intermediate`:
  - larger synthetic data
  - multi-epoch training loop
  - optional CPU vs CUDA timing
- `Advanced`:
  - mini-batch DataLoader
  - train/validation loop
  - gradient clipping + optional AMP on CUDA

Where complexity is in Topic 09:

- data complexity: tiny tensors -> large tensors -> mini-batch tabular tensors
- loop complexity: one step -> full epochs -> full train/validation lifecycle
- optimization complexity: plain SGD -> tuned optimizer flow -> clipping/AMP
- evaluation complexity: print loss -> track first/final loss -> validation loss + R^2
- system complexity: CPU fallback -> optional CUDA -> optional mixed precision path

### Run Instructions (Operatable)

CPU path:

```powershell
python topic09a_pytorch_cuda_simple.py
python topic09_pytorch_cuda_bridge.py
python topic09c_pytorch_cuda_advanced.py
```

With ladder runner:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage3.ps1 -IncludeGpuBridge
```

If CUDA is available, scripts will automatically use it.
If CUDA is unavailable, scripts run on CPU path with fallback messages.

### Minimal bridge example

```python
import torch


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)

    X = torch.tensor([[1.0], [2.0], [3.0], [4.0]], device=device)
    y = torch.tensor([[2.0], [4.0], [6.0], [8.0]], device=device)

    model = torch.nn.Linear(1, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(1, 301):
        optimizer.zero_grad()
        pred = model(X)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"epoch={epoch}, loss={loss.item():.6f}")

    w = model.weight.item()
    b = model.bias.item()
    print(f"Learned line: y = {w:.3f}x + {b:.3f}")


if __name__ == "__main__":
    main()
```

---

## 14) Self-Test (Quick)

1. When is linear regression a poor choice?
2. Why can logistic regression be strong even when simple?
3. What is the main overfitting signal for decision trees?
4. Why does Random Forest usually reduce variance?
5. Why is scaling critical for SVM?
6. Why is KMeans not evaluated like classification?
7. What makes a model comparison unfair?
8. What is data leakage during preprocessing?
9. Why compare train and test metrics together?
10. Which step usually gives bigger gains first: model switching or feature quality?

Scoring suggestion:

- 8-10 correct: strong
- 6-7 correct: acceptable, review weak modules
- <=5 correct: rerun modules and debugging checklist

---

## 15) High-Quality Resources (Use In This Order)

### Intuition-first

- R2D3 Part 1: https://r2d3.us/visual-intro-to-machine-learning-part-1/
- R2D3 Part 2: https://r2d3.us/visual-intro-to-machine-learning-part-2/

### Official implementation

- Google ML Crash Course: https://developers.google.com/machine-learning/crash-course
- sklearn supervised learning: https://scikit-learn.org/stable/supervised_learning.html
- sklearn unsupervised learning: https://scikit-learn.org/stable/unsupervised_learning.html
- sklearn model evaluation: https://scikit-learn.org/stable/model_evaluation.html
- sklearn cross-validation: https://scikit-learn.org/stable/modules/cross_validation.html
- sklearn common pitfalls: https://scikit-learn.org/stable/common_pitfalls.html

### Operatable examples

- sklearn classifier comparison:
  https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
- sklearn tree structure:
  https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
- sklearn forest importances:
  https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
- sklearn RBF SVM params:
  https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
- sklearn KMeans silhouette:
  https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
- sklearn CV visualization:
  https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html
- sklearn underfit vs overfit:
  https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html

### Deeper theory

- CS229 notes 1: https://cs229.stanford.edu/notes_archive/cs229-notes1.pdf
- CS229 notes 3: https://cs229.stanford.edu/notes_archive/cs229-notes3.pdf
- CS229 notes 7A: https://cs229.stanford.edu/notes_archive/cs229-notes7a.pdf
- ISLP: https://www.statlearning.com/
- ISLP labs: https://islp.readthedocs.io/en/latest/labs.html
- ESL (free PDF from authors): https://hastie.su.domains/ElemStatLearn/main.html

---

## 16) What You Must Be Able To Do After Stage 3

- [ ] Explain each core algorithm in plain language.
- [ ] Declare data source and data structure for each experiment.
- [ ] Run complete end-to-end workflow per algorithm.
- [ ] Choose metrics correctly by task type.
- [ ] Compare models fairly on same data conditions.
- [ ] Diagnose overfitting, underfitting, and leakage.
- [ ] Propose one data/feature improvement and validate impact.

---

## 17) What Comes After Stage 3

Stage 4 will focus on deeper optimization, robust experiment design, and production-style ML workflow.
The model behavior knowledge from Stage 3 becomes the foundation for tuning strategy, error analysis, and more advanced pipelines.
Move to Stage 4 only when you can run and explain fair model comparisons without guessing.
