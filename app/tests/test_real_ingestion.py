from app.ingestion.ingestion_pipeline import (
    ingest_pdf,
    ingest_docx
)


pdf_path = (
    "data/pdf/"
    "PRFIP_Engineering_and_Operations_Documentation.pdf"
)

docx_path = (
    "data/docx/"
    "PRFIP_Business_Data_API_Model_Documentation.docx"
)


print("\nIngesting PDF...")

pdf_chunks = ingest_pdf(pdf_path)

print(f"PDF chunks stored: {pdf_chunks}")


print("\nIngesting DOCX...")

docx_chunks = ingest_docx(docx_path)

print(f"DOCX chunks stored: {docx_chunks}")


print("\nIngestion complete.")
print(f"Total chunks stored: {pdf_chunks + docx_chunks}")