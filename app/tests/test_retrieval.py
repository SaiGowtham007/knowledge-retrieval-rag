from app.embedding import create_embedding
from app.retrieval.retrieval import search_similar_chunks
from app.context_builder import build_context
from app.generation import generate_answer
from app.relevance import filter_relevant_results
from app.reranking.reranker import rerank_results

question = "Who is responsible for the fraud detection model?"

query_embedding = create_embedding(question)

results = search_similar_chunks(
    query_embedding=query_embedding,
    top_k=3
)

relevant_results = filter_relevant_results(results)

reranked_results = rerank_results(relevant_results)

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
            f"(chunk {result[5]}, distance={result[6]:.4f})"
        )