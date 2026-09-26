from app.embedding import create_embedding
from app.retrieval import search_similar_chunks
from app.context_builder import build_context
from app.generation import generate_answer
from app.relevance import filter_relevant_results

question = "Who is responsible for the fraud detection model?"

query_embedding = create_embedding(question)

results = search_similar_chunks(
    query_embedding=query_embedding,
    top_k=3
)

relevant_results = filter_relevant_results(results)

if not relevant_results:
    print("\n No Sufficiently Relevant information was found.")
else:
    context = build_context(relevant_results)
    answer = generate_answer(
        question=question,
        context=context
    )


    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)

    print(question)


    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(answer)


    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for result in results:
        print(
            f"- {result[2]} "
            f"(chunk {result[5]}, distance={result[6]:.4f})"
        )