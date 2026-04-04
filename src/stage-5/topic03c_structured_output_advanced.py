"""Stage 5 Topic 03C: structured output repair + fail-fast (advanced).

Data: in-script malformed output set
Records/Samples: 12
Input schema: raw model output text
Output schema: validated JSON object or explicit failure
Split/Eval policy: before-repair vs after-repair
Type: advanced output hardening workflow
"""

from __future__ import annotations

from stage5_utils import repair_json_text, try_parse_json, validate_schema


# Workflow:
# 1) Attempt parse/validate on raw outputs.
# 2) Apply repair strategy on failures.
# 3) Enforce fail-fast for still-invalid records.
def main() -> None:
    raw_outputs = [
        '{"summary": "stable quarter", "risks": ["none_detected"], "citations": []}',
        "{summary: 'delayed launch', risks: ['delay'], citations: []}",
        '{"summary": "legal review", "risks": ["investigation"]}',
        "{summary:'recall impact', risks:['recall'], citations:[]}",
        '{"summary": "margin pressure", "risks": ["debt"], "citations": []}',
        "{summary:'fraud alert', risks:['fraud'], citations:[]}",
        '{"summary": "regulatory update", "risks": ["regulatory"], "citations": []}',
        "{summary:'volatility expected', risks:['volatility'], citations:[]}",
        '{"summary": "shipment issue", "risks": ["shortage"], "citations": []}',
        "{summary:'downgrade risk', risks:['downgrade'], citations:[]}",
        '{"summary": "clean json", "risks": ["none_detected"], "citations": []}',
        "{summary:'missing citations field', risks:['delay']}",
    ]

    print("Data declaration")
    print("source=in_script_raw_output_set")
    print(f"records={len(raw_outputs)}")
    print("input_schema=raw_output:str")
    print("output_schema=validated_json_or_failure")

    before_valid = 0
    after_valid = 0
    hard_fail = 0

    for raw in raw_outputs:
        obj, err = try_parse_json(raw)
        if obj is not None:
            ok, _ = validate_schema(obj)
            if ok:
                before_valid += 1

        candidate = raw if obj is not None else repair_json_text(raw)
        obj2, err2 = try_parse_json(candidate)
        if obj2 is None:
            hard_fail += 1
            continue
        ok2, _ = validate_schema(obj2)
        if ok2:
            after_valid += 1
        else:
            hard_fail += 1

    n = len(raw_outputs)
    print(f"before_valid_rate={before_valid/n:.3f}")
    print(f"after_valid_rate={after_valid/n:.3f}")
    print(f"hard_fail_rate={hard_fail/n:.3f}")
    print("Interpretation: repair helps, but fail-fast handling is required for unresolved outputs.")


if __name__ == "__main__":
    main()
