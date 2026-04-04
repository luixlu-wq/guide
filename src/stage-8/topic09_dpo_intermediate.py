"""
topic09_dpo_intermediate

Intermediate DPO workflow simulation:
- build fixed preference dataset
- estimate baseline preference-win
- estimate post-DPO preference-win
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import print_data_declaration


def _score_response(text: str) -> float:
    """Deterministic scoring proxy for preference optimization examples."""
    t = text.lower()
    score = 0.0
    if "because" in t:
        score += 0.2
    if "step" in t or "first" in t:
        score += 0.2
    if "evidence" in t or "citation" in t:
        score += 0.2
    if "always" in t and "guess" in t:
        score -= 0.4
    if len(text) > 60:
        score += 0.1
    return round(score, 4)


def main() -> None:
    declaration = {
        "Data": "Inline preference pairs",
        "Records": "10 preference pairs",
        "Input schema": "prompt, chosen, rejected",
        "Output schema": "baseline_win_rate, dpo_win_rate",
        "Split/Eval policy": "fixed deterministic pair set",
        "Type": "DPO intermediate simulation",
    }
    print_data_declaration("Topic09 DPO Intermediate", declaration)

    pairs = []
    for i in range(10):
        pairs.append(
            {
                "prompt": f"Preference prompt #{i+1}",
                "chosen": "First inspect evidence, then answer with citation because traceability matters.",
                "rejected": "Always answer quickly and guess if evidence is weak.",
            }
        )

    # Baseline policy is simulated as weaker and misses some chosen preferences.
    baseline_wins = 0
    dpo_wins = 0

    for idx, p in enumerate(pairs):
        chosen_score = _score_response(p["chosen"])
        rejected_score = _score_response(p["rejected"])

        # Baseline misses every 3rd item to simulate weaker preference alignment.
        baseline_pick_chosen = (chosen_score >= rejected_score) and ((idx + 1) % 3 != 0)
        baseline_wins += 1 if baseline_pick_chosen else 0

        # DPO path is simulated as stronger preference alignment.
        dpo_pick_chosen = chosen_score >= rejected_score
        dpo_wins += 1 if dpo_pick_chosen else 0

    baseline_win_rate = round(baseline_wins / len(pairs), 4)
    dpo_win_rate = round(dpo_wins / len(pairs), 4)
    delta = round(dpo_win_rate - baseline_win_rate, 4)

    print(f"baseline_preference_win_rate={baseline_win_rate}")
    print(f"dpo_preference_win_rate={dpo_win_rate}")
    print(f"delta={delta}")
    print("Interpretation: DPO increases chosen-response preference rate on fixed pair set.")


if __name__ == "__main__":
    main()

