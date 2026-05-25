from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.chat_service import stream_chat_response
from app.models.chat_model import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
async def chat(req: ChatRequest):
    async def event_generator():
        async for chunk in stream_chat_response(req):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/even-stream")
