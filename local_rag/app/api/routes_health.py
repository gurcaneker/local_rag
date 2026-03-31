from fastapi import APIRouter, Depends
from app.models.api_schemas import HealthResponse

router = APIRouter()

def get_llm_service():
    from app.main import llm_service
    return llm_service
    
def get_vector_store():
    from app.main import vector_store
    return vector_store

@router.get("/health", response_model=HealthResponse)
async def health_check(
    llm = Depends(get_llm_service),
    store = Depends(get_vector_store)
):
    return HealthResponse(
        status="ok",
        vector_store="connected" if store.health_check() else "disconnected",
        llm_service="connected" if llm.health_check() else "disconnected"
    )
