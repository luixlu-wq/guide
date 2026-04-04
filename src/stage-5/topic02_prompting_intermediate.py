"""Stage 5 Topic 02: prompt version comparison (intermediate).

Data: in-script mini dataset
Records/Samples: 8
Input schema: id, text
Output schema: prompt outputs + quality scores
Split/Eval policy: same dataset for v1 vs v2 comparison
Type: prompt iteration workflow
"""

from __future__ import annotations

from statistics import mean

from stage5_utils import lexical_overlap_score, mock_llm


def quality_score(text: str, output: str) -> float:
    score = 0.0
    if "risks" in output.lower() or "risk" in output.lower():
        score += 0.35
    if len(output.split()) >= 12:
        score += 0.25
    score += 0.40 * lexical_overlap_score(text, output)
    return min(score, 1.0)


# Workflow:
# 1) Evaluate baseline prompt (v1=vague) on fixed dataset.
# 2) Evaluate improved prompt (v2=specific) with same data.
# 3) Compare average quality score delta.
def main() -> None:
    samples = [
        "Revenue rose but debt costs increased.",
        "Company faces lawsuit risk after product recall.",
        "Guidance improved due to stronger enterprise demand.",
        "Regulatory review may delay launch timeline.",
        "Margins expanded while logistics costs normalized.",
        "Management warned about volatility in ad demand.",
        "New model release improved retention metrics.",
        "Analysts downgraded outlook due to weaker pipeline.",
    ]

    v1_scores = []
    v2_scores = []

    print("Data declaration")
    print("source=in_script_prompt_dataset")
    print(f"records={len(samples)}")
    print("input_schema=text:str")
    print("output_schema=response:str, score:float")

    for idx, text in enumerate(samples, start=1):
        out_v1 = mock_llm(text, "vague")
        out_v2 = mock_llm(text, "specific")
        s1 = quality_score(text, out_v1)
        s2 = quality_score(text, out_v2)
        v1_scores.append(s1)
        v2_scores.append(s2)
        print(f"sample={idx} score_v1={s1:.3f} score_v2={s2:.3f}")

    avg_v1 = mean(v1_scores)
    avg_v2 = mean(v2_scores)
    print(f"avg_score_v1={avg_v1:.4f}")
    print(f"avg_score_v2={avg_v2:.4f}")
    print(f"delta={avg_v2 - avg_v1:+.4f}")
    print("Interpretation: prompt versions should be compared with fixed data and explicit metrics.")


if __name__ == "__main__":
    main()
