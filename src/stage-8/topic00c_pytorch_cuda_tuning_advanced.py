"""
topic00c_pytorch_cuda_tuning_advanced

Workflow:
1. Declare data and schema used in this runnable example.
2. Run a complete training loop (forward, loss, backward, optimizer).
3. Use CUDA when available, and keep CPU fallback if not available.
4. Save metrics artifact for reproducible review.
5. Print interpretation so learners know what success looks like.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import run_pytorch_cuda_demo


if __name__ == "__main__":
    run_pytorch_cuda_demo(topic_id="topic00c_pytorch_cuda_tuning_advanced", complexity="advanced")
