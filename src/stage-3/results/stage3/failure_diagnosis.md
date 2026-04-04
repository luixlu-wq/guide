# Failure Diagnosis Notes (Topic 08)

## Overfitting Case
- Baseline (`deep_tree_unrestricted`) test accuracy: 0.777
- Fix (`shallow_tree_max_depth_4`) test accuracy: 0.783
- Gap reduction evidence: baseline gap 0.223 -> fixed gap 0.057

## Leakage Case
- Baseline (`wrong_feature_selection_before_split`) test accuracy: 0.590
- Fix (`pipeline_select_on_train_only`) test accuracy: 0.493
- Interpretation: the inflated baseline collapsed after leakage removal, which confirms the diagnosis.

## Red-Flag Rule (Mandatory)
- If your model reports near-100% accuracy on a complex dataset, assume leakage until proven otherwise.
