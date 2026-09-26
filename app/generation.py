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

If the context does not contain enough information to answer the question,
say that the information is not available in the provided documents.

Do not invent facts.

Always keep the answer concise and factual.

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