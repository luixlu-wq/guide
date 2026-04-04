# Lab4 Data Boundary Policy

Sovereignty gate rules:
1. If payload contains sensitive GeoJSON markers and target is external endpoint, block by default.
2. Redaction/generalization is required before any allowed cross-boundary transfer.
3. Record every blocked attempt with case ID and reason.

Measured privacy_leak_rate: 0.0000