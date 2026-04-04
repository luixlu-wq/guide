"""
topic05c_pattern_comparison_advanced

Stage 12 topic script.

Functional flow:
1. Declare architecture-eval data contract.
2. Run baseline and improved pattern metrics on fixed eval set.
3. Save metrics and sample outputs.
4. Print interpretation for pattern decision workflow.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage12_utils import run_topic_demo, run_pytorch_cuda_reference


if __name__ == "__main__":
    run_topic_demo(
        topic_id="topic05c_pattern_comparison_advanced",
        topic_name="Pattern Comparison",
        complexity="advanced",
        method_focus="pattern_comparison",
    )
    # Runtime reference benchmark for architecture tradeoff context.
    run_pytorch_cuda_reference(
        topic_id="topic05c_pattern_comparison_advanced",
        complexity="advanced",
    )
