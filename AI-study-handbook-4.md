# Stage 4 — Deep Learning

*(Week 7–9)*

## Goal

Understand neural networks and how deep learning works.

You are **NOT** just using libraries.
You are learning:

- how neural networks compute
- how training works
- why models fail or succeed

This stage is where you move from:

> "I can run a PyTorch tutorial"

to:

> "I understand what a neural network is doing, how it learns, why training fails, and how to debug it."

---

## Quick Summary

Deep learning is a way to learn complex functions using many layers of computation.

A neural network:

- takes input data
- transforms it through layers
- produces an output
- compares output with the correct answer
- computes error
- updates weights to reduce that error

A beginner should finish this stage understanding:

- what a neural network is
- what a neuron does
- what a forward pass is
- what a loss function does
- what backpropagation is
- what an optimizer does
- why GPUs matter
- why shapes, gradients, and learning rates are so important

---

## Study Materials

**FastAI Course**
https://course.fast.ai/

**PyTorch Tutorial**
https://pytorch.org/tutorials/

### Topics

- Neural Networks
- Backpropagation
- CNN
- RNN
- Transformers

---

## Key Knowledge (Deep Understanding)

### 1. What is a Neural Network

A neural network is a function made of layers:

```
input → hidden layers → output
```

Each layer:

- multiplies inputs by weights
- adds bias
- applies activation

#### Beginner Explanation

A neural network is just a more flexible function.

In earlier ML, you saw models like:

```
y = wx + b
```

A neural network does something similar, but with many steps and many parameters.

It takes input data, passes it through layers, and gradually transforms it into something useful for prediction.

| Input | Output |
|---|---|
| image | digit label |
| text | sentiment |
| stock features | prediction |
| audio | transcription |

**The key idea:** A neural network learns many small transformations that together create a powerful model.

#### Step-by-Step Mental Model

1. **Input enters the network** — an image, a vector of features, or a sequence of token IDs.
2. **First layer transforms the input** — combines values using weights and bias.
3. **Activation adds nonlinearity** — helps the model learn more than simple straight-line relationships.
4. **More layers repeat the process** — each layer transforms the representation further.
5. **Final layer produces output** — class scores, probability, next token, or numeric value.

#### Why Deep Learning Matters

Traditional ML often depends heavily on manual feature engineering.

Deep learning can learn useful intermediate representations automatically.

*Example: For images, instead of manually coding "edge detector," the network can learn edge-like features itself.*

#### Key Algorithms / Mechanisms

**A. Multilayer Perceptron (MLP)** — The standard fully connected neural network.

How it works:

1. Input enters the first layer
2. Each neuron computes weighted sum + bias
3. Activation is applied
4. Result passes to the next layer
5. Final layer produces prediction

*Why important: This is the simplest deep learning architecture and the foundation for understanding deeper models.*

---

**B. Feedforward Computation** — The basic computation pattern of many neural networks.

*How it works: Data moves from input to output without looping backward in the computation graph during inference.*

*Why important: This is how predictions are computed before learning happens.*

---

**C. Layered Representation Learning** — Each layer learns a new representation of the input.

Example in images:

- early layers: edges
- middle layers: shapes
- later layers: object parts
- final layers: object identity

*Why important: This is one of the main powers of deep learning.*

---

### 2. Neuron (Core Unit)

```
output = activation(weight * input + bias)
```

**Common activation:** ReLU

#### Beginner Explanation

A neuron receives inputs, multiplies them by weights, adds them together, adds a bias, and passes the result through an activation function.

With multiple inputs:

```
z = w1x1 + w2x2 + w3x3 + ... + b
output = activation(z)
```

- **Weights** — determine how important each input is
- **Bias** — shifts the result
- **Activation function** — makes the network nonlinear

#### Why Activation Matters

Without activation functions, stacking layers would still behave like a simple linear model — making deep networks much less useful.

Activation functions let networks learn curves, nonlinear boundaries, and complex patterns.

#### Key Algorithms / Mechanisms

**A. Weighted Sum**

```
z = Wx + b
```

*How it works: Each input is multiplied by a learned weight, then summed, then bias is added.*

*Why important: This is the base mathematical transformation inside neural networks.*

---

**B. ReLU (Rectified Linear Unit)**

```
ReLU(x) = max(0, x)
```

- Negative values become 0
- Positive values stay the same

*Why important: Simple, fast, and works very well in many deep networks.*

---

**C. Sigmoid** — Maps values into 0–1.

- Very negative → near 0
- Very positive → near 1

*Why important: Historically important and still useful for binary output probabilities.*

---

**D. Tanh** — Maps values to -1 to 1.

*Like sigmoid, but centered around zero. Historically used in older networks and sometimes still useful.*

---

### 3. Forward Pass

```
input → layers → output
```

#### Beginner Explanation

The forward pass is the process of **making a prediction**.

This happens before learning. No learning happens yet — learning comes later when the model compares its prediction with the correct answer.

#### Step-by-Step Example

Handwritten digit classification:

1. **Input image** — A 28×28 image is given.
2. **Flatten or process through layers** — The network converts raw pixels into intermediate values.
3. **Hidden layers compute features** — The network transforms raw input into more useful internal representations.
4. **Output layer produces scores** — For 10 digit classes (0–9), the model outputs 10 scores.
5. **Prediction is chosen** — Usually the class with highest score is predicted.

#### Key Algorithms / Mechanisms

**A. Matrix Multiplication** — Most deep learning layers use matrix multiplication.

*How it works: Input vectors are multiplied by weight matrices to produce outputs.*

*Why important: This is why GPUs help so much.*

---

**B. Activation Application** — After linear transformation, activation is applied element-wise.

*Why important: Adds nonlinearity and expressive power.*

---

**C. Softmax** — Common output function for multi-class classification.

*How it works: Takes a vector of scores and converts them into probabilities that sum to 1.*

*Why important: Useful for interpreting class outputs.*

---

### 4. Loss Function

Measures error between prediction and actual value.

| Task | Common Loss |
|---|---|
| Regression | MSE |
| Multi-class classification | Cross-Entropy |
| Binary classification | Binary Cross-Entropy |

#### Beginner Explanation

A loss function tells the model how wrong it is.

Without loss, the network has no idea whether its prediction was good or bad. **Loss is the signal that drives learning.**

- If the model predicts "cat" but the correct answer is "dog" → loss should be high.
- If the prediction is correct and confident → loss should be lower.

> Training is basically: keep changing weights to reduce loss.

#### Key Algorithms / Mechanisms

**A. Mean Squared Error (MSE)** — Used for regression.

1. Subtract prediction from actual value
2. Square the difference
3. Average over examples

*Why important: Penalizes large numeric errors strongly.*

---

**B. Cross-Entropy Loss** — Used for classification.

- Compares predicted probabilities to the true class
- Heavily penalizes confident wrong predictions

*Why important: Standard for training classifiers.*

---

**C. Binary Cross-Entropy** — Used for binary classification.

*Measures error for yes/no probability output. Common for tasks like spam detection or fraud detection.*

---

### 5. Backpropagation

**Core idea:** Adjust weights to reduce loss.

Steps:

1. Compute loss
2. Compute gradients
3. Update weights

#### Beginner Explanation

Backpropagation tells each weight how much it contributed to the error, then weights are adjusted.

This is not magic. It is **chain-rule-based gradient computation** through the network.

#### Step-by-Step Mental Model

1. **Do a forward pass** — Compute the prediction.
2. **Compute the loss** — Compare prediction with truth.
3. **Compute gradients** — Figure out how changing each weight would change the loss.
4. **Send gradient information backward** — Start from the output and propagate sensitivity backward through the network.
5. **Use gradients to update weights** — Optimizer changes parameters in a direction that reduces error.

#### Why Backpropagation Matters

Without backpropagation, deep networks would not know how to improve internal layers. It lets even very deep models learn from output error.

#### Key Algorithms / Mechanisms

**A. Chain Rule** — The math foundation of backpropagation.

*How it works: If A affects B and B affects C, then A affects C through B.*

*Why important: Lets gradients flow through many layers.*

---

**B. Gradient Computation** — The derivative tells how much loss changes if a weight changes slightly.

*Why important: This gives the direction for weight updates.*

---

**C. Automatic Differentiation** — Modern frameworks like PyTorch compute gradients automatically.

*How it works: They record operations during the forward pass and then compute derivatives during backward pass.*

*Why important: You do not manually derive gradients for every model.*

---

### 6. Optimizer

Controls how weights update.

| Optimizer | Description |
|---|---|
| SGD | Simple, foundational |
| Adam | Adaptive, popular default |

#### Beginner Explanation

The optimizer is the rule for updating parameters after gradients are computed.

- **Gradients** = information about slope
- **Optimizer** = movement strategy

#### Key Algorithms / Mechanisms

**A. SGD (Stochastic Gradient Descent)** — Simple optimizer.

*How it works: Update parameters a little in the negative gradient direction.*

*Why important: The basic foundation of optimization in deep learning.*

---

**B. Momentum** — Enhancement to SGD.

*How it works: Keeps some memory of past updates to smooth movement and speed training.*

*Why important: Helps avoid zig-zagging and can accelerate convergence.*

---

**C. Adam** — Very popular optimizer.

*How it works: Combines momentum-like behavior with adaptive learning rates per parameter.*

*Why important: Usually works well out of the box for many problems.*

---

**D. Learning Rate** — The most important optimizer setting.

*Controls step size of parameter updates.*

| Setting | Effect |
|---|---|
| Too large | Unstable training |
| Too small | Very slow learning |

---

### 7. Why GPU is Needed

Deep learning uses large matrices and parallel operations. GPUs accelerate matrix multiplication.

#### Beginner Explanation

- **CPUs** — General-purpose, great for many tasks.
- **GPUs** — Built to do many similar numeric operations in parallel.

Neural networks do many operations in parallel: matrix multiplication, convolution, batched computation. GPUs are much faster for this.

#### Key Mechanisms

**A. Parallel Matrix Math** — Neural networks are built around large batches of matrix operations.

*Why important: GPUs are optimized for this exact pattern.*

---

**B. Batch Processing** — Training often processes many examples at once.

*Why important: GPUs can apply the same computation to many examples in parallel.*

---

**C. Tensor Operations** — Frameworks represent data as tensors and run fast tensor operations on GPUs.

*Why important: Modern deep learning performance depends heavily on efficient tensor math.*

---

### 8. CNN (Convolutional Neural Networks)

Designed especially for **grid-like data** such as images.

#### Beginner Explanation

Instead of connecting every input pixel to every neuron immediately, CNNs use filters that slide across the image.

This helps the network learn local patterns such as edges, corners, textures, and shapes.

#### Step-by-Step Mental Model

1. **Input image enters the network** — e.g., handwritten digit image.
2. **Convolution filters scan across image** — Each filter detects a certain visual pattern.
3. **Activation is applied** — Useful signals are kept and transformed.
4. **Pooling may reduce size** — Compresses information while keeping important patterns.
5. **Deeper layers learn more complex features** — Early layers detect edges, later layers detect shapes or objects.
6. **Final classifier predicts label** — The learned visual features are used to classify the image.

#### Key Algorithms / Mechanisms

**A. Convolution** — Core CNN operation.

*How it works: A small filter slides across the image and computes local weighted sums.*

*Why important: Lets the model detect local patterns efficiently.*

---

**B. Pooling**

- Max pooling
- Average pooling

*How it works: Reduces spatial size by summarizing local areas.*

*Why important: Makes computation cheaper and helps create some spatial robustness.*

---

**C. Shared Weights** — The same filter is reused across different image locations.

*Why important: Greatly reduces parameter count and helps detect the same feature anywhere in the image.*

---

### 9. RNN (Recurrent Neural Networks)

Designed for **sequence data**.

#### Beginner Explanation

RNNs process input one step at a time and keep a **hidden state** that carries information forward — giving them a kind of memory across sequence positions.

Used for: text, time series, speech.

#### Step-by-Step Mental Model

1. **Read first element** — e.g., first word in a sentence.
2. **Update hidden state** — The model stores information from what it has seen so far.
3. **Read next element** — Combines new input with previous hidden state.
4. **Repeat** — Information flows through the sequence.

#### Key Algorithms / Mechanisms

**A. Hidden State Update** — The model keeps an internal state over time.

*Why important: This is how it remembers previous inputs.*

---

**B. Vanilla RNN** — Basic recurrent architecture.

*Conceptually simple, but struggles with long dependencies.*

---

**C. LSTM (Long Short-Term Memory)** — Uses gates to control what to remember, forget, and output.

*Why important: Helps solve vanishing-gradient problems better than vanilla RNN.*

---

**D. GRU (Gated Recurrent Unit)** — A simpler gated recurrent architecture than LSTM.

*Why important: Often performs well with less complexity.*

---

### 10. Transformers

The **dominant** deep learning architecture for language and many other modalities.

#### Beginner Explanation

Transformers replaced RNNs for many tasks because they:

- handle long-range relationships better
- train more efficiently in parallel

Instead of reading tokens one by one with a hidden state, transformers use **attention** to let each token look at other relevant tokens directly.

*Example:*

> "The animal didn't cross the street because **it** was too tired."

The word "it" should relate to "animal," not "street." Attention helps the model learn this connection.

#### Step-by-Step Mental Model

1. **Convert tokens into embeddings** — Words become vectors.
2. **Add positional information** — The model needs to know token order.
3. **Compute attention** — Each token compares itself with others to decide what matters.
4. **Mix information across tokens** — Relevant token information is combined.
5. **Pass through feed-forward layers** — Representations are refined.
6. **Repeat through many layers** — The model builds richer contextual understanding.

#### Key Algorithms / Mechanisms

**A. Self-Attention** — Core transformer operation.

*How it works: Each token computes relationships with other tokens and weighs them by importance.*

*Why important: Lets the model capture long-range dependencies directly.*

---

**B. Query, Key, Value (QKV)** — The internal mechanism of attention.

- **Query** — asks: what am I looking for?
- **Key** — says: what information do I contain?
- **Value** — says: what information should be passed along?

*Why important: This is how attention scores are computed and used.*

---

**C. Multi-Head Attention** — Uses multiple attention mechanisms in parallel.

*Why important: Different heads can focus on different types of relationships.*

---

**D. Positional Encoding** — Adds order information to token representations.

*Why important: Attention alone does not know token order unless position is added.*

---

## Difficulty Points

### 1. Understanding backpropagation

**Why it happens:** Gradients are abstract and involve derivatives across many layers.

**Why it is a problem:** If you treat backpropagation as magic, debugging becomes much harder.

**Fix strategy:** Use this mental model:

- forward pass = prediction
- loss = how wrong
- backward pass = who caused the error and by how much

Start with intuition, then later learn derivatives more deeply.

### 2. Debugging training

**Why it happens:** Many parts can fail — data, labels, shape, learning rate, optimizer, bad loss, wrong output activation.

**Fix strategy:** Check in this order:

1. data loads correctly
2. labels are correct
3. shapes are correct
4. loss decreases
5. gradients are nonzero
6. model can overfit a tiny batch
7. evaluation code is correct

### 3. Shape mismatch errors

**Why it happens:** Deep learning uses tensors with dimensions like batch, channels, height, width, sequence length, embedding dim. Beginners lose track of tensor shapes.

**Why it is a problem:** The code crashes or silently behaves incorrectly.

**Fix strategy:** Always print and verify input shape, output shape, and label shape. Keep a notebook of expected tensor shapes for each layer.

### 4. Overfitting in neural networks

**Why it happens:** Neural networks often have many parameters and strong capacity.

**Fix strategy:** Use more data, data augmentation, regularization, dropout, early stopping, a smaller model, or validation monitoring.

### 5. Learning rate problems

| Setting | Effect |
|---|---|
| Too high | Unstable |
| Too low | Slow learning |

**Fix strategy:** Try smaller or larger learning rates, learning-rate schedules, Adam as a practical baseline, and plot loss curves to observe instability.

### 6. Forgetting training vs evaluation mode

**Why it happens:** Beginners focus on model definition and training loop, but forget mode switching.

**Why it is a problem:** Layers like dropout and batch norm behave differently in training and evaluation.

**Fix strategy:**

```python
model.train()   # during training
model.eval()    # during evaluation
```

### 7. Not monitoring loss and metrics over time

**Why it happens:** People only look at the final result.

**Why it is a problem:** You miss signs of divergence, overfitting, stagnation, or unstable training.

**Fix strategy:** Track train loss, validation loss, train metric, and validation metric — per epoch.

---

## Deep Learning Workflow (Real World)

1. Define task
2. Prepare dataset
3. Build Dataset and DataLoader
4. Define model
5. Define loss
6. Define optimizer
7. Train in epochs
8. Validate regularly
9. Track metrics and curves
10. Tune and improve
11. Save checkpoints
12. Test final model

### Beginner Explanation of Each Step

1. **Define task** — image classification, text classification, sequence prediction, regression.
2. **Prepare dataset** — Make sure inputs and labels are correct.
3. **Build Dataset and DataLoader** — These feed batches of data into training.
4. **Define model** — Choose architecture appropriate for the task.
5. **Define loss** — Pick a loss that matches the problem.
6. **Define optimizer** — Choose how parameters will update.
7. **Train in epochs** — Repeat over the full dataset many times.
8. **Validate regularly** — Check performance on held-out data.
9. **Track metrics and curves** — Use them to understand training behavior.
10. **Tune and improve** — Adjust architecture, learning rate, batch size, etc.
11. **Save checkpoints** — Do not lose progress.
12. **Test final model** — Evaluate after training is finalized.

---

## Debugging Checklist for Stage 4

If your network is not learning, check:

- [ ] Does the dataset load correctly?
- [ ] Are labels correct?
- [ ] Are input and target shapes correct?
- [ ] Is the output layer compatible with the loss?
- [ ] Is loss decreasing at all?
- [ ] Did you call `optimizer.zero_grad()`?
- [ ] Did you call `loss.backward()`?
- [ ] Did you call `optimizer.step()`?
- [ ] Are gradients exploding or vanishing?
- [ ] Is learning rate too high or too low?
- [ ] Did you switch between `train()` and `eval()` correctly?
- [ ] Can the model overfit a tiny subset?

---

## Example Code

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 1)
)
```

**Beginner Walkthrough:**

- `nn.Linear(10, 20)` — takes 10 input features and produces 20 learned hidden values
- `nn.ReLU()` — applies a nonlinear activation
- `nn.Linear(20, 1)` — maps the 20 hidden values to 1 output

This is a very small feedforward neural network. It can be used for a simple regression task if paired with the right loss.

---

## Practice Project

### Project: Neural Network Training Lab

**Goal:** Train a neural network on a simple dataset (MNIST).

You are not only trying to "make it run." You are learning:

- data loading
- batching
- model definition
- loss selection
- optimizer setup
- training loop mechanics
- evaluation
- debugging

**Step 1 — Load dataset**

```python
from torchvision import datasets, transforms

dataset = datasets.MNIST(root="data", download=True, transform=transforms.ToTensor())
```

*Why this step matters: MNIST is a beginner-friendly dataset of handwritten digits, simple enough to learn the training workflow without too much complexity.*

*`ToTensor()` converts image data into PyTorch tensors and scales pixel values into a model-friendly format.*

---

**Step 2 — DataLoader**

```python
from torch.utils.data import DataLoader

loader = DataLoader(dataset, batch_size=64, shuffle=True)
```

- `batch_size=64` — the model processes 64 examples at a time
- `shuffle=True` — helps training by mixing the order of examples

---

**Step 3 — Build model**

```python
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)
```

- `nn.Flatten()` — turns a 28×28 image into a 784-length vector
- First linear layer learns hidden features
- `ReLU` adds nonlinearity
- Final layer outputs 10 scores, one for each digit class

---

**Step 4 — Loss and optimizer**

```python
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

- `CrossEntropyLoss()` — appropriate for multi-class classification
- `Adam` — practical default optimizer
- `lr=0.001` — learning rate

---

**Step 5 — Training loop**

```python
for data, target in loader:
    output = model(data)
    loss = criterion(output, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

Step-by-step:

| Line | Action |
|---|---|
| `output = model(data)` | Do a forward pass |
| `loss = criterion(output, target)` | Compute the error |
| `optimizer.zero_grad()` | Clear old gradients |
| `loss.backward()` | Compute new gradients |
| `optimizer.step()` | Update the weights |

---

**Step 6 — Evaluate**

During evaluation: switch to eval mode, disable gradient tracking, and compute accuracy over the test set.

```python
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for data, target in test_loader:
        output = model(data)
        preds = output.argmax(dim=1)
        correct += (preds == target).sum().item()
        total += target.size(0)

accuracy = correct / total
print(accuracy)
```

### Deliverables

- model code
- training loop
- loss tracking
- results

### Experiment Tasks

**Experiment 1 — Change learning rate**

Try: `0.1`, `0.001`, `0.0001`

- Purpose: See how training stability changes.

**Experiment 2 — Overfit a tiny subset**

Train on a very small number of samples.

- Purpose: Check whether the model and training loop can learn at all.

**Experiment 3 — Remove ReLU**

- Purpose: See how lack of nonlinearity hurts expressiveness.

**Experiment 4 — Compare optimizers**

Try: SGD, Adam.

- Purpose: See how optimization strategy changes learning behavior.

**Experiment 5 — Add validation loss tracking**

- Purpose: Observe overfitting and training progress more clearly.

**Experiment 6 — Increase model size**

Try a larger hidden layer.

- Purpose: See how capacity affects training and overfitting.

### Common Mistakes

1. **Forgetting `zero_grad()`** — Gradients accumulate by default in PyTorch, making updates incorrect. *Fix: Call `optimizer.zero_grad()` before `loss.backward()`.*

2. **Wrong tensor shapes** — Different layers expect specific tensor dimensions, causing runtime errors or incorrect behavior. *Fix: Print tensor shapes often and understand expected layer input/output sizes.*

3. **No evaluation** — You do not know whether the model generalizes. *Fix: Always evaluate on separate data.*

4. **Ignoring loss trends** — You miss unstable learning, stagnation, or divergence. *Fix: Record and plot loss over epochs.*

5. **Wrong loss-output pairing** — Training can fail or behave strangely. *Fix: Know common pairings:*

   | Task | Output + Loss |
   |---|---|
   | Regression | Linear output + MSE |
   | Multi-class classification | Raw logits + CrossEntropyLoss |
   | Binary classification | Sigmoid-style setup + BCE-type loss |

6. **Training forever without validation** — The model may start overfitting. *Fix: Use validation tracking and early stopping logic if needed.*

---

## Final Understanding

> Deep learning trains layered functions using gradient-based optimization to minimize error.

> A neural network is not magic. It is a stack of differentiable computations trained through loss, gradients, and optimization.

---

## Self Test

### Questions

1. What is a neural network?
2. What does a neuron compute?
3. Why is an activation function needed?
4. What does ReLU do?
5. What is a forward pass?
6. What does a loss function measure?
7. Why does a model need a loss function?
8. What is backpropagation?
9. What is a gradient?
10. Why is the chain rule important in deep learning?
11. What does an optimizer do?
12. What is SGD?
13. What is Adam?
14. What does learning rate control?
15. Why can a learning rate be too high or too low?
16. Why are GPUs useful for deep learning?
17. What is a tensor?
18. Why do tensor shapes matter?
19. What does `optimizer.zero_grad()` do?
20. What does `loss.backward()` do?
21. What does `optimizer.step()` do?
22. Why must you evaluate on separate data?
23. What is overfitting in deep learning?
24. What is a CNN mainly used for?
25. What does convolution do?
26. What is pooling?
27. What is an RNN used for?
28. What problem do LSTMs help with?
29. What is a transformer's core idea?
30. What does self-attention do?
31. Why is positional encoding needed in transformers?
32. Why should you track loss curves?
33. What does `model.train()` do?
34. What does `model.eval()` do?
35. What is the main lesson of this stage?

### Answers

1. A neural network is a layered function that transforms input data into predictions using learned weights, biases, and activations.

2. A neuron computes a weighted sum of inputs, adds a bias, and applies an activation function.

3. Because without it, the network would behave like a simple linear model even if it had many layers.

4. ReLU outputs 0 for negative values and keeps positive values unchanged.

5. A forward pass is the process of sending input through the network to produce an output prediction.

6. It measures how wrong the model's prediction is compared with the true answer.

7. Because loss gives the model a training objective and tells it what it should reduce.

8. Backpropagation is the process of computing how each parameter contributed to the loss so the model can update them.

9. A gradient tells how much the loss changes when a parameter changes slightly.

10. Because it allows gradients to be computed through many connected layers.

11. An optimizer updates the model parameters using gradients.

12. SGD is an optimizer that updates parameters in the direction that reduces loss, often using small batches of data.

13. Adam is an adaptive optimizer that combines momentum-like behavior with per-parameter learning-rate adjustment.

14. It controls how large each parameter update step is.

15. Too high can make training unstable or diverge. Too low can make learning extremely slow.

16. Because they can perform large numbers of parallel matrix and tensor operations much faster than CPUs.

17. A tensor is a multidimensional array used to represent data in deep learning.

18. Because layers expect specific dimensions, and wrong shapes cause errors or incorrect computations.

19. It clears old gradients before computing new ones.

20. It computes gradients of the loss with respect to model parameters.

21. It updates model parameters using the gradients.

22. To measure whether the model generalizes beyond the training set.

23. It is when the model learns the training data too specifically and performs poorly on unseen data.

24. CNNs are mainly used for image and grid-like data.

25. It applies a small filter across input regions to detect local patterns.

26. Pooling reduces spatial size by summarizing local regions, helping make models more efficient and somewhat more robust.

27. RNNs are used for sequence data such as text, time series, and speech.

28. They help handle long-range dependencies better than vanilla RNNs and reduce vanishing-gradient issues.

29. Its core idea is attention: letting each token directly focus on other relevant tokens.

30. It computes how strongly each token should attend to other tokens in the same sequence.

31. Because attention alone does not contain sequence order information.

32. Because they reveal whether training is improving, stagnating, diverging, or overfitting.

33. It switches the model into training mode, affecting layers like dropout and batch normalization.

34. It switches the model into evaluation mode so inference behaves correctly.

35. Deep learning is a structured learning system built from layers, loss, gradients, and optimization — and it must be understood and debugged, not treated as magic.

---

## What You Must Be Able To Do After Stage 4

- [ ] Explain what a neural network is in plain English
- [ ] Explain what a neuron computes
- [ ] Explain why activation functions matter
- [ ] Explain forward pass, loss, backpropagation, and optimizer
- [ ] Explain how SGD and Adam differ at a high level
- [ ] Understand why GPUs accelerate deep learning
- [ ] Distinguish MLP, CNN, RNN/LSTM/GRU, and Transformer at a beginner level
- [ ] Build and train a simple PyTorch model
- [ ] Debug basic training issues
- [ ] Recognize overfitting, bad learning rate, and shape errors
- [ ] Understand that deep learning is trainable differentiable computation, not magic
