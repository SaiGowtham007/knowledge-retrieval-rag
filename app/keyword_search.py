from app.database import get_connection
from app.retrieval_models import RetrievedChunk


def search_keyword_chunks(
    question: str,
    top_k: int = 10
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    content,
                    document_name,
                    document_type,
                    source,
                    chunk_id,
                    page_number,
                    document_id,
                    document_version,
                    document_status,
                    effective_date,
                    owner,
                    ts_rank(
                        search_vector,
                        plainto_tsquery('english', %s)
                    ) AS keyword_score
                FROM document_chunks
                WHERE search_vector @@ plainto_tsquery('english', %s)
                ORDER BY keyword_score DESC
                LIMIT %s
                """,
                (
                    question,
                    question,
                    top_k
                )
            )

            rows = cursor.fetchall()

        return [
            RetrievedChunk(
                id=row[0],
                content=row[1],
                document_name=row[2],
                document_type=row[3],
                source=row[4],
                chunk_id=row[5],
                page_number=row[6],
                document_id=row[7],
                document_version=row[8],
                document_status=row[9],
                effective_date=row[10],
                owner=row[11],
                keyword_score=row[12]
            )
            for row in rows
        ]

    finally:
        connection.close()