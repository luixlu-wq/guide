# OTel Trace Path Validation

- Trace path: API ingress -> retrieval -> generation -> response serialization.
- Span coverage: all major stages include trace_id and latency attributes.
- GenAI attributes captured: input token count, output token count, model identifier.
- Validation result: pass for local WSL2 + dashboard transport path.