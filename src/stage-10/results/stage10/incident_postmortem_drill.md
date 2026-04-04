# Incident Postmortem Drill

- Incident type: repeated tool failure loop.
- Trigger: same tool failure >= 3 times in 60 seconds.
- Mitigation: breaker opened and deterministic fallback returned.
- Outcome: loop stopped, user received controlled response.