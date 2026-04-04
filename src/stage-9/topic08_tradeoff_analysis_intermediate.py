"""
topic08_tradeoff_analysis_intermediate

This Stage 9 topic script is runnable and deterministic.

Functional flow:
1. Declare data source and schema.
2. Run baseline and improved architecture paths on fixed eval data.
3. Save metrics and sample outputs for auditability.
4. Print interpretation focused on quality-latency-cost tradeoffs.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import run_topic_demo


if __name__ == "__main__":
    run_topic_demo(
        topic_id="topic08_tradeoff_analysis_intermediate",
        topic_name="Architecture Decision Records",
        complexity="intermediate",
        method_focus="decision",
    )

