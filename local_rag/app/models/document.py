from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class DocumentMetadata(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: Optional[str] = None
    workspace_id: Optional[str] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: DocumentMetadata
    text: str
