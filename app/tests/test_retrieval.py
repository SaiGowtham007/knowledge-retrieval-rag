from app.embedding import create_embedding
from app.retrieval.retrieval import search_similar_chunks
from app.context_builder import build_context
from app.generation import generate_answer
from app.relevance import filter_relevant_results
from app.reranking.reranker import rerank_results
from app.query_intent import detect_document_status, detect_version
from app.hybrid_search import hybrid_search

question = input("Enter your question: ")


query_embedding = create_embedding(question)
document_version = detect_version(question)
document_status = detect_document_status(question)
results = hybrid_search(
    question=question,
    query_embedding=query_embedding,
    vector_top_k=10,
    keyword_top_k=10,
    document_status=document_status
)
relevant_results = filter_relevant_results(results)

reranked_results = rerank_results(
    question=question,
    results=relevant_results,
    top_k=3
)
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


    print("SOURCES")

    for result in reranked_results:
        print(
            f"- {result[2]} "
        f"(chunk {result[5]}, "
        f"page {result[6]}, "
        f"version {result[8]}, "
        f"status {result[9]}, "
        f"distance={result[12]:.4f})"
        )