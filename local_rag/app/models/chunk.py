from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

class ChunkMetadata(BaseModel):
    document_id: str
    source_file: str
    page_number: Optional[int] = None
    chunk_index: int
    tenant_id: Optional[str] = None
    workspace_id: Optional[str] = None

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    metadata: ChunkMetadata
    embedding: Optional[list[float]] = None
