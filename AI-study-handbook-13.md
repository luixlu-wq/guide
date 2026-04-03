# Stage 13 — Capstone Project

## AI Trading Assistant (End-to-End)

---

## Goal

Build a production-style AI Trading Assistant that integrates:

- Market data ingestion
- Feature engineering
- ML prediction
- News analysis (RAG-ready)
- LLM reasoning
- API serving

This is your capstone integration project.

This stage is where everything you learned becomes one complete system.

You are combining:

- data pipelines
- feature engineering
- classical ML
- optional retrieval-ready text processing
- LLM explanation
- API design
- modular system thinking
- evaluation across layers

---

## Quick Summary

This project is not about building "just a model."

It is about building a full AI pipeline where each component has a clear responsibility.

The assistant should:

- ingest market data
- compute structured signals
- generate ML predictions
- incorporate text/news context
- use an LLM to explain results
- return a clean API response

A beginner should finish this stage understanding:

- how to turn many AI parts into one system
- how to keep component responsibilities clear
- how to debug a multi-layer pipeline
- why evaluation must happen at more than one level
- how to build an MVP before overengineering
- how to think like an AI product engineer, not only a model trainer

---

## High-Level Architecture

```
Market Data
↓
Feature Engineering
↓
ML Prediction
↓
News Analysis
↓
LLM Reasoning
↓
Trade Recommendation
```

---

## System Design (Detailed)

### 1. Market Data Layer

**Responsibilities:**

- fetch historical prices
- normalize schema
- store raw + processed data

**Example:**

```python
import yfinance as yf
df = yf.download("NVDA", period="2y")
```

**Output:** clean OHLCV dataframe

#### Beginner Explanation

This is the first layer of the whole system.

Its job is simple: get reliable raw market data into a usable format.

This layer should not try to: make predictions, write explanations, or make trade recommendations.

Its job is only to provide trustworthy input data.

> If this layer is weak, every downstream layer becomes weak.

#### What OHLCV Means

| Column | Meaning |
|---|---|
| Open | opening price |
| High | highest price |
| Low | lowest price |
| Close | closing price |
| Volume | traded volume |

These are the raw ingredients for feature engineering.

#### Step-by-Step Mental Model

| Step | What Happens |
|---|---|
| Step 1 — User provides a symbol | NVDA, MSFT, AAPL |
| Step 2 — System fetches historical data | Using yfinance or another market source. |
| Step 3 — Data is inspected | Check: missing values, column names, date order, weird gaps or formatting issues |
| Step 4 — Data is normalized | Make schema consistent so later layers always receive the same format. |
| Step 5 — Data is stored | Keep raw copy and cleaned copy for debugging and reproducibility. |

#### Important Algorithms / Mechanisms

**A. Time-Series Ingestion**

The system retrieves sequential market data ordered by time.

How it works: fetch rows with date-indexed price data, preserve chronology, keep fields aligned by date.

> Why important: Trading systems depend on correct time order.

**B. Schema Normalization**

Convert incoming data into a stable internal format.

How it works: standardize column names, date format, and missing-value handling.

> Why important: Downstream modules should not guess data format.

**C. Data Validation**

Check whether data is usable before continuing.

How it works: verify required columns exist, verify enough rows exist, verify dates are sorted, verify there are not too many missing values.

> Why important: Bad input data silently ruins later predictions.

**Good Engineering Practice:**

```python
print(df.head())
print(df.info())
print(df.isna().sum())
print(df.shape)
print(df.tail())
```

---

### 2. Feature Engineering Layer

**Create Features:**

```python
df["return"] = df["Close"].pct_change()
df["ma20"] = df["Close"].rolling(20).mean()
df["ma50"] = df["Close"].rolling(50).mean()
df["volatility"] = df["Close"].rolling(20).std()
```

**Target:**

```python
df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
```

> **Key Learning:** feature quality > model complexity

#### Beginner Explanation

This is the layer where raw price data becomes useful learning signals.

A model usually does not learn well from raw prices alone. So you create features that express patterns more clearly:

- daily return
- short moving average
- long moving average
- rolling volatility

#### Why Feature Engineering Matters So Much

A beginner often thinks: *"I need a better model."*

But often the real answer is: *"I need better features."*

> Weak features create weak predictions, no matter how advanced the model is.

#### Step-by-Step Mental Model

| Step | What Happens |
|---|---|
| Step 1 — Start from OHLCV data | Use close, volume, and time-ordered rows. |
| Step 2 — Create derived signals | return, MA20, MA50, volatility |
| Step 3 — Create target variable | `(Close.shift(-1) > Close).astype(int)` → 1 if tomorrow closes higher, 0 otherwise |
| Step 4 — Remove invalid rows | Rolling windows create NaNs at start; shifting target creates NaNs at end. |
| Step 5 — Freeze feature definitions | The model layer should receive a clean, consistent feature table. |

#### Important Algorithms / Mechanisms

**A. Percentage Change**

Used for returns.

How it works: Measures relative change from one row to the next.

> Why important: Returns are often more meaningful than raw price level.

**B. Rolling Window Computation**

Used for moving averages and volatility.

How it works: A sliding window computes a statistic over the last N rows (rolling mean, rolling std).

> Why important: This is the basis of many technical features.

**C. Target Shifting**

Used to align future outcome with current-day features.

How it works: `shift(-1)` moves tomorrow's close into the current row's target comparison.

> Why important: This is how you frame a prediction problem correctly.

**D. Leakage Prevention**

Make sure features do not accidentally include future information.

> Why important: Target leakage creates fake performance.

**Suggested Additional Features (after MVP works):**

- RSI
- MACD-like signals
- rolling volume average
- price minus moving average
- volume percentage change
- rolling max/min breakout features

---

### 3. ML Prediction Layer

**Example Model:**

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
```

**Output:** probability of price going up

#### Beginner Explanation

This layer is responsible for structured predictive signal. It answers:

- what is the probability price goes up tomorrow?
- is the model leaning bullish or bearish?
- how confident is the prediction?

This is not the layer for long natural-language reasoning. That belongs later.

#### Why Start with Logistic Regression

Because it is: simple, fast, interpretable, easy to debug, and good enough for a baseline.

> In a capstone, a clean working baseline is better than a fancy model you cannot trust.

#### Step-by-Step Mental Model

| Step | What Happens |
|---|---|
| Step 1 — Prepare features X | return, ma20, ma50, volatility |
| Step 2 — Prepare target y | The future up/down label. |
| Step 3 — Split train/test | Prevent evaluation cheating. |
| Step 4 — Train model | Fit logistic regression on training data. |
| Step 5 — Predict probabilities | Not just classes — probabilities are useful for downstream reasoning. |
| Step 6 — Evaluate | Check whether signal is meaningful on unseen data. |

#### Important Algorithms / Mechanisms

**A. Logistic Regression**

A binary classification model.

How it works: Estimates the probability that the target belongs to class 1.

> Why important: Excellent baseline for up/down prediction framing.

**B. Train/Test Split**

Separates training data from evaluation data.

> Why important: Without this, model evaluation is misleading.

**C. Probability Estimation**

Model returns probability, not only label.

> Why important: Probability is more useful for downstream reasoning than a raw yes/no label alone.

**D. Thresholding**

Convert probability into class labels if needed.

Example: above 0.5 → up, below 0.5 → down.

> Why important: Useful for simple decision logic.

**Recommended Evaluation for This Layer:**

- training score
- test score
- confusion matrix
- precision / recall
- probability distribution sanity

---

### 4. News Analysis Layer

**Data Sources:** news API, manual dataset, scraped headlines.

**Simplified Version — Store news as text list:**

```python
news = ["NVDA gains due to AI demand", "Chip shortage easing"]
```

#### Beginner Explanation

Price signals are important, but markets are not driven only by numerical history.

News and text context can change interpretation.

For the MVP, keep this layer simple. You can start with:

- manual news text
- a list of headlines
- a small text file
- pasted summaries

This keeps the capstone manageable.

#### What This Layer Should Do

This layer should: collect relevant text, normalize it, possibly summarize it, and pass it forward clearly.

It should **not** make the final recommendation alone.

#### Step-by-Step Mental Model

| Step | What Happens |
|---|---|
| Step 1 — Gather news text | Maybe 2–5 recent headlines or one summary paragraph. |
| Step 2 — Clean text | Remove empty items and obvious formatting junk. |
| Step 3 — Optionally summarize | If the input is too long, compress it. |
| Step 4 — Pass concise news context to LLM layer | This makes the reasoning layer richer without overloading it. |

#### Important Algorithms / Mechanisms

**A. Text Aggregation**

Combine several headlines or notes into one usable context block.

> Why important: The LLM layer needs compact, readable context.

**B. Summarization**

Compress longer text into key points.

> Why important: Reduces prompt size and focuses reasoning.

**C. Sentiment Extraction**

Estimate positive / negative / neutral tone.

> Why important: Can become another structured input for the recommendation layer.

**D. Entity / Topic Extraction**

Identify company names, products, risks, or events.

> Why important: Makes text context more structured and easier to reason about.

#### "RAG-Ready" Meaning

The first MVP can use manual text. Later, you can upgrade it to real retrieval over stored news or research notes.

> This is excellent architecture thinking.

---

### 5. LLM Reasoning Layer

**Prompt Design:**

```
Given:
- indicators: {features}
- prediction: {probability}
- news: {news}

Return:
- summary
- bullish factors
- bearish factors
- recommendation
- confidence
```

#### Beginner Explanation

This is the layer that turns structured signals into human-readable reasoning.

This layer should not invent its own unsupported facts.

Its job is to: explain, organize, compare bullish vs bearish evidence, communicate uncertainty, and produce a useful recommendation format.

Think of this layer as the **analyst narrator**, not the raw predictor.

#### Why This Layer Is Valuable

Without it, you only have: numbers, model probabilities, raw indicators.

That is useful for machines, but not as usable for people. The LLM helps convert the pipeline into something understandable.

#### Better Prompt Design

```
Given:
- technical indicators: {features}
- ML prediction probability: {probability}
- recent news context: {news}

Return:
1. short summary
2. bullish factors
3. bearish factors
4. recommendation
5. confidence

Rules:
- use only the provided inputs
- do not invent facts
- do not overstate certainty
- if signals conflict, say so clearly
```

#### Step-by-Step Mental Model

| Step | What Happens |
|---|---|
| Step 1 — Receive structured inputs | feature values, model probability, news context |
| Step 2 — Organize evidence | Prompt tells model what categories to think in: bullish, bearish, summary, recommendation |
| Step 3 — Generate explanation | The LLM translates structured signal into human language. |
| Step 4 — Constrain output | The system should enforce predictable fields or JSON format. |

#### Important Algorithms / Mechanisms

**A. Structured Prompting**

The prompt specifies exact output sections.

> Why important: Improves consistency and evaluability.

**B. Grounded Prompting**

The model is told to rely only on supplied indicators and news.

> Why important: Reduces hallucination and overclaiming.

**C. Controlled Generation**

Constraints such as cautious tone and uncertainty language are specified.

> Why important: Keeps LLM aligned with product goals.

**D. Schema-Constrained Output**

Force output into fixed JSON or field-based structure.

> Why important: Makes downstream use reliable.

> **Important Warning:** This layer must not override the ML signal blindly. If the ML probability is weak or mixed, the LLM should say that. Otherwise the system becomes persuasive but unreliable.

---

### 6. Output Format

**Basic output:**

```json
{
  "summary": "...",
  "bullish": [],
  "bearish": [],
  "recommendation": "BUY / HOLD / SELL",
  "confidence": 0.0
}
```

#### Beginner Explanation

A real system should not return random unstructured text.

It should return a clean response shape. That makes it easier to: display in UI, validate, test, log, compare outputs, and call from other systems.

#### Better Expanded Output Shape

```json
{
  "symbol": "NVDA",
  "prediction_probability_up": 0.71,
  "summary": "Technical signals suggest bullish momentum, but news risk remains.",
  "bullish": ["MA20 above MA50", "rising volume"],
  "bearish": ["valuation concerns in news"],
  "recommendation": "HOLD",
  "confidence": 0.64
}
```

#### Important Algorithms / Mechanisms

**A. Schema-Based Response Design**

Fixed response fields are required.

> Why important: This creates predictable system behavior.

**B. Post-Generation Validation**

Check required keys and value types after generation.

> Why important: LLM output may look right but still be malformed.

**C. Confidence Propagation**

Pass model confidence into the final response.

> Why important: Users should see uncertainty, not only a recommendation word.

> **Suggested Rule:** Do not let "BUY / HOLD / SELL" appear without an evidence summary, risk section, and confidence context. That makes the output more responsible.

---

### 7. API Layer

**FastAPI Example:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/analyze")
def analyze(symbol: str):
    return {"result": "analysis"}
```

#### Beginner Explanation

This is the layer that makes the project usable as a product.

The API should: accept input, validate it, run the full pipeline, return structured output, and handle errors cleanly.

Without this layer, the system is still mostly a script or notebook.

#### Suggested API Responsibilities

| Section | Fields |
|---|---|
| Input | symbol, optional news text, optional date range |
| Output | analysis JSON, error info if request fails |
| Behavior | validate symbol, run pipeline, return structured result, log request and latency |

#### Important Algorithms / Mechanisms

**A. Request Validation**

Check whether input fields are present and well formed.

> Why important: Bad input should fail early and clearly.

**B. Orchestration**

The API calls the layers in the correct order.

> Why important: The API is the boundary where the full system becomes one product flow.

**C. Response Serialization**

Convert final result into JSON.

> Why important: Clients need predictable outputs.

**D. Error Handling**

Handle: invalid symbol, missing data, model failure, LLM failure.

> Why important: A reliable capstone must handle failure paths, not only success cases.

---

## Step-by-Step Implementation

**Step 1 — Setup project structure**

Basic structure:

```
project/
├── data/
├── features/
├── models/
├── llm/
├── api/
├── notebooks/
```

Improved suggested structure:

```
project/
├── data/
│   ├── raw/
│   └── processed/
├── features/
├── models/
├── llm/
├── api/
├── logs/
├── notebooks/
├── tests/
└── README.md
```

> Why this step matters: A clear repo structure helps you debug faster, avoid mixing responsibilities, keep artifacts organized, and make the capstone easier to explain and demo.

---

**Step 2 — Build each module independently**

Build: data loader, feature generator, ML model, LLM prompt.

> Why this step matters: This prevents integration chaos. Each layer should work alone first — fetch data correctly, compute features correctly, train/infer correctly, prompt/format correctly. Then connect them.

---

**Step 3 — Unit test each layer**

Test: feature correctness, model prediction shape, LLM output format.

> Why this step matters: If each module is not checked independently, integration debugging becomes much harder.

**Better Beginner Test Ideas:**

| Layer | Tests |
|---|---|
| Data Layer | does symbol load? are required columns present? |
| Feature Layer | do moving averages exist? are NaNs handled? |
| ML Layer | does model return probability array of expected shape? |
| LLM Layer | does output contain required fields? |
| API Layer | does endpoint return valid JSON? |

---

**Step 4 — Integrate pipeline**

```
symbol → data → features → model → LLM → output
```

> Why this step matters: This is where isolated parts become one real system. Most beginner integration bugs appear here: wrong column names, bad data handoff, missing fields, invalid prompt formatting, malformed JSON. Integration should be gradual and logged.

---

**Step 5 — Add logging**

Log: inputs, predictions, outputs.

> Why this step matters: Without logs, pipeline failures are very hard to localize.

Better logging — log at minimum:

- request symbol
- data row count
- feature snapshot
- prediction probability
- prompt version
- final response
- error message if any
- latency by stage if possible

---

**Step 6 — Add simple evaluation**

Track: prediction accuracy, consistency of LLM output, runtime.

> Why this step matters: A capstone without evaluation is only a demo.

**Better Evaluation Breakdown:**

| Layer | Evaluate |
|---|---|
| ML layer | accuracy, precision / recall, confusion matrix |
| LLM layer | output schema validity, whether response follows prompt rules, whether explanation matches signals |
| System layer | end-to-end runtime, failure rate, response completeness |

---

## Difficulty Points

### 1. Integration failure

**Why this happens:** Module boundaries are often underspecified. Each component tested alone but schemas mismatch, assumptions differ, outputs are missing fields, timing/order breaks.

**Why this is a problem:** A system that "almost works" in pieces can still fail as a product.

**Fix:** Define interfaces clearly, log intermediate outputs, test handoff between layers.

---

### 2. Feature/model mismatch

**Why this happens:** Features may be incorrectly computed, missing, misaligned, or inconsistent with training.

**Why this is a problem:** The model may still run but produce garbage.

**Fix:** Freeze feature definitions, validate training vs inference columns, inspect feature snapshots manually.

---

### 3. Prompt quality

**Why this happens:** Vague prompts produce vague analysis.

**Why this is a problem:** The final system looks weak even if the upstream signal is useful.

**Fix:** Use structured prompt, enforce grounding, specify fields clearly, tell the model how to express uncertainty.

---

### 4. Overengineering

**Why this happens:** The capstone feels like the place to add everything — agents, RAG, many models, auto-trading logic, complex orchestration.

**Why this is a problem:** You may never finish a stable version.

**Fix:** Build the MVP first: `market data → features → logistic regression → manual news text → LLM explanation → FastAPI`. Only then add complexity.

---

### 5. No validation

**Why this happens:** People trust intermediate outputs too quickly.

**Why this is a problem:** Errors silently compound.

**Fix:** Validate: data schema, feature columns, model output shape, LLM JSON structure, API response schema.

---

### 6. Letting the LLM overclaim

**Why this happens:** LLMs sound more certain than the signal deserves.

**Why this is a problem:** Users may overtrust the final recommendation.

**Fix:** Prompt the LLM to reflect uncertainty, cite input factors, avoid unsupported certainty, describe conflicting signals clearly.

---

### 7. No end-to-end test cases

**Why this happens:** Developers test modules separately and stop there.

**Why this is a problem:** The product boundary remains untested.

**Fix:** Create realistic full-pipeline test cases:

- clean bullish example
- mixed/conflicting example
- missing-news example
- bad symbol example

---

## Deliverables

Basic deliverables:

- full project repo
- working API
- sample outputs
- README with architecture explanation

**Expanded Deliverables Recommendation:**

A strong capstone submission should include:

- project repo
- README.md
- module structure
- sample input/output JSON
- evaluation notes
- screenshots or logs of working API
- test cases
- short architecture diagram

---

## Evaluation Criteria

| Criterion | Weight | Interpretation |
|---|---|---|
| Correctness of pipeline | 30% | Does the full request flow actually work? |
| Modular design | 25% | Are responsibilities clearly separated? |
| Reasoning quality | 20% | Does the final explanation match the signals and stay grounded? |
| Code quality | 15% | Is code organized, readable, and testable? |
| Documentation | 10% | Can another developer understand the system? |

---

## Final Understanding

> "An AI system is a pipeline where each component contributes to the final decision, and reliability depends on every layer."

> A capstone is not judged only by whether it "runs once." It is judged by whether the system is modular, explainable, testable, and understandable.

---

## Next Step

You are now ready for: **Stage 14 — Hedge-Fund Style AI Trading System**

---

## Capstone Workflow (Real World)

| Step | Action | Beginner Explanation |
|---|---|---|
| 1 | Define the MVP scope | Keep it small and complete. |
| 2 | Define layer responsibilities | Each layer should have one main job. |
| 3 | Build raw data ingestion | Start from trustworthy input. |
| 4 | Build feature layer | Create useful structured signals. |
| 5 | Build baseline ML layer | Start with a simple model that works. |
| 6 | Build text/news layer | Keep text context manageable. |
| 7 | Build LLM reasoning layer | Use the LLM for explanation, not raw prediction. |
| 8 | Define output schema | Make the system parseable and testable. |
| 9 | Build API | Make the system callable. |
| 10 | Add logging | Make failures visible. |
| 11 | Add evaluation | Measure instead of guessing. |
| 12 | Test end-to-end | Validate the real product path. |
| 13 | Improve weakest layer first | Do not optimize randomly. |

---

## Debugging Checklist for Stage 13

If the capstone behaves badly, check:

- [ ] Is the market data valid and complete?
- [ ] Are features computed correctly?
- [ ] Is target leakage present?
- [ ] Does the model output probability in expected shape?
- [ ] Is the news layer passing useful text?
- [ ] Is the LLM prompt grounded and structured?
- [ ] Is the LLM staying faithful to provided signals?
- [ ] Is the JSON output valid?
- [ ] Are intermediate outputs logged?
- [ ] Is the API returning stable schema?
- [ ] Is the system too complex for the current MVP?
- [ ] Are you improving the real weak layer, or just changing random parts?

---

## Experiment Tasks

| Experiment | Purpose |
|---|---|
| 1 — ML only vs ML + LLM | See how explanation improves usability, not necessarily prediction quality. |
| 2 — Add one new feature | See whether better features improve signal quality more than changing the model. |
| 3 — Weak prompt vs strong prompt | See how prompt structure affects final analysis quality. |
| 4 — Manual news vs no news | See how text context changes recommendation framing. |
| 5 — Schema validation | Make sure final output is reliably parseable. |
| 6 — Bad symbol / bad input handling | Test failure behavior. |
| 7 — End-to-end logging | Learn to debug integrated systems transparently. |

---

## Self Test

### Questions

1. What is the main goal of this capstone project?
2. Why is this project called an end-to-end system?
3. What is the responsibility of the market data layer?
4. What does OHLCV mean?
5. Why do we normalize and validate raw data before using it?
6. What is the responsibility of the feature engineering layer?
7. Why is feature quality often more important than model complexity?
8. What does `pct_change()` compute?
9. What does a rolling moving average do?
10. What does the target `(Close.shift(-1) > Close).astype(int)` mean?
11. Why is logistic regression a good first baseline here?
12. What is the main responsibility of the ML prediction layer?
13. Why should the ML layer output probabilities, not only class labels?
14. What is the role of the news analysis layer?
15. Why is the simplified manual-news approach good for an MVP?
16. What is the role of the LLM reasoning layer?
17. Why should the LLM be grounded in the provided indicators and news?
18. What is a common danger if the LLM is allowed to overclaim?
19. Why is structured output important in the capstone?
20. What should a good output schema include besides a recommendation?
21. What is the role of the API layer?
22. Why should each module be built independently before integration?
23. Why does integration often fail even if each component works alone?
24. Why is logging important in a capstone pipeline?
25. What should you evaluate in the ML layer?
26. What should you evaluate in the LLM layer?
27. What should you evaluate in the full system?
28. Why is overengineering dangerous in the capstone?
29. What is one sign that the MVP should be simplified?
30. What is the main lesson of this stage?

---

### Answers

**1. What is the main goal of this capstone project?**

To build a production-style AI Trading Assistant that integrates data ingestion, feature engineering, ML prediction, news context, LLM reasoning, and API serving.

**2. Why is this project called an end-to-end system?**

Because it covers the full path from raw input data to final user-facing output.

**3. What is the responsibility of the market data layer?**

To fetch, validate, normalize, and provide clean market data to downstream layers.

**4. What does OHLCV mean?**

Open, High, Low, Close, and Volume.

**5. Why do we normalize and validate raw data before using it?**

Because downstream layers depend on consistent, trustworthy input, and bad raw data can silently break the whole pipeline.

**6. What is the responsibility of the feature engineering layer?**

To transform raw market data into informative features and define the target for prediction.

**7. Why is feature quality often more important than model complexity?**

Because even a strong model cannot learn useful patterns from weak or misleading inputs.

**8. What does `pct_change()` compute?**

It computes relative change between consecutive values, often used as return.

**9. What does a rolling moving average do?**

It computes the average over a recent sliding window of rows.

**10. What does the target `(Close.shift(-1) > Close).astype(int)` mean?**

It means label the current row as 1 if the next day's close is higher than today's close, otherwise 0.

**11. Why is logistic regression a good first baseline here?**

Because it is simple, fast, interpretable, and good enough to validate the first working system.

**12. What is the main responsibility of the ML prediction layer?**

To produce a structured predictive signal from engineered features.

**13. Why should the ML layer output probabilities, not only class labels?**

Because probabilities communicate uncertainty and are more useful for downstream reasoning.

**14. What is the role of the news analysis layer?**

To provide relevant text context that may affect interpretation of the structured signals.

**15. Why is the simplified manual-news approach good for an MVP?**

Because it reduces system complexity while still letting you learn how to incorporate text context.

**16. What is the role of the LLM reasoning layer?**

To explain structured signals in natural language and produce a readable recommendation.

**17. Why should the LLM be grounded in the provided indicators and news?**

Because otherwise it may invent unsupported claims or drift away from the real system inputs.

**18. What is a common danger if the LLM is allowed to overclaim?**

It may produce persuasive but unreliable recommendations that users overtrust.

**19. Why is structured output important in the capstone?**

Because it makes the result easier to validate, test, log, display, and integrate with software systems.

**20. What should a good output schema include besides a recommendation?**

It should include summary, bullish and bearish factors, and confidence or probability-related context.

**21. What is the role of the API layer?**

To receive requests, run the full pipeline, validate inputs, and return structured responses.

**22. Why should each module be built independently before integration?**

Because isolated validation makes integration easier and helps localize failures.

**23. Why does integration often fail even if each component works alone?**

Because interfaces, schemas, assumptions, or handoff logic may not align when components are connected.

**24. Why is logging important in a capstone pipeline?**

Because it helps trace what happened at each stage and makes debugging possible.

**25. What should you evaluate in the ML layer?**

Prediction quality, train/test behavior, and whether the output probabilities are meaningful.

**26. What should you evaluate in the LLM layer?**

Faithfulness to input signals, output structure, reasoning quality, and avoidance of unsupported claims.

**27. What should you evaluate in the full system?**

End-to-end correctness, response completeness, runtime, robustness, and API behavior.

**28. Why is overengineering dangerous in the capstone?**

Because it increases complexity and failure points before a stable MVP exists.

**29. What is one sign that the MVP should be simplified?**

When debugging becomes harder than learning and the full pipeline is no longer stable or explainable.

**30. What is the main lesson of this stage?**

A real AI system is a layered pipeline, and reliability depends on keeping each layer clear, testable, grounded, and well integrated.

---

## What You Must Be Able To Do After Stage 13

- [ ] explain the full capstone system from raw data to final recommendation
- [ ] define clear responsibilities for each layer
- [ ] build a simple but complete AI Trading Assistant MVP
- [ ] create features and a baseline prediction model
- [ ] add a grounded LLM explanation layer
- [ ] design structured outputs and API boundaries
- [ ] validate and debug each stage independently
- [ ] log intermediate outputs for integration debugging
- [ ] evaluate both component-level and end-to-end behavior
- [ ] understand that a successful capstone is a reliable pipeline, not just a clever demo
