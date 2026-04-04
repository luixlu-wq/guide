"""Stage 5 Topic 07C: chain-of-thought style comparison (advanced prompting).

Data: in-script arithmetic/logic word problems with ground-truth answers
Records/Samples: 8
Input schema: problem_text:str, answer:int
Output schema: raw_prediction:int, cot_prediction:int, correctness flags
Split/Eval policy: fixed benchmark list
Type: prompting strategy comparison
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def raw_completion_style(problem: str) -> int:
    """Naive baseline that often fails on compositional logic."""
    nums = [int(n) for n in re.findall(r"-?\d+", problem)]
    return nums[0] if nums else 0


def cot_style_solver(problem: str) -> int:
    """Simple step-by-step parser for + / - style word problems.

    This is not an LLM call. It is an offline stand-in to demonstrate
    why an explicit reasoning procedure can outperform a shallow answer heuristic.
    """
    nums = [int(n) for n in re.findall(r"-?\d+", problem)]
    text = problem.lower()
    if not nums:
        return 0

    # Reasoning skeleton:
    # 1) start from first quantity
    # 2) apply adds/subtracts in narrative order
    total = nums[0]
    idx = 1
    for token in re.findall(r"[a-z']+", text):
        if idx >= len(nums):
            break
        if token in {"buys", "gets", "adds", "gains", "found", "receives", "more"}:
            total += nums[idx]
            idx += 1
        elif token in {"loses", "gives", "spends", "removes", "left", "away"}:
            total -= nums[idx]
            idx += 1
    return total


# Workflow:
# 1) Evaluate the same problems using a raw-answer baseline.
# 2) Evaluate using a step-by-step reasoning policy (CoT-style).
# 3) Compare accuracy and save before/after evidence.
def main() -> None:
    dataset = [
        ("Alice has 7 apples and buys 3 more. How many now?", 10),
        ("A store had 20 books and sold 6. How many remain?", 14),
        ("Tom starts with 12 coins, gives away 5, then gets 4. Total?", 11),
        ("A tank has 30 liters, loses 8, then loses 7. Remaining?", 15),
        ("You own 9 tickets, buy 2, buy 2 more. Total tickets?", 13),
        ("Mia had 15 stickers, gave 4, found 6. How many now?", 17),
        ("Server queue is 18, removes 9, adds 3. Queue length?", 12),
        ("Portfolio had 25 units, spends 10, receives 5. Final?", 20),
    ]

    print("Data declaration")
    print("source=in_script_logic_problems")
    print(f"records={len(dataset)}")
    print("input_schema=problem_text:str")
    print("output_schema=raw_prediction:int, cot_prediction:int")

    rows: list[dict[str, str | int | bool]] = []
    raw_correct = 0
    cot_correct = 0

    for i, (problem, answer) in enumerate(dataset, start=1):
        raw_pred = raw_completion_style(problem)
        cot_pred = cot_style_solver(problem)
        raw_ok = raw_pred == answer
        cot_ok = cot_pred == answer
        raw_correct += int(raw_ok)
        cot_correct += int(cot_ok)

        rows.append(
            {
                "case_id": i,
                "problem": problem,
                "answer": answer,
                "raw_prediction": raw_pred,
                "cot_prediction": cot_pred,
                "raw_correct": raw_ok,
                "cot_correct": cot_ok,
            }
        )

    raw_acc = raw_correct / len(dataset)
    cot_acc = cot_correct / len(dataset)
    print(f"raw_completion_accuracy={raw_acc:.4f}")
    print(f"cot_style_accuracy={cot_acc:.4f}")
    print(f"delta={cot_acc - raw_acc:+.4f}")

    out_dir = Path(__file__).parent / "results" / "stage5"
    out_dir.mkdir(parents=True, exist_ok=True)

    detail_path = out_dir / "topic07c_chain_of_thought_cases.csv"
    pd.DataFrame(rows).to_csv(detail_path, index=False)

    metrics_path = out_dir / "topic07c_chain_of_thought_metrics.csv"
    pd.DataFrame(
        [
            {
                "run_id": "stage5_topic07c_chain_of_thought",
                "stage": "5",
                "topic_or_module": "topic07c_chain_of_thought",
                "metric_name": "accuracy",
                "before_value": raw_acc,
                "after_value": cot_acc,
                "delta": cot_acc - raw_acc,
                "dataset_or_eval_set": "logic_problem_set",
                "seed_or_config_id": "deterministic_rule_demo",
                "decision": "promote" if cot_acc >= raw_acc else "hold",
            }
        ]
    ).to_csv(metrics_path, index=False)

    print(f"Saved: {detail_path}")
    print(f"Saved: {metrics_path}")
    print("Interpretation: explicit reasoning policy can improve reliability on compositional tasks.")


if __name__ == "__main__":
    main()

