"""Stage 7 minimal local RAG baseline.

Purpose:
- Provide a tiny, fully local, deterministic RAG-style example.
- Demonstrate retrieval + grounded answer + citations without external APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    """Minimal retrievable chunk schema used in this baseline example."""

    chunk_id: str
    source: str
    text: str


# Fixed mini corpus used as a local knowledge base.
CORPUS: List[Chunk] = [
    Chunk("c1", "policy_access.md#L10", "Contractors must use VPN and MFA for remote access."),
    Chunk("c2", "policy_password.md#L5", "Passwords must be rotated every 90 days."),
    Chunk("c3", "policy_incident.md#L20", "Security incidents must be reported within 24 hours."),
    Chunk("c4", "policy_data.md#L8", "Sensitive data must not be shared over personal email."),
]

# Build a simple TF-IDF index for lexical/semantic-lite retrieval.
VECTORIZER = TfidfVectorizer()
DOC_MATRIX = VECTORIZER.fit_transform([c.text for c in CORPUS])


def retrieve_top_k(query: str, k: int = 2) -> List[Chunk]:
    """Retrieve top-k chunks by cosine similarity in TF-IDF space."""
    q_vec = VECTORIZER.transform([query])
    sims = cosine_similarity(q_vec, DOC_MATRIX).flatten()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    top_idx = [i for i, _ in ranked[:k]]
    return [CORPUS[i] for i in top_idx]


def grounded_answer(query: str, retrieved: List[Chunk]) -> dict:
    """Return deterministic grounded response and citations."""
    if not retrieved:
        return {
            "answer": "Insufficient evidence in provided context.",
            "citations": [],
            "retrieved_ids": [],
        }

    # In full RAG systems, an LLM would synthesize from context here.
    evidence = " ".join([c.text for c in retrieved])
    answer = f"Based on policy evidence: {evidence}"

    return {
        "answer": answer,
        "citations": [c.source for c in retrieved],
        "retrieved_ids": [c.chunk_id for c in retrieved],
    }


def run_demo() -> None:
    """Run a fixed query set so output stays stable across reruns."""
    queries = [
        "How should contractors access internal systems remotely?",
        "When do we report a security incident?",
        "Can I send sensitive data via my personal email?",
    ]

    for q in queries:
        retrieved = retrieve_top_k(q, k=2)
        result = grounded_answer(q, retrieved)

        print("=" * 72)
        print("query:", q)
        print("retrieved_ids:", result["retrieved_ids"])
        print("citations:", result["citations"])
        print("answer:", result["answer"])


if __name__ == "__main__":
    run_demo()
