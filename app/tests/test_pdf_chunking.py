from app.ingestion.pdf_loader import extract_pages_from_pdf
from app.ingestion.chunker import create_page_chunks


file_path = "data/pdf/PRFIP_Engineering_and_Operations_Documentation.pdf"

pages = extract_pages_from_pdf(file_path)

total_chunks = 0
next_chunk_id = 0

for page in pages:

    chunks = create_page_chunks(
        text=page["text"],
        document_name="PRFIP_Engineering_and_Operations_Documentation.pdf",
        document_type="pdf",
        source=file_path,
        page_number=page["page_number"],
        chunk_size=500,
        chunk_overlap=50,
        starting_chunk_id=next_chunk_id
    )

    for chunk in chunks:

        print("\n" + "=" * 70)
        print(
            f"Page: {chunk.page_number} | "
            f"Chunk: {chunk.chunk_id}"
        )
        print("=" * 70)

        print(chunk.content[:300])

        total_chunks += 1

    next_chunk_id += len(chunks)


print("\n" + "=" * 70)
print(f"TOTAL CHUNKS: {total_chunks}")
print("=" * 70)