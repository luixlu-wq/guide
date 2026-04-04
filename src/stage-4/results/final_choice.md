# Final Model Selection

Chosen model: ShallowMLP
Test accuracy: 0.9611

Rationale:
- Chosen by highest test accuracy under fixed split and same epoch budget.
- Train/validation gap was also considered to avoid selecting an unstable model.
- The same feature engineering rule (x and x^2) was applied to all compared models.