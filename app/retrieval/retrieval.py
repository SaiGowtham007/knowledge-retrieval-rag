from app.database import get_connection


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 3,
    document_status: str | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            if document_status:
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
                        embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE document_status = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_embedding,
                        document_status,
                        query_embedding,
                        top_k
                    )
                )
            else:cursor.execute(
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
                    embedding <=> %s::vector AS distance
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding,
                    query_embedding,
                    top_k
                )
            )

            results = cursor.fetchall()

        return results

    finally:
        connection.close()