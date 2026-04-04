"""Stage 5 Topic 02C: prompt stability and regression checks (advanced).

Data: fixed in-script prompt-eval set
Records/Samples: 6
Input schema: id, text
Output schema: repeated outputs + stability metrics
Split/Eval policy: fixed repeated runs under same prompt settings
Type: advanced prompt evaluation
"""

from __future__ import annotations

from statistics import mean

from stage5_utils import lexical_overlap_score, mock_llm


def stability_score(outputs: list[str]) -> float:
    if len(outputs) < 2:
        return 1.0
    pairs = []
    for i in range(len(outputs)):
        for j in range(i + 1, len(outputs)):
            pairs.append(lexical_overlap_score(outputs[i], outputs[j]))
    return mean(pairs)


# Workflow:
# 1) Run repeated generations for each prompt mode.
# 2) Measure intra-prompt stability.
# 3) Compare deterministic-style prompting vs higher-variance style.
def main() -> None:
    texts = [
        "Supplier delay may reduce next-quarter shipments.",
        "Strong recurring revenue offset weaker hardware demand.",
        "Audit findings triggered compliance review and legal costs.",
        "Cloud contracts expanded in healthcare segment.",
        "Guidance cut due to macro uncertainty and slower pipeline.",
        "Operating margin improved after restructuring program.",
    ]

    print("Data declaration")
    print("source=in_script_prompt_regression_set")
    print(f"records={len(texts)}")
    print("input_schema=text:str")
    print("output_schema=repeated_outputs + stability_score")

    stable_scores = []
    variable_scores = []

    for text in texts:
        stable_outputs = [mock_llm(text, "specific", temperature=0.0) for _ in range(4)]
        variable_outputs = [mock_llm(text, "few_shot", temperature=0.8 + i * 0.1) for i in range(4)]
        s_stable = stability_score(stable_outputs)
        s_var = stability_score(variable_outputs)
        stable_scores.append(s_stable)
        variable_scores.append(s_var)

    print(f"mean_stability_specific={mean(stable_scores):.4f}")
    print(f"mean_stability_few_shot_variance={mean(variable_scores):.4f}")
    print("Interpretation: advanced prompt workflow requires stability/regression checks, not one-off wins.")


if __name__ == "__main__":
    main()
