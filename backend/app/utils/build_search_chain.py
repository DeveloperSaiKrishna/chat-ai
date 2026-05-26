from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.utils.lang_chain_memory import get_session_history


def build_search_chain(model: str):
    llm = ChatOllama(model=model, streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            # (
            #     "system",
            #     """You are a helpful AI assistant for a personal notes system.
            #     RULES:
            #     - Use ONLY the provided context for factual answers
            #     - If context is not enough, say you don't know
            #     - Be concise and clear
            #     Context:
            #     {context}
            #     """,
            # ),
            # Normal RAG (recommended)
            #     ✔ good balance
            #     ✔ smarter answers
            #     ✔ fallback knowledge
            (
                "system",
                """
                    You are a helpful AI assistant.
                    Use the provided context internally.
                    Do NOT expose raw chunks unless explicitly asked.
                    Do NOT copy large portions verbatim.
                    Answer naturally and clearly.
                    Context:
                    {context}
                """,
            ),
            # """
            # ROG: Retrieval Only Generation
            # Strict mode:
            #     ✔ only uploaded files
            #     ❌ worse general intelligence
            #     ❌ may refuse too often
            # """
            # (
            #     "system",
            #     """
            #         You are a notes-based assistant.

            #         RULES:
            #         - You MUST ONLY use the provided context.
            #         - If the answer is not in context, say:
            #         "I don't know based on the uploaded notes."
            #         - Do NOT use external knowledge.

            #         Context:
            #         {context}
            #     """,
            # ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
