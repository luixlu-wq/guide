"""Utility helpers for Stage 5 runnable examples."""

from __future__ import annotations

import json
import math
import random
import re
from collections import Counter
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RISK_KEYWORDS = [
    "lawsuit",
    "regulatory",
    "delay",
    "shortage",
    "fraud",
    "downgrade",
    "recall",
    "investigation",
    "volatility",
    "debt",
]


def tokenize_whitespace(text: str) -> list[str]:
    return [t for t in text.strip().split() if t]


def tokenize_subword_like(text: str) -> list[str]:
    """A lightweight educational tokenizer, not production BPE."""
    words = re.findall(r"[A-Za-z0-9_']+|[^\w\s]", text)
    tokens: list[str] = []
    for w in words:
        if re.fullmatch(r"[^\w\s]", w):
            tokens.append(w)
            continue
        if len(w) <= 6:
            tokens.append(w.lower())
        else:
            tokens.append(w[:3].lower())
            for i in range(3, len(w), 4):
                tokens.append("##" + w[i : i + 4].lower())
    return tokens


def chunk_tokens(tokens: list[str], chunk_size: int, overlap: int) -> list[list[str]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    chunks: list[list[str]] = []
    start = 0
    step = chunk_size - overlap
    while start < len(tokens):
        chunks.append(tokens[start : start + chunk_size])
        start += step
    return chunks


def estimate_token_cost(token_count: int, price_per_1k_tokens: float = 0.001) -> float:
    return (token_count / 1000.0) * price_per_1k_tokens


def simple_summary(text: str, max_words: int = 28) -> str:
    words = tokenize_whitespace(text)
    if not words:
        return ""
    return " ".join(words[:max_words])


def extract_risks(text: str) -> list[str]:
    low = text.lower()
    hits = [k for k in RISK_KEYWORDS if k in low]
    return hits if hits else ["none_detected"]


def mock_llm(
    text: str,
    mode: str,
    *,
    temperature: float = 0.0,
    grounded_context: str | None = None,
) -> str:
    """Offline deterministic-ish LLM simulator for teaching workflow."""
    rng = random.Random(abs(hash((text, mode, round(temperature, 2)))) % (2**32))
    base = simple_summary(text)
    risks = extract_risks(text)

    if grounded_context:
        base = simple_summary(grounded_context, max_words=24)

    if mode == "vague":
        return f"This text is about business performance. Summary: {base}."

    if mode == "specific":
        return (
            "Summary for beginner investor: "
            f"{base}. Key risks: {', '.join(risks)}."
        )

    if mode == "few_shot":
        actions = [
            "Monitor updates.",
            "Escalate risk review.",
            "Track weekly signals.",
            "Validate with external filings.",
        ]
        if temperature > 0.0:
            shuffled = risks[:]
            rng.shuffle(shuffled)
            picked = actions[rng.randrange(len(actions))]
            max_words = 18 + rng.randrange(8)
            return (
                "[SUMMARY] "
                f"{simple_summary(text, max_words=max_words)}\n"
                f"[RISKS] {', '.join(shuffled)}\n"
                f"[ACTION] {picked}"
            )
        return (
            "[SUMMARY] "
            f"{base}\n[RISKS] {', '.join(risks)}\n[ACTION] Monitor updates."
        )

    if mode == "json_weak":
        if rng.random() < 0.35:
            return "{summary: 'bad json', risks: [volatility], citations: []}"
        obj = {"summary": base, "risks": risks, "citations": []}
        return json.dumps(obj)

    if mode == "json_strong":
        obj = {
            "summary": base,
            "risks": risks,
            "confidence_note": "heuristic_offline_demo",
            "citations": [],
        }
        return json.dumps(obj)

    return base


def try_parse_json(raw: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as exc:
        return None, str(exc)


def validate_schema(obj: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    required = ["summary", "risks", "citations"]
    for key in required:
        if key not in obj:
            errors.append(f"missing_field:{key}")
    if "summary" in obj and not isinstance(obj["summary"], str):
        errors.append("summary_not_string")
    if "risks" in obj and not isinstance(obj["risks"], list):
        errors.append("risks_not_list")
    if "citations" in obj and not isinstance(obj["citations"], list):
        errors.append("citations_not_list")
    return (len(errors) == 0), errors


def repair_json_text(raw: str) -> str:
    # Minimal repair for common malformed outputs in demos.
    repaired = raw.strip()
    repaired = repaired.replace("'", '"')
    repaired = re.sub(r"(\{|,\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', repaired)
    return repaired


def build_tfidf_index(docs: list[dict[str, str]]):
    corpus = [d["content"] for d in docs]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


def retrieve_topk(
    query: str,
    docs: list[dict[str, str]],
    vectorizer: TfidfVectorizer,
    matrix,
    top_k: int,
) -> list[dict[str, Any]]:
    qv = vectorizer.transform([query])
    scores = cosine_similarity(qv, matrix)[0]
    order = scores.argsort()[::-1][:top_k]
    out: list[dict[str, Any]] = []
    for idx in order:
        out.append({"doc": docs[idx], "score": float(scores[idx])})
    return out


def lexical_overlap_score(a: str, b: str) -> float:
    ta = set(tokenize_subword_like(a))
    tb = set(tokenize_subword_like(b))
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def most_common_error(errors: list[str]) -> str:
    if not errors:
        return "none"
    return Counter(errors).most_common(1)[0][0]


def token_entropy(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    n = len(tokens)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent
