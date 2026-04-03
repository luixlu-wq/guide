from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


def main():
    X, y = load_diabetes(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    print("correct evaluation")
    print("train R2:", round(r2_score(y_train, train_pred), 4))
    print("test  R2:", round(r2_score(y_test, test_pred), 4))
    print("test MSE:", round(mean_squared_error(y_test, test_pred), 4))

    bad_model = DecisionTreeRegressor(random_state=42)
    bad_model.fit(X, y)
    leaked_pred = bad_model.predict(X)
    print("\nwrong evaluation (same train/test data)")
    print("R2 on same data:", round(r2_score(y, leaked_pred), 4))


if __name__ == "__main__":
    main()
