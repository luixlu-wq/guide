"""
topic10c_task_arithmetic_advanced

Advanced adapter-merging evaluation:
- compare adapter A, adapter B, and merged adapter across tasks
- export canonical artifact: results/stage8/adapter_merge_matrix.csv
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import STAGE8_RESULTS_DIR, print_data_declaration, write_rows_csv


def _merge_score(a: float, b: float) -> float:
    """Deterministic merge proxy (teaching approximation for merge strategies)."""
    return round((a * 0.6) + (b * 0.4), 4)


def main() -> None:
    declaration = {
        "Data": "Synthetic multi-task adapter score matrix",
        "Records": "4 tasks",
        "Input schema": "task, adapter_a_score, adapter_b_score",
        "Output schema": "merged_score, regression flags",
        "Split/Eval policy": "fixed deterministic matrix",
        "Type": "task arithmetic / adapter merge advanced",
    }
    print_data_declaration("Topic10C Task Arithmetic Advanced", declaration)

    matrix = [
        ("ontario_gis_formatting", 0.94, 0.62),
        ("general_translation", 0.60, 0.92),
        ("citation_style_consistency", 0.86, 0.78),
        ("instruction_following", 0.82, 0.84),
    ]

    rows = []
    for task, a, b in matrix:
        merged = _merge_score(a, b)
        best_single = max(a, b)
        regression = round(best_single - merged, 4) > 0.08
        rows.append(
            {
                "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                "task": task,
                "adapter_a_score": a,
                "adapter_b_score": b,
                "merged_score": merged,
                "best_single_score": best_single,
                "regression_flag": regression,
            }
        )

    out = STAGE8_RESULTS_DIR / "adapter_merge_matrix.csv"
    write_rows_csv(out, rows)
    print(f"[INFO] Wrote: {out}")
    print("Interpretation: merged adapter should avoid severe regressions on any protected task.")


if __name__ == "__main__":
    main()

