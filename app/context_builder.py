def build_context(results) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):

        context_parts.append(
            f"""
[SOURCE {index}]
Document: {result.document_name}
Document ID: {result.document_id}
Version: {result.document_version}
Status: {result.document_status}
Effective Date: {result.effective_date}
Owner: {result.owner}
Page: {result.page_number}
Chunk: {result.chunk_id}

Content:
{result.content}
"""
        )

    return "\n\n".join(context_parts)