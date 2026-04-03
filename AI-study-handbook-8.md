# Stage 8 — Fine-Tuning Models

*(Week 15–16)*

## Goal

Understand how to adapt pre-trained models to specific tasks.

You are learning:

- when to fine-tune vs use RAG
- how instruction tuning works
- lightweight tuning methods (LoRA / QLoRA)
- evaluation of tuned models

This stage is where you move from:

> "I can use a pre-trained model"

to:

> "I understand when model adaptation is worth it, how to do it efficiently, how to avoid common failures, and how to measure whether it actually helped."

---

## Quick Summary

Fine-tuning means taking a model that already knows general language or task patterns and adapting it to behave better on your specific task.

**Important:** You are **NOT** training from scratch.

Instead, you are starting from a model that already has learned a lot and nudging it toward:

- a better style
- better task consistency
- better structure
- better domain behavior
- better format following

A beginner should finish this stage understanding:

- what fine-tuning is
- what instruction tuning is
- how LoRA works
- how QLoRA reduces memory usage
- what distillation is
- why fine-tuning changes behavior more than knowledge freshness
- why evaluation matters more than "it looks better to me"

### Topics

- Instruction tuning
- LoRA
- QLoRA
- Distillation

---

## Study Materials

**Hugging Face Fine-tuning Guide**
https://huggingface.co/docs/transformers/training

**PEFT (LoRA)**
https://github.com/huggingface/peft

---

## Key Knowledge (Deep Understanding)

### 1. What is Fine-Tuning

**Fine-tuning = adapting a pre-trained model using new data.**

**Important:** You are NOT training from scratch.

#### Beginner Explanation

A pre-trained model already learned general patterns such as grammar, common facts, general language behavior, some reasoning patterns, and broad instruction following.

Fine-tuning trains it a bit more on your own dataset so it performs better on a narrower task.

Examples:

- make outputs more structured
- make style more professional
- make a support assistant answer in your company format
- make a finance assistant explain indicators consistently
- make a model produce JSON reliably
- make a classifier better match your domain labels

#### What Fine-Tuning Is NOT

Fine-tuning is NOT:

- training a giant model from zero
- magically making the model know all new facts forever
- automatically improving everything
- a replacement for retrieval on changing knowledge

#### Simple Mental Model

Think of the base model like a smart university graduate.

Fine-tuning is like giving that graduate:

- your company's writing guide
- your specific task examples
- your desired output format
- your domain-specific response patterns

#### Step-by-Step Mental Model

1. **Start with a base model** — a pre-trained LLM, encoder model, or classifier backbone.
2. **Prepare task-specific examples** — showing what instruction to follow, what input looks like, and what ideal output looks like.
3. **Continue training on that dataset** — model parameters are updated to better match your target behavior.
4. **Evaluate on unseen examples** — compare whether the adapted model is actually better than the base model.

#### Important Algorithms / Mechanisms

**A. Gradient-Based Continued Training** — Core fine-tuning mechanism.

How it works:

1. Feed training example into the model
2. Compute prediction
3. Compare prediction to target output
4. Compute loss
5. Backpropagate gradients
6. Update parameters
7. Repeat over many examples

*Why important: Fine-tuning is still training. It uses the same learning mechanics as other deep learning.*

---

**B. Supervised Fine-Tuning (SFT)** — Most common beginner fine-tuning setup.

*How it works: The model is shown input-output examples and trained to imitate the desired output.*

*Why important: This is the simplest and most practical starting point.*

---

**C. Full-Parameter Fine-Tuning** — All model weights are updated.

*How it works: The entire model is trainable during adaptation.*

*Why important: Powerful, but expensive in compute and memory.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Improves consistency | Requires high-quality data |
| Improves style following | Can overfit small datasets |
| Improves task-specific response patterns | Can be expensive |
| Can improve structured output behavior | May not help with fresh or private knowledge unless combined with RAG |

---

### 2. Instruction Tuning

**Dataset format:** instruction → input → output

```json
{
  "instruction": "Analyze stock trend",
  "input": "MA20 > MA50, volume rising",
  "output": "This suggests a bullish trend because short-term momentum is stronger than long-term trend and rising volume supports the move."
}
```

#### Beginner Explanation

Instruction tuning is a special kind of fine-tuning where the model learns to follow instructions better.

Instead of just learning raw text continuation, the model learns examples like:

- user asks something
- model should answer in a desired way

This is one of the main reasons modern LLMs feel more helpful than plain base models.

#### Why Instruction Tuning Matters

Instruction tuning helps the model become better at:

- following user requests
- using the right tone
- giving structured answers
- staying task-focused
- behaving consistently across tasks

#### Step-by-Step Mental Model

1. **Define the task behavior** — explanation style, format consistency, safer refusals, better classification wording.
2. **Write many good examples** — Examples must show the exact style and quality you want.
3. **Train the model on those examples** — The model learns the mapping from instruction/input to output.
4. **Test on new instructions** — The real question is whether it generalized, not whether it memorized training examples.

#### Important Algorithms / Mechanisms

**A. Sequence-to-Sequence Supervision** — The model learns to produce the target output conditioned on instruction and input.

*Why important: This is the core training behavior in instruction tuning.*

---

**B. Teacher Forcing** — During training, the model is guided using the true target sequence.

*How it works: Instead of relying fully on its own generated previous token during training, it learns from the true sequence.*

*Why important: Makes learning more stable and efficient.*

---

**C. Cross-Entropy Loss** — Used to measure how well the model predicts the correct output tokens.

*Why important: This is the usual objective for language-model fine-tuning.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Improves instruction following | Bad examples teach bad behavior |
| Improves output consistency | Inconsistent examples confuse the model |
| Very useful for domain-specific assistants | Small datasets can lead to brittle improvements |

---

### 3. LoRA (Low-Rank Adaptation)

Instead of updating the full model:

- **freeze** base model
- **train** small additional layers

| Benefit | Description |
|---|---|
| Faster | Fewer parameters to update |
| Cheaper | Less compute required |
| Less memory | Smaller training footprint |

#### Beginner Explanation

LoRA keeps the base model frozen and learns a small set of extra trainable parameters.

This makes tuning much cheaper. That is why LoRA is widely used for:

- LLM adaptation
- domain-specific tuning
- local experimentation
- budget-friendly fine-tuning

#### Why LoRA Matters

Large models can be too expensive to fine-tune fully.

LoRA says: *"Do not change everything. Learn a small set of adjustment matrices instead."*

This lets you adapt large models with much less memory and storage.

#### Simple Mental Model

- **Full fine-tuning** — changes the whole machine.
- **LoRA** — adds a small "adapter" that nudges the machine's behavior without rebuilding everything.

#### Step-by-Step Mental Model

1. **Load the pre-trained model** — This model stays mostly frozen.
2. **Insert LoRA adapters into selected layers** — Usually attention layers or other important linear modules.
3. **Train only adapter parameters** — Base weights remain fixed.
4. **Use the adapted model at inference time** — The adapter changes how the frozen base behaves.

#### Important Algorithms / Mechanisms

**A. Low-Rank Matrix Decomposition** — Core LoRA idea.

*How it works: Instead of learning a full update matrix, LoRA learns two smaller low-rank matrices whose product approximates the update.*

*Why important: This drastically reduces trainable parameter count.*

---

**B. Frozen Base Model + Trainable Adapters** — The original model weights are not updated.

*Why important: This lowers memory use and makes training more efficient.*

---

**C. Rank Hyperparameter** — LoRA uses a rank value that controls adapter capacity.

*Why important: Higher rank can model more complex updates, but costs more memory.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Far cheaper than full fine-tuning | May not match full fine-tuning on every task |
| Easier to run on limited hardware | Still depends heavily on dataset quality |
| Easy to store and swap adapters | Wrong rank or target layers can hurt results |
| Practical for experimentation | |

---

### 4. QLoRA

Optimized LoRA with:

- **quantization**
- even lower memory usage

#### Beginner Explanation

QLoRA takes the LoRA idea and makes it even more memory-efficient.

It uses quantization so the base model weights are stored in a lower-precision format, while still training LoRA adapters on top.

This means you can fine-tune bigger models on smaller hardware.

#### Simple Mental Model

| Method | What it does |
|---|---|
| **LoRA** | Freeze big model, train small adapters |
| **QLoRA** | Compress the frozen base model + train small adapters = save even more memory |

#### Important Algorithms / Mechanisms

**A. Quantization** — Store weights in lower precision (often 4-bit or related efficient formats).

*How it works: Weights use fewer bits, reducing memory footprint.*

*Why important: This is the key reason QLoRA can run larger models on smaller hardware.*

---

**B. Quantized Base + LoRA Adapters** — The base model is compressed, but adapters remain trainable.

*Why important: Combines memory efficiency with task adaptation.*

---

**C. Paged Optimizers / Memory Management Tricks** — QLoRA implementations often use memory-saving optimizer and paging strategies.

*Why important: Large-model fine-tuning is constrained not just by model size, but also by optimizer and activation memory.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Very memory efficient | Setup can be more complex |
| Enables tuning of larger models | Quantization tradeoffs can affect stability or quality |
| Practical for limited hardware environments | Still not a substitute for good dataset design |

---

### 5. Distillation

Train a **smaller model** using outputs from a **larger model**.

**Goal:** reduce cost and improve speed.

#### Beginner Explanation

Distillation transfers useful behavior from a bigger model to a smaller model.

| Model | Characteristics |
|---|---|
| **Teacher** | Strong but expensive |
| **Student** | Weaker but cheaper |

**Goal:** Make student imitate teacher as much as practical.

#### Why Distillation Matters

In production, the best model is not always the biggest one. Sometimes you want:

- lower latency
- lower cost
- on-device inference
- higher throughput

Distillation helps you keep some of the bigger model's quality while reducing deployment cost.

#### Step-by-Step Mental Model

1. **Use teacher model to generate outputs** — The teacher answers examples.
2. **Collect teacher outputs** — labels, probabilities, full responses, or explanations.
3. **Train student model on this signal** — The student learns from teacher behavior.
4. **Evaluate whether the student is good enough** — The point is useful cost-quality tradeoff, not perfect imitation.

#### Important Algorithms / Mechanisms

**A. Teacher-Student Training** — Core distillation setup.

*How it works: A stronger model produces supervision for a smaller model.*

*Why important: This is the foundation of distillation.*

---

**B. Soft Targets** — Instead of only using hard labels, the student can learn from the teacher's probability distribution.

*Why important: Soft targets contain richer information than a simple correct/incorrect label.*

---

**C. Temperature Scaling in Distillation** — A temperature parameter smooths probabilities from the teacher.

*Why important: This can make the teacher's signal more informative for the student.*

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|---|---|
| Reduces inference cost | Student still has limited capacity |
| Improves speed | Quality drop is common |
| Useful for deployment and scaling | Teacher errors can be transferred too |
| Can make smaller models surprisingly strong | |

---

### 6. Fine-Tuning vs RAG

| Method | Purpose |
|---|---|
| **Fine-tuning** | Change behavior |
| **RAG** | Add knowledge |

> **Important:** Do NOT use fine-tuning to add knowledge → use RAG

#### Beginner Explanation

**Use fine-tuning when you want the model to:**

- answer in a certain format
- behave more consistently
- follow your style
- perform a narrow task better

**Use RAG when you want the model to:**

- access private documents
- know recent information
- answer from changing knowledge
- cite real sources

#### Simple Rule

> Use fine-tuning to **change behavior**.
> Use RAG to **provide knowledge**.

#### Examples

| Fine-Tuning Use Cases | RAG Use Cases |
|---|---|
| Make outputs always follow financial report schema | Answer from your policy documents |
| Improve support-ticket classification style | Search internal research notes |
| Improve consistency of internal analysis tone | Answer questions about changing market reports |
| | Retrieve product documentation |

#### Practical Rule for Beginners

Before fine-tuning, ask:

- Is my problem really behavior/style/format?
- Or is my problem missing/changing knowledge?
- Can better prompting solve it first?
- Can structured output solve it first?
- Can RAG solve it better?

Often the answer is:

1. **prompting first**
2. **RAG next**
3. **fine-tuning only if still needed**

#### Important Algorithms / Mechanisms

**A. Parametric Memory vs External Memory**

- Fine-tuning changes what is stored in model parameters.
- RAG uses external stored knowledge.

*Why important: Fresh knowledge belongs in external retrieval systems, not buried in weights.*

---

**B. Retrieval-Augmented Inference** — RAG injects current evidence at answer time.

*Why important: This is how systems stay updatable.*

---

**C. Behavior Alignment via Fine-Tuning** — Fine-tuning aligns the style and task behavior of the model.

*Why important: This is why fine-tuning and RAG solve different problems.*

---

## Difficulty Points

### 1. Bad dataset quality

**Why it happens:** Beginners focus on model size or training scripts, but the real problem is low-quality examples.

Examples of bad data: inconsistent outputs, weak instructions, wrong answers, mixed styles, duplicate examples, low-information examples.

**Why it is a problem:** Bad data teaches bad style, bad structure, bad reasoning patterns, and inconsistency.

**Fix strategy:** Create clear examples, keep output style consistent, remove duplicates and weak examples, review samples manually, start with a small high-quality dataset before growing larger.

### 2. Confusing behavior vs knowledge

**Why it happens:** It feels intuitive to "teach the model facts" by fine-tuning.

**Why it is a problem:** Facts change. Private knowledge changes. New documents appear. Fine-tuning is bad at staying current on changing knowledge.

**Fix strategy:** Use fine-tuning for behavior/style/task pattern. Use RAG for fresh, private, or changing knowledge.

### 3. Overfitting small dataset

**Why it happens:** Small datasets make the model memorize examples instead of learning reusable patterns.

**Why it is a problem:** The model may look better on seen prompts but fail on unseen prompts.

**Fix strategy:** Keep a validation/test split, evaluate on unseen prompts, reduce training intensity if overfitting, increase example variety, use LoRA carefully rather than assuming it prevents overfitting automatically.

### 4. Evaluation difficulty

**Why it happens:** Fine-tuning improvements are often subtle — slightly better structure, slightly better tone, slightly better consistency.

**Why it is a problem:** Without evaluation, you may think the tuned model is better when it is not.

**Fix strategy:** Compare base model vs tuned model on the same prompts and same evaluation rubric. Track format accuracy, task correctness, consistency, and latency/cost if relevant.

### 5. Expecting huge improvement

**Why it happens:** People expect fine-tuning to completely transform the model.

**Why it is a problem:** Unrealistic expectations lead to disappointment and poor decisions.

**Fix strategy:** Expect fine-tuning to improve consistency, style, narrow-task behavior, and format adherence — not to solve all reasoning, knowledge, or system-design problems.

### 6. Mixing multiple goals in one dataset

**Why it happens:** Beginners try to teach style, classification, extraction, reasoning, and safety behavior all at once in a tiny dataset.

**Why it is a problem:** The model receives mixed signals and improvements become hard to measure.

**Fix strategy:** Choose one main goal per fine-tuning experiment.

*Example:*

- experiment A = structured financial summary
- experiment B = safer refusal behavior
- experiment C = classification style

### 7. No baseline comparison

**Why it happens:** People start tuning without properly testing the base model.

**Why it is a problem:** You do not know whether tuning actually helped.

**Fix strategy:** Always save baseline outputs on a held-out evaluation set before tuning.

---

## Fine-Tuning Workflow (Real World)

1. Define the behavior goal
2. Decide whether fine-tuning is actually needed
3. Choose base model
4. Design dataset format
5. Collect and clean examples
6. Split train / validation / test
7. Choose tuning method (full / LoRA / QLoRA)
8. Train carefully
9. Evaluate base vs tuned model
10. Inspect failure cases
11. Improve data or setup
12. Save artifacts and document results

### Beginner Explanation of Each Step

1. **Define the behavior goal** — Be specific. *Bad: "Make model better." Good: "Make model produce a consistent financial analysis JSON schema."*
2. **Decide whether fine-tuning is actually needed** — Try prompting, structured output, and RAG first when appropriate.
3. **Choose base model** — Pick a model that already fits your task size and hardware budget.
4. **Design dataset format** — For instruction tuning, define instruction, input, and output.
5. **Collect and clean examples** — Quality matters more than raw quantity early on.
6. **Split train / validation / test** — You need unseen evaluation data.
7. **Choose tuning method** — full fine-tuning (expensive), LoRA (practical), QLoRA (more memory-efficient).
8. **Train carefully** — Watch loss, memory usage, and training stability.
9. **Evaluate base vs tuned model** — Use the same held-out prompts.
10. **Inspect failure cases** — Do not trust only averages.
11. **Improve data or setup** — Often the dataset is the main bottleneck.
12. **Save artifacts and document results** — Keep dataset version, prompt format, hyperparameters, evaluation outputs, and final adapter/checkpoint.

---

## Debugging Checklist for Stage 8

If the fine-tuned model is disappointing, check:

- [ ] Is fine-tuning actually the right solution, or should this be RAG?
- [ ] Is the dataset high quality?
- [ ] Are outputs consistent in style and structure?
- [ ] Are train / validation / test separated properly?
- [ ] Did you compare against the base model fairly?
- [ ] Is the model overfitting?
- [ ] Is the training objective aligned with your real task?
- [ ] Did you try too many goals in one dataset?
- [ ] Is LoRA rank / target module choice reasonable?
- [ ] Is your evaluation set representative?
- [ ] Are you measuring behavior change or just subjective impressions?
- [ ] Would better prompting solve the problem more cheaply?

---

## Practice Project

### Project: Financial Instruction-Tuned Model

**Goal:** Train a model to analyze financial signals and produce structured outputs.

You are not only trying to "fine-tune a model." You are learning:

- dataset design
- behavior targeting
- adapter-based tuning
- fair evaluation
- realistic expectations

**Step 1 — Define goal**

Good goals:

- "Always return JSON with trend, risk, and recommendation"
- "Explain technical indicators in beginner-friendly language"
- "Classify market condition into bullish / neutral / bearish with one-sentence rationale"

*Bad goal: "Make it smarter"*

*Why this step matters: If the goal is vague, the dataset will be vague.*

---

**Step 2 — Create dataset**

Create 50–200 examples:

```json
{
  "instruction": "Analyze the stock setup and return structured output.",
  "input": "MA20 > MA50, RSI=68, volume rising, price above resistance",
  "output": "{\"trend\":\"bullish\",\"risk\":\"moderate\",\"reason\":\"Short-term trend is above long-term trend, momentum is strong, and rising volume confirms the move.\"}"
}
```

Your examples should be: consistent, realistic, representative, and varied enough to avoid memorization.

Include: bullish examples, bearish examples, neutral examples, edge cases, and ambiguous cases.

*Why this step matters: The dataset teaches the model what "good behavior" means.*

---

**Step 3 — Save dataset**

```
data/processed/dataset.jsonl
```

Also save: dataset version, train/val/test split files, and example generation notes.

*Why this step matters: A clean dataset file makes training repeatable.*

---

**Step 4 — Train with LoRA**

Use HuggingFace + PEFT.

What to monitor:

- training loss
- validation loss
- GPU memory
- time per step
- whether outputs become more consistent

*Why this step matters: LoRA is the most practical starting point for beginners — cheaper and more realistic for local or limited-budget tuning.*

---

**Step 5 — Evaluate**

Compare base model vs fine-tuned model on unseen prompts.

Evaluation dimensions:

- structure consistency
- domain style
- correctness
- refusal behavior if relevant
- output stability
- whether improvement holds on unseen prompts

*Why this step matters: Without direct comparison, tuning results are meaningless.*

---

**Step 6 — Analyze results**

Better analysis questions:

- Did JSON validity improve?
- Did explanations become more consistent?
- Did accuracy improve on held-out cases?
- Did the model become too repetitive?
- Did it overfit the exact examples?

*Why this step matters: A model can improve in one dimension and get worse in another.*

### Deliverables

- dataset
- training script
- evaluation results
- README

### Experiment Tasks

**Experiment 1 — Base vs tuned comparison**

Run the same evaluation prompts on base model and LoRA-tuned model.

- Lesson: Never assume tuning helps without comparison.

**Experiment 2 — Small dataset vs better dataset**

Try a quick weak dataset vs a smaller but better curated dataset.

- Lesson: Quality often beats quantity early on.

**Experiment 3 — One-goal dataset vs mixed-goal dataset**

Compare pure structured-finance-output dataset vs mixed finance + summarization + extraction dataset.

- Lesson: Single-goal tuning is easier to evaluate and often works better.

**Experiment 4 — LoRA rank comparison**

Try two or three rank settings.

- Lesson: Adapter capacity affects behavior and cost.

**Experiment 5 — Fine-tuning vs prompt engineering**

See whether a strong prompt plus base model can already solve much of the task.

- Lesson: Fine-tuning should justify its extra complexity.

**Experiment 6 — Fine-tuning vs RAG**

Ask a knowledge-fresh task and compare tuned model only vs RAG system.

- Lesson: Fresh knowledge problems are usually better solved with retrieval.

**Experiment 7 — Distillation-style mini experiment**

Use a stronger model to generate higher-quality target outputs for a small student-training dataset.

- Lesson: Teacher quality influences student quality.

### Common Mistakes

1. **Weak dataset** — Examples are inconsistent, vague, or low quality. *Fix: Improve dataset quality before changing training setup.*

2. **No evaluation** — You cannot tell whether improvement is real. *Fix: Create a held-out prompt set and compare base vs tuned outputs systematically.*

3. **Mixing multiple goals** — Results become noisy and hard to interpret. *Fix: Tune for one main behavior goal at a time.*

4. **Expecting knowledge updates** — The model still will not be a reliable source of fresh, changing facts. *Fix: Use RAG for fresh/private/changing knowledge.*

5. **Overfitting on small data** — The model memorizes instead of generalizing. *Fix: Use better data variety and evaluate on unseen prompts.*

6. **No baseline saved** — You lose the ability to measure improvement fairly. *Fix: Record base-model outputs first.*

7. **Choosing fine-tuning when prompting is enough** — You add cost and complexity unnecessarily. *Fix: Try prompting and structured output first.*

---

## Final Understanding

> Fine-tuning improves **how** a model responds, while RAG improves **what** it knows.

> Fine-tuning is mainly about behavior adaptation, not magical knowledge updates.

> The biggest determinants of success are usually **goal clarity**, **dataset quality**, and **fair evaluation**.

---

## Self Test

### Questions

1. What is fine-tuning?
2. Why is fine-tuning different from training from scratch?
3. What kinds of problems is fine-tuning good for?
4. What is instruction tuning?
5. What fields usually appear in an instruction-tuning dataset?
6. Why is instruction tuning useful for LLM behavior?
7. What is supervised fine-tuning?
8. What is cross-entropy loss used for in language-model fine-tuning?
9. What is LoRA?
10. Why is LoRA cheaper than full fine-tuning?
11. What does "freeze the base model" mean?
12. What is the meaning of "low-rank" in LoRA?
13. What is QLoRA?
14. Why does quantization help in QLoRA?
15. What is distillation?
16. What is the teacher-student idea in distillation?
17. Why are soft targets useful in distillation?
18. What is the main difference between fine-tuning and RAG?
19. Why should you not use fine-tuning to add fresh knowledge?
20. What kind of goal is a good candidate for fine-tuning?
21. Why is dataset quality so important in fine-tuning?
22. Why can small datasets cause overfitting?
23. Why is evaluation difficult in fine-tuning?
24. Why should you compare base and tuned models on the same prompts?
25. What is a common mistake when beginners build a fine-tuning dataset?
26. Why should you usually try prompting before fine-tuning?
27. What should you save besides the final tuned adapter or checkpoint?
28. Why can a tuned model still fail on unseen prompts?
29. What is one main reason fine-tuning projects disappoint?
30. What is the main lesson of this stage?

### Answers

1. Fine-tuning is adapting a pre-trained model to behave better on a specific task using additional training data.

2. Because the model already has learned general language or task patterns, and you are only adapting it further instead of starting with random weights.

3. It is good for improving style, consistency, output format, instruction following, and narrow task behavior.

4. Instruction tuning is fine-tuning a model on examples formatted as instructions plus inputs plus desired outputs.

5. Usually instruction, input, and output.

6. Because it teaches the model how to respond to user instructions in a more consistent and useful way.

7. It is fine-tuning where the model is trained directly on input-output examples with known target responses.

8. It measures how well the model predicts the correct target tokens during training.

9. LoRA is a parameter-efficient fine-tuning method that freezes the base model and trains small low-rank adapters instead.

10. Because it updates far fewer parameters and uses less memory and compute.

11. It means the original model weights are not updated during training.

12. It means the update is represented using smaller matrices that approximate a full update more efficiently.

13. QLoRA is a more memory-efficient version of LoRA that uses quantized base-model weights.

14. Because lower-precision weights take much less memory.

15. Distillation is training a smaller model to imitate a larger teacher model.

16. A stronger teacher model provides supervision that helps a smaller student model learn better behavior.

17. Because they contain richer information than just hard labels and reveal how the teacher distributes confidence.

18. Fine-tuning changes model behavior through training, while RAG adds external knowledge at inference time.

19. Because model weights are not a reliable or updatable way to handle changing, recent, or private knowledge.

20. A behavior goal such as better structure, better style consistency, or better domain-specific instruction following.

21. Because the model learns directly from those examples, so poor examples teach poor behavior.

22. Because the model may memorize the examples instead of learning a reusable pattern.

23. Because improvements are often subtle and can be mistaken for success without fair comparison.

24. Because otherwise the comparison is unfair and you cannot measure real improvement.

25. They mix too many different goals into one small dataset.

26. Because prompting is cheaper, simpler, and often enough to solve the problem.

27. You should save dataset versions, train/validation/test splits, hyperparameters, prompts, evaluation outputs, and experiment notes.

28. Because it may overfit the training examples or the dataset may not cover enough variation.

29. Poor dataset quality or unclear goals.

30. Fine-tuning is a tool for behavior adaptation, not a universal solution, and success depends on clear goals, strong data, and honest evaluation.

---

## What You Must Be Able To Do After Stage 8

- [ ] Explain what fine-tuning is in plain English
- [ ] Explain instruction tuning, LoRA, QLoRA, and distillation at a beginner level
- [ ] Distinguish full fine-tuning from adapter-based tuning
- [ ] Explain why fine-tuning changes behavior more than knowledge freshness
- [ ] Decide when to use prompting, RAG, or fine-tuning
- [ ] Design a simple instruction-tuning dataset
- [ ] Compare a base model and a tuned model fairly
- [ ] Identify overfitting and weak-data problems
- [ ] Understand that evaluation is mandatory, not optional
- [ ] Treat fine-tuning as a targeted engineering tool, not magic
