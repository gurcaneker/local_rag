from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from typing import Optional
from app.models.api_schemas import UploadResponse, DocumentListResponse, DocumentItem
from app.services.ingestion_service import IngestionService
from app.db.vector_store_lancedb import LanceDBStore

router = APIRouter()

def get_ingestion_service():
    from app.main import ingestion_service
    return ingestion_service
    
def get_vector_store():
    from app.main import vector_store
    return vector_store

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    tenant_id: Optional[str] = Form(None),
    workspace_id: Optional[str] = Form(None),
    ingester: IngestionService = Depends(get_ingestion_service)
):
    try:
        content = await file.read()
        chunks_count = ingester.ingest_file(
            filename=file.filename,
            content=content,
            tenant_id=tenant_id,
            workspace_id=workspace_id
        )
        
        return UploadResponse(
            document_id="auto",
            filename=file.filename,
            chunks_created=chunks_count,
            message="Upload successful"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("", response_model=DocumentListResponse)
async def list_documents(store: LanceDBStore = Depends(get_vector_store)):
    docs = store.list_documents()
    items = []
    for d in docs:
        items.append(DocumentItem(
            document_id=d.get("document_id", "Unknown"),
            filename=d.get("source_file", "Unknown"),
            created_at="N/A"
        ))
    return DocumentListResponse(documents=items)
