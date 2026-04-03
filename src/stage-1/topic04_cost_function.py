import numpy as np
from sklearn.metrics import log_loss, mean_squared_error


def mse_manual(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.mean((y_true - y_pred) ** 2)


def log_loss_manual(y_true, y_prob, eps=1e-15):
    y_true = np.asarray(y_true, dtype=float)
    y_prob = np.asarray(y_prob, dtype=float)
    y_prob = np.clip(y_prob, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob))


def main():
    y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])

    y_true_cls = np.array([1, 0, 1, 1, 0, 0])
    y_prob_cls = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.4])

    print("MSE manual :", round(mse_manual(y_true_reg, y_pred_reg), 6))
    print("MSE sklearn:", round(mean_squared_error(y_true_reg, y_pred_reg), 6))

    print("LogLoss manual :", round(log_loss_manual(y_true_cls, y_prob_cls), 6))
    print("LogLoss sklearn:", round(log_loss(y_true_cls, y_prob_cls), 6))


if __name__ == "__main__":
    main()
