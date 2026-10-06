from app.database import get_connection


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

            results = cursor.fetchall()

        return results

    finally:
        connection.close()