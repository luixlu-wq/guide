"""Stage 5 Topic 04C: RAG grounded-answer pipeline (advanced).

Data: fixed docs + QA set
Records/Samples: 7 docs, 7 queries
Input schema: query + expected supporting doc
Output schema: answer, citation, groundedness metrics
Split/Eval policy: fixed test set
Type: advanced RAG evaluation with citation checks
"""

from __future__ import annotations

from stage5_utils import build_tfidf_index, lexical_overlap_score, retrieve_topk, simple_summary


def generate_grounded_answer(query: str, retrieved: list[dict]) -> tuple[str, str]:
    top_doc = retrieved[0]["doc"]
    answer = simple_summary(top_doc["content"], max_words=18)
    citation = top_doc["id"]
    return answer, citation


# Workflow:
# 1) Retrieve top-k docs.
# 2) Generate answer constrained to top document.
# 3) Evaluate citation correctness and lexical grounding score.
def main() -> None:
    docs = [
        {"id": "d1", "title": "Revenue", "content": "Revenue increased 18 percent while costs rose modestly."},
        {"id": "d2", "title": "Regulation", "content": "The regulator started an investigation into disclosure timing."},
        {"id": "d3", "title": "Launch", "content": "Launch was delayed due to supplier shortage and testing issues."},
        {"id": "d4", "title": "Hiring", "content": "The company expanded hiring in cloud infrastructure teams."},
        {"id": "d5", "title": "Debt", "content": "Debt refinancing increased interest expense and margin pressure."},
        {"id": "d6", "title": "Guidance", "content": "Management issued cautious guidance because of demand volatility."},
        {"id": "d7", "title": "Security", "content": "A security incident triggered internal audit and remediation steps."},
    ]

    qa = [
        {"query": "What regulatory risk is reported?", "gold": "d2"},
        {"query": "What launch risk is discussed?", "gold": "d3"},
        {"query": "What debt issue affects margins?", "gold": "d5"},
        {"query": "What guidance concern is mentioned?", "gold": "d6"},
        {"query": "What security issue occurred?", "gold": "d7"},
        {"query": "What revenue result was reported?", "gold": "d1"},
        {"query": "What hiring action was taken?", "gold": "d4"},
    ]

    vectorizer, matrix = build_tfidf_index(docs)

    citation_hit = 0
    grounding_scores: list[float] = []

    print("Data declaration")
    print("source=in_script_docs_plus_qa")
    print(f"docs={len(docs)} queries={len(qa)}")
    print("input_schema=query:str,gold_doc_id:str")
    print("output_schema=answer:str,citation:str,grounding_score:float")

    for row in qa:
        retrieved = retrieve_topk(row["query"], docs, vectorizer, matrix, top_k=3)
        answer, citation = generate_grounded_answer(row["query"], retrieved)
        top_doc_content = retrieved[0]["doc"]["content"]
        grounding_scores.append(lexical_overlap_score(answer, top_doc_content))
        if citation == row["gold"]:
            citation_hit += 1

    n = len(qa)
    print(f"citation_accuracy={citation_hit/n:.3f}")
    print(f"avg_grounding_score={sum(grounding_scores)/n:.3f}")
    print("Interpretation: advanced RAG evaluation should include retrieval + citation + grounding checks.")


if __name__ == "__main__":
    main()
