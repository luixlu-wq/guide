# Stage 3 Pain-Point Matrix Evidence (Topic 08)

| Topic | Pain Point | Root Cause | Resolution Strategy | Verification Evidence | Mapped Script |
|---|---|---|---|---|---|
| Decision Tree | Train high, test low | Excessive depth and memorization | Constrain `max_depth` and compare gaps | Gap shrinks from deep-tree to shallow-tree run | `topic08_failure_modes_overfit_leakage.py` |
| Pipeline Integrity | Suspiciously high score with random labels | Feature selection before split (leakage) | Split first, fit selection inside train pipeline | Accuracy drops near chance after fix | `topic08_failure_modes_overfit_leakage.py` |
