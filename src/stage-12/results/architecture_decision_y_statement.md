# Architecture Decision Y-Statement

In the context of MapToGo + Ontario GIS support workflows,
we decided to use RAG to handle grounded, freshness-sensitive knowledge requests,
because it outperformed alternatives on weighted quality-risk score and remains operationally simpler than full multi-agent routing,
and measured p95 latency stayed within the defined release budget.