from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import io
from PyPDF2 import PdfReader

from app.services.notes_service import add_note_service, search_notes_service_stream
from app.models.chat_model import ChatRequest

router = APIRouter(prefix="/notes", tags=["Notes"])


# ----------------------------
# Helper: Extract text safely
# ----------------------------
async def extract_text(file: UploadFile) -> str:
    raw = await file.read()
    filename = file.filename.lower()

    # 📄 PDF handling
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(raw))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"PDF parsing failed: {str(e)}")

    # 📝 TXT / general text handling
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return raw.decode("latin-1")
        except Exception:
            raise HTTPException(status_code=400, detail="Unsupported file encoding")


# ----------------------------
# Upload Note
# ----------------------------
@router.post("/upload")
async def upload_note(file: UploadFile = File(...)):
    content = await extract_text(file)

    if not content.strip():
        raise HTTPException(status_code=400, detail="Empty file content")

    result = add_note_service(file.filename, content)

    return {
        "message": "Note uploaded successfully",
        "filename": file.filename,
        "result": result,
    }


# ----------------------------
# Search Notes
# ----------------------------
# @router.get("/search")
# def search_notes(
#     search_query: str = Query(..., description="What you want to search"),
#     session_id: str = Query(..., description="User/session identifier"),
#     model: str = Query("llama3", description="LLM model to use (Ollama)"),
# ):
#     return search_notes_service_stream(query=search_query, session_id=session_id, model=model)


@router.post("/search")
async def search_notes(payload: ChatRequest):

    return StreamingResponse(
        search_notes_service_stream(
            query=payload.message,
            session_id=payload.session_id,
            model=payload.model,
        ),
        # media_type="text/plain",
        media_type="text/event-stream"
    )
