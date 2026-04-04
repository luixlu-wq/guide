"""Stage 5 Topic 05A: embedding basics with nn.Embedding (simple).

Data: tiny in-script token-id sentences
Records/Samples: 4
Input schema: token_ids tensor [batch, seq_len]
Output schema: token embeddings [batch, seq_len, d_model], sentence embeddings [batch, d_model]
Split/Eval policy: not applicable
Type: embedding concept demonstration
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


# Workflow:
# 1) Build toy token-id sequences.
# 2) Map token ids to vectors with nn.Embedding.
# 3) Aggregate token vectors into sentence embeddings and compare cosine similarities.
def main() -> None:
    torch.manual_seed(50)

    x = torch.tensor(
        [
            [1, 2, 3, 4, 0, 0],
            [1, 2, 3, 5, 0, 0],
            [6, 7, 8, 9, 0, 0],
            [6, 7, 10, 9, 0, 0],
        ],
        dtype=torch.long,
    )

    vocab_size = 16
    d_model = 12
    emb = torch.nn.Embedding(vocab_size, d_model, padding_idx=0)

    token_vecs = emb(x)
    sent_vecs = token_vecs.mean(dim=1)

    sim_01 = F.cosine_similarity(sent_vecs[0], sent_vecs[1], dim=0).item()
    sim_02 = F.cosine_similarity(sent_vecs[0], sent_vecs[2], dim=0).item()

    print("Data declaration")
    print("source=in_script_token_ids")
    print(f"records={x.size(0)}")
    print("input_schema=token_ids:[batch,seq_len]")
    print("output_schema=token_embeddings,sentence_embeddings")
    print(f"token_embedding_shape={tuple(token_vecs.shape)}")
    print(f"sentence_embedding_shape={tuple(sent_vecs.shape)}")
    print(f"cos_sim(sent0,sent1)={sim_01:.4f}")
    print(f"cos_sim(sent0,sent2)={sim_02:.4f}")
    print("Interpretation: embeddings convert discrete token IDs into dense vectors for similarity math.")


if __name__ == "__main__":
    main()
