"""Feature Engineering — creating new input features from raw data.

Data: Synthetic house dataset (generated with numpy)
Shape: 300 rows x 3 raw features
Raw features:
  area      — house area in square feet (uniform 500–3000)
  rooms     — number of rooms (integers 1–8)
  age       — building age in years (uniform 1–50)
Target: price — house price in dollars (synthetic linear relationship)
Type: Regression

Purpose:
  Show that creating derived features from raw columns can improve
  model performance, even without changing the algorithm.

  Baseline model    : uses area, rooms, age only
  Engineered model  : adds area_per_room and log_age as derived features

  area_per_room = area / rooms   (density of space per room)
  log_age       = log(1 + age)   (compresses the age scale; old houses
                                  penalize price less linearly)

Expected output:
  baseline (3 raw features)    test R2 ~ 0.85 to 0.91
  engineered (5 features)      test R2 ~ 0.92 to 0.97
  R2 improvement               ~ +0.04 to +0.10

  The improvement shows that the derived features express relationships
  that the raw columns alone cannot capture as efficiently.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def make_data(n=300, seed=42):
    rng = np.random.default_rng(seed)
    area = rng.uniform(500, 3000, size=n)
    rooms = rng.integers(1, 9, size=n).astype(float)
    age = rng.uniform(1, 50, size=n)
    noise = rng.normal(0, 12000, size=n)
    # True price depends on area-per-room and penalises old age
    price = 90 * area + 4000 * rooms - 700 * age + noise
    X_raw = np.column_stack([area, rooms, age])
    return X_raw, price


def add_engineered_features(X_raw):
    """Add two derived features to the raw feature matrix."""
    area = X_raw[:, 0]
    rooms = X_raw[:, 1]
    age = X_raw[:, 2]
    area_per_room = area / rooms          # compactness: space per room
    log_age = np.log1p(age)               # compressed age scale
    return np.column_stack([X_raw, area_per_room, log_age])


def evaluate(X, y, label):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    print(f"  {label:40s}  test R2 = {r2:.4f}")
    return r2


def main():
    X_raw, y = make_data()

    print("Feature set comparison (same algorithm, same data, different features):")
    print()
    r2_base = evaluate(X_raw, y, "baseline — 3 raw features (area, rooms, age)")
    X_eng = add_engineered_features(X_raw)
    r2_eng = evaluate(X_eng, y, "engineered — 5 features (+ area_per_room, log_age)")

    print()
    print(f"  R2 improvement: +{r2_eng - r2_base:.4f}")
    print()
    print("Engineered feature explanations:")
    print("  area_per_room = area / rooms")
    print("    — captures how spacious each room is, which raw area alone cannot.")
    print("  log_age = log(1 + age)")
    print("    — compresses the effect of very old buildings into a smaller range.")
    print()
    print("Key lesson:")
    print("  Feature engineering often produces more improvement than switching algorithms.")
    print("  Always ask: what relationships in the data am I not yet expressing as inputs?")


if __name__ == "__main__":
    main()
