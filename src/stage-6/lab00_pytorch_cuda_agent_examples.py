"""Stage 6 Lab 00: PyTorch/CUDA agent examples moved from chapter text.

This lab bundles three runnable examples:
1) Simple risk scoring on device
2) Intermediate retrieval reranking with cosine similarity
3) Advanced mini training loop for policy scoring

Run:
    python ./lab00_pytorch_cuda_agent_examples.py
"""

from __future__ import annotations

import torch


def example_a_compute_risk_score(features: dict[str, float]) -> float:
    """Example A (Simple): device-aware weighted risk scoring."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x = torch.tensor(
        [
            features["security_signal"],
            features["outage_signal"],
            features["billing_signal"],
        ],
        dtype=torch.float32,
        device=device,
    )
    w = torch.tensor([0.6, 0.25, 0.15], dtype=torch.float32, device=device)
    score = torch.dot(x, w).item()
    return float(score)


def example_b_cosine_rank(query_vec, doc_vecs):
    """Example B (Intermediate): retrieval reranking with cosine similarity."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    q = torch.tensor(query_vec, dtype=torch.float32, device=device)
    d = torch.tensor(doc_vecs, dtype=torch.float32, device=device)

    qn = q / (q.norm() + 1e-12)
    dn = d / (d.norm(dim=1, keepdim=True) + 1e-12)
    scores = dn @ qn
    order = torch.argsort(scores, descending=True).detach().cpu().tolist()
    return [(idx, float(scores[idx].detach().cpu().item())) for idx in order]


def example_c_train_policy_model(epochs: int = 120):
    """Example C (Advanced): tiny supervised training loop for risk policy."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    X = torch.tensor(
        [
            [0.9, 0.2, 0.1],
            [0.8, 0.4, 0.2],
            [0.2, 0.8, 0.2],
            [0.1, 0.2, 0.9],
            [0.7, 0.6, 0.2],
            [0.2, 0.1, 0.7],
        ],
        dtype=torch.float32,
        device=device,
    )
    y = torch.tensor([[1.0], [1.0], [1.0], [0.0], [1.0], [0.0]], dtype=torch.float32, device=device)

    model = torch.nn.Sequential(torch.nn.Linear(3, 1), torch.nn.Sigmoid()).to(device)
    loss_fn = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

    for epoch in range(epochs):
        optimizer.zero_grad()
        pred = model(X)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        if epoch % 30 == 0:
            print(f"[Example C] epoch={epoch:03d} loss={loss.item():.4f}")

    return model, device


def main() -> None:
    print("=== Lab00 PyTorch/CUDA Agent Examples ===")
    print(f"torch_version={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"selected_device={'cuda' if torch.cuda.is_available() else 'cpu'}")

    # Example A
    sample = {
        "security_signal": 0.9,
        "outage_signal": 0.3,
        "billing_signal": 0.2,
    }
    risk = example_a_compute_risk_score(sample)
    print(f"[Example A] risk_score={risk:.4f} needs_human_approval={risk >= 0.7}")

    # Example B
    query = [0.9, 0.1, 0.0, 0.2]
    docs = [
        [0.8, 0.1, 0.0, 0.3],
        [0.1, 0.9, 0.2, 0.1],
        [0.7, 0.2, 0.1, 0.1],
    ]
    ranked = example_b_cosine_rank(query, docs)
    print("[Example B] ranked_docs:", [(i, round(s, 4)) for i, s in ranked])

    # Example C
    model, device = example_c_train_policy_model()
    x_new = torch.tensor([[0.85, 0.30, 0.15]], dtype=torch.float32, device=device)
    prob = float(model(x_new).item())
    print(f"[Example C] predicted_risk_probability={prob:.4f} needs_human_approval={prob >= 0.7}")


if __name__ == "__main__":
    main()
