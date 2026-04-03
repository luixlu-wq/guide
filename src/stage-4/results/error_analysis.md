# Error Analysis

## Observations
- ShallowMLP: train-val gap 0.0226 -> 0.0217; test accuracy 0.9556 -> 0.9611.
- DeepMLP: train-val gap 0.0286 -> 0.0243; test accuracy 0.9694 -> 0.9667.

## Diagnosis
- If train-val gap remains high, overfitting still exists and stronger regularization may be needed.
- If both train and val are low, model capacity or optimization settings are likely insufficient.

## Applied Fix
- Added explicit feature engineering change: append squared pixel features x^2 to all inputs.