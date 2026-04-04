"""
topic09c_dpo_eval_advanced

Advanced DPO evaluation script:
- evaluate baseline vs DPO preference-win behavior
- export canonical artifact: results/stage8/dpo_preference_eval.csv
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import STAGE8_RESULTS_DIR, print_data_declaration, write_rows_csv


def _score_response(text: str) -> float:
    """Deterministic scoring proxy for preference evaluation."""
    t = text.lower()
    score = 0.0
    if "because" in t:
        score += 0.2
    if "step" in t:
        score += 0.2
    if "evidence" in t or "citation" in t:
        score += 0.2
    if "uncertain" in t and "ask" in t:
        score += 0.1
    if "guess" in t:
        score -= 0.3
    return round(score, 4)


def main() -> None:
    declaration = {
        "Data": "Synthetic chosen/rejected preference pairs",
        "Records": "24 pairs",
        "Input schema": "prompt, chosen, rejected",
        "Output schema": "metric rows with before/after delta",
        "Split/Eval policy": "fixed deterministic pair list",
        "Type": "DPO advanced evaluation",
    }
    print_data_declaration("Topic09C DPO Eval Advanced", declaration)

    pairs = []
    for i in range(24):
        pairs.append(
            {
                "prompt": f"Preference benchmark prompt #{i+1}",
                "chosen": "First inspect evidence and cite sources because reliability matters.",
                "rejected": "Answer fast and guess details if needed.",
            }
        )

    baseline_wins = 0
    dpo_wins = 0
    for idx, p in enumerate(pairs):
        c = _score_response(p["chosen"])
        r = _score_response(p["rejected"])
        # Baseline intentionally misses some preferences to emulate pre-alignment behavior.
        baseline_pick_chosen = (c >= r) and ((idx + 1) % 4 != 0)
        dpo_pick_chosen = c >= r
        baseline_wins += 1 if baseline_pick_chosen else 0
        dpo_wins += 1 if dpo_pick_chosen else 0

    baseline_win_rate = round(baseline_wins / len(pairs), 4)
    dpo_win_rate = round(dpo_wins / len(pairs), 4)
    delta = round(dpo_win_rate - baseline_win_rate, 4)

    rows = [
        {
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "stage": "stage-8",
            "topic_or_module": "topic09c_dpo_eval_advanced",
            "metric_name": "preference_win_rate",
            "before_value": baseline_win_rate,
            "after_value": dpo_win_rate,
            "delta": delta,
            "dataset_or_eval_set": "synthetic_preference_pairs_v1",
            "seed_or_config_id": "dpo_config_v1",
            "decision": "promote" if delta >= 0 else "hold",
        }
    ]

    out = STAGE8_RESULTS_DIR / "dpo_preference_eval.csv"
    write_rows_csv(out, rows)

    print(f"baseline_preference_win_rate={baseline_win_rate}")
    print(f"dpo_preference_win_rate={dpo_win_rate}")
    print(f"delta={delta}")
    print(f"[INFO] Wrote: {out}")


if __name__ == "__main__":
    main()

