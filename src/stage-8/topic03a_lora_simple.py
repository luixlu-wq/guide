"""
topic03a_lora_simple

Workflow:
1. Declare data source and structure before running any model logic.
2. Run baseline and tuned paths on the same fixed split.
3. Save metrics and sample outputs so results are auditable.
4. Print interpretation focused on quality-cost tradeoffs.
5. Keep deterministic behavior to support fair comparisons.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import run_topic_demo


if __name__ == "__main__":
    run_topic_demo(
        topic_id="topic03a_lora_simple",
        topic_name="LoRA Tuning",
        complexity="simple",
        method_focus="lora",
    )
