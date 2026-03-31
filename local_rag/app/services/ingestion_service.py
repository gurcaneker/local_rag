import uuid
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.db.vector_store_base import VectorStoreBase

class IngestionService:
    def __init__(self, 
                 vector_store: VectorStoreBase, 
                 embedding_service: EmbeddingService,
                 document_service: DocumentService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.document_service = document_service
        
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def _chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunks.append(text[start:end])
            if end == text_length:
                break
            start += self.chunk_size - self.chunk_overlap
            
        return chunks

    def ingest_file(self, filename: str, content: bytes, tenant_id: str = None, workspace_id: str = None) -> int:
        logger.info(f"Starting ingestion for {filename}")
        
        raw_dir = "./data/raw"
        file_path = self.document_service.save_raw_file(filename, content, raw_dir)
        
        text = self.document_service.parse_document(file_path)
        if not text.strip():
            logger.warning("No text extracted from document.")
            return 0
            
        text_chunks = self._chunk_text(text)
        logger.info(f"Created {len(text_chunks)} chunks for {filename}")
        
        document_id = str(uuid.uuid4())
        
        embeddings = self.embedding_service.embed_batch(text_chunks)
        
        prepared_chunks = []
        for i, (chunk_txt, emb) in enumerate(zip(text_chunks, embeddings)):
            prepared_chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk_txt,
                "embedding": emb,
                "metadata": {
                    "document_id": document_id,
                    "source_file": filename,
                    "chunk_index": i,
                    "tenant_id": tenant_id,
                    "workspace_id": workspace_id
                }
            })
            
        self.vector_store.upsert_chunks(prepared_chunks)
        logger.info(f"Successfully ingested {filename}")
        return len(prepared_chunks)
