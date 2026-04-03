# Stage 3 — Machine Learning Algorithms

*(Week 4–6)*

## Goal

Understand major machine learning algorithms and how they behave.

You are **NOT** just learning APIs.
You are learning:

- how models think
- when to use each model
- why models fail

This stage is where you move from:

> "I can call `.fit()`"

to:

> "I understand what kind of model I am using, why it works, and when it is a bad choice."

---

## Quick Summary

Different machine learning algorithms solve problems in different ways.

Some models:

- assume simple relationships
- split data with rules
- draw boundaries between classes
- combine many weak learners
- group similar examples without labels

A beginner should finish this stage understanding:

- what each major classical ML algorithm does
- what kind of data each model likes
- what the strengths and weaknesses are
- how to compare models fairly
- why features and preprocessing strongly affect performance

---

## Study Materials

**Google ML Crash Course**
https://developers.google.com/machine-learning/crash-course

### Algorithms to Learn

- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- SVM
- Clustering (KMeans)

---

## Key Knowledge (Deep Understanding)

### 1. Linear Regression

Used for predicting **continuous values**.

```
y = wx + b
```

**Key idea:** Find the best line that fits the data.

#### Beginner Explanation

Linear Regression is one of the simplest machine learning algorithms.

It is used when:

- the output is a number
- you want to predict a continuous value

Examples: house price, temperature, demand, sales, expected return.

- If you have one feature, it learns a **line**.
- If you have many features, it learns a **higher-dimensional plane**.

*Intuition: If house size increases, price may also increase. Linear regression learns how much each input affects the output.*

#### Step-by-Step Mental Model

| Step | Description |
|---|---|
| 1 | Start with inputs and outputs |
| 2 | Guess a line |
| 3 | Compare predictions to real values |
| 4 | Adjust the line to reduce error |
| 5 | Repeat until a better-fitting line is found |

Example data:

| Size | Price |
|---|---|
| 1000 | 200000 |
| 1500 | 300000 |
| 2000 | 400000 |

#### Important Core Ideas

- output is continuous
- model is linear in parameters
- learning means minimizing prediction error
- each feature gets a weight

#### Key Algorithms / Mechanisms

**A. Ordinary Least Squares (OLS)** — The standard algorithm for linear regression.

How it works:

1. Predict a value for each row
2. Compute the error between prediction and actual value
3. Square those errors
4. Find the parameters that minimize the total squared error

*Why important: OLS is the classic mathematical foundation of linear regression.*

---

**B. Gradient Descent for Linear Regression** — Another way to learn the weights.

How it works:

1. Start with random weights
2. Predict
3. Compute loss
4. Compute gradients
5. Update weights in the direction that lowers error
6. Repeat

*Why important: Useful when datasets are large or when understanding learning mechanics.*

---

**C. Regularized Linear Regression**

Examples: Ridge Regression, Lasso Regression.

*How it works: Adds a penalty for large weights.*

*Why important: Helps reduce overfitting and improves generalization.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Simple | Assumes mostly linear relationships |
| Fast | Sensitive to outliers |
| Interpretable | May underfit complex patterns |
| Good baseline model | |

#### When to Use

Use linear regression when:

- output is numeric
- you want interpretability
- you need a strong baseline
- relationships may be roughly linear

---

### 2. Logistic Regression

Used for **classification**.

**Output:** probability between 0 and 1.

#### Beginner Explanation

Despite its name, logistic regression is used for **classification**, not regression.

It predicts the probability that an input belongs to a class.

Examples: spam or not spam, churn or not churn, fraud or not fraud, survive or not survive.

It is often one of the best first models for classification.

#### Step-by-Step Mental Model

1. **Compute a weighted score** — Like linear regression, it first computes a score from the inputs.
2. **Convert score to probability** — Uses the sigmoid function to turn any number into a value between 0 and 1.
3. **Apply a threshold** — If probability > 0.5, predict class 1. Otherwise predict class 0.

#### Why the Sigmoid Matters

The sigmoid squashes output into 0 to 1, making it useful for probability-based classification.

#### Key Algorithms / Mechanisms

**A. Sigmoid Function**

```
σ(z) = 1 / (1 + e^-z)
```

- Very negative score → probability near 0
- Very positive score → probability near 1

*Why important: This is what turns raw model output into class probability.*

---

**B. Log Loss / Cross-Entropy Optimization** — Logistic regression is trained by minimizing log loss.

- If the model is confidently wrong → penalized heavily
- If the model is confidently correct → loss is lower

*Why important: This teaches the model to output better probabilities.*

---

**C. Gradient Descent** — Used to update weights to reduce log loss.

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Simple | Assumes a relatively simple decision boundary |
| Fast | May struggle with complex nonlinear patterns |
| Interpretable | |
| Strong baseline for classification | |
| Outputs probabilities | |

#### When to Use

Use logistic regression when:

- task is classification
- you want class probabilities
- you need a fast, explainable baseline
- dataset is not extremely complex

---

### 3. Decision Trees

Rule-based model.

```python
if age > 30:
    predict yes
else:
    predict no
```

#### Beginner Explanation

A decision tree makes predictions by asking a sequence of questions.

Example questions:

- Is age > 30?
- Is income > 50k?
- Is country = Canada?

Each question splits the data into smaller groups until the tree reaches a final decision.

This makes trees easy to understand visually.

#### Step-by-Step Mental Model

1. **Look at all features** — The model checks many possible questions.
2. **Choose the best split** — Picks the question that separates the data best.
3. **Split the data** — Rows are separated into groups.
4. **Repeat recursively** — Each group is split again.
5. **Stop and assign prediction** — When a group is pure enough or small enough, the tree stops growing.

#### Key Algorithms / Mechanisms

**A. Split Selection** — A tree chooses the best question at each step.

- For classification: Gini impurity, entropy / information gain
- For regression: reduction in variance or MSE

*How it works: The tree measures how much a split improves purity or reduces error.*

---

**B. Gini Impurity** — Measures how mixed a node is.

- Low impurity = mostly one class
- High impurity = mixed classes

*Why important: Trees try to create purer child nodes.*

---

**C. Information Gain** — Measures how much uncertainty is reduced after a split.

*Why important: A good split gives a large information gain.*

---

**D. Tree Pruning** — Used to reduce overfitting.

- Remove branches that are too specific
- Simplify the tree

*Why important: Deep trees can memorize the training data.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Easy to understand | Overfits easily |
| Works with nonlinear patterns | Unstable: small data changes can create different trees |
| Handles mixed feature types well | Single trees often generalize poorly |
| Little preprocessing needed | |

#### When to Use

Use decision trees when:

- interpretability is important
- you want rule-based behavior
- you need a quick nonlinear model baseline

---

### 4. Random Forest

Collection of trees.

**Key idea:** many weak models → strong model.

#### Beginner Explanation

Random Forest improves decision trees by combining many of them.

A single tree can overfit badly. A forest reduces that risk by:

- training many trees
- making them different from each other
- combining their predictions

It is one of the most useful classical ML algorithms.

#### Step-by-Step Mental Model

1. **Create many different training samples** — Each tree sees a slightly different version of the dataset.
2. **Build one tree per sample** — Each tree learns different details.
3. **Randomly limit features at splits** — This increases diversity between trees.
4. **Combine predictions** — Classification: majority vote. Regression: average prediction.

#### Key Algorithms / Mechanisms

**A. Bagging (Bootstrap Aggregating)**

*Core idea: Train models on random sampled versions of the data.*

How it works:

1. Sample rows with replacement
2. Train one tree on each sample
3. Combine predictions

*Why important: Bagging reduces variance.*

---

**B. Random Feature Subsampling** — At each split, only a random subset of features is considered.

*Why important: Prevents all trees from becoming too similar.*

---

**C. Voting / Averaging**

- Classification: trees vote
- Regression: outputs are averaged

*Why important: Combining many imperfect models often gives stronger performance.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Strong general-purpose model | Less interpretable than a single tree |
| Less overfitting than a single tree | Can be slower than simpler models |
| Handles nonlinear relationships | May struggle with sparse or very high-dimensional problems |
| Can estimate feature importance | |

#### When to Use

Use Random Forest when:

- you want a strong tabular-data baseline
- data may contain nonlinear patterns
- you want good performance without huge tuning effort

---

### 5. SVM

Finds the **best boundary** between classes.

**Good for:** small datasets with clear separation.

#### Beginner Explanation

SVM stands for **Support Vector Machine**.

It tries to separate classes with the best possible boundary — not just any line, but the line with the **maximum margin**: the largest gap between classes.

That usually helps generalization.

#### Step-by-Step Mental Model

1. **Plot the classes in feature space** — Imagine points from two categories.
2. **Find a separating boundary** — There may be many possible lines.
3. **Choose the boundary with maximum margin** — The best line is the one farthest from both groups.
4. **Use support vectors** — Only some important boundary points strongly influence the final separator.

#### Key Algorithms / Mechanisms

**A. Maximum Margin Classifier** — The core idea of SVM.

*How it works: Find the separating line or plane that maximizes the distance to the closest points in each class.*

*Why important: This often improves robustness.*

---

**B. Support Vectors** — The critical points closest to the boundary.

*Why important: They determine the final decision boundary.*

---

**C. Kernel Trick** — Used when classes are not linearly separable.

Examples: linear kernel, polynomial kernel, RBF kernel.

*How it works: Instead of explicitly transforming data into higher dimensions, the kernel lets SVM behave as if it did.*

*Why important: Allows SVM to model more complex boundaries.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Powerful on small to medium datasets | Can be slower on large datasets |
| Strong for clear class separation | Sensitive to scaling |
| Kernels allow nonlinear boundaries | Harder to interpret than logistic regression or trees |

#### When to Use

Use SVM when:

- dataset is not huge
- feature space is meaningful
- you want a strong classifier with a well-defined margin

---

### 6. Clustering (KMeans)

Groups **similar data** without labels.

#### Beginner Explanation

KMeans is an **unsupervised** learning algorithm.

It does not get correct answers. Instead, it tries to group similar data points together.

Example uses:

- customer segmentation
- grouping similar products
- document grouping
- finding natural structure in data

#### Step-by-Step Mental Model

1. **Choose K** — You decide how many groups you want.
2. **Place K centers** — Start with initial cluster centers.
3. **Assign each point to the nearest center** — Each point joins its nearest cluster.
4. **Recompute each center** — Each cluster center moves to the average of its assigned points.
5. **Repeat** — Reassign and update until clusters stop changing much.

#### Key Algorithms / Mechanisms

**A. Distance-Based Assignment** — Usually uses Euclidean distance.

*How it works: Each point goes to the nearest center.*

*Why important: This defines the cluster membership.*

---

**B. Centroid Update** — After assignment, each center becomes the average of its cluster points.

*Why important: This is how the clusters move toward better positions.*

---

**C. Iterative Optimization** — KMeans alternates: assign points → update centers → until stable.

*Why important: This is how the algorithm improves cluster quality.*

---

**D. Elbow Method** — A common method for choosing K.

*How it works: Train KMeans with different K values and look at within-cluster error. Choose a K where improvement starts slowing down.*

*Why important: K must usually be chosen by the user.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Simple | Must choose K |
| Fast | Sensitive to initialization |
| Useful first clustering algorithm | Struggles with irregular cluster shapes |
| Works well for roughly spherical clusters | Sensitive to scaling |

#### When to Use

Use KMeans when:

- you want simple clustering
- features are numerical
- cluster shapes may be compact and separated

---

## Difficulty Points

### 1. Choosing wrong model

**Why it happens:** Many tutorials focus on code first, not model behavior.

**Why it is a problem:** You may use regression for a classification problem, choose a complex model for simple data, or choose an unsuitable model for nonlinear patterns.

**Fix strategy:** Before selecting a model, ask:

- Is the target numeric or categorical?
- Do I need interpretability?
- Is the dataset small or large?
- Are relationships likely linear or nonlinear?
- Am I solving supervised or unsupervised learning?

### 2. Overfitting trees

**Why it happens:** Trees keep splitting until they fit tiny details.

**Why it is a problem:** Training score becomes very high, but test performance drops.

**Fix strategy:** Use max depth limits, minimum samples per leaf, pruning, or Random Forest instead of a single tree.

### 3. Ignoring feature importance

**Why it happens:** Beginners often focus on algorithms more than data.

**Why it is a problem:** Even a strong algorithm performs poorly with weak inputs.

**Fix strategy:** Improve feature quality, domain-informed features, preprocessing, and encoding/scaling where needed.

### 4. Not comparing models fairly

**Why it happens:** People retrain with different random splits and compare raw scores.

**Why it is a problem:** The comparison becomes unfair because each model saw different train/test examples.

**Fix strategy:** Use the same split for all models (or cross-validation), the same metric, and the same preprocessing rules.

### 5. Using wrong evaluation metric

**Why it happens:** Beginners often use accuracy for every classification task.

**Why it is a problem:** Accuracy may hide failure on minority classes.

**Fix strategy:**

| Task | Metrics |
|---|---|
| Regression | MSE, MAE, R² |
| Classification | accuracy, precision, recall, F1, ROC-AUC depending on needs |

### 6. Forgetting preprocessing differences between models

**Why it happens:** People assume all models can consume the same inputs equally well.

**Why it is a problem:** Some models, like SVM and logistic regression, are more sensitive to scaling than trees.

**Fix strategy:**

| Model Type | Scaling Sensitivity |
|---|---|
| Trees / Random Forest | Often less sensitive to scaling |
| SVM / Logistic Regression | Often benefit from scaling |
| Categorical features | May require encoding |

---

## Model Selection Workflow (Real World)

1. Define task type
2. Inspect target type
3. Prepare features
4. Choose baseline models
5. Train fairly
6. Evaluate with correct metrics
7. Check overfitting
8. Compare tradeoffs
9. Improve features and preprocessing
10. Retest

### Beginner Explanation of Each Step

1. **Define task type** — Is this regression, classification, or clustering?
2. **Inspect target type** — Make sure you know what the output means.
3. **Prepare features** — Clean and encode data if needed.
4. **Choose baseline models** — Start with simple models first.
5. **Train fairly** — Use the same split and same data conditions.
6. **Evaluate with correct metrics** — Do not rely on one metric blindly.
7. **Check overfitting** — Compare train vs test results.
8. **Compare tradeoffs** — Accuracy is not the only factor. Also consider speed, interpretability, and robustness.
9. **Improve features and preprocessing** — Often this matters more than switching models immediately.
10. **Retest** — Re-evaluate after changes.

---

## Debugging Checklist for Stage 3

If results look strange, check:

- [ ] Is the problem regression or classification?
- [ ] Did you define the correct target?
- [ ] Did you accidentally leak information?
- [ ] Did all models use the same train/test split?
- [ ] Did you use the right metric?
- [ ] Is one model badly overfitting?
- [ ] Are features scaled where needed?
- [ ] Are categories encoded properly?
- [ ] Is the dataset too small for the chosen model?
- [ ] Did you compare train and test performance?

---

## Practice Project

### Project: Model Comparison Lab

**Goal:** Train multiple models and compare them.

You are not just trying to get the highest score. You are trying to learn:

- how models behave differently
- how preprocessing changes results
- how overfitting appears
- how feature engineering changes performance

**Step 1 — Load dataset**

Use: Titanic, Iris, or stock dataset.

*Beginner guidance:*
- Iris → easiest classification dataset
- Titanic → good real-world style tabular dataset
- Stock dataset → more advanced, requires careful target design

If you are a beginner, start with Iris, then try Titanic.

---

**Step 2 — Preprocess**

- Clean missing values
- Encode categories
- Define target

Step-by-step:

1. Inspect columns
2. Identify target
3. Handle missing values
4. Encode categorical columns
5. Select feature columns
6. Optionally scale numerical features for sensitive models

*Why this step matters: If preprocessing is weak, comparison becomes meaningless.*

---

**Step 3 — Split data**

```python
from sklearn.model_selection import train_test_split
```

> **Beginner rule:** Do NOT create a new split for each model. Make one split and reuse it.

---

**Step 4 — Train models**

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Train each model on the same data
```

*Suggested extension: Also include LinearRegression for regression datasets and KMeans separately for clustering experiments.*

---

**Step 5 — Evaluate**

Compare train score and test score to see underfitting, overfitting, and generalization.

For classification, compare:

- training accuracy
- test accuracy
- confusion matrix
- precision / recall / F1 when useful

For regression, compare:

- training error
- test error
- MSE / MAE / R²

---

**Step 6 — Compare results**

Build a comparison table:

| Model | Train Score | Test Score | Overfitting? | Notes |
|---|---|---|---|---|
| Logistic Regression | | | | |
| Decision Tree | | | | |
| Random Forest | | | | |
| SVM | | | | |

---

**Step 7 — Add a feature**

Add one new engineered feature and repeat the full comparison.

*Why this step matters: Better features can change model performance significantly.*

Beginner ideas:

- For Titanic: family size, title extracted from name
- For stock dataset: moving average, return, volatility proxy
- For Iris: petal length × petal width interaction

### Deliverables

- dataset
- model scripts
- comparison table
- analysis

### Experiment Tasks

**Experiment 1 — Compare simple vs complex models**

Try: logistic regression, decision tree, random forest, SVM.

- Purpose: See which models underfit, overfit, or generalize best.

**Experiment 2 — Limit tree depth**

Train decision trees with depth 2, depth 4, and unlimited depth.

- Purpose: See how tree complexity affects train and test scores.

**Experiment 3 — Scale features for SVM and Logistic Regression**

Train before and after scaling.

- Purpose: See how some models depend strongly on preprocessing.

**Experiment 4 — Add one engineered feature**

Repeat the full comparison.

- Purpose: See whether feature engineering helps more than swapping models.

**Experiment 5 — Use cross-validation**

Instead of a single split, evaluate each model with cross-validation.

- Purpose: Get a more reliable comparison.

### Common Mistakes

1. **Different splits per model** — Scores become unfair to compare. *Fix: Reuse the exact same split, or use the same cross-validation procedure for all models.*

2. **No evaluation** — You do not know whether the model actually works. *Fix: Always record metrics on unseen data.*

3. **Ignoring overfitting** — A high training score feels impressive but the model may fail on new data. *Fix: Always compare train and test performance.*

4. **No feature engineering** — Weak inputs limit all models. *Fix: Try adding useful derived features and compare results again.*

5. **Using SVM or logistic regression without scaling** — Performance can degrade because features are on very different scales. *Fix: Use feature scaling for sensitive models.*

6. **Treating clustering like labeled classification** — Cluster IDs from KMeans are not true category labels. *Fix: Remember that clusters are discovered structure, not known ground truth labels.*

---

## Final Understanding

> Different ML models have different strengths, and performance depends on both data and features.

> There is no single "best model" for every problem. Good ML practice means choosing models thoughtfully, comparing them fairly, and improving data and features — not just chasing scores.

---

## Self Test

### Questions

1. What is linear regression used for?
2. What is logistic regression used for?
3. Why is logistic regression a classification model even though it has "regression" in the name?
4. What does a decision tree do?
5. Why do decision trees overfit easily?
6. What is Random Forest?
7. Why does Random Forest often generalize better than a single tree?
8. What does SVM try to maximize?
9. What are support vectors?
10. What is the kernel trick?
11. What is KMeans used for?
12. Does KMeans need labels?
13. Why must you choose K in KMeans?
14. What is the difference between regression and classification?
15. What is the difference between supervised and unsupervised learning?
16. Why should all models use the same train/test split in comparison?
17. Why can accuracy be misleading?
18. Why are features so important?
19. Which models are more sensitive to scaling?
20. Which models are usually less sensitive to scaling?
21. What is overfitting?
22. What is underfitting?
23. What is pruning?
24. What is bagging?
25. What does Random Forest combine at the end?
26. Why should you compare train and test scores?
27. What is a good first baseline for regression?
28. What is a good first baseline for classification?
29. Why is feature engineering important in model comparison?
30. What is the main lesson of this stage?

### Answers

1. It is used for predicting continuous numerical values, such as price, demand, or temperature.

2. It is used for classification problems, especially binary classification.

3. Because it predicts class probabilities using a sigmoid function and then maps those probabilities to class labels.

4. It makes predictions by repeatedly splitting data using rule-based questions.

5. Because they can keep splitting until they memorize small details and noise in the training data.

6. Random Forest is an ensemble of many decision trees whose predictions are combined.

7. Because combining many varied trees reduces variance and makes predictions more stable.

8. It tries to maximize the margin between classes.

9. They are the important training points closest to the decision boundary that help define the SVM separator.

10. It is a method that allows SVM to model nonlinear boundaries without explicitly transforming data into higher-dimensional space.

11. It is used for clustering similar points into groups.

12. No. KMeans is an unsupervised algorithm.

13. Because the algorithm needs to know how many clusters to form.

14. Regression predicts numbers. Classification predicts categories.

15. Supervised learning uses labeled data. Unsupervised learning uses unlabeled data.

16. Because otherwise the comparison is unfair: each model would be evaluated on different data.

17. Because on imbalanced datasets, a model can get high accuracy while still failing on the most important class.

18. Because models can only learn from the information present in the features.

19. SVM and logistic regression are often more sensitive to feature scaling.

20. Decision trees and Random Forest are usually less sensitive to scaling.

21. Overfitting is when a model performs very well on training data but poorly on unseen data because it memorized too much detail.

22. Underfitting is when a model is too simple to capture important patterns in the data.

23. Pruning is the process of removing unnecessary branches from a decision tree to reduce overfitting.

24. Bagging is training multiple models on different random samples of the data and combining their predictions.

25. It combines tree predictions using majority vote for classification or averaging for regression.

26. Because the gap between them helps you detect overfitting or underfitting.

27. Linear Regression is often a good first baseline for regression.

28. Logistic Regression is often a good first baseline for classification.

29. Because better features can improve many models and sometimes matter more than switching algorithms.

30. Different models think differently, behave differently, and must be chosen and compared thoughtfully using the same data conditions and good features.

---

## What You Must Be Able To Do After Stage 3

- [ ] Explain what each major classical ML algorithm does
- [ ] Distinguish regression, classification, and clustering
- [ ] Explain how linear regression, logistic regression, trees, forests, SVM, and KMeans work at a beginner level
- [ ] Choose a reasonable baseline model for a problem
- [ ] Compare models fairly on the same dataset split
- [ ] Recognize overfitting from train/test results
- [ ] Explain why preprocessing and features matter
- [ ] Understand that model choice is about fit to the problem, not random trial and error
