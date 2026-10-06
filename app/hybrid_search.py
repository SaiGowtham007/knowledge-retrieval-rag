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

    rrf_scores = {}
    result_lookup = {}

    k = 60

    # -------------------------
    # VECTOR RESULTS
    # -------------------------
    for rank, result in enumerate(vector_results, start=1):

        result_lookup[result.id] = result

        rrf_scores[result.id] = (
            rrf_scores.get(result.id, 0)
            + 1 / (k + rank)
        )

    # -------------------------
    # KEYWORD RESULTS
    # -------------------------
    for rank, result in enumerate(keyword_results, start=1):

        if result.id in result_lookup:

            # Preserve the object from vector search
            # and copy the keyword score onto it.
            result_lookup[result.id].keyword_score = (
                result.keyword_score
            )

        else:

            # This chunk only came from keyword search.
            result_lookup[result.id] = result

        rrf_scores[result.id] = (
            rrf_scores.get(result.id, 0)
            + 1 / (k + rank)
        )

    # -------------------------
    # STORE RRF SCORE
    # -------------------------
    for result_id, rrf_score in rrf_scores.items():

        result_lookup[result_id].rrf_score = rrf_score

    # -------------------------
    # SORT BY RRF SCORE
    # -------------------------
    ranked_ids = sorted(
        rrf_scores,
        key=rrf_scores.get,
        reverse=True
    )

    return [
        result_lookup[result_id]
        for result_id in ranked_ids
    ]