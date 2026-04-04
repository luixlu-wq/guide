"""Stage 6 Topic 00C: PyTorch/CUDA in agents (advanced).

Demonstrates batched scoring, optional AMP on CUDA, and budget-style timing logs.
This mirrors production concerns: latency/cost controls for agent pipelines.
"""

from __future__ import annotations

import random
import time


try:
    import torch  # type: ignore
except Exception:
    torch = None


print("=== Topic00C PyTorch/CUDA Agent Advanced ===")
print("Use case: batched reranking in retrieval-heavy agents with latency budgets")

# Fixed seed for reproducible educational output.
random.seed(42)

num_docs = 256
dim = 64
query = [random.random() for _ in range(dim)]
docs = [[random.random() for _ in range(dim)] for _ in range(num_docs)]

if torch is None:
    print("PyTorch not installed. Running fallback timing mode.")
    t0 = time.perf_counter()

    # Simple dot-product scoring fallback.
    scores = [sum(q * d for q, d in zip(query, doc)) for doc in docs]

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    top3 = sorted(scores, reverse=True)[:3]

    print(f"fallback_latency_ms={elapsed_ms:.3f}")
    print("top3_scores=", [round(x, 4) for x in top3])
    print("Interpretation: CUDA can reduce latency for this repeated heavy math.")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    q = torch.tensor(query, dtype=torch.float32, device=device)
    d = torch.tensor(docs, dtype=torch.float32, device=device)

    # Warm-up pass is common for fair measurement on GPU backends.
    _ = d @ q
    if device.type == "cuda":
        torch.cuda.synchronize()

    t0 = time.perf_counter()

    # Optional mixed precision (AMP) is CUDA-specific optimization for throughput.
    if device.type == "cuda":
        with torch.cuda.amp.autocast():
            scores = d @ q
        torch.cuda.synchronize()
    else:
        scores = d @ q

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    top3 = torch.topk(scores, k=3).values.detach().cpu().tolist()

    print(f"torch_version={torch.__version__}")
    print(f"selected_device={device}")
    print(f"batch_scoring_latency_ms={elapsed_ms:.3f}")
    print("top3_scores=", [round(x, 4) for x in top3])
    print("Interpretation: this optimization directly affects agent p95 latency.")
