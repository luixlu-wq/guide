# Prompt Regression Golden Set Report

- Project context: `MapToGo`
- Requirement: protected high-priority facts must keep 100% pass rate.

| case_id | category | original_result | fixed_result | regression_flag |
|---|---|---|---|---|
| tour_5a_001 | protected_fact | pass | pass | no |
| tour_5a_002 | protected_fact | pass | pass | no |
| tour_5a_003 | protected_fact | pass | pass | no |

- Golden-set pass rate (protected facts): `100%`
- Decision: `pass`


## ICV Audit Trail

Identify:
- failure metric: format_valid_rate
- threshold: < 0.85
- failing case: prompt_case_p01

Compare:
- option A: add_schema_examples
- option B: tighten_system_constraints

Verify:
- measured delta: format_valid_rate: +0.19 (0.72 -> 0.91)
- decision: promote
