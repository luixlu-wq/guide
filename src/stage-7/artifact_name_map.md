# Artifact Name Map - stage-7

Purpose:
- Keep existing stage output files unchanged.
- Map stage-specific artifact names to canonical cross-plan names.
- Support additive-only standardization from `Cross-Plan Consistency Addendum (2026-04-04, Additive-Only)`.

Compatibility rules:
- Do not delete existing artifact files.
- Do not rename existing artifact files unless explicitly requested.
- Use aliases or this mapping file to standardize reporting.

Canonical decision labels:
- `promote`
- `hold`
- `rollback`

Canonical troubleshooting flow labels:
1. `identify`
2. `evidence`
3. `compare`
4. `change`
5. `verify`
6. `decide`

Stage metadata:
- Stage: `stage-7`
- Recommended output root: `results/stage7/`
- Last updated: `2026-04-04`

## Mapping Table

| Canonical artifact name | Current stage artifact path/name | Status (`mapped`/`todo`) | Notes |
|---|---|---|---|
| `pain_point_matrix.md` | `results/lab6_project_solution_options.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `before_after_metrics.csv` | `results/lab6_project_metrics_comparison.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `verification_report.md` | `results/lab6_project_verification_report.md` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `decision_log.md` | `results/decision_log.md` | `mapped` | Alias placeholder created automatically on 2026-04-04; replace TODO content with stage-specific evidence. |
| `reproducibility.md` | `results/reproducibility.md` | `mapped` | Alias placeholder created automatically on 2026-04-04; replace TODO content with stage-specific evidence. |

## Optional alias files (recommended)

If existing names differ, create lightweight alias files in the same results folder:

- `pain_point_matrix.md` -> points to existing stage file
- `before_after_metrics.csv` -> export/copy of existing comparison table
- `verification_report.md` -> summary alias
- `decision_log.md` -> summary alias
- `reproducibility.md` -> summary alias

## Minimum evidence schema for `before_after_metrics.csv`

Recommended columns:
- `run_id`
- `stage`
- `topic_or_module`
- `metric_name`
- `before_value`
- `after_value`
- `delta`
- `dataset_or_eval_set`
- `seed_or_config_id`
- `decision`

## Completion checklist

- [ ] All 5 canonical artifacts mapped
- [ ] At least one `before_after_metrics.csv` generated for this stage
- [ ] Decision uses canonical labels (`promote`/`hold`/`rollback`)
- [ ] Mapping reviewed after next stage run
