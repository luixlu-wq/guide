# Artifact Name Map - stage-12

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
- Stage: `stage-12`
- Recommended output root: `results/stage12/`
- Last updated: `2026-04-04`

## Mapping Table

| Canonical artifact name | Current stage artifact path/name | Status (`mapped`/`todo`) | Notes |
|---|---|---|---|
| `pain_point_matrix.md` | `results/lab1_tradeoff_matrix.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `before_after_metrics.csv` | `results/lab4_metrics_comparison.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `verification_report.md` | `results/lab2_verification_rerun.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `decision_log.md` | `results/lab4_release_decision.md` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `reproducibility.md` | `results/reproducibility.md` | `mapped` | Alias placeholder created automatically on 2026-04-04; replace TODO content with stage-specific evidence. |
| `agent_card_registry.json` | `results/agent_card_registry.json` | `mapped` | A2A capability-discovery artifact. |
| `a2a_handoff_trace.jsonl` | `results/a2a_handoff_trace.jsonl` | `mapped` | Inter-agent handoff evidence artifact. |
| `mcp_tool_contracts.md` | `results/mcp_tool_contracts.md` | `mapped` | MCP-compatible tool schema documentation. |
| `nvfp4_throughput_quality.csv` | `results/nvfp4_throughput_quality.csv` | `mapped` | Blackwell precision tradeoff evidence. |
| `prefix_cache_latency_profile.csv` | `results/prefix_cache_latency_profile.csv` | `mapped` | Prefix-caching loop-latency comparison. |
| `agent_loop_latency_report.md` | `results/agent_loop_latency_report.md` | `mapped` | Agent loop latency interpretation report. |
| `owasp_llm_v2_redteam_report.md` | `results/owasp_llm_v2_redteam_report.md` | `mapped` | OWASP 2026 red-team summary report. |
| `indirect_injection_case_log.jsonl` | `results/indirect_injection_case_log.jsonl` | `mapped` | Indirect prompt injection incident evidence. |
| `unbounded_consumption_guard.csv` | `results/unbounded_consumption_guard.csv` | `mapped` | Consumption guardrail evidence under loop pressure. |
| `coordinate_projection_validation_report.md` | `results/coordinate_projection_validation_report.md` | `mapped` | GIS coordinate/projection validation report. |
| `geojson_schema_guard_failures.csv` | `results/geojson_schema_guard_failures.csv` | `mapped` | GeoJSON schema/projection failure table. |
| `loop_breaker_events.jsonl` | `results/loop_breaker_events.jsonl` | `mapped` | Loop-breaker state transition events. |
| `mobile_latency_guard_report.md` | `results/mobile_latency_guard_report.md` | `mapped` | Mobile latency guard drill report. |
| `architecture_decision_y_statement.md` | `results/architecture_decision_y_statement.md` | `mapped` | Mandatory Y-statement ADR output. |
| `adr_scorecard_with_thresholds.csv` | `results/adr_scorecard_with_thresholds.csv` | `mapped` | Threshold-aware ADR scorecard. |

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
