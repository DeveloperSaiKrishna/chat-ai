from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

from app.utils.build_chain import build_chat_chain


async def stream_chat_response(req):
    chat_chain = build_chat_chain(req.model)

    async for event in chat_chain.astream_events(
        {"input": req.message},
        config={"configurable": {"session_id": req.session_id}},
        version="v2",
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield chunk.content
