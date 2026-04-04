# Lab 1 Boundary Checklist

- API layer owns transport, auth, and schema validation only.
- Retrieval layer owns indexing/query/filter logic only.
- Model layer owns inference logic only.
- Observability layer tags all events with trace_id/request_id.
- No module imports leak across boundaries in invalid direction.