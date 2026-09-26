from .document import DocumentChunk


def create_chunks(
    text: str,
    document_name: str,
    document_type: str,
    source: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[DocumentChunk]:

    paragraphs = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    chunks = []
    current_chunk = ""
    chunk_id = 0

    for paragraph in paragraphs:

        proposed_chunk = current_chunk + paragraph + "\n\n"

        if len(proposed_chunk) <= chunk_size:

            current_chunk = proposed_chunk

        else:

            if current_chunk:

                chunks.append(
                    DocumentChunk(
                        content=current_chunk.strip(),
                        document_name=document_name,
                        document_type=document_type,
                        source=source,
                        chunk_id=chunk_id
                    )
                )

                chunk_id += 1

            # Get approximately the last chunk_overlap characters
            overlap_text = current_chunk[-chunk_overlap:]

            # Move backward until we reach a space
            while overlap_text and not overlap_text.startswith(" "):
                overlap_text = overlap_text[1:]

            current_chunk = overlap_text.strip() + "\n\n" + paragraph + "\n\n"

    if current_chunk:

        chunks.append(
            DocumentChunk(
                content=current_chunk.strip(),
                document_name=document_name,
                document_type=document_type,
                source=source,
                chunk_id=chunk_id
            )
        )

    return chunks