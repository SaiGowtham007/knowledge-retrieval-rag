from .document import DocumentChunk


def _split_long_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int
) -> list[str]:

    words = text.split()
    chunks = []

    current_words = []
    current_length = 0

    for word in words:

        added_length = len(word) + 1

        if current_words and current_length + added_length > chunk_size:

            chunks.append(" ".join(current_words))

            overlap_words = []
            overlap_length = 0

            for previous_word in reversed(current_words):

                word_length = len(previous_word) + 1

                if overlap_length + word_length > chunk_overlap:
                    break

                overlap_words.insert(0, previous_word)
                overlap_length += word_length

            current_words = overlap_words
            current_length = overlap_length

        current_words.append(word)
        current_length += added_length

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def _build_chunks(
    text: str,
    document_name: str,
    document_type: str,
    source: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    page_number: int | None = None,
    starting_chunk_id: int = 0
) -> list[DocumentChunk]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""
    chunk_id = starting_chunk_id

    for paragraph in paragraphs:

        # Handle paragraphs larger than chunk_size
        if len(paragraph) > chunk_size:

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
                current_chunk = ""

            smaller_chunks = _split_long_text(
                paragraph,
                chunk_size,
                chunk_overlap
            )

            for smaller_chunk in smaller_chunks:

                chunks.append(
                    DocumentChunk(
                        content=smaller_chunk,
                        document_name=document_name,
                        document_type=document_type,
                        source=source,
                        chunk_id=chunk_id,
                        page_number=page_number
                    )
                )

                chunk_id += 1

            continue

        proposed_chunk = (
            current_chunk
            + paragraph
            + "\n\n"
        )

        if len(proposed_chunk) <= chunk_size:

            current_chunk = proposed_chunk

        else:

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

            overlap_text = current_chunk[-chunk_overlap:]

            if " " in overlap_text:
                overlap_text = overlap_text[
                    overlap_text.find(" ") + 1:
                ]

            current_chunk = (
                overlap_text.strip()
                + "\n\n"
                + paragraph
                + "\n\n"
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