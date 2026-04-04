# Pain Point Matrix - stage-3

Status: first draft populated from real outputs on 2026-04-04.

| topic | pain_point | root_causes | solution_options | chosen_fix | verification_evidence | decision |
|---|---|---|---|---|---|---|
| Fair model comparison | Teams choose model by intuition, not fixed benchmark | Inconsistent split/preprocess/metrics across models | Enforce one fixed split and one metric set for all models | Use `topic07_fair_model_comparison.py` benchmark as selection gate | LogisticRegression ranked best: accuracy=0.9825, F1=0.9861, ROC-AUC=0.9954 | promote |
| Overfitting-prone tree baseline | Tree underperforms relative to linear baseline | Model complexity not controlled and weaker discrimination | Compare tree against stronger baselines before selection | Select logistic regression for stage baseline | DecisionTree accuracy=0.9386 vs LogisticRegression=0.9825 | promote |
| SVM/ensemble tradeoff interpretation | Similar accuracy but different precision/recall behavior | No per-metric analysis and no ranking policy | Add multi-metric ranking (accuracy + F1 + ROC-AUC) | Keep ranking by F1 then ROC-AUC | SVM/RandomForest both below logistic on F1/ROC-AUC | hold |
