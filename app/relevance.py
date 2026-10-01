def filter_relevant_results(
    results,
    max_distance: float = 0.50
):
    return [
        result
        for result in results
        if result[12] <= max_distance
    ]