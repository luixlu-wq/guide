"""Stage 5 Topic 03A: structured output basics (simple).

Data: one in-script text sample
Records/Samples: 1
Input schema: text
Output schema: JSON object (summary, risks, citations)
Split/Eval policy: not applicable
Type: structured-output validation basics
"""

from __future__ import annotations

from stage5_utils import mock_llm, try_parse_json, validate_schema


# Workflow:
# 1) Request weak JSON output from mock model.
# 2) Parse JSON and validate required schema.
# 3) Show pass/fail result.
def main() -> None:
    text = "Product recall triggered investigation and volatility concerns."
    raw = mock_llm(text, "json_weak")

    print("Data declaration")
    print("source=in_script_text")
    print("records=1")
    print("input_schema=text:str")
    print("output_schema={summary:str, risks:list, citations:list}")

    obj, err = try_parse_json(raw)
    if err:
        print("raw_output=", raw)
        print("parse_status=FAILED")
        print("parse_error=", err)
        return

    ok, errors = validate_schema(obj)
    print("raw_output=", raw)
    print("parse_status=OK")
    print("schema_valid=", ok)
    print("schema_errors=", errors)
    print("Interpretation: parse success is not enough; schema validation is still required.")


if __name__ == "__main__":
    main()
