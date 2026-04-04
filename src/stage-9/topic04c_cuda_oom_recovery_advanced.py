"""
topic04c_cuda_oom_recovery_advanced

This Stage 9 topic script demonstrates PyTorch/CUDA inference operations.

Functional flow:
1. Declare tensor data schema and fixed eval policy.
2. Run device-aware inference loop.
3. Use CUDA path when available, otherwise deterministic CPU fallback.
4. Save latency and throughput metrics for reliability checks.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import run_pytorch_cuda_inference_demo


if __name__ == "__main__":
    run_pytorch_cuda_inference_demo(
        topic_id="topic04c_cuda_oom_recovery_advanced",
        complexity="advanced",
    )

