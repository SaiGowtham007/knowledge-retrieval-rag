from app.database import get_connection


def insert_chunk(
    content: str,
    document_name: str,
    document_type: str,
    source: str,
    chunk_id: int,
    embedding: list[float],
    page_number: int | None = None,
    document_id: str | None = None,
    document_version: str | None = None,
    document_status: str | None = None,
    effective_date: str | None = None,
    owner: str | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO document_chunks (
                    content,
                    document_name,
                    document_type,
                    source,
                    chunk_id,
                    embedding,
                    page_number,
                    document_id,
                    document_version,
                    document_status,
                    effective_date,
                    owner
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    content,
                    document_name,
                    document_type,
                    source,
                    chunk_id,
                    embedding,
                    page_number,
                    document_id,
                    document_version,
                    document_status,
                    effective_date,
                    owner
                )
            )

        connection.commit()

    finally:
        connection.close()