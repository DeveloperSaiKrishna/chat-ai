from app.utils.lang_chain_memory import chat_chain


async def stream_chat_response(req):

    async for chunk in chat_chain.astream(
        req.message, config={"configurable": {"session_id": req.session_id}}
    ):

        if chunk.content:
            yield f"data: {chunk.content}\n\n"
