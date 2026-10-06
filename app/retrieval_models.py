from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    id: int
    content: str
    document_name: str
    document_type: str
    source: str
    chunk_id: int
    page_number: int | None
    document_id: str | None
    document_version: str | None
    document_status: str | None
    effective_date: str | None
    owner: str | None

    # Retrieval scores
    vector_distance: float | None = None
    keyword_score: float | None = None
    rrf_score: float | None = None
    reranker_score: float | None = None