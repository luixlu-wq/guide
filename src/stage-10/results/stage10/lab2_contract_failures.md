# Lab 2 Contract Failures

1. `llm_payload_has_probabilities` failed because ML probability field was not included in reasoning payload.
2. `trace_id_propagation` failed because orchestration layer did not forward trace id to LLM step.

Fix policy:
- enforce schema validation before each layer call
- add contract unit tests in CI