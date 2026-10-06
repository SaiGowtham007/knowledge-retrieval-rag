from app.embedding import create_embedding
from app.context_builder import build_context
from app.generation import generate_answer
from app.reranking.reranker import rerank_results
from app.query_intent import detect_document_status
from app.hybrid_search import hybrid_search
from app.relevance import filter_relevant_results

question = input("Enter your question: ")


query_embedding = create_embedding(question)
document_status = detect_document_status(question)

results = hybrid_search(
    question=question,
    query_embedding=query_embedding,
    vector_top_k=10,
    keyword_top_k=10,
    document_status=document_status
)
reranked_candidates = rerank_results(
    question=question,
    results=results,
    top_k=10
)

relevant_results = filter_relevant_results(
    reranked_candidates,
    min_reranker_score=60
)

reranked_results = relevant_results[:3]
if not relevant_results:
    print("\n No Sufficiently Relevant information was found.")
else:
    context = build_context(reranked_results)
    answer = generate_answer(
        question=question,
        context=context
    )


    print("QUESTION")

    print(question)


    print("ANSWER")

    print(answer)


    print("\nSOURCES")

    for result in reranked_results:
        print(
            f"- {result.document_name} "
            f"(chunk {result.chunk_id}, "
            f"page {result.page_number}, "
            f"version {result.document_version}, "
            f"status {result.document_status}, "
            f"vector_distance={result.vector_distance}, "
            f"keyword_score={result.keyword_score}, "
            f"rrf_score={result.rrf_score}, "
            f"reranker_score={result.reranker_score})"
        )