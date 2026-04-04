"""
topic08_ops_release_intermediate

Stage 10 topic script.

Functional flow:
1. Declare data/source/schema contract through stage10_utils.
2. Run baseline and improved paths on fixed data/evaluation policy.
3. Save metrics and sample outputs for auditability.
4. Print interpretation for troubleshooting and improvement decisions.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import run_topic_demo, run_pytorch_cuda_component


if __name__ == "__main__":
    run_topic_demo(
        topic_id="topic08_ops_release_intermediate",
        topic_name="Operations and Release",
        complexity="intermediate",
        method_focus="ops_release",
    )
