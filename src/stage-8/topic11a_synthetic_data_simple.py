"""
topic11a_synthetic_data_simple

Simple synthetic-data generation demo:
- generate instruction/response pairs from fixed templates
- print sample records
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
        "Data": "Template-generated synthetic instruction pairs",
        "Records": "12",
        "Input schema": "instruction, input",
        "Output schema": "structured response text",
        "Split/Eval policy": "fixed deterministic generation",
        "Type": "synthetic data simple",
    }
    print_data_declaration("Topic11A Synthetic Data Simple", declaration)

    templates = [
        "Summarize subdivision risk signals",
        "Generate policy-compliant response",
        "Extract structured trend/risk/reason output",
    ]
    records = []
    for i in range(12):
        records.append(
            {
                "id": f"syn_{i:03d}",
                "instruction": templates[i % len(templates)],
                "input": f"Ontario subdivision case {i}",
                "output": "trend=neutral; risk=medium; reason=insufficient supporting evidence.",
            }
        )

    print(f"generated_records={len(records)}")
    for r in records[:4]:
        print(r)


if __name__ == "__main__":
    main()

