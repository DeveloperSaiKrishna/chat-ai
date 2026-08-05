from fastapi import UploadFile
import base64
import httpx
import json

from app.utils.image_to_text_memory import get_history, save_message

OLLAMA_URL = "http://localhost:11434/api/chat"


async def stream_chat_response(
    session_id: str,
    message: str,
    image: UploadFile | None = None,
):
    assistant_text = ""

    user_message = {
        "role": "user",
        "content": message,
    }

    # Optional image
    if image:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        user_message["images"] = [image_base64]

    # Save FULL structured message
    save_message(session_id, user_message)

    # Get conversation history
    messages = get_history(session_id)

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            url=OLLAMA_URL,
            json={
                "model": "qwen2.5vl:latest",
                "messages": messages,
                "stream": True,
            },
        ) as response:

            async for line in response.aiter_lines():

                if not line:
                    continue

                data = json.loads(line)

                chunk = data.get("message", {}).get("content", "")

                if chunk:
                    assistant_text += chunk
                    yield chunk

    assistant_message = {
        "role": "assistant",
        "content": assistant_text,
    }

    save_message(session_id, assistant_message)
