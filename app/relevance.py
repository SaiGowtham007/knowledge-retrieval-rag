def filter_relevant_results(
        results,
        max_distance: float = 0.50
):

    return [
        result 
        for result in results
        if result[6] <= max_distance
    ]