"""
topic09a_dpo_foundations_simple

Simple DPO foundations walkthrough:
- define preference pair structure
- score chosen vs rejected quality
- report baseline preference-win estimate
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import print_data_declaration


def _quality_score(text: str) -> float:
    """Tiny deterministic quality score used only for teaching preference ranking."""
    score = 0.0
    t = text.lower()
    if "because" in t:
        score += 0.2
    if "step" in t or "first" in t:
        score += 0.2
    if len(text) > 40:
        score += 0.2
    if "unsafe" in t or "ignore policy" in t:
        score -= 0.4
    return round(score, 4)


def main() -> None:
    declaration = {
        "Data": "Inline synthetic preference pairs",
        "Records": "6 preference pairs",
        "Input schema": "prompt:str, chosen:str, rejected:str",
        "Output schema": "win_rate:float",
        "Split/Eval policy": "fixed deterministic examples",
        "Type": "DPO foundations (simple)",
    }
    print_data_declaration("Topic09A DPO Foundations Simple", declaration)

    pairs = [
        {
            "prompt": "Explain Ontario subdivision validation.",
            "chosen": "First validate geometry, then verify IDs because structure errors propagate.",
            "rejected": "Looks fine. Ship it.",
        },
        {
            "prompt": "How should we handle unknown evidence?",
            "chosen": "State insufficient evidence and ask for a supported source.",
            "rejected": "Answer anyway from memory.",
        },
        {
            "prompt": "How to debug retrieval misses?",
            "chosen": "Step 1 inspect chunk IDs, step 2 inspect top-k scores, then rerank.",
            "rejected": "Just increase model size.",
        },
    ]

    wins = 0
    for p in pairs:
        c = _quality_score(p["chosen"])
        r = _quality_score(p["rejected"])
        win = c >= r
        wins += 1 if win else 0
        print({"prompt": p["prompt"], "chosen_score": c, "rejected_score": r, "chosen_wins": win})

    win_rate = round(wins / len(pairs), 4)
    print(f"\npreference_win_rate={win_rate}")
    print("Interpretation: DPO optimizes model preference toward chosen responses.")


if __name__ == "__main__":
    main()

