"""
topic11_synthetic_data_curation_intermediate

Intermediate synthetic-data curation:
- generate synthetic records
- dedupe and quality-filter
- print retained vs removed summary
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
        "Data": "Synthetic instruction pairs",
        "Records": "200 raw generated",
        "Input schema": "instruction, input",
        "Output schema": "output text",
        "Split/Eval policy": "fixed deterministic generation/filter rules",
        "Type": "synthetic data curation intermediate",
    }
    print_data_declaration("Topic11 Synthetic Data Curation Intermediate", declaration)

    raw = []
    for i in range(200):
        instruction = "Generate Ontario GIS-safe structured summary"
        # Duplicate pattern every 10th row to force dedupe behavior.
        input_text = f"case_{i if i % 10 else 0}"
        output = (
            "trend=neutral; risk=medium; reason=provide citation before escalation."
            if i % 17 != 0
            else "bad"
        )
        raw.append({"instruction": instruction, "input": input_text, "output": output})

    # Dedupe by (instruction, input, output).
    seen = set()
    deduped = []
    for r in raw:
        k = (r["instruction"], r["input"], r["output"])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(r)

    # Quality filter: keep minimum output length threshold.
    curated = [r for r in deduped if len(r["output"]) >= 24]

    print(f"raw_count={len(raw)}")
    print(f"deduped_count={len(deduped)}")
    print(f"curated_count={len(curated)}")
    print(f"rejection_count={len(raw) - len(curated)}")


if __name__ == "__main__":
    main()

