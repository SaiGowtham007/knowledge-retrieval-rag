import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def rerank_results(
    question: str,
    results,
    top_k: int = 3
):
    scored_results = []

    for result in results:

        content = result[1]

        prompt = f"""
Rate how relevant the following document chunk is
to the user's question.

User question:
{question}

Document chunk:
{content}

Return only a number from 0 to 100.

100 = directly answers the question
50 = somewhat relevant
0 = not relevant
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        score = int(
            response.choices[0].message.content.strip()
        )

        scored_results.append(
            (score, result)
        )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        result
        for score, result in scored_results[:top_k]
    ]