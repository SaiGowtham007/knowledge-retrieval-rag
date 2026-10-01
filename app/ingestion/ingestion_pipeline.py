from pathlib import Path

from app.embedding import create_embedding
from app.vector_store import insert_chunk

from app.ingestion.pdf_loader import extract_pages_from_pdf
from app.ingestion.docx_loader import extract_text_from_docx
from app.ingestion.chunker import create_chunks, create_page_chunks


def ingest_pdf(file_path: str):
    file = Path(file_path)

    pages = extract_pages_from_pdf(file_path)

    total_chunks = 0
    next_chunk_id = 0

    for page in pages:

        chunks = create_page_chunks(
            text=page["text"],
            document_name=file.name,
            document_type="pdf",
            source=file_path,
            page_number=page["page_number"],
            chunk_size=500,
            chunk_overlap=50,
            starting_chunk_id=next_chunk_id
        )

        for chunk in chunks:

            embedding = create_embedding(chunk.content)

            insert_chunk(
                content=chunk.content,
                document_name=chunk.document_name,
                document_type=chunk.document_type,
                source=chunk.source,
                chunk_id=chunk.chunk_id,
                embedding=embedding,
                page_number=chunk.page_number,

                document_id="PRFIP_ENGINEERING",
                document_version="2026.3",
                document_status="CURRENT",
                effective_date="2026-08-27",
                owner="Marcus Lee"
            )

            total_chunks += 1

        next_chunk_id += len(chunks)

    return total_chunks


def ingest_docx(file_path: str):
    file = Path(file_path)

    text = extract_text_from_docx(file_path)

    chunks = create_chunks(
        text=text,
        document_name=file.name,
        document_type="docx",
        source=file_path,
        chunk_size=500,
        chunk_overlap=50
    )

    for chunk in chunks:

        embedding = create_embedding(chunk.content)

        insert_chunk(
            content=chunk.content,
            document_name=chunk.document_name,
            document_type=chunk.document_type,
            source=chunk.source,
            chunk_id=chunk.chunk_id,
            embedding=embedding,
            page_number=None,

            document_id="PRFIP_BUSINESS_DATA_API_MODEL",
            document_version="2026.3",
            document_status="CURRENT",
            effective_date="2026-09-25",
            owner="Grace Chen"
        )

    return len(chunks)