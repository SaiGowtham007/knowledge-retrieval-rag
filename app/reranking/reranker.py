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

        content = result.content
        document_name = result.document_name
        chunk_id = result.chunk_id
        page_number = result.page_number
        document_id = result.document_id
        document_version = result.document_version
        document_status = result.document_status
        effective_date = result.effective_date
        owner = result.owner

        prompt = f"""
        Rate how relevant the following document chunk is
        to the user's question.

        Consider BOTH the content and the document metadata.

        User question:
        {question}

        Document metadata:
        Document: {document_name}
        Document ID: {document_id}
        Document Version: {document_version}
        Document Status: {document_status}
        Effective Date: {effective_date}
        Owner: {owner}
        Page: {page_number}
        Chunk: {chunk_id}

        Document chunk:
        {content}

        Scoring:

        100 = directly answers the question
        80 = strongly supports the answer
        60 = useful supporting information
        40 = related but does not answer the question
        20 = weakly related
        0 = not relevant

        Return only a whole number from 0 to 100.
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
        
        result.reranker_score = score
        scored_results.append(result)

    scored_results.sort(
    key=lambda result: result.reranker_score,
    reverse=True
)

    return scored_results[:top_k]