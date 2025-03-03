import structlog
from fastapi import APIRouter, Depends

from app.models.request_models import RAGRequest
from app.models.response_models import ErrorResponse, Response
from app.services.rag_service import ask_question
from app.utils.exceptions import CustomHTTPException

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post(
    path="/",
    tags=["RAG"],
    description="Ask question related to the knowledge base")
async def chat(
    request: RAGRequest = Depends()
):
    try:
        result = await ask_question(
            api_key=request.llm_api_key,
            collection_name=request.collection_name,
            question=request.query
        )
        return Response(
            status=200,
            data={"result": result}
        )
    except Exception as e:
        logger.error("Error asking question", exc_info=e)
        raise CustomHTTPException(
            status_code=500,
            detail=ErrorResponse(
                status=500,
                message="Call retriever service failed"
            ).
            model_dump()
        )