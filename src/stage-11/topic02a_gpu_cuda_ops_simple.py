"""
topic02a_gpu_cuda_ops_simple

Stage 11 topic script.

Functional flow:
1. Declare infrastructure workload schema.
2. Run baseline and improved paths with fixed workload profile.
3. Save metrics and sample outputs.
4. Print interpretation for operations decisions.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage11_utils import run_topic_demo, run_gpu_demo


if __name__ == "__main__":
    run_topic_demo(
        topic_id="topic02a_gpu_cuda_ops_simple",
        topic_name="GPU and CUDA Operations",
        complexity="simple",
        method_focus="gpu_cuda_ops",
    )
    # Additional CUDA benchmark for GPU topics.
    run_gpu_demo(
        topic_id="topic02a_gpu_cuda_ops_simple",
        complexity="simple",
    )
