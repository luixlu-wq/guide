"""Topic 06: Compare correct holdout evaluation vs leakage-style evaluation."""

from __future__ import annotations

from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from common.runtime import create_logger, write_json_artifact


def main() -> None:
    script_stem = "topic06_training_vs_testing"
    logger = create_logger(script_stem)

    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    good_train_r2 = float(r2_score(y_train, train_pred))
    good_test_r2 = float(r2_score(y_test, test_pred))
    good_test_mse = float(mean_squared_error(y_test, test_pred))

    bad_model = DecisionTreeRegressor(random_state=42)
    bad_model.fit(X, y)
    leaked_pred = bad_model.predict(X)
    bad_r2_same_data = float(r2_score(y, leaked_pred))

    logger.info("correct_evaluation train_r2=%.4f test_r2=%.4f test_mse=%.4f",
                good_train_r2, good_test_r2, good_test_mse)
    logger.info("wrong_evaluation_same_data_r2=%.4f", bad_r2_same_data)

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "diabetes",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "test_r2",
            "quality_metric_value": good_test_r2,
            "metrics": {
                "correct_train_r2": good_train_r2,
                "correct_test_r2": good_test_r2,
                "correct_test_mse": good_test_mse,
                "wrong_same_data_r2": bad_r2_same_data,
                "leakage_illusion_gap": bad_r2_same_data - good_test_r2,
            },
            "decision_note": "always keep a true holdout set for honest generalization checks",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
