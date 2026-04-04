"""Stage 5 Topic 07: prompt evaluation regression checks.

Data: fixed prompt evaluation set
Records/Samples: 12
Input schema: id, text
Output schema: prompt metrics table
Split/Eval policy: same set across prompt versions
Type: reliability diagnostics
"""

from __future__ import annotations

from statistics import mean

from stage5_utils import lexical_overlap_score, mock_llm


def score_output(text: str, output: str) -> dict[str, float]:
    overlap = lexical_overlap_score(text, output)
    has_risk = 1.0 if "risk" in output.lower() else 0.0
    return {"overlap": overlap, "has_risk": has_risk, "total": 0.7 * overlap + 0.3 * has_risk}


# Workflow:
# 1) Run v1 and v2 prompts on the same evaluation set.
# 2) Compute stable metrics for both versions.
# 3) Report delta to catch regressions.
def main() -> None:
    samples = [
        f"case-{i}: revenue outlook updated with potential regulatory and delay concerns."
        for i in range(1, 13)
    ]

    v1_totals = []
    v2_totals = []

    print("Data declaration")
    print("source=in_script_prompt_eval_set")
    print(f"records={len(samples)}")
    print("input_schema=text:str")
    print("output_schema=metrics:{overlap,has_risk,total}")

    for text in samples:
        out_v1 = mock_llm(text, "vague")
        out_v2 = mock_llm(text, "specific")
        m1 = score_output(text, out_v1)
        m2 = score_output(text, out_v2)
        v1_totals.append(m1["total"])
        v2_totals.append(m2["total"])

    avg_v1 = mean(v1_totals)
    avg_v2 = mean(v2_totals)
    print(f"v1_total_score={avg_v1:.4f}")
    print(f"v2_total_score={avg_v2:.4f}")
    print(f"delta={avg_v2 - avg_v1:+.4f}")
    print("Interpretation: prompt updates should be accepted only with measured improvement.")


if __name__ == "__main__":
    main()
