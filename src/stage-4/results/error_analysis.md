# Error Analysis

## Observations
- ShallowMLP: train-val gap 0.0051 -> 0.0217; test accuracy 0.9333 -> 0.9611.
- DeepMLP: train-val gap 0.0234 -> 0.0312; test accuracy 0.9583 -> 0.9556.

## Diagnosis
- If train-val gap remains high, overfitting still exists and stronger regularization may be needed.
- If both train and val are low, model capacity or optimization settings are likely insufficient.

## Applied Fix
- Added explicit feature engineering change: append squared pixel features x^2 to all inputs.