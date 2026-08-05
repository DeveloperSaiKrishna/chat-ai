from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from app.services.image_to_text_service import stream_chat_response

router = APIRouter(prefix="/image-to-text", tags=["Image to Text"])


@router.post("")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...),
    image: UploadFile | None = File(None),
):

    async def event_generator():
        async for chunk in stream_chat_response(session_id, message, image):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/event-stream")
