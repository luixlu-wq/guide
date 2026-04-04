# Lab 3 Root Cause Analysis

- Primary cause: semantic drift after boundary-data ingestion changed chunk distribution.
- Secondary cause: retrieval chunking strategy was not validated against new schema shape.
- Corrective actions: rebuild chunking profile, rerun fixed eval set, and tighten drift alert policy.
