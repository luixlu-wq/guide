"""
topic10a_adapter_merge_simple

Simple adapter-merging intuition:
- show task-specific adapter strengths
- introduce merge objective
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import print_data_declaration


def main() -> None:
    declaration = {
        "Data": "Synthetic task-score table",
        "Records": "2 tasks x 2 adapters",
        "Input schema": "task, adapter_a_score, adapter_b_score",
        "Output schema": "merge_intuition",
        "Split/Eval policy": "fixed deterministic scores",
        "Type": "adapter merge foundations",
    }
    print_data_declaration("Topic10A Adapter Merge Simple", declaration)

    rows = [
        {"task": "ontario_gis_formatting", "adapter_a": 0.92, "adapter_b": 0.61},
        {"task": "general_translation", "adapter_a": 0.58, "adapter_b": 0.90},
    ]
    for r in rows:
        print(r)

    print(
        "\nInterpretation: merge aims to keep strengths from both adapters while limiting regression."
    )


if __name__ == "__main__":
    main()

