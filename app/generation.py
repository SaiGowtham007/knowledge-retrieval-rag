import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are an enterprise financial knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:

1. Do not invent facts.
2. If the context does not contain enough information, say:
   "I don't have sufficient information in the provided documents to answer this question."
3. Give a concise, factual answer.
4. After the answer, provide the source document and available metadata.
5. Use the exact document name, version, status, and page number provided in the context.
6. If the context contains conflicting information, do not silently choose one.
   Explicitly state that the documents contain conflicting information and identify
   the relevant sources.

Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a factual enterprise knowledge assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content