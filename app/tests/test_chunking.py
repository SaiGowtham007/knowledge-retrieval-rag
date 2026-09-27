from app.ingestion.text_loader import extract_text_from_txt
from app.ingestion.chunker import create_chunks


file_path = "data/payment_risk_requirements.txt"

text = extract_text_from_txt(file_path)

chunks = create_chunks(
    text=text,
    document_name="payment_risk_requirements.txt",
    document_type="txt",
    source=file_path,
    chunk_size=500,
    chunk_overlap=10
)

print(f"Total Chunks: {len(chunks)}")

for chunk in chunks:
    print("\n" + "=" * 60)
    print(f"Chunk ID: {chunk.chunk_id}")
    print("=" * 60)
    print(chunk.content)