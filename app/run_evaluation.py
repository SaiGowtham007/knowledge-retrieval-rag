from app.embedding import create_embedding
from app.context_builder import build_context
from app.generation import generate_answer
from app.reranking.reranker import rerank_results
from app.query_intent import detect_document_status
from app.hybrid_search import hybrid_search
from app.relevance import filter_relevant_results
from app.evaluation import load_evaluation_questions


EVALUATION_FILE = "data/PRFIP_Evaluation_Question_Set.xlsx"


def run_question(question_data):

    question = question_data["question"]

    print("\n" + "=" * 80)
    print(f"QUESTION {question_data['id']}")
    print("=" * 80)

    print(f"\nQuestion: {question}")

    # ---------------------------------------------------------
    # 1. CREATE QUERY EMBEDDING
    # ---------------------------------------------------------

    query_embedding = create_embedding(question)

    # ---------------------------------------------------------
    # 2. DETECT QUERY INTENT
    # ---------------------------------------------------------

    document_status = detect_document_status(question)

    # ---------------------------------------------------------
    # 3. HYBRID RETRIEVAL
    # ---------------------------------------------------------

    results = hybrid_search(
        question=question,
        query_embedding=query_embedding,
        vector_top_k=10,
        keyword_top_k=10,
        document_status=document_status
    )

    # ---------------------------------------------------------
    # 4. RERANK
    # ---------------------------------------------------------

    reranked_candidates = rerank_results(
        question=question,
        results=results,
        top_k=10
    )

    # ---------------------------------------------------------
    # 5. SHOW RETRIEVAL EVIDENCE
    # ---------------------------------------------------------

    print("\nTOP RETRIEVED SOURCES")

    for rank, result in enumerate(
        reranked_candidates[:3],
        start=1
    ):
        print(
            f"{rank}. {result.document_name} "
            f"(page {result.page_number}, "
            f"chunk {result.chunk_id}, "
            f"reranker={result.reranker_score})"
        )

    # ---------------------------------------------------------
    # 6. RELEVANCE FILTER
    # ---------------------------------------------------------

    relevant_results = filter_relevant_results(
        reranked_candidates,
        min_reranker_score=60
    )

    final_results = relevant_results[:3]

    # ---------------------------------------------------------
    # 7. SHOW FINAL RESULTS
    # ---------------------------------------------------------

    print("\nFINAL SELECTED SOURCES")

    if not final_results:

        print(
            "No sufficiently relevant information was found."
        )

        answer = (
            "No sufficiently relevant information was found."
        )

    else:

        for result in final_results:

            print(
                f"- {result.document_name} | "
                f"chunk={result.chunk_id} | "
                f"page={result.page_number} | "
                f"score={result.reranker_score}"
            )

        # -----------------------------------------------------
        # 8. BUILD CONTEXT
        # -----------------------------------------------------

        context = build_context(final_results)

        # -----------------------------------------------------
        # 9. GENERATE ANSWER
        # -----------------------------------------------------

        answer = generate_answer(
            question=question,
            context=context
        )

    # ---------------------------------------------------------
    # 10. SHOW ANSWER
    # ---------------------------------------------------------

    print("\nSYSTEM ANSWER")
    print(answer)

    # ---------------------------------------------------------
    # 11. SHOW EXPECTED ANSWER
    # ---------------------------------------------------------

    print("\nEXPECTED ANSWER")
    print(question_data["expected_answer"])

    print("\nREQUIRED DOCUMENT(S)")
    print(question_data["required_documents"])

    return {
        "id": question_data["id"],
        "question": question,
        "expected_answer": question_data["expected_answer"],
        "required_documents": question_data["required_documents"],
        "answer": answer,
        "retrieved_candidates": reranked_candidates,
        "final_results": final_results
    }


def main():

    questions = load_evaluation_questions(
        EVALUATION_FILE
    )
    questions = questions[:5]
    print(
        f"Loaded {len(questions)} evaluation questions."
    )

    results = []

    for question_data in questions:

        result = run_question(
            question_data
        )

        results.append(result)

    print("\n" + "=" * 80)
    print("EVALUATION RUN COMPLETE")
    print("=" * 80)

    print(
        f"Questions processed: {len(results)}"
    )


if __name__ == "__main__":
    main()