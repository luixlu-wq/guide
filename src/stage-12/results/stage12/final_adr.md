# ADR-001: Pattern Choice for Knowledge Assistant

## Context
- Need grounded answers over changing internal documentation.
- Must keep p95 latency under 700ms where possible.

## Options
- llm_app
- rag
- agent
- multi_agent

## Decision
- Selected: rag
- Reason: best weighted score under quality + operational constraints.

## Risks
- retrieval freshness drift
- index maintenance overhead

## Rollback trigger
- grounding score < 0.75 for 3 windows

## Validation plan
- fixed eval replay weekly
- incident drill monthly