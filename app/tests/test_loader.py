from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.docx_loader import extract_text_from_docx

pdf_path = "data\pdf\PRFIP_Engineering_and_Operations_Documentation.pdf"
docx_path = "data\docx\PRFIP_Business_Data_API_Model_Documentation.docx"
pdf_text = extract_text_from_pdf(pdf_path)
docx_text = extract_text_from_docx(docx_path)

print("PDF Text:")
print(pdf_text[:3000])

print("\nDOCX Text:")
print(docx_text[:3000])