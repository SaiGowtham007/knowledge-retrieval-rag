def build_context(results) -> str:
    context_parts = []

    for result in results:
        context = result[1]
        document_name = result[2]
        chunk_id = result[5]

        context_parts.append(
            f"""
Source: {document_name}
Chunk: {chunk_id}
{context}
"""
        )
    return "\n\n".join(context_parts)