# Lab 2 Contract Fix Report

Implemented fixes:
- Added `pred_prob_up` as required field in LLM payload contract.
- Enforced trace propagation from API ingress to retrieval and generation steps.

OpenTelemetry GenAI contract checks:
- trace_id: required and propagated
- gen_ai.usage.input_tokens: required
- gen_ai.usage.output_tokens: required
- gen_ai.response.model: required
- gen_ai.finish_reason: required