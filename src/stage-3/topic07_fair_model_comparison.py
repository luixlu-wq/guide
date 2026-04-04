"""Stage 3 Topic 07: Fair model comparison on one fixed split.

Data Source: sklearn.datasets.load_breast_cancer
Schema: 30 numeric features | Target: binary class (0=malignant, 1=benign)
Preprocessing: Model-specific pipelines; scaling required for logistic/SVM branches
Null Handling: None (dataset is verified clean by source package)

Workflow:
1) fixed train/test split
2) model-specific preprocessing in pipelines
3) same metric set for all models
4) save results artifact
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def build_models(random_state: int):
    return {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=3000, random_state=random_state)),
            ]
        ),
        "decision_tree": DecisionTreeClassifier(max_depth=4, random_state=random_state),
        "random_forest": RandomForestClassifier(
            n_estimators=300, random_state=random_state, n_jobs=-1
        ),
        "svm_rbf": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", SVC(kernel="rbf", C=10, gamma=0.1, probability=True, random_state=random_state)),
            ]
        ),
    }


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_train_score = model.predict_proba(X_train)[:, 1]
        y_score = model.predict_proba(X_test)[:, 1]
    else:
        # Fallback path for models without predict_proba.
        y_train_score = y_train_pred
        y_score = y_pred

    train_accuracy = float(accuracy_score(y_train, y_train_pred))
    test_accuracy = float(accuracy_score(y_test, y_pred))
    train_precision = float(precision_score(y_train, y_train_pred))
    test_precision = float(precision_score(y_test, y_pred))
    train_recall = float(recall_score(y_train, y_train_pred))
    test_recall = float(recall_score(y_test, y_pred))
    train_f1 = float(f1_score(y_train, y_train_pred))
    test_f1 = float(f1_score(y_test, y_pred))
    train_roc_auc = float(roc_auc_score(y_train, y_train_score))
    test_roc_auc = float(roc_auc_score(y_test, y_score))

    return {
        "model": name,
        # Keep legacy keys for backward compatibility with existing readers.
        "accuracy": test_accuracy,
        "precision": test_precision,
        "recall": test_recall,
        "f1": test_f1,
        "roc_auc": test_roc_auc,
        # Richer train/test breakdown for diagnosis and fair comparison evidence.
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "train_precision": train_precision,
        "test_precision": test_precision,
        "train_recall": train_recall,
        "test_recall": test_recall,
        "train_f1": train_f1,
        "test_f1": test_f1,
        "train_roc_auc": train_roc_auc,
        "test_roc_auc": test_roc_auc,
        "generalization_gap_f1": train_f1 - test_f1,
    }


# Workflow:
# 1) Keep one fixed split for all compared models.
# 2) Train multiple models with model-appropriate pipelines.
# 3) Save comparable metrics to CSV/JSON artifacts.
def main() -> None:
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    print("Data source: sklearn.datasets.load_breast_cancer")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print("Fairness rule: all models use the same split and same metric set.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = build_models(random_state=42)

    rows = []
    for name, model in models.items():
        rows.append(evaluate_model(name, model, X_train, X_test, y_train, y_test))

    df = (
        pd.DataFrame(rows)
        .sort_values(by="test_f1", ascending=False)
        .assign(
            stability_flag=lambda d: d["generalization_gap_f1"].abs().apply(
                lambda v: "stable" if v < 0.03 else "watch_gap"
            )
        )
        .reset_index(drop=True)
    )
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    top = df.iloc[0]
    print(
        "Business decision note: choose the model that balances high test F1 and low gap, "
        "not only the single highest one-split score."
    )
    print(
        f"Current winner: {top['model']} | test_f1={top['test_f1']:.3f} | "
        f"gap={top['generalization_gap_f1']:.3f} | stability={top['stability_flag']}"
    )

    # Stability add-on: run multiple random seeds and summarize mean/std.
    seed_rows = []
    for seed in [7, 21, 42, 84, 168]:
        X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
            X, y, test_size=0.2, random_state=seed, stratify=y
        )
        for name, model in build_models(random_state=seed).items():
            out = evaluate_model(name, model, X_train_s, X_test_s, y_train_s, y_test_s)
            out["seed"] = seed
            seed_rows.append(out)
    seed_df = pd.DataFrame(seed_rows)
    stability_df = (
        seed_df.groupby("model", as_index=False)
        .agg(
            test_f1_mean=("test_f1", "mean"),
            test_f1_std=("test_f1", "std"),
            test_accuracy_mean=("test_accuracy", "mean"),
            test_accuracy_std=("test_accuracy", "std"),
            gap_mean=("generalization_gap_f1", "mean"),
        )
        .sort_values("test_f1_mean", ascending=False)
    )
    print("\n--- Multi-Seed Stability (5 seeds) ---")
    print(stability_df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    stage_dir = out_dir / "stage3"
    stage_dir.mkdir(exist_ok=True)

    csv_path = out_dir / "topic07_fair_comparison.csv"
    json_path = out_dir / "topic07_fair_comparison.json"
    stage_csv_path = stage_dir / "model_compare_before_after.csv"
    seed_csv_path = out_dir / "topic07_fair_comparison_seed_stats.csv"
    seed_json_path = out_dir / "topic07_fair_comparison_seed_stats.json"
    stage_seed_csv_path = stage_dir / "model_compare_seed_stability.csv"
    checklist_path = stage_dir / "fair_comparison_checklist.md"

    df.to_csv(csv_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    # Stage-level artifact expected by the handbook:
    # one table that can later append "after feature engineering" rows.
    stage_df = df.copy()
    stage_df.insert(0, "phase", "before_feature_change")
    stage_df.to_csv(stage_csv_path, index=False)
    stability_df.to_csv(seed_csv_path, index=False)
    with open(seed_json_path, "w", encoding="utf-8") as sf:
        json.dump(stability_df.to_dict(orient="records"), sf, indent=2)
    stability_df.to_csv(stage_seed_csv_path, index=False)

    checklist_text = f"""# Fair Comparison Checklist (Topic 07)

Run timestamp (UTC): {datetime.now(timezone.utc).isoformat()}

- [x] Same task and dataset for all models (`load_breast_cancer`)
- [x] Same split policy for all models (`test_size=0.2`, `random_state=42`, `stratify=y`)
- [x] Same metric set for all models (`accuracy`, `precision`, `recall`, `f1`, `roc_auc`)
- [x] Model-specific preprocessing is isolated inside each model pipeline
- [x] Train/test metrics are both recorded
- [x] Generalization gap is reported (`train_f1 - test_f1`)
- [x] Stability report uses 5 different split seeds (`mean` and `std`)

Primary evidence file:
- `model_compare_before_after.csv`
"""
    checklist_path.write_text(checklist_text, encoding="utf-8")

    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print(f"Saved: {stage_csv_path}")
    print(f"Saved: {seed_csv_path}")
    print(f"Saved: {seed_json_path}")
    print(f"Saved: {stage_seed_csv_path}")
    print(f"Saved: {checklist_path}")


if __name__ == "__main__":
    main()

