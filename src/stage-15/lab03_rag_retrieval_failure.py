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

from stage15_utils import (
    print_data_declaration,
    write_rows_csv_dual,
    write_text_dual,
    resolve_project_profile,
    build_gis_boundary_compare_rows,
    build_gis_boundary_report,
    build_icv_audit_trail,
)


def main() -> None:
    project = resolve_project_profile()
    declaration = {
        "Data": "Synthetic retrieval diagnostics set",
        "Requests/Samples": "80 retrieval cases",
        "Input schema": "query, retrieved_docs, freshness_age",
        "Output schema": "relevance_at_k, grounding_score",
        "Eval policy": "fixed retrieval replay",
        "Type": f"rag_retrieval_failure/{project}",
    }
    print_data_declaration("Lab 3 - RAG Retrieval Failure", declaration)

    baseline = [
        {"metric": "relevance_at_5", "value": 0.62},
        {"metric": "freshness_compliance", "value": 0.71},
    ]
    write_rows_csv_dual("lab3_retrieval_baseline.csv", baseline)

    options = [
        {"option": "metadata_filter_tighten", "expected_relevance_delta": 0.08},
        {"option": "daily_reindex_policy", "expected_freshness_delta": 0.17},
    ]
    write_rows_csv_dual("lab3_retrieval_options.csv", options)

    verification = [
        {"metric": "relevance_at_5", "before": 0.62, "after": 0.72, "delta": 0.10},
        {"metric": "freshness_compliance", "before": 0.71, "after": 0.88, "delta": 0.17},
    ]
    write_rows_csv_dual("lab3_retrieval_verification.csv", verification)

    # Canonical chapter-aligned artifacts.
    write_rows_csv_dual("retrieval_diagnostics.csv", baseline)
    write_rows_csv_dual("groundedness_delta.csv", [{"metric": "grounding_score", "before": 0.64, "after": 0.82, "delta": 0.18}])

    boundary_compare = build_gis_boundary_compare_rows()
    write_rows_csv_dual("lab03_projection_vs_topk_compare.csv", boundary_compare)

    icv_block = build_icv_audit_trail(
        identify_metric="retrieval_hit_rate",
        identify_threshold="< 0.80 on boundary cases",
        failing_case="ontario_boundary_001",
        option_a="projection_fix_nad83_to_wgs84",
        option_b="increase_top_k_5_to_12",
        verification_delta="boundary retrieval_hit: 0 -> 1 with projection fix",
        decision="promote",
    )
    write_text_dual("lab03_gis_boundary_failure_report.md", build_gis_boundary_report(project) + "\n\n" + icv_block)


if __name__ == "__main__":
    main()
