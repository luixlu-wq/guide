# Artifact Name Map - stage-11

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
- Stage: `stage-11`
- Recommended output root: `results/stage11/`
- Last updated: `2026-04-04`

## Mapping Table

| Canonical artifact name | Current stage artifact path/name | Status (`mapped`/`todo`) | Notes |
|---|---|---|---|
| `pain_point_matrix.md` | `results/lab4_solution_options.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `before_after_metrics.csv` | `results/before_after_metrics.csv` | `mapped` | Alias placeholder created automatically on 2026-04-04; replace TODO content with stage-specific evidence. |
| `verification_report.md` | `results/lab4_verification_rerun.csv` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `decision_log.md` | `results/lab4_release_decision.md` | `mapped` | Auto-mapped from existing stage output (2026-04-04). |
| `reproducibility.md` | `results/reproducibility.md` | `mapped` | Alias placeholder created automatically on 2026-04-04; replace TODO content with stage-specific evidence. |
| `throughput_vs_latency_batch_profile.csv` | `results/throughput_vs_latency_batch_profile.csv` | `mapped` | Stage 11 expert-tier batching evidence. |
| `fp4_throughput_quality_tradeoff.csv` | `results/fp4_throughput_quality_tradeoff.csv` | `mapped` | Blackwell precision tradeoff evidence. |
| `hardware_saturation_profile.jsonl` | `results/hardware_saturation_profile.jsonl` | `mapped` | GPU saturation timeline for incident analysis. |
| `wsl_io_before_after.csv` | `results/wsl_io_before_after.csv` | `mapped` | WSL2 storage-path hardening evidence. |
| `vector_recall_vs_latency_matrix.csv` | `results/vector_recall_vs_latency_matrix.csv` | `mapped` | HNSW/quantization tradeoff evidence. |
| `qdrant_persistence_recovery.md` | `results/qdrant_persistence_recovery.md` | `mapped` | Vector DB persistence recovery drill. |
| `circuit_breaker_events.jsonl` | `results/circuit_breaker_events.jsonl` | `mapped` | Stateful infrastructure protection evidence. |
| `sse_ttft_metrics.csv` | `results/sse_ttft_metrics.csv` | `mapped` | Streaming TTFT benchmark evidence. |
| `sse_disconnect_recovery.md` | `results/sse_disconnect_recovery.md` | `mapped` | Streaming disconnect recovery drill evidence. |
| `otel_trace_path_validation.md` | `results/otel_trace_path_validation.md` | `mapped` | End-to-end OTel trace validation evidence. |
| `wsl_network_trace_check.md` | `results/wsl_network_trace_check.md` | `mapped` | WSL networking/trace transport validation. |
| `incident_postmortem_infra.md` | `results/incident_postmortem_infra.md` | `mapped` | Infra-specific incident postmortem artifact. |
| `local_stack_boot_report.md` | `results/local_stack_boot_report.md` | `mapped` | IaC one-command stack startup evidence. |
| `service_health_snapshot.json` | `results/service_health_snapshot.json` | `mapped` | Local stack service health snapshot. |
| `release_readiness.json` | `results/release_readiness.json` | `mapped` | Mandatory Stage 11 go/no-go decision schema. |

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
