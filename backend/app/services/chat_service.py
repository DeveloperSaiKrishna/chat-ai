import httpx
import json

from app.models.chat_model import ChatRequest
from app.utils.memory import get_history, save_message

OLLAMA_URL = "http://localhost:11434/api/chat"


async def stream_chat_response(query: ChatRequest):
    assistant_text = ""

    save_message(query.session_id, "user", query.message)

    history = get_history(query.session_id)
    messages = history

    # print(messages, "messages")

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            url=OLLAMA_URL,
            json={
                "model": query.model,
                "messages": messages,
                "stream": True,
            },
        ) as response:

            async for line in response.aiter_lines():
                if not line:
                    continue  # skips current iteration and moves to the next iteration

                data = json.loads(line)  # line is string, so converting it into object

                # 🔥 THIS is your chunk loop location
                if "message" in data:
                    chunk = data["message"].get("content", "")
                    if chunk:
                        assistant_text += chunk
                        yield chunk

    save_message(query.session_id, "assistant", assistant_text)
