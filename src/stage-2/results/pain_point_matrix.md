# Pain Point Matrix - stage-2

Status: first draft populated from real outputs on 2026-04-04.

| topic | pain_point | root_causes | solution_options | chosen_fix | verification_evidence | decision |
|---|---|---|---|---|---|---|
| End-to-end regression baseline | Pipeline quality unknown without baseline comparator | Only one model run recorded | Compare DummyRegressor baseline vs RF pipeline | Keep RF pipeline with preprocessing + one-hot + imputation | Dummy baseline R2=-0.0004 vs pipeline R2=0.9312 | promote |
| Data quality handling | Missing values can silently degrade model quality | No imputation policy | Add median (numeric) + mode (categorical) imputers in pipeline | Keep explicit ColumnTransformer preprocessing | `topic09_metrics.json` shows stable metrics on split (train=400,test=100) | promote |
| Metric interpretation | Single metric can hide quality issues | Overfocus on R2 | Track R2 + MAE + MSE together | Keep metric triad in artifact output | R2=0.9312, MAE=22909.21, MSE=826,880,013.62 | promote |
