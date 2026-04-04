# Synthetic Data Curation Report

generated_at: 2026-04-04T19:59:53.227641+00:00
dataset_version: synthetic_v1

## Volume
- raw_count: 1000
- deduped_count: 915
- curated_count: 872
- rejected_count: 43
- acceptance_rate: 0.872

## Governance checks
- min_output_length_threshold: 24
- dedupe_policy: exact tuple dedupe on instruction/input/output
- quality_policy: reject low-information outputs

## Samples (curated)
- instruction=Create citation-grounded GIS response | input=ontario_subdivision_case_1 | output=trend=neutral; risk=medium; reason=insufficient evidence, cite authoritative source.
- instruction=Format policy-safe trend/risk/reason JSON | input=ontario_subdivision_case_2 | output=trend=neutral; risk=medium; reason=insufficient evidence, cite authoritative source.
- instruction=Generate Ontario subdivision safety summary | input=ontario_subdivision_case_3 | output=trend=neutral; risk=medium; reason=insufficient evidence, cite authoritative source.