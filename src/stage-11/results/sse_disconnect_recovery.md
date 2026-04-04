# SSE Disconnect Recovery

- Failure injection: client terminated stream before completion.
- Expected behavior: server stops token generation and releases runtime resources.
- Observed result: generation halted early and circuit metrics remained stable.
- Status: pass.