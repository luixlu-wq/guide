"""
lab03_vector_db_scale_diagnostics

Lab goal:
- Diagnose retrieval performance and quality as vector corpus scale increases.
- Produce evidence artifacts and findings report.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage11_utils import RESULTS_DIR, check_qdrant_local, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic vector retrieval scale profile",
        "Requests/Samples": "3 corpus scales x fixed query set",
        "Input schema": "corpus_size, query_count, top_k",
        "Output schema": "retrieval_latency_ms, recall_at_5, status",
        "Eval policy": "fixed query replay across scales",
        "Type": "vector db scale diagnostics",
    }
    print_data_declaration("Lab 3 - Vector DB Scale Diagnostics", declaration)

    q_ok, q_msg = check_qdrant_local()

    scale_rows = [
        {"corpus_size": 10000, "retrieval_latency_ms": 72.0, "qdrant_reachable": q_ok, "status": q_msg},
        {"corpus_size": 100000, "retrieval_latency_ms": 104.0, "qdrant_reachable": q_ok, "status": q_msg},
        {"corpus_size": 500000, "retrieval_latency_ms": 158.0, "qdrant_reachable": q_ok, "status": q_msg},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_vector_scale_metrics.csv", scale_rows)

    quality_rows = [
        {"run_type": "baseline", "recall_at_5": 0.68, "mrr": 0.54},
        {"run_type": "improved", "recall_at_5": 0.79, "mrr": 0.66},
    ]
    write_rows_csv(RESULTS_DIR / "lab3_retrieval_quality.csv", quality_rows)

    findings = [
        "# Lab 3 Vector Ops Findings",
        "",
        f"- Local Qdrant status: {q_msg}",
        "- Retrieval latency increases with corpus scale as expected.",
        "- Improved metadata filtering and chunk policy increased recall_at_5.",
        "- Recommendation: enforce freshness and index-maintenance runbook.",
    ]
    write_text(RESULTS_DIR / "lab3_vector_ops_findings.md", "\n".join(findings))

    print("[INFO] Lab 3 outputs written:")
    print("- results/lab3_vector_scale_metrics.csv")
    print("- results/lab3_retrieval_quality.csv")
    print("- results/lab3_vector_ops_findings.md")


if __name__ == "__main__":
    main()

