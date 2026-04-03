# Stage 15 — When Model Does Not Work as Expected
## How to Adjust, Tune, or Improve It

**(Week 26)**

---

## Goal

Learn how to diagnose and improve models and AI systems systematically.

This stage teaches you how to answer questions like:

- Why is my model not performing well?
- Is the problem in the data, feature engineering, target, model, or evaluation?
- How do I improve performance without guessing randomly?
- How do I debug ML models, deep learning models, and LLM/RAG systems?

You are learning:

- structured debugging
- controlled tuning
- root-cause analysis
- experiment tracking
- systematic improvement

---

## Quick Summary

When a model is not working well, the problem is usually not only the algorithm.

Typical failure sources are:

- bad data
- weak target definition
- poor features
- train/test leakage
- overfitting
- underfitting
- wrong evaluation metric
- prompt problems
- retrieval problems
- production drift

> **The key lesson is: Do NOT tune blindly. Diagnose first.**

A strong AI engineer does not immediately jump to:

- bigger model
- more layers
- more prompts
- more hyperparameter tuning

Instead, they ask:

- What exactly is failing?
- Where in the pipeline is it failing?
- What evidence supports that diagnosis?
- What is the smallest controlled change to test next?

---

## Study Materials

- **Scikit-learn model evaluation docs:** https://scikit-learn.org/stable/model_selection.html
- **PyTorch training/evaluation tutorials:** https://pytorch.org/tutorials/
- **ML experiment tracking concepts:** MLflow / Weights & Biases concepts are useful
- **For LLM/RAG system debugging:**
  - prompt evaluation
  - retrieval inspection
  - chunking inspection
  - grounding checks

---

## Core Idea

When a model is not working well, the problem is usually not only the algorithm.

Typical failure sources are:

- bad data
- weak target definition
- poor features
- train/test leakage
- overfitting
- underfitting
- wrong evaluation metric
- prompt problems
- retrieval problems
- production drift

> **The key lesson: Do NOT tune blindly. Diagnose first.**

---

## Key Knowledge (Deep Understanding)

### 1. First Define What "Not Working" Means

Before changing anything, define the failure clearly.

A model can fail in many ways:

- low accuracy
- weak recall
- unstable predictions
- good offline performance but bad live results
- good technical metric but poor business result
- correct retrieval but weak final answer
- good answer quality but too much latency

#### Example

Do not say:

> "the model is bad"

Instead say:

- "test accuracy is only 54%"
- "live results dropped after new data source was added"
- "RAG answers fail on multi-document questions"
- "LLM output format is inconsistent"

#### Why this matters

> If the failure is vague, the fix will also be vague.

#### Beginner Explanation

This is the first and most important debugging rule.

If you say: "It's not working" — that is not enough.

You need to define:

- what is wrong
- where it shows up
- how you noticed it
- which metric or symptom proves it

A vague complaint leads to random tuning. A precise failure statement leads to useful diagnosis.

#### Step-by-Step Mental Model

**Step 1 — Name the symptom**

Examples:
- low test accuracy
- slow inference
- wrong answers on recent docs
- unstable JSON format

**Step 2 — Name where it appears**

Examples:
- training set
- validation set
- live deployment
- only RAG answers
- only high-volatility trading days

**Step 3 — Name when it started**

Examples:
- after changing feature pipeline
- after adding new data source
- after switching prompt
- after moving to live data feed

**Step 4 — Name how you measure it**

Examples:
- accuracy dropped from 0.64 to 0.54
- latency increased from 1.2s to 4.8s
- JSON validity fell from 95% to 61%

#### Important Algorithms / Mechanisms for Failure Definition

**A. Metric-Based Diagnosis**

Use one or more measurable metrics to define failure.

How it works:
- choose a metric
- compare baseline vs current result
- identify the gap

> **Why important:** You cannot debug well if failure is not measurable.

**B. Symptom Classification**

Group the failure by type:
- quality failure
- stability failure
- latency failure
- retrieval failure
- formatting failure
- drift failure

> **Why important:** Different failure types require different debugging paths.

**C. Baseline Comparison**

Compare current behavior with a known earlier baseline.

> **Why important:** A model may feel "bad," but only comparison shows whether it actually regressed.

#### Good Debugging Rule

Before changing anything, write:

- observed failure
- affected metric
- suspected area
- confidence level in the diagnosis

That simple habit improves debugging a lot.

---

### 2. Underfitting vs Overfitting

This is the first major diagnosis.

#### Underfitting

The model is too weak.

**Symptoms:**
- bad train performance
- bad validation/test performance

**Possible causes:**
- weak features
- wrong target
- model too simple
- not enough training

#### Overfitting

The model memorizes training data.

**Symptoms:**
- strong train performance
- weak validation/test performance

**Possible causes:**
- too complex model
- too many noisy features
- too little data
- leakage

#### What to check

- train metric vs validation metric
- learning curves
- feature complexity
- data size

#### Beginner Explanation

This is one of the most important model diagnosis concepts.

If a model is weak, you need to know which kind of weak.

- **Underfitting** means: The model did not learn enough.
- **Overfitting** means: The model learned the training data too specifically and does not generalize.

These are opposite problems, and the fixes are different.

#### Simple Mental Model

- **Underfitting:** Like a student who did not learn the material.
- **Overfitting:** Like a student who memorized the practice test instead of understanding the subject.

#### Step-by-Step Diagnosis

**Step 1 — Look at training performance**

Is training accuracy / loss already weak?

**Step 2 — Look at validation/test performance**

Is generalization also weak?

**Step 3 — Compare the gap**

- small gap + both weak → underfitting likely
- big gap + train strong / test weak → overfitting likely

**Step 4 — Check whether the problem changed after increasing model complexity**

That can help confirm the diagnosis.

#### Important Algorithms / Mechanisms for Underfitting vs Overfitting

**A. Train vs Validation Comparison**

Compare performance across data splits.

> **Why important:** This is the most direct first signal of underfitting vs overfitting.

**B. Learning Curves**

Plot train and validation performance as training progresses or as data size grows.

How it works:
- train score curve
- validation score curve

> **Why important:** Shows whether more training or more data may help.

**C. Regularization**

Used to fight overfitting.

Examples:
- L1/L2 regularization
- weight decay
- dropout
- pruning

> **Why important:** Controls model complexity.

**D. Model Capacity Control**

Adjust how powerful the model is.

Examples:
- shallower tree
- fewer hidden units
- smaller network
- fewer estimators

> **Why important:** Too little capacity underfits; too much may overfit.

#### Fix Strategies

**If underfitting:**
- improve features
- fix target
- train longer
- use a slightly stronger model
- reduce overly aggressive regularization

**If overfitting:**
- simplify model
- use regularization
- add more data
- remove noisy features
- improve validation discipline
- check for leakage

---

### 3. Data Problems Are Extremely Common

Many bad models are actually data problems.

#### Common data issues

- missing values
- wrong timestamps
- duplicate rows
- inconsistent schema
- bad labels
- stale data
- target leakage

#### Trading examples

- future price accidentally used in feature
- split-adjusted price mixed with unadjusted feature
- earnings date misaligned
- missing volume rows

#### RAG examples

- documents parsed badly
- wrong page order
- duplicate chunk ingestion
- stale knowledge base

#### What to do

Always inspect:
- raw data
- processed data
- labels/targets
- row counts
- missing-value counts

#### Beginner Explanation

This is one of the biggest practical lessons in AI work: many "model problems" are really data problems.

A model can only learn from what you give it.

If the data is broken, the model may:
- learn the wrong pattern
- look unstable
- fail only in live use
- produce fake good performance due to leakage

#### Step-by-Step Data Diagnosis

**Step 1 — Check raw source data**

Is the original input already broken?

**Step 2 — Check processed data**

Did your pipeline introduce the problem?

**Step 3 — Check labels or targets**

Are targets misaligned, noisy, or incorrect?

**Step 4 — Compare train and live pipeline**

Are they computing the same fields the same way?

**Step 5 — Check freshness**

Is the data outdated, partially updated, or inconsistent?

#### Important Algorithms / Mechanisms for Data Diagnosis

**A. Missing-Value Analysis**

Count missing values and understand why they exist.

> **Why important:** Missingness can distort training and evaluation.

**B. Duplicate Detection**

Check whether rows are duplicated.

> **Why important:** Duplicates can distort model behavior and evaluation.

**C. Timestamp Validation**

Verify chronological order and alignment.

> **Why important:** Time-aware systems break badly when timestamps are wrong.

**D. Schema Validation**

Check whether expected columns and types are present.

> **Why important:** Upstream data changes often cause downstream failure.

**E. Leakage Detection**

Check whether future or answer-like information is present in features.

> **Why important:** Leakage creates fake success.

#### Good Beginner Practice

Always run checks such as:

```python
print(df.shape)
print(df.head())
print(df.info())
print(df.isna().sum())
print(df.duplicated().sum())
```

And for time series:

```python
print(df.index.is_monotonic_increasing)
```

---

### 4. Feature Engineering Is Often the Biggest Lever

If the model cannot see a useful pattern, changing the algorithm may not help.

#### Signs of weak features

- model cannot separate classes
- predictions look random
- strong algorithm gives only small improvement
- train/test both weak

#### Improvement ideas

- better domain features
- remove noisy features
- create interaction features
- add time-aware features
- simplify feature set

#### Trading examples

Better features may include:
- returns instead of raw prices
- moving-average distance
- volatility regime
- volume surge
- relative strength vs sector
- earnings proximity

#### Beginner Explanation

When a beginner sees weak performance, they often think: "I need a stronger model."

Very often the better answer is: "I need better features."

The model only sees the inputs you give it. If your features do not contain useful signal, a more complex model may only memorize noise better.

#### Step-by-Step Feature Diagnosis

**Step 1 — Check whether features make sense logically**

Would a domain expert consider them informative?

**Step 2 — Check whether features are noisy or redundant**

Too many weak features can hurt.

**Step 3 — Compare simple vs engineered features**

Did feature engineering improve signal?

**Step 4 — Remove one feature group at a time**

This reveals which features matter.

**Step 5 — Inspect feature distributions**

Are values stable, sane, and consistent?

#### Important Algorithms / Mechanisms for Feature Improvement

**A. Feature Ablation**

Remove one feature or feature group and compare results.

> **Why important:** Shows what actually helps.

**B. Interaction Features**

Combine variables into more informative signals.

Example:
- MA20 / MA50
- price / volatility
- return × volume surge

> **Why important:** Some patterns only appear when variables are combined.

**C. Domain Feature Design**

Use problem-specific signals.

> **Why important:** Domain-informed features often outperform generic feature lists.

**D. Feature Simplification**

Remove weak, unstable, or noisy features.

> **Why important:** More features is not always better.

**E. Time-Aware Features**

Add temporal structure where relevant.

Examples:
- rolling averages
- lagged returns
- event flags
- month or regime indicator

> **Why important:** Many real problems are time-dependent.

---

### 5. Target Definition Can Be More Important Than Model Choice

If you predict the wrong target, a strong model still fails.

#### Trading target examples

- next-day direction
- next-5-day return
- ranking score
- volatility-adjusted signal
- event-driven outcome

#### Why target matters

A target can be:
- mathematically easy but not useful
- realistic but noisy
- easy to compute but misaligned with business goal

#### Common mistake

Keep changing the model without questioning the target.

#### Beginner Explanation

The target is what you ask the model to learn.

If the target itself is weak, confusing, or misaligned with the real business need, the model will optimize the wrong thing very efficiently.

That means you can have:
- a technically good model
- solving the wrong problem

#### Simple Mental Model

> A target is like the exam question. If the exam question is bad, even a smart student answering it well does not solve the real need.

#### Step-by-Step Target Diagnosis

**Step 1 — Write the target in plain English**

Example: "Predict whether tomorrow's close is higher than today's close."

**Step 2 — Ask whether that target really matches the decision goal**

Does the business or strategy actually care about that exact horizon?

**Step 3 — Check noise level**

Is the target too unstable to learn well?

**Step 4 — Check actionability**

Does success on the target lead to useful downstream action?

**Step 5 — Compare alternative target definitions**

Sometimes target redesign matters more than model redesign.

#### Important Algorithms / Mechanisms for Target Design

**A. Horizon Definition**

Choose how far ahead the target looks.

Examples:
- next step
- next day
- next week
- next event window

> **Why important:** Different horizons create very different learning problems.

**B. Thresholded Targeting**

Convert continuous outcomes into categories.

Example: return > 1% = positive signal

> **Why important:** Target definition changes class balance and decision meaning.

**C. Ranking Targets**

Predict relative ordering instead of exact direction or value.

> **Why important:** Some use cases care more about ranking than absolute prediction.

**D. Event-Conditioned Targets**

Target only specific situations.

Example:
- post-earnings move
- outage risk
- churn after warning signal

> **Why important:** Can reduce noise and better match real decision points.

---

### 6. Hyperparameter Tuning Should Be Controlled

Hyperparameters matter, but random tuning wastes time.

#### Examples

- tree depth
- number of estimators
- learning rate
- regularization
- batch size
- hidden layer size

#### Good tuning process

- confirm data is valid
- confirm target is valid
- establish baseline
- tune one group of parameters at a time
- save all experiments

#### Bad tuning process

- change features, model, and parameters all at once
- no record of what changed
- compare runs unfairly

#### Beginner Explanation

Hyperparameters are model settings you choose, not learn.

They matter, but they should come after:
- data check
- target check
- baseline creation

Otherwise you spend hours tuning a broken setup.

#### Step-by-Step Tuning Process

**Step 1 — Freeze the dataset and evaluation setup**

No fair tuning happens if the benchmark keeps changing.

**Step 2 — Establish a baseline**

You need something to beat.

**Step 3 — Choose one tuning axis**

Example:
- only learning rate
- only max depth
- only regularization

**Step 4 — Record every run**

Without tracking, tuning becomes guessing.

**Step 5 — Compare fairly**

Same split, same data, same metric.

#### Important Algorithms / Mechanisms for Hyperparameter Tuning

**A. Grid Search**

Test predefined combinations systematically.

> **Why important:** Simple, transparent baseline search.

**B. Random Search**

Try random parameter combinations.

> **Why important:** Often more efficient than exhaustive search in large spaces.

**C. Bayesian / Smarter Search (conceptual)**

Future improvement path for more efficient tuning.

> **Why important:** Useful at larger scale, but not your first debugging tool.

**D. Experiment Tracking**

Record params + metrics + dataset version.

> **Why important:** A tuning process without records is not reliable.

---

### 7. Error Analysis Is a Core Skill

Do not only look at average metrics. Inspect bad cases.

#### For ML

Look at:
- false positives
- false negatives
- biggest regression errors

#### For trading

Slice by:
- volatility regime
- earnings periods
- sector
- bull vs bear period
- high-volume vs low-volume days

#### For RAG

Slice by:
- short vs long questions
- single-doc vs multi-doc questions
- recent vs old documents

#### Why this matters

> Average performance can hide the true failure pattern.

#### Beginner Explanation

Averages hide structure.

If you only look at one average metric, you may miss:
- one important class failing badly
- one market regime failing badly
- one document type failing badly
- one prompt style failing badly

Error analysis teaches you where the system breaks.

#### Step-by-Step Error Analysis

**Step 1 — Collect failed examples**

Do not only keep summary numbers.

**Step 2 — Group them by type**

Examples:
- false positive
- false negative
- recent docs
- long context
- high-vol regime

**Step 3 — Look for repeated patterns**

What kind of examples fail repeatedly?

**Step 4 — Form hypothesis**

Example: "Model fails during earnings weeks because target noise rises."

**Step 5 — Test one corrective change**

Then re-evaluate.

#### Important Algorithms / Mechanisms for Error Analysis

**A. Confusion Matrix**

Used for classification breakdown.

> **Why important:** Shows where classes are being confused.

**B. Residual Analysis**

Used for regression.

> **Why important:** Shows where error magnitude is largest.

**C. Slice-Based Analysis**

Evaluate subgroups separately.

> **Why important:** Real-world failure often concentrates in slices.

**D. Hard-Case Collection**

Store examples with highest error or weakest grounding.

> **Why important:** These are often the most educational cases.

---

### 8. Evaluation Must Match Reality

A model can look good if evaluation is unrealistic.

#### Bad evaluation patterns

- random split for time-series
- leakage between train/test
- using only easy samples
- using accuracy when business needs risk-adjusted performance

#### Better evaluation

**For trading:**
- walk-forward validation
- rolling backtest
- transaction costs included

**For RAG:**
- retrieval relevance checks
- grounded answer validation
- source coverage
- hallucination rate checks

**For LLM output:**
- structure validity
- consistency
- factual grounding

#### Beginner Explanation

A model is not "good" just because one metric looks nice in a notebook.

Evaluation must match the real way the system will be used. If your evaluation setup is unrealistic, the system will disappoint in practice.

#### Step-by-Step Reality Check

**Step 1 — Ask how the model will be used in real life**

Time-based? Interactive? Document-grounded? High-stakes?

**Step 2 — Match split strategy to the real setting**

Time-series should usually not use random split.

**Step 3 — Match metrics to the business need**

Accuracy is not always enough.

**Step 4 — Include realistic constraints**

Costs, latency, structure validity, grounding.

#### Important Algorithms / Mechanisms for Realistic Evaluation

**A. Walk-Forward Validation**

Train on past, test on future repeatedly.

> **Why important:** Much better for time-series realism.

**B. Rolling Backtest**

Simulate repeated time progression.

> **Why important:** Useful for trading systems.

**C. Retrieval Relevance Evaluation**

Check whether the retriever found the right evidence.

> **Why important:** RAG quality starts before generation.

**D. Schema Validity Rate**

Measure how often structured output is actually valid.

> **Why important:** LLM apps often fail through formatting inconsistency.

**E. Grounding Evaluation**

Check whether answer claims are supported by evidence.

> **Why important:** A fluent answer may still be wrong.

---

### 9. Deep Learning Failure Modes

Neural networks fail in ways traditional ML often does not.

#### Common deep learning problems

- loss does not go down
- loss becomes NaN
- train improves but validation collapses
- model is too slow
- shapes are wrong
- GPU memory errors

#### Common causes

- learning rate too high
- data not normalized
- label bug
- too much model capacity
- small dataset
- unstable batching

#### Common fixes

- lower learning rate
- inspect one batch manually
- normalize inputs
- simplify model
- add regularization
- use early stopping

#### Beginner Explanation

Deep learning adds more failure modes because:
- more parameters
- more tensor operations
- more sensitivity to scale
- more complex training loops

So you need a more disciplined debugging habit.

#### Step-by-Step DL Diagnosis

**Step 1 — Check whether loss decreases at all**

If not, the system may be broken at a basic level.

**Step 2 — Inspect one batch manually**

Make sure:
- inputs are sane
- labels are sane
- shapes are correct

**Step 3 — Try to overfit one tiny batch**

If the model cannot learn one tiny batch, something fundamental is wrong.

**Step 4 — Check learning rate and normalization**

These are common causes of instability.

**Step 5 — Compare train vs validation**

Look for overfitting or collapse.

#### Important Algorithms / Mechanisms for Deep Learning Debugging

**A. Gradient Descent Stability**

Training can fail if updates are too large.

> **Why important:** Learning rate is often the first culprit.

**B. Gradient Clipping**

Cap gradient size.

> **Why important:** Helps with exploding gradients.

**C. Early Stopping**

Stop training when validation stops improving.

> **Why important:** Simple defense against overfitting.

**D. Normalization**

Scale inputs to stable ranges.

> **Why important:** Unstable inputs make neural training harder.

**E. Tiny-Batch Overfit Test**

Force model to fit a tiny subset.

> **Why important:** This is one of the best sanity checks in deep learning.

---

### 10. LLM / RAG Failure Modes

LLM systems fail differently from standard ML.

#### Prompt problems

- vague prompt
- inconsistent prompt
- no output schema
- no grounding instruction

#### Retrieval problems

- poor chunking
- wrong top-k
- bad embeddings
- missing metadata filters
- no reranking

#### Synthesis problems

- correct docs but weak final answer
- answer ignores evidence
- too much irrelevant context

#### What to debug separately

- query
- retrieval
- prompt
- final answer

> Do not treat "LLM system" as one black box.

#### Beginner Explanation

LLM and RAG systems are pipelines, not one model call.

So when they fail, you must debug the pipeline in parts.

A weak answer might come from:
- wrong query formation
- bad retrieval
- bad chunking
- vague prompt
- too much context
- no grounding instruction
- weak synthesis

If you treat it as one black box, you will waste time.

#### Step-by-Step LLM/RAG Debugging

**Step 1 — Inspect the input query**

Was it clear and specific enough?

**Step 2 — Inspect retrieved chunks**

Were they relevant and sufficient?

**Step 3 — Inspect prompt construction**

Did the prompt clearly instruct grounded answering?

**Step 4 — Inspect final answer**

Did it actually use the retrieved evidence?

**Step 5 — Check structure**

Was output valid, grounded, and complete?

#### Important Algorithms / Mechanisms for LLM/RAG Debugging

**A. Prompt Evaluation**

Test prompt variants against a fixed set of examples.

> **Why important:** Prompting should be evaluated, not improvised endlessly.

**B. Retrieval Inspection**

Manually inspect top-k chunks.

> **Why important:** Many RAG failures are retrieval failures.

**C. Chunking Inspection**

Read actual chunk samples.

> **Why important:** Bad chunks cause bad retrieval.

**D. Re-Ranking**

Use stronger ranking after initial retrieval.

> **Why important:** Can rescue poor top-k ordering.

**E. Grounding Check**

Compare answer claims to source evidence.

> **Why important:** A good-sounding answer may still be unsupported.

---

### 11. Production Drift and Real-World Change

A model can work offline and fail live because the environment changed.

#### Examples

- data schema changed
- market regime changed
- live features differ from training features
- embedding store outdated
- API data delayed
- new prompt version changed behavior

#### What to monitor

- feature distributions
- prediction distributions
- error rate over time
- retrieval hit quality
- latency trends

#### Beginner Explanation

A system can degrade without any obvious code bug.

Why? Because the real world changes. That is called **drift** or **environment change**. The model may still be the same, but the world around it is different.

#### Types of Drift

**A. Data drift**

Input distribution changed.

**B. Concept drift**

Relationship between input and target changed.

**C. Pipeline drift**

Feature pipeline or schema changed.

**D. Retrieval drift**

Knowledge base became stale or inconsistent.

**E. Prompt drift**

Prompt version changed system behavior.

#### Step-by-Step Drift Diagnosis

**Step 1 — Compare old vs recent input distributions**

Look for major feature shifts.

**Step 2 — Compare old vs recent prediction distributions**

Are predictions behaving oddly?

**Step 3 — Check data freshness and schema**

Did inputs change structure?

**Step 4 — Check system changes**

Did a new prompt, source, or parser cause the issue?

**Step 5 — Decide response**

Options:
- retrain
- update target
- refresh knowledge base
- fix pipeline
- rollback prompt

#### Important Algorithms / Mechanisms for Drift Detection

**A. Distribution Comparison**

Compare mean, std, quantiles, or histograms across periods.

> **Why important:** Simple drift checks are often already useful.

**B. Time-Based Monitoring**

Track metrics over time.

> **Why important:** Drift often appears gradually.

**C. Canary / Version Comparison**

Compare old system version vs new version on overlapping traffic or eval set.

> **Why important:** Helps isolate regressions caused by system changes.

**D. Feature Distribution Alerts**

Flag large shifts in important features.

> **Why important:** Live monitoring should not depend only on user complaints.

---

## Practical Debugging Playbook

**Step 1 — Define the problem precisely**

Write:
- what failed
- where it failed
- when it started
- which metric is affected

**Step 2 — Check data and target first**

Inspect:
- row counts
- missing values
- timestamps
- labels
- leakage

**Step 3 — Compare train vs validation vs test**

This tells you:
- underfitting
- overfitting
- leakage suspicion
- instability

**Step 4 — Inspect failed examples**

Look at:
- wrong predictions
- misclassified cases
- weak RAG answers
- hallucinated outputs

**Step 5 — Improve target or features before complex tuning**

Ask:
- is target meaningful?
- are features informative?
- are features noisy?
- can domain knowledge improve signal?

**Step 6 — Tune parameters in a controlled way**

Change one dimension at a time.

**Step 7 — Re-evaluate with realistic tests**

Always retest under realistic assumptions.

### Beginner Version of the Playbook

When stuck, do this in order:

1. define the failure in one sentence
2. verify the data
3. verify the target
4. compare train vs validation
5. inspect bad cases
6. test one hypothesis
7. log the result
8. only then try another change

> That simple order prevents random debugging.

---

## ML Debugging Checklist

Use this checklist whenever a classic ML model performs poorly.

### Data
- [ ] Is the dataset clean?
- [ ] Are timestamps correct?
- [ ] Are there duplicates?
- [ ] Are labels correct?
- [ ] Is leakage possible?

### Features
- [ ] Are features informative?
- [ ] Are they stable?
- [ ] Are there too many noisy features?
- [ ] Are train/live features computed the same way?

### Target
- [ ] Does target match business goal?
- [ ] Is target horizon correct?
- [ ] Is label too noisy?

### Model
- [ ] Too simple?
- [ ] Too complex?
- [ ] Reasonable defaults?
- [ ] Overfitting signs?

### Evaluation
- [ ] Same split for fair comparison?
- [ ] Time-aware split if needed?
- [ ] Correct metric?

### Production
- [ ] Has data drifted?
- [ ] Did pipeline change?
- [ ] Did input schema change?

---

## Deep Learning Troubleshooting Table

| **Symptom** | **Possible Causes** | **Try** |
|---|---|---|
| Loss does not decrease | Learning rate wrong, label issue, bad preprocessing, code bug | Lower learning rate, inspect one batch manually, simplify model, overfit one tiny batch intentionally |
| Validation gets worse while training improves | Overfitting, too much capacity, too little data | Dropout, weight decay, smaller model, early stopping |
| Loss becomes NaN | Exploding gradients, numerical instability, bad input scale | Lower learning rate, gradient clipping, inspect invalid values |
| Training too slow | Data loader bottleneck, batch size too small, CPU/GPU mismatch | Profile pipeline, increase batch size if possible, optimize data loading |

---

## RAG / LLM Failure Diagnosis Matrix

| **Symptom** | **Likely Causes** | **Check / Try** |
|---|---|---|
| Answer sounds good but is wrong | Hallucination, weak retrieval, no grounding instruction | Retrieved chunks, prompt wording, source quality |
| Answer misses important info | Chunking poor, top-k too small, retrieval weak | Larger top-k, better chunking, reranking |
| Answer too generic | Vague prompt, generic retrieved text, weak task framing | More structured prompt, focused retrieval, explicit required sections |
| Inconsistent output format | No schema, ambiguous prompt, temperature too high | JSON schema, lower temperature, stronger format instruction |

---

## Trading-Model Improvement Workflow

This is especially useful for your trading systems.

**Step 1 — Separate prediction failure from trading failure**

A model can have okay accuracy but poor trading results.

Why?
- transaction costs
- bad sizing
- bad target
- bad risk control

**Step 2 — Recheck target**

Does it match strategy horizon?

Examples:
- next-day move
- next-week return
- ranking signal

**Step 3 — Recheck features**

Use domain features:
- return
- MA distance
- volatility
- sector-relative strength
- event flags

**Step 4 — Slice by regime**

Evaluate performance in:
- bull markets
- bear markets
- high volatility
- low volatility
- earnings periods

**Step 5 — Add cost-aware evaluation**

Include:
- turnover
- slippage
- commissions or proxy cost

**Step 6 — Separate alpha model from portfolio logic**

A good signal can still produce bad portfolio results.

### Beginner Explanation

This is crucial for trading projects.

A weak trading result does not automatically mean the prediction model is useless.

The system may fail because:
- the target horizon is wrong
- you trade too often
- costs kill the signal
- the portfolio layer sizes badly
- one market regime dominates losses

So trading systems require two-level diagnosis:
- signal quality
- strategy implementation quality

---

## Practice Project

### Project: Failure Analysis Toolkit

#### Goal

Build a toolkit that helps diagnose weak AI systems.

You will create:
- experiment tracking
- wrong prediction analysis
- slice-based analysis
- drift checks
- debugging report

### Step-by-Step Instructions

#### Step 1 — Create experiment log format

Every run should save:
- run id
- dataset version
- feature version
- model name
- parameters
- metrics

**Suggested JSON:**

```json
{
  "run_id": "exp_001",
  "dataset_version": "v1",
  "feature_version": "f3",
  "model": "random_forest",
  "params": {"max_depth": 5},
  "metrics": {"accuracy": 0.58}
}
```

Save logs into: `data/outputs/experiments/`

> **Why this step matters:** Without experiment history, improvement becomes guesswork.

**Beginner rule:** If you cannot answer what changed, when it changed, and what metric moved — then you are not debugging systematically yet.

#### Step 2 — Build wrong prediction report

For classification:
- save false positives
- save false negatives

For regression:
- save highest-error rows

For RAG:
- save question
- retrieved chunks
- answer
- expected answer if known

> **Why this step matters:** Failed examples are often more valuable than average metrics.

**Beginner explanation:** You learn much more from where the model was confidently wrong, which questions retrieval missed, and which prompts broke structure — than from one global metric alone.

#### Step 3 — Add slice analysis

Create reports such as:
- performance by month
- performance by volatility regime
- performance by sector
- performance on short vs long questions

> **Why this step matters:** This shows whether failure is concentrated in a specific subset.

**Beginner explanation:** A model that looks "okay on average" may be terrible in one important slice.

#### Step 4 — Run one feature ablation

Remove one feature or feature group and compare results.

This teaches:
- which features actually help
- which features add noise

> **Why this step matters:** It turns feature discussion into evidence.

#### Step 5 — Add drift check

Compare:
- training feature distributions
- recent/live feature distributions

Even a simple mean/std comparison is useful for beginners.

> **Why this step matters:** Many live failures come from input shift, not only weak models.

#### Step 6 — Write debugging report

Must include:
- observed problem
- hypothesis
- checks performed
- findings
- fix applied
- new result

> **Why this step matters:** This trains engineering communication, not only code.

A good engineer can explain:
- what failed
- why they think it failed
- what they changed
- whether it helped

### Deliverables

- experiment log files
- wrong prediction report
- slice analysis
- drift analysis
- debugging report
- README

### Evaluation

Students should be evaluated on:

1. **Structure of debugging process** — Was the process systematic?
2. **Evidence quality** — Did the student show real evidence, not guesses?
3. **Improvement logic** — Was the proposed fix reasonable?
4. **Reflection quality** — Did the student clearly explain what was learned?

### Grading Rubric

| **Component** | **Weight** |
|---|---|
| Experiment tracking | 20% |
| Error analysis | 25% |
| Drift / slice analysis | 20% |
| Debugging report | 25% |
| Organization | 10% |

---

## Common Mistakes

- changing too many variables at once
- no experiment history
- no inspection of failed examples
- guessing instead of diagnosing
- fixing output without checking upstream data

### Expanded Common Mistakes with Reasons and Fixes

**1. Changing too many variables at once**

- **Reason:** It feels faster.
- **Problem:** You cannot tell what caused the result.
- **Fix:** Change one major thing at a time.

**2. No experiment history**

- **Reason:** People trust memory.
- **Problem:** They forget which result belongs to which run.
- **Fix:** Log every run with IDs, params, and metrics.

**3. No inspection of failed examples**

- **Reason:** Average metrics feel sufficient.
- **Problem:** Failure patterns stay hidden.
- **Fix:** Always review error cases directly.

**4. Guessing instead of diagnosing**

- **Reason:** People want quick fixes.
- **Problem:** Random tuning wastes time and may make things worse.
- **Fix:** Write hypothesis + evidence before tuning.

**5. Fixing output without checking upstream data**

- **Reason:** The final bad answer is most visible.
- **Problem:** The true root cause may be data or retrieval.
- **Fix:** Debug from upstream to downstream.

**6. Treating every problem as a model problem**

- **Reason:** The model is the most visible component.
- **Problem:** You miss data, target, prompt, or pipeline bugs.
- **Fix:** Use whole-system diagnosis.

**7. Ignoring live vs offline differences**

- **Reason:** Offline metrics look reassuring.
- **Problem:** Production can still fail.
- **Fix:** Track drift and live behavior separately.

---

## Final Understanding

You should understand:

> When a model fails, the right move is not random tuning — it is structured diagnosis.

A top AI engineer improves systems by:
- defining failure clearly
- checking data and targets first
- analyzing bad cases
- changing one thing at a time
- re-evaluating honestly

That is what this stage teaches.

> The strongest improvement skill in AI is not "knowing one more model." It is being able to diagnose where a system is weak and improve it systematically.

---

## Stage 15 Debugging Workflow (REAL WORLD)

```
1.  Define the failure precisely
2.  Check data and schema
3.  Check target/labels
4.  Compare train/validation/test
5.  Inspect failed examples
6.  Analyze slices
7.  Form one hypothesis
8.  Change one thing
9.  Re-run and log result
10. Decide whether the hypothesis was supported
```

### Beginner Explanation of Each Step

1. **Define the failure precisely** — Do not start with vague frustration.
2. **Check data and schema** — Many bugs start before the model.
3. **Check target/labels** — Wrong labels make good models look bad.
4. **Compare train/validation/test** — This reveals underfitting, overfitting, or leakage suspicion.
5. **Inspect failed examples** — Learn from concrete cases.
6. **Analyze slices** — See whether failure is localized.
7. **Form one hypothesis** — Debugging needs a theory to test.
8. **Change one thing** — Controlled experiments beat random tuning.
9. **Re-run and log result** — You need evidence, not memory.
10. **Decide whether the hypothesis was supported** — Not every fix works. That is normal.

---

## Self Test

### Questions

1. Why is "the model is bad" not a useful diagnosis?
2. What kinds of failures can "not working" mean?
3. What is underfitting?
4. What is overfitting?
5. How can comparing train and validation performance help diagnose model problems?
6. Why are data problems so common in AI systems?
7. What are some common data issues?
8. What is target leakage?
9. Why can feature engineering matter more than changing the model?
10. What are signs that features may be weak?
11. Why can target definition matter more than model choice?
12. What makes a target badly designed?
13. Why should hyperparameter tuning be controlled?
14. What is a bad tuning process?
15. Why is experiment tracking important?
16. What is error analysis?
17. Why are average metrics not enough?
18. What is slice-based analysis?
19. Why must evaluation match real usage?
20. Why is random split often wrong for time-series?
21. What is one useful deep learning sanity check?
22. What can cause loss to become NaN?
23. Why should LLM/RAG systems be debugged in parts instead of as one black box?
24. What are common RAG failure sources?
25. What is production drift?
26. Why can a model work offline but fail live?
27. In trading, why must prediction failure be separated from trading failure?
28. Why can transaction costs change conclusions?
29. What is the main purpose of the Failure Analysis Toolkit project?
30. What is the main lesson of this stage?

---

### Answers

**1. Why is "the model is bad" not a useful diagnosis?**

Because it does not define the exact symptom, location, timing, or metric of the failure.

**2. What kinds of failures can "not working" mean?**

It can mean low accuracy, weak recall, unstable predictions, bad live results, poor business value, weak retrieval, inconsistent output, or excessive latency.

**3. What is underfitting?**

Underfitting is when the model is too weak to learn useful patterns, leading to poor training and poor test performance.

**4. What is overfitting?**

Overfitting is when the model learns the training data too specifically and performs much worse on validation or test data.

**5. How can comparing train and validation performance help diagnose model problems?**

Because it shows whether the model is weak everywhere or only fails to generalize.

**6. Why are data problems so common in AI systems?**

Because every model depends on input data quality, and real pipelines often contain missing values, bad labels, schema issues, or time alignment problems.

**7. What are some common data issues?**

Missing values, wrong timestamps, duplicate rows, bad labels, inconsistent schema, stale data, and leakage.

**8. What is target leakage?**

It is when future information or answer-like information accidentally enters the features or training process.

**9. Why can feature engineering matter more than changing the model?**

Because the model can only learn from the information present in the features.

**10. What are signs that features may be weak?**

Predictions look random, both train and test performance are weak, and stronger models do not help much.

**11. Why can target definition matter more than model choice?**

Because a model can optimize the wrong target very well and still fail the real business goal.

**12. What makes a target badly designed?**

It may be noisy, misaligned with the real decision, too easy but useless, or unrealistic for the use case.

**13. Why should hyperparameter tuning be controlled?**

Because uncontrolled tuning makes it impossible to know which change helped or hurt.

**14. What is a bad tuning process?**

Changing features, model type, and parameters all at once with no tracking and unfair comparisons.

**15. Why is experiment tracking important?**

Because it preserves the history of what changed and what results each run produced.

**16. What is error analysis?**

It is the practice of inspecting failed examples directly instead of only reading average metrics.

**17. Why are average metrics not enough?**

Because they can hide concentrated failure patterns in important subgroups.

**18. What is slice-based analysis?**

It is evaluating performance on meaningful subsets such as time periods, regimes, sectors, or question types.

**19. Why must evaluation match real usage?**

Because unrealistic evaluation gives misleading confidence and fails to predict real-world performance.

**20. Why is random split often wrong for time-series?**

Because it leaks future patterns into training and breaks realistic chronological evaluation.

**21. What is one useful deep learning sanity check?**

Try to intentionally overfit one tiny batch to confirm that the training loop can learn at all.

**22. What can cause loss to become NaN?**

Exploding gradients, numerical instability, invalid inputs, or an excessively high learning rate.

**23. Why should LLM/RAG systems be debugged in parts instead of as one black box?**

Because failures can come from query formulation, retrieval, chunking, prompt design, or answer synthesis separately.

**24. What are common RAG failure sources?**

Poor chunking, wrong top-k, weak embeddings, missing metadata filters, no reranking, vague prompts, or weak grounding.

**25. What is production drift?**

Production drift is when the real environment changes over time, making old model behavior less reliable.

**26. Why can a model work offline but fail live?**

Because live data, schemas, market regimes, prompts, or retrieval stores may differ from the offline setup.

**27. In trading, why must prediction failure be separated from trading failure?**

Because a decent signal can still lead to weak trading performance due to turnover, costs, sizing, or poor portfolio logic.

**28. Why can transaction costs change conclusions?**

Because a strategy that looks profitable before costs may become weak or unprofitable after realistic frictions are included.

**29. What is the main purpose of the Failure Analysis Toolkit project?**

To build a structured system for tracking experiments, analyzing errors, checking slices and drift, and writing evidence-based debugging reports.

**30. What is the main lesson of this stage?**

Model improvement should be driven by structured diagnosis, evidence, and controlled experiments instead of random guessing.

---

## What You Must Be Able To Do After Stage 15

- [ ] Define model failure precisely instead of vaguely
- [ ] Distinguish underfitting from overfitting
- [ ] Check data, target, and feature quality before random tuning
- [ ] Design controlled hyperparameter experiments
- [ ] Inspect failed examples directly
- [ ] Perform slice-based analysis
- [ ] Debug deep learning issues systematically
- [ ] Debug LLM/RAG systems by separating retrieval, prompt, and answer stages
- [ ] Think about live drift, not only offline metrics
- [ ] Improve systems through evidence-based iteration instead of trial-and-error
