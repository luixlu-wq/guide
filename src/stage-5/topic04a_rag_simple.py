"""Stage 5 Topic 04A: RAG retrieval basics (simple).

Data: in-script mini document set
Records/Samples: 5 docs
Input schema: query:str + docs[{id,title,content}]
Output schema: top-k retrieved docs with scores
Split/Eval policy: one fixed query
Type: retrieval-augmented generation (retrieval step)
"""

from __future__ import annotations

from stage5_utils import build_tfidf_index, retrieve_topk, simple_summary


# Workflow:
# 1) Build TF-IDF index on a tiny document set.
# 2) Retrieve top-k docs for a query.
# 3) Build grounded answer draft from top document.
def main() -> None:
    docs = [
        {"id": "d1", "title": "Revenue", "content": "Revenue increased 18 percent while costs rose modestly."},
        {"id": "d2", "title": "Regulation", "content": "The regulator started an investigation into disclosure timing."},
        {"id": "d3", "title": "Product", "content": "Launch was delayed due to supplier shortage and testing issues."},
        {"id": "d4", "title": "Hiring", "content": "The company expanded hiring in cloud infrastructure teams."},
        {"id": "d5", "title": "Debt", "content": "Debt refinancing increased interest expense and margin pressure."},
    ]
    query = "What are the investigation and supplier delay risks?"

    vectorizer, matrix = build_tfidf_index(docs)
    top = retrieve_topk(query, docs, vectorizer, matrix, top_k=3)

    print("Data declaration")
    print("source=in_script_docs")
    print(f"records={len(docs)}")
    print("input_schema=query:str, doc:{id,title,content}")
    print("output_schema=top_k_docs_with_scores")

    for row in top:
        d = row["doc"]
        print(f"doc_id={d['id']} score={row['score']:.4f} title={d['title']}")

    if all(row["score"] == 0.0 for row in top):
        print("warning=all retrieval scores are zero; revise query terms or indexing strategy.")

    grounded = simple_summary(top[0]["doc"]["content"])
    print(f"grounded_answer_draft={grounded}")
    print("Interpretation: RAG quality starts with retrieval quality.")


if __name__ == "__main__":
    main()
