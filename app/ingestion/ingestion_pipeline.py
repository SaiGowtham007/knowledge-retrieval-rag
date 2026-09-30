from pathlib import Path

from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.docx_loader import extract_text_from_docx
from app.ingestion.text_loader import extract_text_from_txt

def extract_text(file_path: str) -> str:

    extension = Path(file_path).suffix.lower()

    if extension == ".txt":
        return extract_text_from_txt(file_path)
    elif extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
        )