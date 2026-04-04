"""Stage 6 Topic 02C: Tool failure recovery advanced.

This script simulates transient tool timeouts and demonstrates retry with capped
attempts and linear backoff.
"""

from stage6_utils import print_data_declaration, sleep_ms


print_data_declaration("Topic02C Tool Failure Recovery Advanced")


class TimeoutErrorForDemo(RuntimeError):
    """Dedicated timeout exception used in this educational script."""


def flaky_tool(call_index: int) -> str:
    """Fail first two calls, then succeed, to demonstrate retry behavior."""
    if call_index < 3:
        raise TimeoutErrorForDemo("simulated_timeout")
    return "TOOL_SUCCESS"


def run_with_retry(max_attempts: int = 4, backoff_ms: int = 120) -> tuple[bool, str, int]:
    """Retry transient failures while preserving deterministic max attempt behavior."""
    for attempt in range(1, max_attempts + 1):
        try:
            result = flaky_tool(attempt)
            return True, result, attempt
        except TimeoutErrorForDemo as exc:
            # The delay models practical backoff and keeps runbook behavior explicit.
            sleep_ms(backoff_ms * attempt)
            last_error = str(exc)
    return False, last_error, max_attempts


ok, result, used_attempts = run_with_retry(max_attempts=4)
print("\n=== Retry Result ===")
print(f"success={ok}")
print(f"result_or_error={result}")
print(f"attempts_used={used_attempts}")

print("\nKey reliability note:")
print("- Cap retries to avoid retry storms during persistent outages.")
