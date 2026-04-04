# Dependency Risk Map

| Dependency | Risk Event | Detection | Guardrail | Owner |
|---|---|---|---|---|
| Land Information Ontario (LIO) schema | Upstream schema change | Schema diff check in ingest job | Schema guard + circuit breaker to safe mode | data_owner |
| Baidu Baike content/API | Field contract drift or content format change | contract validation and parse error monitor | fallback parser + retrieval quarantine | retrieval_owner |
