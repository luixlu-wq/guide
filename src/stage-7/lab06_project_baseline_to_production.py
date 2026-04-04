"""Stage 7 Lab 06: Realistic project improvement from beginning to production.

Deliverables:
- results/lab6_project_baseline_outputs.jsonl
- results/lab6_project_improved_outputs.jsonl
- results/lab6_project_solution_options.csv
- results/lab6_project_metrics_comparison.csv
- results/lab6_project_verification_report.md
- results/lab6_project_production_readiness.md

Educational objective:
- Teach a full troubleshooting capability loop:
  1) identify failure from evidence,
  2) compare solution options,
  3) verify chosen fix with controlled reruns,
  4) make production promotion/rollback decision.
"""

from __future__ import annotations

from pathlib import Path

from stage7_utils import (
    RESULTS_DIR,
    answer_metrics,
    as_csv,
    as_jsonl,
    build_tfidf_index,
    dense_retrieve,
    ensure_stage7_dataset,
    grounded_answer,
    hybrid_retrieve,
    latency_and_cost,
    load_docs,
    load_eval_queries,
    now_ts,
    print_data_declaration,
    rerank_candidates,
    retrieval_metrics,
)


def run_baseline_flow(docs, queries, vectorizer, matrix) -> tuple[list[dict], dict[str, list[str]], list[dict]]:
    """Run intentionally simple baseline configuration.

    Baseline design choices (kept simple on purpose):
    - dense retrieval only
    - larger top-k (more noise)
    - lower grounding threshold (more chance of weakly-grounded output)
    - no reranker
    """
    outputs: list[dict] = []
    per_query_ids: dict[str, list[str]] = {}
    evidence_rows: list[dict] = []

    for q in queries:
        rows = dense_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=5)
        result = grounded_answer(q.query_text, rows, min_score=0.07)
        latency_ms, token_cost = latency_and_cost(q.query_text, top_k=5, rerank=False)

        per_query_ids[q.query_id] = result["retrieved_ids"]

        top_score = float(rows[0]["score"]) if rows else 0.0
        evidence_rows.append({"query_id": q.query_id, "top_score": top_score, "retrieved_count": len(rows)})

        outputs.append(
            {
                "variant": "baseline",
                "query_id": q.query_id,
                "role": q.role,
                "query": q.query_text,
                "retrieved_ids": result["retrieved_ids"],
                "answer": result["answer"],
                "citations": result["citations"],
                "grounded": result["grounded"],
                "latency_ms": latency_ms,
                "token_cost": token_cost,
            }
        )

    return outputs, per_query_ids, evidence_rows


def run_improved_flow(docs, queries, vectorizer, matrix) -> tuple[list[dict], dict[str, list[str]], list[dict]]:
    """Run improved production-oriented configuration.

    Controlled improvements applied:
    - hybrid retrieval (dense + lexical)
    - reranking pass
    - smaller top-k to reduce context noise
    - stricter grounding threshold for safer abstention behavior
    """
    outputs: list[dict] = []
    per_query_ids: dict[str, list[str]] = {}
    evidence_rows: list[dict] = []

    for q in queries:
        hybrid = hybrid_retrieve(q.query_text, docs, vectorizer, matrix, role=q.role, top_k=4, alpha=0.65)
        reranked = rerank_candidates(q.query_text, hybrid, role=q.role)
        result = grounded_answer(q.query_text, reranked, min_score=0.12)
        latency_ms, token_cost = latency_and_cost(q.query_text, top_k=4, rerank=True)

        per_query_ids[q.query_id] = result["retrieved_ids"]

        top_score = float(reranked[0].get("rerank_score", 0.0)) if reranked else 0.0
        evidence_rows.append({"query_id": q.query_id, "top_score": top_score, "retrieved_count": len(reranked)})

        outputs.append(
            {
                "variant": "improved",
                "query_id": q.query_id,
                "role": q.role,
                "query": q.query_text,
                "retrieved_ids": result["retrieved_ids"],
                "answer": result["answer"],
                "citations": result["citations"],
                "grounded": result["grounded"],
                "latency_ms": latency_ms,
                "token_cost": token_cost,
            }
        )

    return outputs, per_query_ids, evidence_rows


def main() -> None:
    print_data_declaration("Lab06 Project Baseline to Production", "lab/troubleshooting+production")
    ensure_stage7_dataset()

    docs = load_docs()
    queries = load_eval_queries()
    vectorizer, matrix = build_tfidf_index(docs)

    # -------------------------------
    # Step 1: Baseline project run
    # -------------------------------
    baseline_outputs, baseline_per_query, baseline_evidence = run_baseline_flow(docs, queries, vectorizer, matrix)

    # -------------------------------
    # Step 2: Improved project run
    # -------------------------------
    improved_outputs, improved_per_query, improved_evidence = run_improved_flow(docs, queries, vectorizer, matrix)

    # -------------------------------
    # Step 3: Metric comparison
    # -------------------------------
    baseline_retrieval = retrieval_metrics(baseline_per_query, queries, k=4)
    improved_retrieval = retrieval_metrics(improved_per_query, queries, k=4)

    baseline_answer = answer_metrics(baseline_outputs)
    improved_answer = answer_metrics(improved_outputs)

    # Operational summary metrics (latency/cost) for production-readiness checks.
    baseline_avg_latency = sum(x["latency_ms"] for x in baseline_outputs) / len(baseline_outputs)
    improved_avg_latency = sum(x["latency_ms"] for x in improved_outputs) / len(improved_outputs)
    baseline_avg_cost = sum(x["token_cost"] for x in baseline_outputs) / len(baseline_outputs)
    improved_avg_cost = sum(x["token_cost"] for x in improved_outputs) / len(improved_outputs)

    # -------------------------------
    # Step 4: Persist deliverables
    # -------------------------------
    baseline_path = Path(RESULTS_DIR) / "lab6_project_baseline_outputs.jsonl"
    improved_path = Path(RESULTS_DIR) / "lab6_project_improved_outputs.jsonl"
    options_path = Path(RESULTS_DIR) / "lab6_project_solution_options.csv"
    metrics_path = Path(RESULTS_DIR) / "lab6_project_metrics_comparison.csv"
    verify_path = Path(RESULTS_DIR) / "lab6_project_verification_report.md"
    prod_path = Path(RESULTS_DIR) / "lab6_project_production_readiness.md"

    as_jsonl(baseline_path, baseline_outputs)
    as_jsonl(improved_path, improved_outputs)

    # Explicit solution options: teach tradeoff comparison before implementation.
    solution_options = [
        {
            "option_id": "A",
            "change": "Increase top-k only",
            "expected_gain": "potentially higher recall",
            "risk": "higher prompt noise and cost",
            "decision": "not selected",
        },
        {
            "option_id": "B",
            "change": "Hybrid retrieval + reranking + stricter grounding",
            "expected_gain": "better relevance ranking and safer answers",
            "risk": "extra compute/latency",
            "decision": "selected",
        },
        {
            "option_id": "C",
            "change": "Prompt-only tweaks without retrieval changes",
            "expected_gain": "faster iteration",
            "risk": "does not fix retrieval-root-cause failures",
            "decision": "not selected",
        },
    ]
    as_csv(options_path, solution_options)

    metric_rows = [
        {
            "variant": "baseline",
            **baseline_retrieval,
            **baseline_answer,
            "avg_latency_ms": baseline_avg_latency,
            "avg_token_cost": baseline_avg_cost,
        },
        {
            "variant": "improved",
            **improved_retrieval,
            **improved_answer,
            "avg_latency_ms": improved_avg_latency,
            "avg_token_cost": improved_avg_cost,
        },
    ]
    as_csv(metrics_path, metric_rows)

    # -------------------------------
    # Step 5: Verification and production decision
    # -------------------------------
    # Basic acceptance thresholds for this educational project:
    # - retrieval should not regress
    # - grounded/citation metrics should stay healthy
    # - latency/cost should remain within safe toy thresholds
    retrieval_non_regression = improved_retrieval["hit_at_k"] >= baseline_retrieval["hit_at_k"]
    grounding_ok = improved_answer["grounded_rate"] >= 0.80
    citation_ok = improved_answer["citation_coverage"] >= 0.80
    latency_ok = improved_avg_latency < 900
    cost_ok = improved_avg_cost < 500

    promote = all([retrieval_non_regression, grounding_ok, citation_ok, latency_ok, cost_ok])

    verify_lines = [
        "# Lab6 Verification Report",
        f"run_at={now_ts()}",
        "",
        "## 1) Problem Identification",
        "Observed baseline issues: retrieval noise from larger top-k and weak grounding threshold.",
        "Evidence source: baseline outputs, top scores, retrieval/answer metrics.",
        "",
        "## 2) Solution Comparison",
        "Compared options A/B/C in solution options CSV and selected Option B.",
        "",
        "## 3) Verification",
        f"retrieval_non_regression={retrieval_non_regression}",
        f"grounding_ok={grounding_ok}",
        f"citation_ok={citation_ok}",
        f"latency_ok={latency_ok}",
        f"cost_ok={cost_ok}",
        "",
        "## 4) Decision",
        f"production_decision={'promote' if promote else 'hold_and_iterate'}",
        "",
        "## Supporting Evidence",
        f"baseline_top_score_avg={sum(x['top_score'] for x in baseline_evidence)/len(baseline_evidence):.4f}",
        f"improved_top_score_avg={sum(x['top_score'] for x in improved_evidence)/len(improved_evidence):.4f}",
    ]
    verify_path.write_text("\n".join(verify_lines), encoding="utf-8")

    prod_lines = [
        "# Lab6 Production Readiness",
        f"run_at={now_ts()}",
        f"retrieval_non_regression={retrieval_non_regression}",
        f"grounding_ok={grounding_ok}",
        f"citation_ok={citation_ok}",
        f"latency_ok={latency_ok}",
        f"cost_ok={cost_ok}",
        f"final_decision={'PROMOTE' if promote else 'DO_NOT_PROMOTE'}",
    ]
    prod_path.write_text("\n".join(prod_lines), encoding="utf-8")

    print("\nLab06 completed:")
    print(f"- {baseline_path}")
    print(f"- {improved_path}")
    print(f"- {options_path}")
    print(f"- {metrics_path}")
    print(f"- {verify_path}")
    print(f"- {prod_path}")


if __name__ == "__main__":
    main()
