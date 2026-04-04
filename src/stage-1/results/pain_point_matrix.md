# Pain Point Matrix - stage-1

Status: first draft populated from real runs on 2026-04-04.

| topic | pain_point | root_causes | solution_options | chosen_fix | verification_evidence | decision |
|---|---|---|---|---|---|---|
| Supervised baseline | High training confidence can hide test errors | No strict split/metric review | Add fixed split + confusion matrix review | Keep stratified split (`random_state=42`) and review precision/recall/F1 together | `topic01_supervised_learning.py`: accuracy=0.9825, precision=0.9861, recall=0.9861, F1=0.9861, CM=[[41,1],[1,71]] | promote |
| Train/test discipline | Same-data evaluation can look perfect but mislead deployment | Data leakage from reusing full dataset as test | Compare correct split vs wrong same-data evaluation | Keep locked train/test split and reject same-data scoring | `topic06_training_vs_testing.py`: test R2=0.0607 vs leaked R2=1.0 | promote |
| Regularization selection | Weak regularization overfits and reduces test performance | C too high in logistic regression | Sweep C and choose by validation/test evidence | Use balanced C=1.0, avoid extreme C values | `topic11_regularization.py`: test_acc(C=1.0)=0.9825 vs test_acc(C=1000)=0.9298 | promote |
