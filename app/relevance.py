def filter_relevant_results(
    results,
    min_reranker_score: int = 60
):
    return [
        result
        for result in results
        if result.reranker_score is not None
        and result.reranker_score >= min_reranker_score
    ]