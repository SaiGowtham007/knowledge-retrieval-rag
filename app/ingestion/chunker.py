from .document import DocumentChunk



def _build_chunks(
    text: str,
    document_name: str,
    document_type: str,
    source: str,
    page_number: int,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    starting_chunk_id: int = 0
) -> list[DocumentChunk]:

    paragraphs = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    chunks = []
    current_chunk = ""
    chunk_id = starting_chunk_id

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
                        chunk_id=chunk_id,
                        page_number=page_number
                    )
                )

                chunk_id += 1

            # Get approximately the last chunk_overlap characters
            overlap_text = current_chunk[-chunk_overlap:]

            if " " in overlap_text:
                overlap_text = overlap_text[
                    overlap_text.find(" ") + 1:
                ]

            current_chunk = (
                overlap_text.strip() + "\n\n" + paragraph + "\n\n"
          )
    if current_chunk:

        chunks.append(
            DocumentChunk(
                content=current_chunk.strip(),
                document_name=document_name,
                document_type=document_type,
                source=source,
                chunk_id=chunk_id,
                page_number=page_number
            )
        )

    return chunks

def create_chunks(
    text: str,
    document_name: str,
    document_type: str,
    source: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[DocumentChunk]:

    return _build_chunks(
        text=text,
        document_name=document_name,
        document_type=document_type,
        source=source,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )


def create_page_chunks(
    text: str,
    document_name: str,
    document_type: str,
    source: str,
    page_number: int,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    starting_chunk_id: int = 0
) -> list[DocumentChunk]:

    return _build_chunks(
        text=text,
        document_name=document_name,
        document_type=document_type,
        source=source,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        page_number=page_number,
        starting_chunk_id=starting_chunk_id
    )