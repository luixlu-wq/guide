# Semantic Drift Incident Report

- Incident class: `semantic_drift`
- Trigger: new municipal boundary ingestion without chunk profile update
- Detection evidence: OpenTelemetry retrieval spans showed context miss spike
- Resolution: apply schema-aware chunking, rebuild index, verify on fixed replay set
- Decision: hold release until rerun delta meets gate thresholds
