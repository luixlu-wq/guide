# Stage 2 — Python for AI

*(Week 3)*

## Goal

Learn the Python ecosystem used in AI.

You are **NOT** learning general Python.
You are learning **data + computation tools for AI**.

This stage is important because most AI work is not "just training models."
A large part of real AI work is:

- loading data
- cleaning data
- transforming data
- visualizing data
- building pipelines
- preparing data for machine learning

> A beginner should finish this stage understanding that:
> **AI starts with clean, structured, computable data — not models first.**

---

## Quick Summary

In AI engineering, Python is the main working language because it has strong libraries for:

- numerical computation
- data handling
- visualization
- machine learning

The four core libraries in this stage are:

| Library | Purpose |
|---|---|
| **NumPy** | arrays and fast numerical computation |
| **Pandas** | structured/tabular data handling |
| **Matplotlib** | charts and plots |
| **Scikit-learn** | preprocessing, models, and evaluation |

---

## Study Materials

**Python Data Science Handbook**
https://jakevdp.github.io/PythonDataScienceHandbook/

### Libraries to Learn

- NumPy
- Pandas
- Matplotlib
- Scikit-learn

---

## Key Knowledge (Deep Understanding)

### 1. NumPy — Numerical Computation

NumPy is used for:

- fast numerical operations
- vectorized computation

**Key idea:** Replace loops with vector operations

```python
import numpy as np

arr = np.array([1,2,3])
print(arr * 2)
```

#### Beginner Explanation

NumPy is the foundation for numerical work in Python.

A normal Python list can store values, but it is not optimized for fast math operations on large amounts of data.

```python
[1, 2, 3]   # Python list
```

A NumPy array looks similar, but it is designed for:

- fast computation
- efficient memory usage
- array-wide operations

```python
np.array([1, 2, 3])   # NumPy array
```

Instead of writing a loop, you can do:

```python
arr * 2
```

And NumPy multiplies every element for you.

#### Why NumPy Matters in AI

Most AI data eventually becomes numbers:

- images → pixel arrays
- text → token IDs or embeddings
- stock data → numerical columns
- audio → wave arrays

NumPy gives you the tools to handle this numerical data efficiently.

#### Step-by-Step Mental Model

1. **Store numbers in arrays** — Place numbers into a NumPy array.
2. **Perform operations on the whole array** — Instead of processing one item at a time, NumPy can process the whole array at once.
3. **Use vectorized math** — This is faster and cleaner than Python loops.

#### Key Concepts

**Array** — A grid of numbers.

- 1D array = vector
- 2D array = matrix
- 3D+ array = tensor-like structure

**Shape** — The dimensions of the array.

```python
arr.shape
# For a 2x3 matrix: (2, 3)
```

**Data Type (dtype)** — The type of numbers stored (int, float, bool).

*Why important: Different data types use different memory and can affect performance.*

#### Key Algorithms / Core Mechanisms for NumPy

**A. Vectorization**

Vectorization means operating on whole arrays at once instead of writing loops.

```python
arr = np.array([1, 2, 3])
arr + 5
# Output: [6, 7, 8]
```

*Why important: This is the foundation of efficient AI preprocessing and numerical computation.*

---

**B. Broadcasting**

Broadcasting lets NumPy apply operations between arrays of different shapes when the shapes are compatible.

```python
arr = np.array([1, 2, 3])
arr + 10
# The scalar 10 is automatically treated like [10, 10, 10]
```

*Why important: Lets you write less code and still do powerful array operations.*

---

**C. Matrix Operations**

Many ML formulas are based on vectors and matrices: dot product, matrix multiplication, transpose.

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5], [6]])
print(a @ b)
```

*Why important: Neural networks and many ML models are built on matrix math.*

#### Common Beginner Problems with NumPy

| Problem | Why It Happens | Fix |
|---|---|---|
| Confusing list and array | Both look similar at first | list = general container; NumPy array = optimized numeric structure |
| Not checking shape | Beginners focus on values, not dimensions | Always inspect `arr.shape` |
| Using loops unnecessarily | People come from basic programming habits | Try array operations first |

---

### 2. Pandas — Data Handling

Pandas is used for:

- tabular data
- CSV handling
- data cleaning

**Data structure:** DataFrame (table)

```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
```

#### Beginner Explanation

Pandas is the main tool for handling structured data in Python.

If NumPy is for arrays of numbers, Pandas is for tables like spreadsheets or SQL query results.

A Pandas DataFrame is like:

- an Excel sheet
- a database result table
- a structured CSV file in memory

Example:

| date | close | volume |
|---|---|---|
| 2025-01-01 | 100 | 10000 |
| 2025-01-02 | 102 | 12000 |

#### Why Pandas Matters in AI

Most beginner AI projects start with structured data: CSV files, stock market data, customer records, logs, tabular business data.

Before building a model, you usually need to:

- inspect the data
- clean missing values
- rename columns
- sort rows
- create new features
- filter useful subsets

Pandas is built for exactly this.

#### Step-by-Step Mental Model

1. **Load data** — Read CSV, Excel, JSON, or database output into a DataFrame.
2. **Inspect structure** — Check columns, data types, missing values, and sample rows.
3. **Clean the data** — Fix wrong formats, missing values, duplicates, and bad column names.
4. **Transform the data** — Create new columns and filter rows.
5. **Export or pass to model** — Use the cleaned result for plotting or ML.

#### Key Structures

- **Series** — A single column.
- **DataFrame** — A full table.
- **Index** — The row labels. *Pandas aligns data by index, not only by row position.*

#### Key Algorithms / Core Mechanisms for Pandas

**A. Filtering** — Keep only rows that match a condition.

```python
df[df["close"] > 100]
```

*How it works: Pandas creates a boolean mask and keeps rows where the condition is true.*

---

**B. GroupBy Aggregation** — Group rows and compute summaries.

```python
df.groupby("sector")["close"].mean()
```

How it works:

1. Split rows into groups
2. Apply an aggregation (mean, sum, count)
3. Combine results

---

**C. Merge / Join** — Combine tables.

*Example: Merge stock prices with company metadata.*

How it works: Match rows using common keys.

*Why important: Real AI datasets often come from multiple sources.*

---

**D. Rolling Window Computation** — Used for time series features.

```python
df["ma5"] = df["close"].rolling(5).mean()
```

*How it works: Take a moving window of rows and compute a statistic.*

*Why important: Very useful for finance, sensor data, logs, and sequential data.*

#### Common Beginner Problems with Pandas

| Problem | Why It Happens | Fix |
|---|---|---|
| Forgetting column data types | CSV reading may infer unexpected types | Always inspect `df.info()` |
| Misunderstanding index behavior | Beginners assume rows are always simple numbered lists | Use `df.reset_index()` when needed |
| Editing a copy instead of expected data | Pandas slicing can be tricky | Use clear assignment patterns and verify results |

---

### 3. Matplotlib — Visualization

Used for:

- plotting trends
- understanding data

```python
import matplotlib.pyplot as plt

df["Close"].plot()
plt.show()
```

#### Beginner Explanation

Matplotlib is used to create plots and charts.

Before using a model, you should try to **see** the data.

Visualization helps you detect:

- trends
- outliers
- missing periods
- unusual spikes
- bad preprocessing

#### Why Visualization Matters in AI

> A model can hide problems. A plot can reveal them immediately.

*Example: If stock dates are unsorted, a line chart may look messy or broken. That visual clue tells you something is wrong.*

#### Step-by-Step Mental Model

1. **Choose what you want to understand** — trend over time, relationship between columns, distribution of values.
2. **Pick a plot type** — line chart, histogram, scatter plot, bar chart.
3. **Plot and inspect** — Use the plot to understand the data before modeling.

#### Key Chart Types

| Chart | Best For | How It Works |
|---|---|---|
| **Line Plot** | Trends over time | Connect data points with lines in order |
| **Histogram** | Distributions | Split values into bins and count occurrences |
| **Scatter Plot** | Relationships between two variables | Each point represents one row |
| **Box Plot** | Outliers and spread | Shows median, quartiles, and extreme values |

#### Common Beginner Problems with Visualization

| Problem | Why It Happens | Fix |
|---|---|---|
| Plotting before cleaning | People are eager to see charts immediately | Clean dates, missing values, and sorting first |
| Choosing the wrong chart | Using one chart type for everything | trend → line; distribution → histogram; relationship → scatter |
| Reading the chart too quickly | A pretty chart can create false confidence | Ask: Is data sorted? Are there missing values? Are scales misleading? |

---

### 4. Scikit-learn — ML Toolkit

Used for:

- models
- preprocessing
- evaluation

#### Beginner Explanation

Scikit-learn is the main beginner-friendly machine learning library in Python.

It gives you ready-made tools for:

- splitting data
- scaling features
- encoding labels
- training models
- evaluating performance

#### Step-by-Step Mental Model

1. **Prepare data** — Clean data, choose features, define target.
2. **Split data** — Use train/test split.
3. **Preprocess** — Scale numeric data or encode categories if needed.
4. **Train model** — Use `.fit()`.
5. **Predict** — Use `.predict()`.
6. **Evaluate** — Use metrics like accuracy or MSE.

#### Key Tools in Scikit-learn

**A. Train/Test Split** — Separate training and testing data.

*How it works: Randomly divides the dataset into two parts.*

---

**B. StandardScaler** — Scale numeric features.

Transforms each feature to have roughly:

- mean = 0
- standard deviation = 1

*Why important: Some algorithms work better when features are scaled.*

---

**C. Label Encoding / One-Hot Encoding** — Convert categories into numbers.

*Why important: Most models need numerical input.*

---

**D–G. Algorithms**

| Algorithm | Type | Description |
|---|---|---|
| Linear Regression | Regression | Fits a line/hyperplane to minimize squared error |
| Logistic Regression | Classification | Predicts class probability and label |
| Decision Tree | Both | Learns rule-based splits |
| Random Forest | Both | Combines many trees |

---

**H. Metrics**

| Task | Metrics |
|---|---|
| Regression | MSE, MAE, R² |
| Classification | accuracy, precision, recall, F1 |

#### Common Beginner Problems with Scikit-learn

| Problem | Why It Happens | Fix |
|---|---|---|
| Using the wrong metric | Using whatever metric you see first | Choose metric based on problem type |
| Fitting preprocessing on all data | Preprocessing before the split | Fit preprocessing on training data only, then apply to test |
| Using model API mechanically | Easy to memorize `.fit()` without understanding | Always know what input, target, and metric mean |

---

## Difficulty Points

### 1. Confusing DataFrame vs array

- NumPy → numbers only
- Pandas → structured data

**Why it matters:** Using the wrong structure makes operations harder.

**Fix:** NumPy for numerical arrays and math; Pandas for tables and cleaning.

### 2. Not understanding vectorization

Loops are slow. Use:

```python
df["a"] + df["b"]
```

Instead of loops.

**Fix:** Whenever you want to process a whole column, first ask: *"Can this be done as a column operation?"*

### 3. Ignoring missing values

Most real data has missing values. They can break calculations, plots, and models.

**Fix:** Always check:

```python
df.isna().sum()
```

Then choose: drop rows, fill values, or investigate source quality.

### 4. Misusing indexes

Pandas aligns by index labels, which can create unexpected behavior.

**Fix:** Inspect indexes and reset when needed:

```python
df = df.reset_index()
```

### 5. Cleaning too late

Dirty data causes confusing downstream errors.

**Fix:** Adopt this order: load → inspect → clean → transform → analyze/model.

### 6. Treating plots as decoration

Charts are not just for presentation. They are debugging tools for data quality and patterns.

**Fix:** Use plots to answer a question, not just to "make a graph."

### 7. Copying code without understanding shape and columns

Your data may have different columns, types, or missing values than the example.

**Fix:** Always inspect before modifying code:

```python
df.head()
df.info()
df.columns
df.shape
```

---

## Python for AI Workflow (Real World)

1. Load data
2. Inspect data
3. Clean data
4. Transform data
5. Create features
6. Visualize data
7. Prepare ML-ready inputs
8. Train/evaluate model
9. Save outputs and findings

### Beginner Explanation of Each Step

1. **Load data** — Read CSV, API data, JSON, or downloaded files.
2. **Inspect data** — Look at sample rows and data types.
3. **Clean data** — Fix missing values, duplicated rows, bad column names, wrong types.
4. **Transform data** — Reformat columns, convert dates, sort rows.
5. **Create features** — Add useful derived columns like returns or moving averages.
6. **Visualize data** — Use plots to understand what is happening.
7. **Prepare ML-ready inputs** — Separate features and target if modeling is needed.
8. **Train/evaluate model** — Only after data is ready.
9. **Save outputs and findings** — Store processed data, plots, and notes.

---

## Debugging Checklist for Stage 2

If something goes wrong, check:

- [ ] Did the file load correctly?
- [ ] Are the column names what you expect?
- [ ] Are dates really datetime objects?
- [ ] Is the data sorted correctly?
- [ ] Are there missing values?
- [ ] Are you using the right structure: DataFrame or array?
- [ ] Are plot axes using the correct columns?
- [ ] Did you create NaN values during rolling calculations?
- [ ] Are shapes compatible for NumPy operations?
- [ ] Did preprocessing accidentally include test data?

---

## Practice Project

### Project: Stock Analysis Script

**Goal:** Learn data download, preprocessing, feature creation, and visualization.

> Also learn a real beginner AI engineering lesson:
> **Before you train a model, you must be able to trust your data pipeline.**

**Step 1 — Download data**

```python
import yfinance as yf

df = yf.download("AAPL", period="1y")
df.to_csv("data/raw/aapl.csv")
```

*Why this step matters: You need a real dataset to practice loading, cleaning, and feature engineering. Downloaded market data often looks clean, but you should still inspect it carefully.*

---

**Step 2 — Inspect**

```python
print(df.head())
print(df.info())
print(df.shape)
print(df.isna().sum())
print(df.columns)
```

*Why this step matters: You need to confirm what columns exist, whether the index is the date, whether there are missing values, and whether data types make sense.*

---

**Step 3 — Clean data**

```python
df = df.reset_index()
df.columns = [c.lower() for c in df.columns]
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
```

*Why this step matters: This makes the data easier to work with consistently.*

Step-by-step explanation:

- `reset_index()` turns the date index into a regular column
- lowercase column names reduce naming mistakes
- `to_datetime()` ensures date operations work correctly
- sorting by date ensures time-series logic is correct

---

**Step 4 — Add indicators**

```python
df["return"] = df["close"].pct_change()
df["ma5"] = df["close"].rolling(5).mean()
df["ma20"] = df["close"].rolling(20).mean()
```

*Why this step matters: Raw price alone is often less useful than derived features.*

Step-by-step explanation:

- `pct_change()` computes daily percentage return
- `rolling(5).mean()` computes 5-day moving average
- `rolling(20).mean()` computes 20-day moving average

These are examples of **feature engineering**.

---

**Step 5 — Handle missing values**

```python
df = df.dropna()
```

*Why this step matters: Rolling calculations create missing values at the beginning because there is not enough prior data yet. For a 20-day moving average, the first 19 rows cannot have a value — that is expected.*

---

**Step 6 — Plot**

```python
import matplotlib.pyplot as plt

df.plot(x="date", y=["close","ma5","ma20"])
plt.show()
```

*Why this step matters: Plotting helps verify that dates are sorted, features were created correctly, and trends make sense visually.*

### Deliverables

- raw data
- processed data
- plots
- script

### Experiment Tasks

**Experiment 1 — Do not sort dates**

- Purpose: See how important time ordering is.
- Expected result: Plots and time-based features may become misleading.
- Lesson: Time-series data must be sorted correctly.

**Experiment 2 — Keep NaN values and try plotting/modeling**

- Purpose: See how missing values affect downstream work.
- Lesson: Missing values must be handled intentionally.

**Experiment 3 — Compute indicators with loops and with vectorized operations**

- Purpose: Compare style and performance.
- Lesson: Vectorized operations are cleaner and usually faster.

**Experiment 4 — Add more features**

Try: `high - low`, `close - open`, 10-day moving average, volume change.

- Lesson: Feature engineering changes what the data can express.

**Experiment 5 — Plot histogram of returns**

```python
df["return"].hist()
plt.show()
```

- Lesson: Not all insights come from line charts; distributions matter too.

### Common Mistakes

1. **Unsorted dates** — Rolling features and line plots can become incorrect or misleading. *Fix: `df = df.sort_values("date")`*

2. **Ignoring NaN** — Calculations, plots, and ML models may fail or silently behave badly. *Fix: `df.isna().sum()` then `df = df.dropna()` or use filling strategies.*

3. **Using loops instead of vector ops** — Code becomes slower, longer, and harder to read. *Fix: Use Pandas/NumPy column operations when possible.*

4. **Forgetting imports after moving code blocks** — Code fails in confusing ways. *Fix: Keep scripts runnable top to bottom; rerun from a clean kernel sometimes.*

5. **Assuming downloaded data is already perfect** — Even official data can have gaps, bad types, or unexpected format changes. *Fix: Always inspect before trusting.*

---

## Final Understanding

> AI starts with clean, structured data — not models.

---

## Self Test

### Questions

1. What is NumPy mainly used for?
2. Why are NumPy arrays better than plain Python lists for numerical work?
3. What is vectorization?
4. What is broadcasting in NumPy?
5. What is a DataFrame?
6. What is the difference between a Pandas DataFrame and a NumPy array?
7. Why is `df.info()` important?
8. Why do indexes matter in Pandas?
9. Why should you check for missing values?
10. What does `df.isna().sum()` tell you?
11. Why do rolling calculations often create NaN values?
12. What is feature engineering?
13. Why is sorting by date important in time-series data?
14. What is a moving average?
15. Why do we visualize data before modeling?
16. When should you use a line plot?
17. When should you use a histogram?
18. When should you use a scatter plot?
19. What is Scikit-learn mainly used for?
20. What does train/test split do?
21. Why can preprocessing before the split be dangerous?
22. What does StandardScaler do?
23. Why is one-hot encoding needed?
24. What is the difference between `.fit()` and `.predict()`?
25. Why is using loops for column operations often a bad idea?
26. What is the recommended workflow order for Python-for-AI data work?
27. Why should plots be treated as debugging tools?
28. What is the first thing you should check if a script fails on a CSV?
29. Why should you inspect `df.columns`?
30. What does this stage try to teach beyond syntax?

### Answers

1. NumPy is mainly used for fast numerical computation with arrays.

2. Because they are optimized for efficient math operations, use memory more efficiently, and support vectorized computation.

3. Vectorization means applying operations to whole arrays or columns at once instead of looping through items one by one.

4. Broadcasting is NumPy's way of allowing operations between arrays of different but compatible shapes.

5. A DataFrame is a table-like data structure in Pandas with rows and columns.

6. A DataFrame is designed for labeled, structured tabular data. A NumPy array is designed for fast numerical computation.

7. It shows column names, data types, non-null counts, and helps identify data issues early.

8. Because Pandas aligns operations by index labels, which can affect filtering, merging, and assignments.

9. Because missing values can break calculations, distort plots, and cause ML pipelines to fail or behave badly.

10. It tells you how many missing values exist in each column.

11. Because the first few rows do not have enough earlier values to compute the rolling statistic.

12. Feature engineering is creating new useful input columns from existing data.

13. Because time-based calculations and plots depend on correct chronological order.

14. A moving average is the average of a value over a recent sliding window, such as the last 5 or 20 days.

15. Because visualization helps reveal trends, anomalies, missing values, and preprocessing mistakes.

16. Use a line plot to show trends over time or ordered sequences.

17. Use a histogram to understand the distribution of one numerical variable.

18. Use a scatter plot to examine the relationship between two numerical variables.

19. Scikit-learn is used for preprocessing, model training, prediction, and evaluation in machine learning workflows.

20. It separates data into training data for learning and test data for evaluation on unseen examples.

21. Because it can leak information from the test set into the training process, making evaluation unrealistically optimistic.

22. It scales numeric features so they have roughly mean 0 and standard deviation 1.

23. Because most ML models require numeric input, so categorical values must be converted to numeric form.

24. `.fit()` trains the model on data. `.predict()` uses the trained model to produce outputs for new inputs.

25. Because loops are usually slower, longer, and less idiomatic than vectorized Pandas or NumPy operations.

26. Load, inspect, clean, transform, create features, visualize, prepare ML-ready data, then train/evaluate if needed.

27. Because they can reveal data quality problems and pattern issues that code output alone may hide.

28. Check whether the file loaded correctly and whether the column names and data types match your assumptions.

29. Because your code may fail if the actual column names differ from what you expect.

30. It teaches data thinking: how to inspect, trust, clean, transform, and prepare data for real AI workflows.

---

## What You Must Be Able To Do After Stage 2

- [ ] Explain what NumPy is for
- [ ] Explain what Pandas is for
- [ ] Explain why vectorization matters
- [ ] Load and inspect a dataset
- [ ] Clean missing values and fix basic data issues
- [ ] Create new features from raw columns
- [ ] Visualize data for understanding and debugging
- [ ] Explain why time-series data must be sorted
- [ ] Use Scikit-learn tools in a simple workflow
- [ ] Understand that reliable AI work begins with reliable data pipelines
