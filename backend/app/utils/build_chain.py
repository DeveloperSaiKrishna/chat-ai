from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.utils.lang_chain_memory import get_session_history


def build_chat_chain(model: str):
    llm = ChatOllama(model=model, streaming=True)

    prompt = ChatPromptTemplate.from_messages(
        [
            # ("system", "You are a helpful assistant."),
            MessagesPlaceholder("history"),
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
