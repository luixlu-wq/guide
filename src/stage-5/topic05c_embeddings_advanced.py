"""Stage 5 Topic 05C: embedding quality with hit@k (advanced).

Data: fixed corpus + query set with gold ids
Records/Samples: 8 docs, 6 queries
Input schema: query + gold_doc_id
Output schema: hit@1/hit@3 for embedding retrieval
Split/Eval policy: fixed evaluation set
Type: embedding retrieval evaluation
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Workflow:
# 1) Build embedding index from fixed corpus.
# 2) Evaluate retrieval against gold ids.
# 3) Report hit@1 and hit@3 for quality tracking.
def main() -> None:
    docs = [
        "Revenue increased but debt costs pressured margin.",
        "Regulatory investigation delayed product launch.",
        "Cloud demand improved retention and renewal rates.",
        "Supplier shortage affected hardware shipments.",
        "Security incident triggered internal audit.",
        "Hiring expanded in machine learning teams.",
        "Management issued cautious guidance on volatility.",
        "Legal review followed product recall complaints.",
    ]

    qa = [
        ("Which text mentions regulatory investigation?", 1),
        ("Where is supplier shortage discussed?", 3),
        ("Which text talks about debt pressure?", 0),
        ("Where is cautious guidance mentioned?", 6),
        ("Where is product recall legal review discussed?", 7),
        ("Which line is about security incident audit?", 4),
    ]

    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(docs)

    hit1 = 0
    hit3 = 0

    print("Data declaration")
    print("source=in_script_docs_plus_queries")
    print(f"docs={len(docs)} queries={len(qa)}")
    print("input_schema=query:str,gold_doc_idx:int")
    print("output_schema=hit_at_k_metrics")

    for q, gold in qa:
        qv = vec.transform([q])
        scores = cosine_similarity(qv, X)[0]
        order = np.argsort(scores)[::-1]
        if order[0] == gold:
            hit1 += 1
        if gold in order[:3]:
            hit3 += 1

    n = len(qa)
    print(f"hit_at_1={hit1/n:.3f}")
    print(f"hit_at_3={hit3/n:.3f}")
    print("Interpretation: advanced embedding work needs retrieval evaluation, not only qualitative examples.")


if __name__ == "__main__":
    main()
