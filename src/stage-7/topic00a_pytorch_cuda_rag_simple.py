"""Stage 7 Topic 00A: PyTorch/CUDA in RAG (simple).

This script demonstrates the minimum CUDA-aware workflow:
1. choose a device (cpu/cuda)
2. move tensors
3. compute simple scores
4. print deterministic outputs
"""

from __future__ import annotations

from stage7_utils import print_data_declaration

try:
    import torch  # type: ignore
except Exception:
    torch = None


print_data_declaration("Topic00A PyTorch/CUDA RAG Simple", "retrieval scoring")
print("\n=== Workflow ===")
print("1) select device")
print("2) build small embedding tensors")
print("3) score query-chunk relevance")

if torch is None:
    print("\nPyTorch not installed. Running deterministic fallback mode.")

    # Fallback vector math keeps script runnable even without torch.
    query = [0.6, 0.2, 0.3]
    chunks = [[0.9, 0.1, 0.1], [0.2, 0.8, 0.1], [0.5, 0.2, 0.4]]

    def dot(a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    scores = [dot(query, c) for c in chunks]
    print(f"selected_device=cpu")
    print(f"scores={scores}")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Query/chunk vectors represent embedding-like features in this mini demo.
    query = torch.tensor([0.6, 0.2, 0.3], dtype=torch.float32, device=device)
    chunks = torch.tensor(
        [[0.9, 0.1, 0.1], [0.2, 0.8, 0.1], [0.5, 0.2, 0.4]],
        dtype=torch.float32,
        device=device,
    )

    # Matrix-vector multiplication computes one relevance score per chunk.
    scores = chunks @ query

    print(f"torch_version={torch.__version__}")
    print(f"selected_device={device}")
    print(f"scores={scores.detach().cpu().tolist()}")

print("\nInterpretation: this is the core tensor path used inside local rerank models.")
