from app.retrieval.retrieval import search_similar_chunks
from app.keyword_search import search_keyword_chunks


def hybrid_search(
    question: str,
    query_embedding: list[float],
    vector_top_k: int = 10,
    keyword_top_k: int = 10,
    document_status: str | None = None
):
    vector_results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=vector_top_k,
        document_status=document_status
    )

    keyword_results = search_keyword_chunks(
        question=question,
        top_k=keyword_top_k
    )

    combined_results = vector_results + keyword_results

    unique_results = {}
    
    for result in combined_results:
        result_id = result[0]
        unique_results[result_id] = result

    return list(unique_results.values())