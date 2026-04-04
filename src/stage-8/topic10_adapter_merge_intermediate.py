"""
topic10_adapter_merge_intermediate

Intermediate adapter merge simulation:
- evaluate two task-specific adapters
- simulate merged scores
- inspect tradeoffs
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import print_data_declaration


def _merge_score(a: float, b: float) -> float:
    """Simple weighted merge proxy used for deterministic teaching."""
    return round(0.55 * max(a, b) + 0.45 * min(a, b), 4)


def main() -> None:
    declaration = {
        "Data": "Synthetic adapter-task score matrix",
        "Records": "3 tasks",
        "Input schema": "task, adapter_a, adapter_b",
        "Output schema": "merged_score",
        "Split/Eval policy": "fixed deterministic matrix",
        "Type": "adapter merge intermediate",
    }
    print_data_declaration("Topic10 Adapter Merge Intermediate", declaration)

    tasks = [
        ("ontario_gis_formatting", 0.93, 0.60),
        ("general_translation", 0.57, 0.91),
        ("citation_style_consistency", 0.84, 0.78),
    ]

    for task, a, b in tasks:
        m = _merge_score(a, b)
        print({"task": task, "adapter_a": a, "adapter_b": b, "merged": m})

    print("\nInterpretation: merged adapter should reduce task-specific blind spots.")


if __name__ == "__main__":
    main()

