# Lab 2 Failure Cases and Fixes

## Case 1: High similarity but wrong context
- Cause: weak metadata filtering and broad chunk window.
- Fix: add `department`/`doc_type` filters and tighter chunking policy.

## Case 2: Fresh documents not retrieved
- Cause: ingestion/index update lag.
- Fix: add index freshness check and ingestion completion signal.

## Case 3: Query phrasing mismatch
- Cause: embedding model weak for domain-specific terms.
- Fix: switch embedding model and rerun fixed relevance evaluation.