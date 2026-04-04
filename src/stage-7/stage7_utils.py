"""Shared utilities for Stage 7 RAG runnable examples.

Design goals:
1. Keep all examples runnable offline without API keys.
2. Keep behavior deterministic so before/after comparisons are meaningful.
3. Provide clear, reusable helpers that print data/schema declarations.
"""

from __future__ import annotations

import csv
import json
import math
import random
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Resolve key directories relative to this file so scripts can run from any cwd.
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "stage-7"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


@dataclass
class DocChunk:
    """Single retrievable chunk with metadata used for retrieval, ACL, and citations."""

    chunk_id: str
    doc_id: str
    source: str
    section: str
    acl_tag: str
    updated_at: str
    text: str


@dataclass
class EvalQuery:
    """Fixed evaluation query with expected evidence chunk ids and role context."""

    query_id: str
    role: str
    query_text: str
    gold_chunk_ids: list[str]


def ensure_stage7_dirs() -> None:
    """Create stage-7 data/results directories if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def get_stage7_schema() -> dict[str, Any]:
    """Return standard data/output schema declaration used across all scripts."""
    return {
        "data": "red-book/data/stage-7/docs_stage7.jsonl",
        "documents": 12,
        "chunking": "one semantic section per chunk, with metadata",
        "input_schema": {
            "query_id": "string",
            "role": "enum(employee,security,finance,hr)",
            "query_text": "string",
        },
        "output_schema": {
            "query_id": "string",
            "retrieved_ids": "array<string>",
            "answer": "string",
            "citations": "array<string>",
            "grounded": "bool",
            "latency_ms": "int",
            "cost_tokens": "int",
        },
    }


def print_data_declaration(title: str, run_type: str) -> None:
    """Print the mandatory declaration block required by handbook policy."""
    schema = get_stage7_schema()
    print(f"\n=== {title}: Data Declaration ===")
    print(f"Data: {schema['data']}")
    print(f"Documents: {schema['documents']}")
    print(f"Chunking: {schema['chunking']}")
    print(f"Input schema: {schema['input_schema']}")
    print(f"Output schema: {schema['output_schema']}")
    print("Eval policy: fixed queries from red-book/data/stage-7/eval_queries_stage7.jsonl")
    print(f"Type: {run_type}")


def _generate_docs() -> list[DocChunk]:
    """Generate deterministic mini-corpus spanning policy/ops/security/finance topics."""
    base_time = datetime(2026, 3, 1, 9, 0, 0)

    # Each chunk has ACL tag so scripts can demonstrate permission-aware retrieval.
    rows = [
        DocChunk("c001", "d001", "policy_access.md#L10", "remote_access", "employee", (base_time + timedelta(days=1)).isoformat(), "Contractors must use VPN and MFA for all remote access to internal systems."),
        DocChunk("c002", "d002", "policy_password.md#L5", "password_rotation", "employee", (base_time + timedelta(days=2)).isoformat(), "Passwords must be rotated every 90 days and cannot be reused within three cycles."),
        DocChunk("c003", "d003", "policy_incident.md#L20", "incident_reporting", "employee", (base_time + timedelta(days=3)).isoformat(), "Security incidents must be reported within 24 hours through the incident portal."),
        DocChunk("c004", "d004", "policy_data.md#L8", "data_handling", "employee", (base_time + timedelta(days=4)).isoformat(), "Sensitive customer data must not be sent over personal email or unmanaged storage."),
        DocChunk("c005", "d005", "finance_controls.md#L12", "expense_policy", "finance", (base_time + timedelta(days=5)).isoformat(), "Expense reimbursements above 2000 USD require finance manager approval and receipts."),
        DocChunk("c006", "d006", "hr_leave.md#L9", "leave_policy", "hr", (base_time + timedelta(days=6)).isoformat(), "Contractors are not eligible for paid vacation under standard policy terms."),
        DocChunk("c007", "d007", "ops_slo.md#L4", "service_slo", "engineering", (base_time + timedelta(days=7)).isoformat(), "Core API SLO target is 99.9 percent monthly availability with p95 latency under 900ms."),
        DocChunk("c008", "d008", "ops_recovery.md#L14", "incident_recovery", "engineering", (base_time + timedelta(days=8)).isoformat(), "During severe outage, trigger incident bridge, assign commander, and update status every 30 minutes."),
        DocChunk("c009", "d009", "security_acl.md#L7", "access_control", "security", (base_time + timedelta(days=9)).isoformat(), "Access to security audit logs is restricted to security role and approved incident responders."),
        DocChunk("c010", "d010", "security_injection.md#L17", "prompt_injection", "security", (base_time + timedelta(days=10)).isoformat(), "Ignore previous instructions patterns are prompt-injection indicators and must trigger safe refusal."),
        DocChunk("c011", "d011", "product_faq.md#L3", "password_reset", "employee", (base_time + timedelta(days=11)).isoformat(), "Users reset passwords through the account portal by verifying email and MFA code."),
        DocChunk("c012", "d012", "ops_ingestion.md#L11", "index_freshness", "engineering", (base_time + timedelta(days=12)).isoformat(), "Knowledge index must be refreshed at least daily and immediately after critical policy updates."),
    ]
    return rows


def _generate_eval_queries() -> list[EvalQuery]:
    """Generate fixed eval queries with known relevant chunk ids for metric calculations."""
    return [
        EvalQuery("q001", "employee", "How should contractors access internal systems remotely?", ["c001"]),
        EvalQuery("q002", "employee", "How often should passwords be rotated?", ["c002", "c011"]),
        EvalQuery("q003", "employee", "What is the incident reporting time requirement?", ["c003"]),
        EvalQuery("q004", "employee", "Can we send sensitive customer data via personal email?", ["c004"]),
        EvalQuery("q005", "finance", "When is finance manager approval required for expenses?", ["c005"]),
        EvalQuery("q006", "hr", "Do contractors receive paid vacation?", ["c006"]),
        EvalQuery("q007", "engineering", "What are API reliability targets?", ["c007"]),
        EvalQuery("q008", "engineering", "What steps happen during severe outage response?", ["c008"]),
        EvalQuery("q009", "security", "Who can access security audit logs?", ["c009"]),
        EvalQuery("q010", "security", "How should prompt injection patterns be handled?", ["c010"]),
        EvalQuery("q011", "engineering", "How often should the knowledge index refresh?", ["c012"]),
    ]


def ensure_stage7_dataset() -> tuple[Path, Path]:
    """Create docs/eval files if missing and return their paths."""
    ensure_stage7_dirs()
    docs_path = DATA_DIR / "docs_stage7.jsonl"
    eval_path = DATA_DIR / "eval_queries_stage7.jsonl"

    if not docs_path.exists():
        docs = _generate_docs()
        with docs_path.open("w", encoding="utf-8") as fp:
            for doc in docs:
                fp.write(json.dumps(asdict(doc), ensure_ascii=True) + "\n")

    if not eval_path.exists():
        eval_rows = _generate_eval_queries()
        with eval_path.open("w", encoding="utf-8") as fp:
            for row in eval_rows:
                fp.write(json.dumps(asdict(row), ensure_ascii=True) + "\n")

    return docs_path, eval_path


def load_docs(path: Path | None = None) -> list[DocChunk]:
    """Load document chunks from JSONL into dataclass objects."""
    if path is None:
        path, _ = ensure_stage7_dataset()

    rows: list[DocChunk] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            data = json.loads(line)
            rows.append(DocChunk(**data))
    return rows


def load_eval_queries(path: Path | None = None) -> list[EvalQuery]:
    """Load fixed evaluation queries from JSONL."""
    if path is None:
        _, path = ensure_stage7_dataset()

    rows: list[EvalQuery] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            data = json.loads(line)
            rows.append(EvalQuery(**data))
    return rows


def build_tfidf_index(docs: list[DocChunk]) -> tuple[TfidfVectorizer, Any]:
    """Build vectorizer + matrix used as dense baseline retriever in this offline lab."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([d.text for d in docs])
    return vectorizer, matrix


def _tokenize(text: str) -> list[str]:
    """Very simple tokenizer used by lexical scoring helpers."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return [tok for tok in cleaned.split() if tok]


def lexical_score(query: str, text: str) -> float:
    """Compute token-overlap score for lexical retrieval baseline."""
    q = set(_tokenize(query))
    t = set(_tokenize(text))
    if not q or not t:
        return 0.0
    return float(len(q & t) / len(q | t))


def _acl_allowed(doc: DocChunk, role: str) -> bool:
    """Simple ACL policy for demonstration.

    Rule set:
    - employee can read employee + engineering docs
    - engineering can read engineering + employee docs
    - finance can read finance + employee docs
    - hr can read hr + employee docs
    - security can read all
    """
    if role == "security":
        return True

    allow = {
        "employee": {"employee", "engineering"},
        "engineering": {"engineering", "employee"},
        "finance": {"finance", "employee"},
        "hr": {"hr", "employee"},
    }
    return doc.acl_tag in allow.get(role, {"employee"})


def dense_retrieve(query: str, docs: list[DocChunk], vectorizer: TfidfVectorizer, matrix: Any, *, role: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Retrieve top-k documents by cosine similarity with ACL filtering."""
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, matrix).flatten()

    rows: list[dict[str, Any]] = []
    for idx, score in enumerate(sims):
        doc = docs[idx]
        if not _acl_allowed(doc, role):
            continue
        rows.append({"chunk": doc, "score": float(score), "method": "dense"})

    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows[:top_k]


def lexical_retrieve(query: str, docs: list[DocChunk], *, role: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Retrieve top-k documents using lexical overlap score with ACL filtering."""
    rows: list[dict[str, Any]] = []
    for doc in docs:
        if not _acl_allowed(doc, role):
            continue
        score = lexical_score(query, doc.text)
        rows.append({"chunk": doc, "score": score, "method": "lexical"})

    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows[:top_k]


def _normalize_scores(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize scores to 0-1 for safer dense+lexical combination."""
    if not rows:
        return rows
    vals = [r["score"] for r in rows]
    lo = min(vals)
    hi = max(vals)
    if math.isclose(lo, hi):
        for r in rows:
            r["norm_score"] = 0.5
        return rows

    for r in rows:
        r["norm_score"] = (r["score"] - lo) / (hi - lo)
    return rows


def hybrid_retrieve(query: str, docs: list[DocChunk], vectorizer: TfidfVectorizer, matrix: Any, *, role: str, top_k: int = 3, alpha: float = 0.6) -> list[dict[str, Any]]:
    """Combine dense and lexical signals into one hybrid ranking.

    alpha controls dense weight. lexical weight is (1 - alpha).
    """
    dense_rows = dense_retrieve(query, docs, vectorizer, matrix, role=role, top_k=len(docs))
    lexical_rows = lexical_retrieve(query, docs, role=role, top_k=len(docs))

    dense_map = {r["chunk"].chunk_id: r for r in _normalize_scores(dense_rows)}
    lex_map = {r["chunk"].chunk_id: r for r in _normalize_scores(lexical_rows)}

    # Merge by chunk id so every eligible chunk can get both signals.
    chunk_ids = set(dense_map) | set(lex_map)
    merged: list[dict[str, Any]] = []
    for cid in chunk_ids:
        d = dense_map.get(cid)
        l = lex_map.get(cid)

        # Pick one chunk object from whichever map contains it.
        chunk = (d or l)["chunk"]
        d_score = (d or {}).get("norm_score", 0.0)
        l_score = (l or {}).get("norm_score", 0.0)

        final_score = alpha * d_score + (1.0 - alpha) * l_score
        merged.append(
            {
                "chunk": chunk,
                "score": final_score,
                "dense_component": d_score,
                "lexical_component": l_score,
                "method": "hybrid",
            }
        )

    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged[:top_k]


def rerank_candidates(query: str, candidates: list[dict[str, Any]], *, role: str) -> list[dict[str, Any]]:
    """Apply a simple reranking heuristic to simulate stronger relevance scoring.

    Heuristics used:
    - token overlap bonus
    - section-intent bonus (query contains terms matching section keywords)
    - small penalty for too-short chunks
    """
    q_tokens = set(_tokenize(query))

    reranked: list[dict[str, Any]] = []
    for row in candidates:
        chunk = row["chunk"]
        text_tokens = set(_tokenize(chunk.text))

        overlap_bonus = len(q_tokens & text_tokens) * 0.01
        section_bonus = 0.05 if any(tok in chunk.section for tok in q_tokens) else 0.0
        short_penalty = -0.03 if len(chunk.text) < 60 else 0.0

        adjusted = row["score"] + overlap_bonus + section_bonus + short_penalty
        reranked.append(
            {
                **row,
                "rerank_score": adjusted,
                "role": role,
            }
        )

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked


def grounded_answer(query: str, ranked_rows: list[dict[str, Any]], *, min_score: float = 0.08) -> dict[str, Any]:
    """Create a deterministic grounded answer with citations and abstention support."""
    if not ranked_rows:
        return {
            "answer": "Insufficient evidence from retrieved context.",
            "citations": [],
            "retrieved_ids": [],
            "grounded": False,
        }

    # Determine best score key depending on whether reranking has run.
    best = ranked_rows[0]
    score_key = "rerank_score" if "rerank_score" in best else "score"
    best_score = float(best.get(score_key, 0.0))

    if best_score < min_score:
        return {
            "answer": "Insufficient evidence from retrieved context.",
            "citations": [],
            "retrieved_ids": [r["chunk"].chunk_id for r in ranked_rows],
            "grounded": False,
        }

    evidence_parts = [r["chunk"].text for r in ranked_rows[:2]]
    answer_text = "Based on retrieved policy evidence: " + " ".join(evidence_parts)

    return {
        "answer": answer_text,
        "citations": [r["chunk"].source for r in ranked_rows[:2]],
        "retrieved_ids": [r["chunk"].chunk_id for r in ranked_rows],
        "grounded": True,
    }


def retrieval_metrics(per_query_retrieved: dict[str, list[str]], eval_queries: list[EvalQuery], *, k: int) -> dict[str, float]:
    """Compute core retrieval metrics: hit@k, recall@k, and MRR."""
    if not eval_queries:
        return {"hit_at_k": 0.0, "recall_at_k": 0.0, "mrr": 0.0}

    hits = 0
    recall_sum = 0.0
    rr_sum = 0.0

    for q in eval_queries:
        retrieved = per_query_retrieved.get(q.query_id, [])[:k]
        gold = q.gold_chunk_ids
        gold_set = set(gold)

        # hit@k: any gold item appears in top-k
        if any(cid in gold_set for cid in retrieved):
            hits += 1

        # recall@k: fraction of gold items found in top-k
        found = sum(1 for gid in gold if gid in retrieved)
        recall_sum += found / max(len(gold), 1)

        # reciprocal rank for first matching gold chunk
        rr = 0.0
        for rank, cid in enumerate(retrieved, start=1):
            if cid in gold_set:
                rr = 1.0 / rank
                break
        rr_sum += rr

    n = float(len(eval_queries))
    return {
        "hit_at_k": hits / n,
        "recall_at_k": recall_sum / n,
        "mrr": rr_sum / n,
    }


def answer_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Compute simple answer-side quality metrics for groundedness and citations."""
    if not rows:
        return {"grounded_rate": 0.0, "citation_coverage": 0.0, "abstention_rate": 0.0}

    grounded = sum(1 for r in rows if r.get("grounded"))
    citation = sum(1 for r in rows if r.get("citations"))
    abstain = sum(1 for r in rows if "insufficient evidence" in r.get("answer", "").lower())

    n = float(len(rows))
    return {
        "grounded_rate": grounded / n,
        "citation_coverage": citation / n,
        "abstention_rate": abstain / n,
    }


def latency_and_cost(query: str, top_k: int, rerank: bool) -> tuple[int, int]:
    """Deterministic latency/token-cost simulation used by ops and evaluation scripts."""
    base_latency = 220 + (top_k * 18)
    if rerank:
        base_latency += 90

    token_cost = int(120 + len(_tokenize(query)) * 4 + top_k * 35 + (50 if rerank else 0))
    return base_latency, token_cost


def as_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write dictionaries to JSONL output path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        for row in rows:
            fp.write(json.dumps(row, ensure_ascii=True) + "\n")


def as_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write dictionaries as CSV using stable union of keys."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fields.append(key)

    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def now_ts() -> str:
    """Return UTC timestamp string for logs and run artifacts."""
    return datetime.utcnow().isoformat() + "Z"


def sleep_ms(ms: int) -> None:
    """Helper used by operations demos to simulate latency effects."""
    time.sleep(max(ms, 0) / 1000.0)


def acl_violation_count(rows: list[dict[str, Any]], docs_by_id: dict[str, DocChunk], role: str) -> int:
    """Count ACL violations in retrieved ids for a specific role."""
    violations = 0
    for row in rows:
        for cid in row.get("retrieved_ids", []):
            doc = docs_by_id.get(cid)
            if doc is None:
                continue
            if not _acl_allowed(doc, role):
                violations += 1
    return violations


def summarize_incident(case_id: str, failure: str, fix: str, outcome: str) -> str:
    """Create standardized incident summary string."""
    return (
        f"Incident Case: {case_id}\n"
        f"Detected At: {now_ts()}\n"
        f"Failure Type: {failure}\n"
        f"Fix Applied: {fix}\n"
        f"Outcome: {outcome}\n"
    )


def score_distribution(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Return min/avg/max score distribution for retrieved rows."""
    if not rows:
        return {"score_min": 0.0, "score_avg": 0.0, "score_max": 0.0}

    scores: list[float] = []
    for row in rows:
        if "rerank_score" in row:
            scores.append(float(row["rerank_score"]))
        else:
            scores.append(float(row["score"]))

    return {
        "score_min": float(np.min(scores)),
        "score_avg": float(np.mean(scores)),
        "score_max": float(np.max(scores)),
    }
