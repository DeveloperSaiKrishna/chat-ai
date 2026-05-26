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


# import httpx
# import json

# from app.models.chat_model import ChatRequest
# from app.utils.memory import get_history, save_message


# OLLAMA_URL = "http://localhost:11434/api/chat"


# def format_history(history):
#     """
#     Convert stored history into Ollama format:
#     [{role: "user", content: "..."}]
#     """
#     return [
#         {
#             "role": role,
#             "content": msg
#         }
#         for role, msg in history
#     ]


# async def stream_chat_response(query: ChatRequest):

#     assistant_text = ""

#     # 1. Save user message
#     save_message(query.session_id, "user", query.message)

#     # 2. Load history
#     history = get_history(query.session_id)
#     messages = format_history(history)

#     # 3. Add current user message (important for correct ordering)
#     messages.append({
#         "role": "user",
#         "content": query.message
#     })

#     # 4. Call Ollama streaming API
#     async with httpx.AsyncClient(timeout=None) as client:
#         async with client.stream(
#             "POST",
#             OLLAMA_URL,
#             json={
#                 "model": query.model,
#                 "messages": messages,
#                 "stream": True,
#             },
#         ) as response:

#             async for line in response.aiter_lines():

#                 if not line:
#                     continue

#                 try:
#                     data = json.loads(line)
#                 except json.JSONDecodeError:
#                     continue

#                 # Ollama stream format
#                 if "message" in data:
#                     chunk = data["message"].get("content", "")
#                     if chunk:
#                         assistant_text += chunk
#                         yield chunk

#                 # optional: stop signal
#                 if data.get("done"):
#                     break

#     # 5. Save final assistant response
#     save_message(query.session_id, "assistant", assistant_text)