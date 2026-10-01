def build_context(results) -> str:
    context_parts = []

    for result in results:
        content = result[1]
        document_name = result[2]
        chunk_id = result[5]
        page_number = result[6]
        document_id = result[7]
        document_version = result[8]
        document_status = result[9]
        effective_date = result[10]
        owner = result[11]

        context_parts.append(
            f"""
Source: {document_name}
Document ID: {document_id}
Version: {document_version}
Status: {document_status}
Effective Date: {effective_date}
Owner: {owner}
Page: {page_number}
Chunk: {chunk_id}

{content}
"""
        )

    return "\n\n".join(context_parts)