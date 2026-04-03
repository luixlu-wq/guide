# Stage 1 — AI and Machine Learning Fundamentals

*(Week 1–2)*

## Goal

Understand how Machine Learning works conceptually.

You are **NOT** trying to be advanced here.

You are building a correct mental model of:

- what a model is
- what learning means
- how data is used
- how evaluation works

---

## Quick Summary

Machine Learning is about learning patterns from data so a model can make predictions on new, unseen data.

A beginner should finish this stage being able to explain:

- what a model is
- what training means
- why testing matters
- what overfitting is
- why features are important
- how simple ML algorithms work at a high level

---

## Study Materials

### Best Free Course

**Andrew Ng — Machine Learning**
https://www.coursera.org/learn/machine-learning

**Practise repo**
https://github.com/Zhenye-Na/coursera-ml

### Alternative (Fully Free)

**MIT Machine Learning**
https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/

### Recommended Book (Free)

**Dive Into Deep Learning**
https://d2l.ai/

---

## Key Topics

- Supervised Learning
- Unsupervised Learning
- Cost function
- Gradient descent
- Training vs Testing
- Overfitting
- Bias vs Variance

---

## Key Knowledge (Deep Understanding)

### 1. What Machine Learning REALLY is

Machine Learning is **NOT** magic.

It is:

- Learning a function from data
- input (features) → output (target)

**Example:**

| Input | Output |
|---|---|
| house size | price |
| stock indicators | up/down |
| email text | spam |

> The model = a mathematical function.

#### Beginner Explanation

Think of it like this:

You show the computer many examples.

| house size | house price |
|---|---|
| 1000 | 200000 |
| 1500 | 300000 |
| 2000 | 400000 |

The computer tries to discover the pattern between input and output.

It may learn something like:

```
price ≈ 200 × size
```

That learned pattern is **the model**.

The computer does NOT "understand" houses the way humans do.
It only finds relationships in data.

#### Mental Model

> Machine Learning = pattern finding from examples.

#### Important Limitation

A model only learns from the data it sees.

So if the data is:

- incomplete
- biased
- noisy
- misleading

then the model can also become incomplete, biased, noisy, or misleading.

#### Key Algorithms for This Idea

**Linear Regression**

Used when the relationship between input and output can be approximated by a line.

How it works:

1. Start with a line
2. See how wrong the line is
3. Adjust the line
4. Repeat until the error becomes smaller

Simple form:

```
y = wx + b
```

Where:

- `x` = input
- `w` = slope
- `b` = intercept
- `y` = predicted output

*Intuition: It draws the "best fit line" through data points.*

---

**Decision Tree**

Used to learn rules from data.

How it works:

1. Choose the best question to split the data
2. Split the dataset into groups
3. Repeat on each group
4. Build a tree of decisions

Example:

```python
if house_size > 1500:
    price = high
else:
    price = low
```

*Intuition: It learns by asking a sequence of yes/no questions.*

---

**k-Nearest Neighbors (kNN)**

Used to predict based on similar past examples.

How it works:

1. Look at the new input
2. Find the nearest examples in training data
3. Use their labels/values to predict

*Example: If 5 houses most similar to your house are expensive, your house is likely expensive too.*

*Intuition: "Similar things tend to behave similarly."*

---

### 2. Supervised Learning

Learning from **labeled** data.

You provide:

- input (X)
- output (y)

**Types:**

- **Regression** — Predict a number (e.g. house price)
- **Classification** — Predict a category (e.g. spam / not spam)

#### Beginner Explanation

In supervised learning, the model is trained using examples that already have the correct answers.

| Email Text | Label |
|---|---|
| "Win money now" | spam |
| "Meeting at 3 PM" | not spam |

The model learns from those examples so later it can classify new emails.

#### Step-by-Step

1. Give the model input data
2. Give the correct answer
3. Let the model make a prediction
4. Compare prediction with real answer
5. Measure the error
6. Update model parameters
7. Repeat many times

#### Key Algorithms

**Linear Regression** — For regression problems.

- Predicts a continuous number
- Finds the line or plane that best matches the data
- *Use case: Predicting house prices, demand, temperature, stock-related numeric targets*

---

**Logistic Regression** — For classification problems.

How it works:

1. Compute a weighted score from features
2. Pass it through a sigmoid function
3. Output a probability between 0 and 1
4. Convert probability into a class label

*Example: Probability(spam) = 0.92 → classify as spam.*

*Intuition: "How likely is this input to belong to class A?"*

---

**Decision Tree** — For both classification and regression.

- Repeatedly splits data using rules
- Creates branches and leaves
- Final leaf gives prediction

---

**Random Forest** — A stronger version of decision trees.

How it works:

1. Build many decision trees
2. Each tree sees slightly different data
3. Combine their predictions

- For classification: majority vote
- For regression: average output

*Intuition: Instead of trusting one expert, ask many experts and combine their opinions.*

---

**Support Vector Machine (SVM)** — Mainly for classification.

- Finds a boundary that separates classes
- Chooses the boundary with the largest gap between groups

*Intuition: Find the clearest possible dividing line between two groups.*

---

### 3. Unsupervised Learning

**No labels.**

Model tries to:

- find patterns
- group data
- compress structure

#### Beginner Explanation

In unsupervised learning, the model gets only input data, without correct answers.

*Example: You have customer behavior data, but nobody tells you which customers belong to which group. The model tries to discover hidden structure.*

#### What It Is Good For

- customer segmentation
- anomaly detection
- grouping similar documents
- reducing dimensions for visualization

#### Key Algorithms

**K-Means Clustering** — Used to group similar data into K clusters.

How it works:

1. Pick K random centers
2. Assign each point to the nearest center
3. Move each center to the average of its assigned points
4. Repeat until stable

*Intuition: Group points into clusters around centers.*

---

**Hierarchical Clustering** — Builds clusters step by step.

How it works:

1. Start with each point as its own cluster
2. Merge the closest clusters repeatedly
3. Build a hierarchy of groups

*Intuition: Like building a family tree of similarity.*

---

**PCA (Principal Component Analysis)** — Used for dimensionality reduction.

How it works:

1. Look for directions where data varies the most
2. Project the data into fewer dimensions
3. Keep the most informative directions

*Intuition: Compress data while preserving important structure.*

---

### 4. Features vs Target

- `X` = features (inputs)
- `y` = target (output)

> Bad features → bad model.

#### Beginner Explanation

A feature is any piece of information used by the model to make prediction.

Examples:

- For house price: size, location, number of bedrooms
- For spam detection: number of suspicious words, sender domain, number of links

The **target** is what you want to predict.

#### Important Rule

> Garbage in → garbage out

If your features are poor, the model usually performs poorly.

#### Key Techniques Related to Features

**Feature Scaling** — Some models work better when features are on similar scales.

- Standardization
- Min-Max scaling

*Why needed: If one feature is 0–1 and another is 0–1,000,000, some algorithms can be dominated by the large-scale feature.*

---

**One-Hot Encoding** — Used for categorical data.

```
Color = red, blue, green

red   -> [1,0,0]
blue  -> [0,1,0]
green -> [0,0,1]
```

*Why needed: Models usually work with numbers, not text categories directly.*

---

**Feature Selection** — Choose the most useful features and remove weak or noisy ones.

*Why: Too many useless features can hurt model performance.*

---

### 5. Training vs Testing

- **Training** — Used to learn patterns
- **Testing** — Used to evaluate generalization

> **IMPORTANT: Never test on training data**

#### Beginner Explanation

If you teach a student using practice questions, then test them using the exact same questions, you do not know whether they truly learned. Maybe they just memorized.

The same applies to ML.

- Training data = what the model learns from
- Testing data = new data used to check if it truly learned

#### Why This Matters

The real goal is not to do well on old data.
The real goal is to do well on **new data**.

#### Key Techniques

**Train/Test Split** — Divide data into two parts.

- 80% training
- 20% testing

---

**Cross Validation** — A stronger evaluation method.

How it works:

1. Split data into several folds
2. Train on some folds
3. Test on the remaining fold
4. Repeat multiple times
5. Average the results

*Why useful: Gives a more reliable estimate of model performance.*

---

### 6. Generalization

- **Goal:** Perform well on unseen data
- **Not:** Memorize training data

#### Beginner Explanation

- **Good model:** Learns "larger houses tend to cost more"
- **Bad model:** Memorizes "this exact house cost 300k"

#### Why Generalization Is the Real Goal

In real life, models are used on future data, not on the old training set.

#### Key Methods That Support Generalization

**Regularization** — Adds a penalty for making the model too complex.

```
Total Loss = Error Loss + Complexity Penalty
```

Types:

- L1 regularization
- L2 regularization

---

**Simpler Model Selection** — Sometimes a simpler model generalizes better than a more complex one.

*Why: Complex models can overfit more easily.*

---

### 7. Overfitting

Model memorizes training data instead of learning pattern.

| | |
|---|---|
| **Bad** | `if x == 1 → 2` / `if x == 2 → 4` |
| **Good** | `y = 2x` |

#### Beginner Explanation

Overfitting means the model becomes too specialized to the training data.

It learns: noise, exceptions, accidental quirks — instead of the general pattern.

#### Signs of Overfitting

- training performance is very high
- test performance is much worse

#### Why It Happens

- model too complex
- too little data
- noisy data
- too many features
- training too long

#### Important Fix Methods

**Regularization** — Discourages complexity.

**Pruning (for Trees)** — Removes branches that are too specific.

1. Build a large tree
2. Cut branches that do not improve generalization

**Early Stopping** — Stop training before the model starts memorizing too much. *(Common in neural networks.)*

**More Data** — With more diverse examples, the model has less chance to memorize only a few patterns.

---

### 8. Bias vs Variance

| Concept | Meaning |
|---|---|
| Bias | too simple |
| Variance | too complex |

> Goal = balance both.

#### Beginner Explanation

**High Bias** — The model is too simple to capture the pattern.

- *Example: Trying to fit a straight line to data that clearly curves*
- Result: **underfitting**

**High Variance** — The model is too sensitive to training data.

- *Example: It bends too much to fit every small fluctuation*
- Result: **overfitting**

#### Key Methods

**Ensemble Methods** — Combine multiple models to improve performance.

- *Example: Random Forest*
- *Why useful: Combining many models can reduce variance.*

**Model Selection** — Choose the right level of complexity for the problem.

---

### 9. Loss Function (How the model learns)

Model learns by minimizing error.

```
Loss = difference between prediction and truth
MSE = (y_pred - y_true)²
```

> Goal: minimize loss

#### Common Loss Functions

**Mean Squared Error (MSE)** — Common for regression.

1. Take prediction minus actual value
2. Square the difference
3. Average across examples

*Why square? So negative and positive errors do not cancel each other, and larger errors are penalized more.*

---

**Log Loss / Cross-Entropy Loss** — Common for classification.

- Compares predicted probability to the true class
- Penalizes confident wrong predictions heavily

*Why useful: Helps classification models learn probabilities correctly.*

---

### 10. How Learning Happens

```
Data → Model → Prediction → Error → Update → Repeat
```

Steps:

1. Predict
2. Calculate loss
3. Update parameters

> This is called **Gradient Descent**

#### Key Optimization Algorithms

**Gradient Descent** — Move model parameters in the direction that reduces loss.

1. Calculate loss
2. Measure how loss changes when parameters change
3. Move parameters slightly downhill
4. Repeat

*Intuition: Like walking downhill toward the lowest point in a valley.*

---

**Stochastic Gradient Descent (SGD)** — Variant of gradient descent.

- Updates using one sample at a time, or very small batches
- Benefits: faster updates, works well on large datasets
- Tradeoff: noisier than full-batch gradient descent

---

**Mini-Batch Gradient Descent** — Middle ground.

- Updates parameters using a small group of samples each time
- *Why popular: Balances speed and stability.*

---

## Difficulty Points

### 1. Thinking ML is "smart"

> It is NOT intelligence. It is math + optimization.

**Why Beginners Make This Mistake:** Because model outputs can look impressive.

**Fix Strategy:** Always ask:
- What data did it learn from?
- What pattern is it using?
- What are its limits?

### 2. Confusing correlation vs causation

> Model does NOT understand cause.

**Example:** Ice cream sales increase → Drowning incidents increase. The model may think they are related, but both are caused by hot weather.

**Fix Strategy:** Use domain knowledge. Do not assume the model discovered true cause.

### 3. Misunderstanding evaluation

> High accuracy ≠ good model.

**Example:** If 95% of emails are not spam, a model that always predicts "not spam" gets 95% accuracy — but it is useless.

**Fix Strategy:** Use the right metrics:
- precision
- recall
- F1 score
- confusion matrix
- MSE / MAE for regression

### 4. Ignoring features

> Features determine everything.

**Real Problem:** A bad model with good features can sometimes outperform a fancy model with bad features.

**Fix Strategy:** Spend time on better data, better features, and better preprocessing before trying a more complex model.

### 5. Expecting reasoning

> ML models do NOT reason.

**Fix Strategy:** Treat traditional ML as function approximation, not reasoning.

### 6. Data Leakage

> Model accidentally sees future or hidden information.

**Example:** Predict house price using a feature created after the sale happened.

**Why This Is Dangerous:** The model appears amazing during evaluation but fails in real deployment.

**Fix Strategy:**
- Split data properly
- Avoid future information
- Make preprocessing use only training data where appropriate
- Simulate real-world prediction conditions

---

## ML Workflow (Real World)

1. Define problem
2. Collect data
3. Clean data
4. Select features
5. Train model
6. Evaluate
7. Improve

### Beginner Explanation of Each Step

1. **Define problem** — Be specific.
   - Bad: "Predict the market"
   - Good: "Predict whether stock price will go up or down tomorrow"

2. **Collect data** — Gather examples related to the problem.

3. **Clean data** — Fix missing values, errors, duplicates, bad formatting.

4. **Select features** — Choose what information the model should use.

5. **Train model** — Let the algorithm learn patterns.

6. **Evaluate** — Check performance on unseen data.

7. **Improve** — Refine data, features, model choice, and evaluation.

---

## Debugging ML Models

If model is bad, check:

- data quality
- feature quality
- train/test split
- overfitting

**NOT:** change model first

### Beginner Debugging Checklist

If performance is poor, ask:

- [ ] Is the target correct?
- [ ] Are there missing values?
- [ ] Are features meaningful?
- [ ] Is there leakage?
- [ ] Is the dataset too small?
- [ ] Is the model overfitting?
- [ ] Is the evaluation metric appropriate?

---

## Example Code

```python
import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([[1],[2],[3],[4]])
y = np.array([2,4,6,8])

model = LinearRegression()
model.fit(x,y)

print(model.predict([[5]]))
```

**What this code does:**

It learns: `y ≈ 2x`

**Beginner Walkthrough:**

- `x` contains input values
- `y` contains correct outputs
- `LinearRegression()` creates the model
- `fit(x, y)` learns the relationship
- `predict([[5]])` asks the model for a new prediction

Expected output is near: **10**

---

## Self Test

### Questions

1. What is Machine Learning?
2. What is a model?
3. What is supervised learning?
4. What is unsupervised learning?
5. What is the difference between regression and classification?
6. What are features?
7. What is the target?
8. Why do we split data into training and testing sets?
9. What is generalization?
10. What is overfitting?
11. What is underfitting?
12. What is bias?
13. What is variance?
14. What is a loss function?
15. Why does a model need a loss function?
16. What is MSE?
17. What is gradient descent?
18. What is the difference between batch gradient descent and SGD?
19. What is data leakage?
20. Why can high accuracy be misleading?
21. Why are features so important?
22. What does "garbage in, garbage out" mean in ML?
23. How does linear regression work?
24. How does logistic regression work?
25. How does a decision tree work?
26. How does random forest work?
27. How does K-Means work?
28. What is PCA used for?
29. What are common causes of overfitting?
30. What are common ways to reduce overfitting?

### Answers

1. Machine Learning is a way for computers to learn patterns from data so they can make predictions or decisions on new data.

2. A model is a mathematical function or system that maps input data to output predictions.

3. Supervised learning means training a model with input data and correct answers (labels).

4. Unsupervised learning means training a model on unlabeled data so it can discover hidden patterns or groups.

5. Regression predicts numbers, while classification predicts categories or labels.

6. Features are the input variables used by the model to make predictions.

7. The target is the output value the model is trying to predict.

8. To check whether the model can perform well on unseen data instead of only memorizing the training set.

9. Generalization is the ability of a model to perform well on new data it has never seen before.

10. Overfitting happens when a model memorizes training data too closely and performs poorly on new data.

11. Underfitting happens when a model is too simple and fails to learn important patterns in the data.

12. Bias is error caused by a model being too simple or making overly strong assumptions.

13. Variance is error caused by a model being too sensitive to the specific training data.

14. A loss function measures how wrong a model's predictions are.

15. Because the loss function tells the model how bad its predictions are and gives it a direction for improvement.

16. MSE, or Mean Squared Error, is a regression loss that averages squared differences between predictions and true values.

17. Gradient descent is an optimization method that updates model parameters to reduce loss step by step.

18. Batch gradient descent uses the whole dataset for each update. SGD updates using one sample or a very small batch at a time, which is faster but noisier.

19. Data leakage happens when the model accidentally uses information that would not be available in real-world prediction.

20. Because a model can achieve high accuracy on imbalanced data while still being useless for the minority class.

21. Because they determine what information the model has access to. Better features often lead to better predictions.

22. If the input data or features are poor quality, the model output will likely also be poor.

23. It finds the line or plane that best fits the data by minimizing prediction error.

24. It computes a score from inputs, converts it to a probability using a sigmoid function, and uses that probability for classification.

25. It splits data into smaller groups using decision rules, forming a tree structure that leads to predictions.

26. It builds many decision trees on slightly different data and combines their predictions.

27. It repeatedly assigns data points to the nearest cluster center and updates the centers until the clusters stabilize.

28. PCA is used to reduce the number of features while preserving as much important information as possible.

29. Too much model complexity, too little data, noisy data, too many weak features, and training too long.

30. Use more data, simplify the model, apply regularization, prune trees, use early stopping, and improve feature quality.

---

## Appendix — Stage 1 Project

### Project: Mini Predictor

**Goal:** Build a simple ML pipeline.

### Steps

**Step 1 — Get Data**

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

*Why This Step Matters: You need to understand what columns exist, whether there are missing values, the scale of values, and whether anything looks suspicious.*

**Step 3 — Define X and y**

```python
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]
```

*Why This Step Matters: You separate inputs (X) from output (y).*

**Step 4 — Split**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)
```

*Why This Step Matters: This simulates real-world prediction.*

**Step 5 — Train**

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

*Why This Step Matters: The model learns the relationship between features and target.*

**Step 6 — Predict**

```python
preds = model.predict(X_test)
```

*Why This Step Matters: Now the model tries to predict values it has not seen before.*

**Step 7 — Evaluate**

```python
from sklearn.metrics import mean_squared_error

print(mean_squared_error(y_test, preds))
```

*Why This Step Matters: This tells you how wrong the predictions are on unseen data.*

### Deliverables

- code
- dataset
- results
- README

### Experiment Tasks

**Experiment 1 — Train and test on the same data**

- Purpose: See how evaluation can become misleading.
- Expected result: Performance looks unrealistically good.
- Lesson: Testing on training data is cheating.

**Experiment 2 — Remove some features**

- Purpose: See how features affect model quality.
- Expected result: Performance may worsen or improve depending on the feature.
- Lesson: Features matter a lot.

**Experiment 3 — Change test size**

- Purpose: See how evaluation stability changes.
- Lesson: Different splits can change results.

**Experiment 4 — Try another model**

Try:

- Decision Tree Regressor
- Random Forest Regressor

Lesson: Different algorithms behave differently on the same problem.

### Common Mistakes

1. **Target leakage** — Using information that directly or indirectly reveals the answer. *Fix: Remove any feature that contains future or hidden answer information.*

2. **Testing on training data** — It feels easier, but gives fake confidence. *Fix: Always keep a separate test set.*

3. **Ignoring missing values** — Dirty data can silently hurt model quality. *Fix: Inspect and handle missing data before training.*

4. **Using meaningless features** — The model cannot learn useful patterns from useless inputs. *Fix: Think carefully about which features logically help prediction.*

5. **Believing one metric tells the whole story** — One score can hide many problems. *Fix: Use multiple metrics and inspect model behavior.*

---

## Final Understanding

You must be able to explain:

> "ML learns patterns from data and evaluates on unseen data."

### What You Must Be Able To Do After Stage 1

- [ ] Explain ML in plain English
- [ ] Explain the difference between supervised and unsupervised learning
- [ ] Explain regression vs classification
- [ ] Explain training vs testing
- [ ] Explain overfitting vs generalization
- [ ] Explain what a loss function is
- [ ] Explain how gradient descent improves a model
- [ ] Explain why features matter
- [ ] Build a simple ML pipeline
- [ ] Evaluate a simple model correctly
- [ ] Identify common beginner mistakes
