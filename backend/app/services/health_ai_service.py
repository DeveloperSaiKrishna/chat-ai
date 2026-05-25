from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def build_chat_chain(model: str):
    llm = ChatOllama(model=model, streaming=True)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a medical report analysis assistant and clinical nutritionist.\n"
                "\n"
                "Your task is to analyze blood reports and provide output in exactly two sections only.\n"
                "\n"
                "1. Health Summary:\n"
                "- Present the summary in bullet points only.\n"
                "- Each bullet should describe one clear observation about the patient's health.\n"
                "- Use simple, easy-to-understand language.\n"
                "- Keep it to 4–6 bullet points.\n"
                "- Do NOT diagnose diseases.\n"
                "\n"
                "2. Diet Plan:\n"
                "- Provide a practical diet plan in bullet points.\n"
                "- Clearly divide into:\n"
                "  • Foods to eat\n"
                "  • Foods to avoid\n"
                "\n"
                "Rules:\n"
                "- Do NOT give medical diagnosis.\n"
                "- Do NOT prescribe medicines.\n"
                "- Keep language simple, clear, and practical.\n"
                "- Use only information inferred from the blood report.\n"
                "- Output must contain ONLY the two sections above.",
            ),
            ("human", "{input}"),
        ]
    )
    return prompt | llm


async def stream_chat_response(req):
    chat_chain = build_chat_chain(req.model)

    async for chunk in chat_chain.astream({"input": req.message}):
        if chunk.content:
            yield chunk.content
