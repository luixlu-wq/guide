# Reproducibility

- Dataset: sklearn.load_digits
- Rows: 1797
- Input schema (before): 64 numeric pixel features scaled to [0, 1]
- Input schema (after): 128 numeric features (x and x^2)
- Target: digit class 0-9
- Split policy: train_test_split(test_size=0.2, random_state=81, stratify=y) then validation split with same random_state
- Random seed: torch.manual_seed(81)
- Run date: 2026-04-04