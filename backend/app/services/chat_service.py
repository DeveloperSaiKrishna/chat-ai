import httpx
import json

from app.models.chat_model import ChatRequest

OLLAMA_URL = "http://localhost:11434/api/chat"


async def stream_chat_response(query: ChatRequest):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            url=OLLAMA_URL,
            json={
                "model": query.model,
                "messages": [{"role": "user", "content": query.message}],
                "stream": True,
            },
        ) as response:

            async for line in response.aiter_lines():
                if not line:
                    continue #skips current iteration and moves to the next iteration

                data = json.loads(line) #line is string, so converting it into object

                # 🔥 THIS is your chunk loop location
                if "message" in data:
                    chunk = data["message"].get("content", "")
                    if chunk:
                        yield chunk
