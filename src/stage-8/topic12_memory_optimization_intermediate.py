"""
topic12_memory_optimization_intermediate

Intermediate memory optimization guide:
- compare baseline vs checkpoint-enabled config assumptions
- print expected tradeoffs
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
        "Data": "Config comparison table",
        "Records": "2 configs",
        "Input schema": "config, checkpointing, attention_path",
        "Output schema": "estimated memory/latency tradeoff",
        "Split/Eval policy": "fixed deterministic table",
        "Type": "memory optimization intermediate",
    }
    print_data_declaration("Topic12 Memory Optimization Intermediate", declaration)

    rows = [
        {
            "config": "baseline",
            "checkpointing": False,
            "flash_attention_path": "off",
            "expected_memory": "higher",
            "expected_latency": "lower",
        },
        {
            "config": "optimized",
            "checkpointing": True,
            "flash_attention_path": "on if supported",
            "expected_memory": "lower",
            "expected_latency": "higher",
        },
    ]
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()

