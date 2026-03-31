from typing import List, Dict, Any
from app.core.config import settings
from app.db.vector_store_base import VectorStoreBase
from app.services.embedding_service import EmbeddingService

class RetrievalService:
    def __init__(self, vector_store: VectorStoreBase, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.top_k = settings.TOP_K

    def retrieve(self, query: str, tenant_id: str = None, workspace_id: str = None) -> List[Dict[str, Any]]:
        query_emb = self.embedding_service.embed_text(query)
        
        filters = {}
        if tenant_id:
            filters["tenant_id"] = tenant_id
        if workspace_id:
            filters["workspace_id"] = workspace_id
            
        results = self.vector_store.search(query_emb, top_k=self.top_k, filters=filters)
        return results
