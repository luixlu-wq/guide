"""
lab01_modular_ai_backend

Lab goal:
- Build and validate a modular backend blueprint with clear boundaries.
- Produce contract and latency artifacts that are reviewable.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage9_utils import RESULTS_DIR, aggregate_latency, print_data_declaration, write_json, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic API request profiles",
        "Requests/Samples": "100 representative requests",
        "Input schema": "request_id:str, endpoint:str, payload:dict",
        "Output schema": "status:int, response_body:dict, latency_ms:float",
        "Eval policy": "fixed deterministic latency profile",
        "Type": "architecture modular backend",
    }
    print_data_declaration("Lab 1 - Modular AI Backend", declaration)

    # API contract artifact used by frontend/backend integration checks.
    api_contract = {
        "service_name": "stage9_ai_backend",
        "version": "v1",
        "endpoints": [
            {
                "path": "/health",
                "method": "GET",
                "request_schema": {},
                "response_schema": {"status": "str"},
            },
            {
                "path": "/predict",
                "method": "POST",
                "request_schema": {"query": "str", "context": "optional[str]"},
                "response_schema": {"route": "str", "answer": "str", "trace_id": "str"},
            },
            {
                "path": "/retrieve",
                "method": "POST",
                "request_schema": {"query": "str", "top_k": "int", "filters": "optional[dict]"},
                "response_schema": {"matches": "list[dict]", "trace_id": "str"},
            },
        ],
    }
    write_json(RESULTS_DIR / "lab1_api_contract.json", api_contract)

    # Deterministic component latency model to teach latency budget decomposition.
    api_lat = [22 + (i % 4) for i in range(100)]
    retrieval_lat = [55 + (i % 7) for i in range(100)]
    model_lat = [160 + (i % 11) for i in range(100)]
    post_lat = [14 + (i % 3) for i in range(100)]
    total_lat = [a + r + m + p for a, r, m, p in zip(api_lat, retrieval_lat, model_lat, post_lat)]

    rows = [
        {"component": "api", **aggregate_latency(api_lat)},
        {"component": "retrieval", **aggregate_latency(retrieval_lat)},
        {"component": "model", **aggregate_latency(model_lat)},
        {"component": "postprocess", **aggregate_latency(post_lat)},
        {"component": "end_to_end", **aggregate_latency(total_lat)},
    ]
    write_rows_csv(RESULTS_DIR / "lab1_latency_breakdown.csv", rows)

    checklist = [
        "# Lab 1 Boundary Checklist",
        "",
        "- API layer owns transport, auth, and schema validation only.",
        "- Retrieval layer owns indexing/query/filter logic only.",
        "- Model layer owns inference logic only.",
        "- Observability layer tags all events with trace_id/request_id.",
        "- No module imports leak across boundaries in invalid direction.",
    ]
    write_text(RESULTS_DIR / "lab1_boundary_checklist.md", "\n".join(checklist))

    print("[INFO] Lab 1 outputs written:")
    print("- results/lab1_api_contract.json")
    print("- results/lab1_latency_breakdown.csv")
    print("- results/lab1_boundary_checklist.md")


if __name__ == "__main__":
    main()
