"""Stage 5 Topic 02A: prompt specificity (simple).

Data: one in-script news paragraph
Records/Samples: 1
Input schema: text
Output schema: free-text response
Split/Eval policy: not applicable
Type: prompt engineering basics
"""

from __future__ import annotations

from stage5_utils import lexical_overlap_score, mock_llm


# Workflow:
# 1) Run a vague prompt style and a specific prompt style on same input.
# 2) Compare output clarity and risk signal presence.
# 3) Print overlap score to show content anchoring.
def main() -> None:
    text = (
        "ACME announced quarterly revenue growth, but warned that a regulatory "
        "investigation and component shortage may delay product launch."
    )

    vague = mock_llm(text, "vague")
    specific = mock_llm(text, "specific")

    print("Data declaration")
    print("source=in_script_news_text")
    print("records=1")
    print("input_schema=text:str")
    print("output_schema=response:str")

    print("\nresponse_vague:")
    print(vague)
    print("\nresponse_specific:")
    print(specific)

    print(f"overlap_vague={lexical_overlap_score(text, vague):.4f}")
    print(f"overlap_specific={lexical_overlap_score(text, specific):.4f}")
    print("Interpretation: specific prompts usually produce more anchored and useful outputs.")


if __name__ == "__main__":
    main()
