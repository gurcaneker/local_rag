from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.db.vector_store_lancedb import LanceDBStore
from app.services.embedding_service import EmbeddingService
from app.services.document_service import DocumentService
from app.services.ingestion_service import IngestionService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService

from app.api.routes_chat import router as chat_router
from app.api.routes_documents import router as doc_router
from app.api.routes_health import router as health_router

vector_store = LanceDBStore()
embedding_service = EmbeddingService()
document_service = DocumentService()
ingestion_service = IngestionService(vector_store, embedding_service, document_service)
retrieval_service = RetrievalService(vector_store, embedding_service)
llm_service = LLMService()

app = FastAPI(
    title=settings.APP_NAME,
    description="A foundational Local RAG Platform ready for scale.",
    version="0.1.0"
)

@app.on_event("startup")
def startup_event():
    logger.info("Starting up Local RAG Platform...")
    vector_store.initialize()

app.include_router(health_router, tags=["Health"])
app.include_router(doc_router, prefix="/documents", tags=["Documents"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
