from dataclasses import dataclass


@dataclass
class DocumentChunk:
    content: str
    document_name: str
    document_type: str
    source: str
    chunk_id: int
    page_number: int | None = None

    document_id: str | None = None
    document_version: str | None = None
    document_status: str | None = None
    effective_date: str | None = None
    owner: str | None = None