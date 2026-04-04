"""
topic01a_qdrant_ingest_simple

This Stage 9 topic script is runnable and deterministic.

Functional flow:
1. Declare data source and schema.
2. Run retrieval diagnostics with optional local Qdrant check.
3. Save metrics artifact for audit and comparison.
4. Print interpretation focused on architecture tradeoffs.
"""

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import run_qdrant_topic_demo


if __name__ == "__main__":
    run_qdrant_topic_demo(
        topic_id="topic01a_qdrant_ingest_simple",
        complexity="simple",
    )

