"""Stage 7 Topic 00: PyTorch/CUDA in RAG (intermediate).

This script demonstrates a tiny reranker training loop.
It shows how forward/loss/backward/optimizer steps map to relevance learning.
"""

from __future__ import annotations

from stage7_utils import print_data_declaration

try:
    import torch  # type: ignore
    from torch import nn  # type: ignore
except Exception:
    torch = None
    nn = None


print_data_declaration("Topic00 PyTorch/CUDA RAG Intermediate", "reranker training")
print("\n=== Workflow ===")
print("1) prepare labeled relevance features")
print("2) train linear scorer")
print("3) inspect probabilities")

if torch is None or nn is None:
    print("\nPyTorch is not installed. Skipping training and showing expected behavior.")
    print("expected: relevant samples move toward higher probability after epochs")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"selected_device={device}")

    # Features: [dense_similarity, lexical_overlap, section_match]
    x = torch.tensor(
        [
            [0.91, 0.70, 1.0],
            [0.22, 0.10, 0.0],
            [0.78, 0.45, 1.0],
            [0.30, 0.08, 0.0],
            [0.87, 0.60, 1.0],
            [0.20, 0.05, 0.0],
        ],
        dtype=torch.float32,
        device=device,
    )
    y = torch.tensor([[1.0], [0.0], [1.0], [0.0], [1.0], [0.0]], dtype=torch.float32, device=device)

    model = nn.Sequential(nn.Linear(3, 1)).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=0.08)
    loss_fn = nn.BCEWithLogitsLoss()

    for epoch in range(1, 121):
        opt.zero_grad()
        logits = model(x)
        loss = loss_fn(logits, y)
        loss.backward()
        opt.step()

        if epoch % 30 == 0:
            print(f"epoch={epoch} loss={loss.item():.4f}")

    with torch.no_grad():
        probs = torch.sigmoid(model(x)).squeeze(1)
        print("relevance_probs=", [round(v, 4) for v in probs.detach().cpu().tolist()])

print("\nInterpretation: this mimics local rerank-model training used in advanced RAG stacks.")
