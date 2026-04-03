from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def main():
    X, y = make_classification(
        n_samples=1500,
        n_features=20,
        n_informative=6,
        n_redundant=4,
        flip_y=0.05,
        class_sep=1.0,
        random_state=42,
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    results = []
    for depth in range(1, 21):
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        train_err = 1 - accuracy_score(y_train, model.predict(X_train))
        val_err = 1 - accuracy_score(y_val, model.predict(X_val))
        results.append((depth, train_err, val_err))

    best = min(results, key=lambda row: row[2])
    print("best depth by validation error:", best[0])
    print("depth | train_error | val_error")
    for depth, train_err, val_err in results[::3]:
        print(f"{depth:>5} | {train_err:>11.4f} | {val_err:>8.4f}")

    print("\nInterpretation:")
    print("- Very small depth -> high bias (both errors high).")
    print("- Very large depth -> high variance (train error low, val error worse).")


if __name__ == "__main__":
    main()
