"""Stage 3 Topic 08: Failure modes (overfitting and data leakage).

Data Source:
- Overfitting demo: sklearn.datasets.make_classification
- Leakage demo: synthetic random features + random labels
Schema: numeric tabular matrices | Target: binary labels
Preprocessing: fit-on-train-only pipeline discipline required
Null Handling: None (synthetic generators produce complete arrays)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


def overfitting_demo() -> dict:
    X, y = make_classification(
        n_samples=1200,
        n_features=25,
        n_informative=4,
        n_redundant=8,
        flip_y=0.07,
        class_sep=0.8,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    deep_tree = DecisionTreeClassifier(max_depth=None, random_state=42)
    shallow_tree = DecisionTreeClassifier(max_depth=4, random_state=42)

    deep_tree.fit(X_train, y_train)
    shallow_tree.fit(X_train, y_train)

    deep_train = accuracy_score(y_train, deep_tree.predict(X_train))
    deep_test = accuracy_score(y_test, deep_tree.predict(X_test))
    shallow_train = accuracy_score(y_train, shallow_tree.predict(X_train))
    shallow_test = accuracy_score(y_test, shallow_tree.predict(X_test))

    deep_gap = deep_train - deep_test
    shallow_gap = shallow_train - shallow_test

    print("Overfitting demo (Decision Tree):")
    print(f"  deep tree    train={deep_train:.3f}, test={deep_test:.3f}, gap={deep_gap:.3f}")
    print(f"  shallow tree train={shallow_train:.3f}, test={shallow_test:.3f}, gap={shallow_gap:.3f}")

    return {
        "scenario": "overfitting_depth_control",
        "baseline_name": "deep_tree_unrestricted",
        "fixed_name": "shallow_tree_max_depth_4",
        "baseline_train_accuracy": float(deep_train),
        "baseline_test_accuracy": float(deep_test),
        "baseline_gap": float(deep_gap),
        "fixed_train_accuracy": float(shallow_train),
        "fixed_test_accuracy": float(shallow_test),
        "fixed_gap": float(shallow_gap),
        "delta_test_accuracy": float(shallow_test - deep_test),
        "root_cause": "Tree depth too high causes memorization.",
        "resolution": "Limit model capacity with depth constraints.",
        "verification_evidence": "Generalization gap shrinks after depth control.",
    }


def leakage_demo() -> dict:
    rng = np.random.default_rng(42)
    n_samples = 1200
    n_features = 600

    # Random features and random labels: no true signal.
    X = rng.normal(size=(n_samples, n_features))
    y = rng.integers(0, 2, size=n_samples)

    # Wrong workflow: feature selection on full data (leakage), then split.
    # This mirrors target leakage in industry: features accidentally encode future/target info.
    selector = SelectKBest(score_func=f_classif, k=30)
    X_selected_wrong = selector.fit_transform(X, y)

    Xw_train, Xw_test, yw_train, yw_test = train_test_split(
        X_selected_wrong, y, test_size=0.25, random_state=42, stratify=y
    )

    wrong_model = LogisticRegression(max_iter=3000, random_state=42)
    wrong_model.fit(Xw_train, yw_train)
    wrong_acc = accuracy_score(yw_test, wrong_model.predict(Xw_test))

    # Correct workflow: split first, then select features inside pipeline on train only.
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    correct_model = Pipeline(
        [
            ("select", SelectKBest(score_func=f_classif, k=30)),
            ("clf", LogisticRegression(max_iter=3000, random_state=42)),
        ]
    )
    correct_model.fit(Xc_train, yc_train)
    correct_acc = accuracy_score(yc_test, correct_model.predict(Xc_test))

    print("Leakage demo (random labels, expected near 0.5 when correct):")
    print(f"  wrong workflow (leakage) accuracy : {wrong_acc:.3f}")
    print(f"  correct workflow accuracy         : {correct_acc:.3f}")

    return {
        "scenario": "feature_selection_leakage",
        "baseline_name": "wrong_feature_selection_before_split",
        "fixed_name": "pipeline_select_on_train_only",
        "baseline_test_accuracy": float(wrong_acc),
        "fixed_test_accuracy": float(correct_acc),
        "delta_test_accuracy": float(correct_acc - wrong_acc),
        "root_cause": "Feature selection was fitted on full data before split.",
        "resolution": "Split first, then fit selection inside training pipeline.",
        "verification_evidence": "Accuracy drops toward chance after leakage removal.",
    }


def write_stage3_artifacts(overfit: dict, leakage: dict) -> None:
    out_dir = Path(__file__).parent / "results" / "stage3"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Machine-readable evidence table for before/after failure correction.
    rows = [
        {
            "scenario": overfit["scenario"],
            "baseline_name": overfit["baseline_name"],
            "fixed_name": overfit["fixed_name"],
            "baseline_metric": overfit["baseline_test_accuracy"],
            "fixed_metric": overfit["fixed_test_accuracy"],
            "delta_metric": overfit["delta_test_accuracy"],
            "diagnosis": "overfitting",
            "root_cause": overfit["root_cause"],
            "resolution": overfit["resolution"],
            "verification_evidence": overfit["verification_evidence"],
        },
        {
            "scenario": leakage["scenario"],
            "baseline_name": leakage["baseline_name"],
            "fixed_name": leakage["fixed_name"],
            "baseline_metric": leakage["baseline_test_accuracy"],
            "fixed_metric": leakage["fixed_test_accuracy"],
            "delta_metric": leakage["delta_test_accuracy"],
            "diagnosis": "data_leakage",
            "root_cause": leakage["root_cause"],
            "resolution": leakage["resolution"],
            "verification_evidence": leakage["verification_evidence"],
        },
    ]
    df = pd.DataFrame(rows)

    csv_path = out_dir / "failure_class_before_after.csv"
    json_path = out_dir / "failure_class_before_after.json"
    df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # Handbook-mandated artifact names from Stage 3 plan.
    pain_point_matrix_path = out_dir / "pain_point_matrix.md"
    matrix_text = """# Stage 3 Pain-Point Matrix Evidence (Topic 08)

| Topic | Pain Point | Root Cause | Resolution Strategy | Verification Evidence | Mapped Script |
|---|---|---|---|---|---|
| Decision Tree | Train high, test low | Excessive depth and memorization | Constrain `max_depth` and compare gaps | Gap shrinks from deep-tree to shallow-tree run | `topic08_failure_modes_overfit_leakage.py` |
| Pipeline Integrity | Suspiciously high score with random labels | Feature selection before split (leakage) | Split first, fit selection inside train pipeline | Accuracy drops near chance after fix | `topic08_failure_modes_overfit_leakage.py` |
"""
    pain_point_matrix_path.write_text(matrix_text, encoding="utf-8")

    diagnosis_path = out_dir / "failure_diagnosis.md"
    diagnosis_text = f"""# Failure Diagnosis Notes (Topic 08)

## Overfitting Case
- Baseline (`{overfit["baseline_name"]}`) test accuracy: {overfit["baseline_test_accuracy"]:.3f}
- Fix (`{overfit["fixed_name"]}`) test accuracy: {overfit["fixed_test_accuracy"]:.3f}
- Gap reduction evidence: baseline gap {overfit["baseline_gap"]:.3f} -> fixed gap {overfit["fixed_gap"]:.3f}

## Leakage Case
- Baseline (`{leakage["baseline_name"]}`) test accuracy: {leakage["baseline_test_accuracy"]:.3f}
- Fix (`{leakage["fixed_name"]}`) test accuracy: {leakage["fixed_test_accuracy"]:.3f}
- Interpretation: the inflated baseline collapsed after leakage removal, which confirms the diagnosis.

## Red-Flag Rule (Mandatory)
- If your model reports near-100% accuracy on a complex dataset, assume leakage until proven otherwise.
"""
    diagnosis_path.write_text(diagnosis_text, encoding="utf-8")

    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print(f"Saved: {pain_point_matrix_path}")
    print(f"Saved: {diagnosis_path}")


# Workflow:
# 1) Show overfitting using deep vs shallow trees.
# 2) Show leakage using wrong-vs-correct feature selection flow.
# 3) Print diagnostics that explain suspiciously high scores.
def main() -> None:
    print("Failure Mode 1: overfitting")
    overfit = overfitting_demo()
    print()
    print("Failure Mode 2: data leakage")
    leakage = leakage_demo()
    print()
    print("Interpretation: do not trust high score without pipeline and split audit.")
    write_stage3_artifacts(overfit, leakage)


if __name__ == "__main__":
    main()

