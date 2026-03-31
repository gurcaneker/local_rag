from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_created: int
    message: str

class DocumentItem(BaseModel):
    document_id: str
    filename: str
    created_at: str

class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]

class ChatRequest(BaseModel):
    query: str
    tenant_id: Optional[str] = None
    workspace_id: Optional[str] = None

class SourceItem(BaseModel):
    chunk_id: str
    source_file: str
    text_snippet: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

class HealthResponse(BaseModel):
    status: str
    vector_store: str
    llm_service: str
