from app.database import get_connection
from app.retrieval_models import RetrievedChunk


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 3,
    document_status: str | None = None,
    document_version: str | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            filters = []
            filter_parameters = []

            if document_status:
                filters.append("document_status = %s")
                filter_parameters.append(document_status)

            if document_version:
                filters.append("document_version = %s")
                filter_parameters.append(document_version)

            where_clause = ""

            if filters:
                where_clause = "WHERE " + " AND ".join(filters)

            query = f"""
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
                {where_clause}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """

            parameters = [
                query_embedding,
                *filter_parameters,
                query_embedding,
                top_k
            ]

            cursor.execute(query, parameters)

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
                vector_distance=row[12]
            )
            for row in rows
        ]

    finally:
        connection.close()