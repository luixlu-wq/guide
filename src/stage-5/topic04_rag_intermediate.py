"""Stage 5 Topic 04: RAG retrieval evaluation (intermediate).

Data: fixed docs + QA set with gold supporting document
Records/Samples: 6 docs, 6 queries
Input schema: query, gold_doc_id
Output schema: hit@k metrics
Split/Eval policy: fixed test set
Type: retrieval quality evaluation
"""

from __future__ import annotations

from stage5_utils import build_tfidf_index, retrieve_topk


# Workflow:
# 1) Build retrieval index on fixed corpus.
# 2) Run queries with gold supporting doc ids.
# 3) Report hit@1 and hit@3.
def main() -> None:
    docs = [
        {"id": "d1", "title": "Revenue", "content": "Revenue increased 18 percent while costs rose modestly."},
        {"id": "d2", "title": "Regulation", "content": "The regulator started an investigation into disclosure timing."},
        {"id": "d3", "title": "Launch", "content": "Launch was delayed due to supplier shortage and testing issues."},
        {"id": "d4", "title": "Hiring", "content": "The company expanded hiring in cloud infrastructure teams."},
        {"id": "d5", "title": "Debt", "content": "Debt refinancing increased interest expense and margin pressure."},
        {"id": "d6", "title": "Guidance", "content": "Management issued cautious guidance because of demand volatility."},
    ]

    qa = [
        {"query": "Which document discusses regulatory investigation?", "gold": "d2"},
        {"query": "Where is product delay risk mentioned?", "gold": "d3"},
        {"query": "Which text covers debt-related margin pressure?", "gold": "d5"},
        {"query": "Where is cautious guidance discussed?", "gold": "d6"},
        {"query": "Where is revenue growth discussed?", "gold": "d1"},
        {"query": "Which document is about hiring expansion?", "gold": "d4"},
    ]

    vectorizer, matrix = build_tfidf_index(docs)

    hit1 = 0
    hit3 = 0

    print("Data declaration")
    print("source=in_script_docs_plus_qa")
    print(f"docs={len(docs)} queries={len(qa)}")
    print("input_schema=query:str,gold_doc_id:str")
    print("output_schema=hit@1, hit@3")

    for row in qa:
        top3 = retrieve_topk(row["query"], docs, vectorizer, matrix, top_k=3)
        ids = [x["doc"]["id"] for x in top3]
        if row["gold"] == ids[0]:
            hit1 += 1
        if row["gold"] in ids:
            hit3 += 1

    n = len(qa)
    print(f"hit_at_1={hit1/n:.3f}")
    print(f"hit_at_3={hit3/n:.3f}")
    print("Interpretation: retrieval metrics must be measured separately before generation quality claims.")


if __name__ == "__main__":
    main()
