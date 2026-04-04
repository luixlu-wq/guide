"""Stage 5 Topic 05: embedding retrieval workflow (intermediate).

Data: in-script sentence corpus
Records/Samples: 8 corpus entries + 1 query
Input schema: text strings
Output schema: dense vectors + top-k retrieval results
Split/Eval policy: fixed query/corpus
Type: embedding-based semantic retrieval
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


# Workflow:
# 1) Build sparse text features via TF-IDF.
# 2) Project to dense vectors (educational embedding proxy).
# 3) Run cosine retrieval for a query.
def main() -> None:
    corpus = [
        "Revenue increased but debt costs pressured margin.",
        "Regulatory investigation delayed product launch.",
        "Cloud demand improved retention and renewal rates.",
        "Supplier shortage affected hardware shipments.",
        "Security incident triggered internal audit.",
        "Hiring expanded in machine learning teams.",
        "Management issued cautious guidance on volatility.",
        "Legal review followed product recall complaints.",
    ]
    query = "Which items discuss regulatory delay risk?"

    vec = TfidfVectorizer(stop_words="english")
    X_sparse = vec.fit_transform(corpus)

    svd_dim = min(6, X_sparse.shape[1] - 1)
    svd = TruncatedSVD(n_components=svd_dim, random_state=42)
    X_dense = svd.fit_transform(X_sparse)
    q_dense = svd.transform(vec.transform([query]))

    scores = cosine_similarity(q_dense, X_dense)[0]
    order = np.argsort(scores)[::-1][:3]

    print("Data declaration")
    print("source=in_script_sentence_corpus")
    print(f"records={len(corpus)}")
    print("input_schema=text:str")
    print("output_schema=dense_embedding:vector + retrieval_score")
    print(f"dense_shape={X_dense.shape}")

    for rank, idx in enumerate(order, start=1):
        print(f"rank={rank} score={scores[idx]:.4f} text={corpus[idx]}")

    print("Interpretation: embedding retrieval ranks semantically related entries by vector similarity.")


if __name__ == "__main__":
    main()
