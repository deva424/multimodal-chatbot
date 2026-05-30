# src/api/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
import logging
from src.schemas.chat import ChatTurnRequest, ChatTurnResponse
from src.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
router = APIRouter()

def get_gemini_service() -> GeminiService:
    return GeminiService()

@router.post("/chat/submit", response_model=ChatTurnResponse)
async def handle_chat_turn(
    payload: ChatTurnRequest, 
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    try:
        mock_history = [] 
        
        # payload.parts[0].image_bytes is now converted back to raw bytes automatically by Pydantic!
        text_response, generated_visuals = gemini_service.execute_turn(
            history=mock_history,
            new_request_parts=payload.parts
        )
        
        saved_urls = [] 
        
        return ChatTurnResponse(
            conversation_id=payload.conversation_id,
            text_content=text_response,
            generated_image_urls=saved_urls
        )
        
    except ValueError as val_err:
        logger.error(f"Validation Failure: {str(val_err)}")
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        # Crucial for local debugging: logs the exact crash reason to your terminal window
        logger.exception("Inference processing loop hit an unexpected failure:")
        raise HTTPException(status_code=500, detail=f"Internal processing cluster failure: {str(e)}")