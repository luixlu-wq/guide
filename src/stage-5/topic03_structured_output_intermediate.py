"""Stage 5 Topic 03: structured output batch validation (intermediate).

Data: in-script batch set
Records/Samples: 20
Input schema: text
Output schema: JSON object
Split/Eval policy: same inputs for weak vs strong schema prompting
Type: structured-output reliability comparison
"""

from __future__ import annotations

from stage5_utils import mock_llm, most_common_error, try_parse_json, validate_schema


# Workflow:
# 1) Run weak JSON prompt on fixed batch.
# 2) Run strong JSON prompt on same batch.
# 3) Compare parse-valid and schema-valid rates.
def evaluate(mode: str, texts: list[str]) -> tuple[int, int, list[str]]:
    parse_ok = 0
    schema_ok = 0
    all_errors: list[str] = []

    for text in texts:
        raw = mock_llm(text, mode)
        obj, err = try_parse_json(raw)
        if err:
            all_errors.append("parse_error")
            continue
        parse_ok += 1
        valid, errors = validate_schema(obj)
        if valid:
            schema_ok += 1
        else:
            all_errors.extend(errors)

    return parse_ok, schema_ok, all_errors


def main() -> None:
    texts = [f"sample {i}: investigation and delay risk in rollout." for i in range(1, 21)]

    print("Data declaration")
    print("source=in_script_structured_batch")
    print(f"records={len(texts)}")
    print("input_schema=text:str")
    print("output_schema={summary, risks, citations}")

    p1, s1, e1 = evaluate("json_weak", texts)
    p2, s2, e2 = evaluate("json_strong", texts)

    n = len(texts)
    print(f"weak_parse_rate={p1/n:.3f} weak_schema_rate={s1/n:.3f} weak_top_error={most_common_error(e1)}")
    print(f"strong_parse_rate={p2/n:.3f} strong_schema_rate={s2/n:.3f} strong_top_error={most_common_error(e2)}")
    print("Interpretation: stronger output constraints increase integration reliability.")


if __name__ == "__main__":
    main()
