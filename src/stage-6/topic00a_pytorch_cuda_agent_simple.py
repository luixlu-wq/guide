"""Stage 6 Topic 00A: PyTorch/CUDA in agents (simple).

This script answers a practical beginner question:
Where does PyTorch/CUDA appear in agent systems?

It runs in two modes:
1) torch mode (if PyTorch is installed)
2) fallback mode (pure Python) so script remains runnable
"""

from __future__ import annotations


try:
    import torch  # type: ignore
except Exception:
    torch = None


print("=== Topic00A PyTorch/CUDA Agent Simple ===")
print("Use case: local tensor compute for routing/risk scoring in an agent loop")

if torch is None:
    print("PyTorch not installed. Running fallback mode.")

    # Fallback tensors represented as Python lists for educational continuity.
    features = [0.8, 0.4, 0.9]  # [security_signal, outage_signal, billing_signal]
    weights = [0.6, 0.2, 0.2]
    score = sum(f * w for f, w in zip(features, weights))

    print(f"fallback_score={score:.4f}")
    print("Interpretation: higher score can trigger stricter policy gate.")
else:
    # Device selection is the first required step in CUDA-aware workflows.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # In agent systems, these tensors can come from tool outputs or local models.
    features = torch.tensor([0.8, 0.4, 0.9], dtype=torch.float32, device=device)
    weights = torch.tensor([0.6, 0.2, 0.2], dtype=torch.float32, device=device)

    # Tensor dot-product is a common building block for lightweight scoring logic.
    score = torch.dot(features, weights).item()

    print(f"torch_version={torch.__version__}")
    print(f"selected_device={device}")
    print(f"torch_score={score:.4f}")
    print("Interpretation: CUDA can accelerate repeated scoring/model operations.")
