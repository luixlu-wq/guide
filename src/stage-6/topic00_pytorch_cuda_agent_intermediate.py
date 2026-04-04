"""Stage 6 Topic 00: PyTorch/CUDA in agents (intermediate).

Demonstrates local embedding-style similarity for retrieval memory in an agent.
This is a common place where PyTorch/CUDA helps in production-style agents.
"""

from __future__ import annotations

import math


try:
    import torch  # type: ignore
except Exception:
    torch = None


print("=== Topic00 PyTorch/CUDA Agent Intermediate ===")
print("Use case: retrieval similarity scoring for agent memory/tool selection")

# Deterministic tiny vectors for a transparent tutorial.
query_vec = [0.9, 0.1, 0.0, 0.2]
doc_vecs = [
    [0.8, 0.1, 0.0, 0.3],  # likely relevant
    [0.1, 0.9, 0.2, 0.1],  # less relevant
    [0.7, 0.2, 0.1, 0.1],  # moderately relevant
]


def cosine_py(a: list[float], b: list[float]) -> float:
    """Pure Python cosine similarity for fallback mode."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


if torch is None:
    print("PyTorch not installed. Running fallback mode.")
    scores = [cosine_py(query_vec, dv) for dv in doc_vecs]
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Move vectors to selected device so math executes on CPU or CUDA consistently.
    q = torch.tensor(query_vec, dtype=torch.float32, device=device)
    d = torch.tensor(doc_vecs, dtype=torch.float32, device=device)

    # Normalize vectors then compute cosine via matrix-vector multiply.
    qn = q / (q.norm() + 1e-12)
    dn = d / (d.norm(dim=1, keepdim=True) + 1e-12)
    scores_tensor = dn @ qn
    scores = scores_tensor.detach().cpu().tolist()

    print(f"torch_version={torch.__version__}")
    print(f"selected_device={device}")

ranked = sorted(enumerate(scores, start=1), key=lambda x: x[1], reverse=True)
print("similarity_scores=", [round(s, 4) for s in scores])
print("ranking(doc_index,score)=", [(idx, round(score, 4)) for idx, score in ranked])
print("Interpretation: this ranking can drive retrieval context for the agent.")
