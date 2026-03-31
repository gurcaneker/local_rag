from fastapi import APIRouter, Depends, HTTPException
from app.models.api_schemas import ChatRequest, ChatResponse, SourceItem
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.core.prompts import QA_PROMPT_TEMPLATE

router = APIRouter()

def get_retrieval_service():
    from app.main import retrieval_service
    return retrieval_service

def get_llm_service():
    from app.main import llm_service
    return llm_service

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    request: ChatRequest,
    retriever: RetrievalService = Depends(get_retrieval_service),
    llm: LLMService = Depends(get_llm_service)
):
    try:
        results = retriever.retrieve(
            query=request.query, 
            tenant_id=request.tenant_id, 
            workspace_id=request.workspace_id
        )
        
        context_texts = []
        sources = []
        
        for r in results:
            context_texts.append(r["text"])
            sources.append(SourceItem(
                chunk_id=r["id"],
                source_file=r["metadata"]["source_file"],
                text_snippet=r["text"][:100] + "...",
                score=r["score"]
            ))
            
        context_block = "\n\n".join(context_texts)
        if not context_block:
            context_block = "No relevant context found."
            
        prompt = QA_PROMPT_TEMPLATE.format(context=context_block, query=request.query)
        
        answer = llm.generate_response(prompt)
        
        return ChatResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
