"""Stage 6 Topic 02: Tool validation intermediate.

This script validates tool-call arguments against a strict schema and reports
clear error messages when fields are missing or type-like constraints fail.
"""

from stage6_utils import print_data_declaration


print_data_declaration("Topic02 Tool Validation Intermediate")

required_fields = {
    "ticket_id": str,
    "subject": str,
    "body": str,
}


def validate_tool_args(args: dict) -> tuple[bool, list[str]]:
    """Validate arguments with explicit field-by-field checks."""
    errors: list[str] = []

    for key, expected_type in required_fields.items():
        if key not in args:
            errors.append(f"missing_field:{key}")
            continue
        if not isinstance(args[key], expected_type):
            errors.append(f"invalid_type:{key}")

    return (len(errors) == 0), errors


valid_args = {
    "ticket_id": "TKT-2001",
    "subject": "Payment failure",
    "body": "Card charge fails for EU region",
}

invalid_args = {
    "ticket_id": 2001,
    "subject": "Payment failure",
}

ok1, err1 = validate_tool_args(valid_args)
ok2, err2 = validate_tool_args(invalid_args)

print("\n=== Validation Result: valid_args ===")
print(f"ok={ok1}, errors={err1}")

print("\n=== Validation Result: invalid_args ===")
print(f"ok={ok2}, errors={err2}")

print("\nInterpretation:")
print("- Strict validation prevents malformed tool calls from propagating.")
print("- Standardized errors simplify debugging and recovery logic.")
