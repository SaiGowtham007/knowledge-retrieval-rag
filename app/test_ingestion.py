from app.ingestion.text_loader import extract_text_from_txt
from app.ingestion.chunker import create_chunks
from app.embedding import create_embedding
from app.vector_store import insert_chunk

file_path = "data/payment_risk_requirements.txt"

text = extract_text_from_txt(file_path)

chunks = create_chunks(
    text=text, 
    document_name="payment_risk_requirements.txt",
    document_type="txt",
    source=file_path,
    chunk_size=500, 
    )

print(f"Total Chunks: {len(chunks)}")

for chunk in chunks:
    print(f"\nProcessing chunk {chunk.chunk_id + 1} of {len(chunks)}")
    embedding = create_embedding(chunk.content)

    # print("\n" + "=" *40)
    # print(f"CHUNK ID: {chunk.chunk_id}")
    # print(f"DOCUMENT: {chunk.document_name}")
    # print(f"SOURCE: {chunk.source}")
    # print(f"EMBEDDING DIMENSION: {len(embedding)}")
    # print(f"FIRST 5 VALUES: {embedding[:5]}")
    # print("\n" + "=" * 40)
    # print(chunk.content)

    insert_chunk(
        content=chunk.content,
        document_name=chunk.document_name,
        document_type=chunk.document_type,
        source=chunk.source,
        chunk_id=chunk.chunk_id,
        embedding=embedding
    )

    print("Stored Successfully in the database.")