import matplotlib
import numpy as np
from pathlib import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def make_data(n=200, seed=42):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 10, size=n)
    y = 3.0 * X + 5.0 + rng.normal(0, 2, size=n)
    return X, y


def predict(X, w, b):
    return w * X + b


def mse(X, y, w, b):
    y_pred = predict(X, w, b)
    return np.mean((y_pred - y) ** 2)


def gradients(X, y, w, b):
    n = len(X)
    err = predict(X, w, b) - y
    dw = (2 / n) * np.sum(err * X)
    db = (2 / n) * np.sum(err)
    return dw, db


def train_gradient_descent(X, y, lr=0.001, epochs=3000):
    w, b = 0.0, 0.0
    history = []
    for _ in range(epochs):
        dw, db = gradients(X, y, w, b)
        w -= lr * dw
        b -= lr * db
        history.append(mse(X, y, w, b))
    return w, b, history


def main():
    X, y = make_data()
    w, b, loss_history = train_gradient_descent(X, y, lr=0.001, epochs=3000)

    print("learned w:", round(w, 4))
    print("learned b:", round(b, 4))
    print("initial loss:", round(loss_history[0], 4))
    print("final loss  :", round(loss_history[-1], 4))

    plt.plot(loss_history)
    plt.title("Gradient Descent Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.tight_layout()
    out_path = Path(__file__).with_name("topic05_loss_curve.png")
    plt.savefig(out_path)
    print(f"saved plot: {out_path}")


if __name__ == "__main__":
    main()
