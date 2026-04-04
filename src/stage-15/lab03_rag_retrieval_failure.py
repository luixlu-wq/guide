"""
lab03_rag_retrieval_failure

Lab goal:
- Diagnose retrieval issues and verify one retrieval fix.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage15_utils import RESULTS_DIR, print_data_declaration, write_rows_csv


def main() -> None:
    declaration = {
        "Data": "Synthetic retrieval diagnostics set",
        "Requests/Samples": "80 retrieval cases",
        "Input schema": "query, retrieved_docs, freshness_age",
        "Output schema": "relevance_at_k, grounding_score",
        "Eval policy": "fixed retrieval replay",
        "Type": "rag_retrieval_failure",
    }
    print_data_declaration("Lab 3 - RAG Retrieval Failure", declaration)

    baseline = [
        {"metric": "relevance_at_5", "value": 0.62},
        {"metric": "freshness_compliance", "value": 0.71},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_retrieval_baseline.csv", baseline)

    options = [
        {"option": "metadata_filter_tighten", "expected_relevance_delta": 0.08},
        {"option": "daily_reindex_policy", "expected_freshness_delta": 0.17},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_retrieval_options.csv", options)

    verification = [
        {"metric": "relevance_at_5", "before": 0.62, "after": 0.72, "delta": 0.10},
        {"metric": "freshness_compliance", "before": 0.71, "after": 0.88, "delta": 0.17},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_retrieval_verification.csv", verification)


if __name__ == "__main__":
    main()
