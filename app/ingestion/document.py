from dataclasses import dataclass

@dataclass
class DocumentChunk:
    content: str
    document_name: str
    document_type: str
    source: str
    chunk_id: int