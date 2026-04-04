"""
topic03a_evaluation_pack_simple

Stage 13 topic script.

Functional flow:
1. Declare data schema and evaluation policy.
2. Run baseline and improved deterministic metrics.
3. Save metrics and representative outputs.
4. Print interpretation-oriented artifact locations.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage13_utils import run_topic_demo, run_pytorch_cuda_reference


if __name__ == "__main__":
    # Main deterministic topic demonstration.
    run_topic_demo(
        topic_id="topic03a_evaluation_pack_simple",
        topic_name="Evaluation Pack",
        complexity="simple",
        method_focus="evaluation_pack",
    )
    # Runtime benchmark provides PyTorch/CUDA evidence for this module.
    run_pytorch_cuda_reference(
        topic_id="topic03a_evaluation_pack_simple",
        complexity="simple",
    )
