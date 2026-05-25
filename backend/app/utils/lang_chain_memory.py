from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory

memory_store = {}


def get_session_history(session_id: str):
    print(session_id, 'SESSSION')
    if session_id not in memory_store:
        memory_store[session_id] = InMemoryChatMessageHistory()

    return memory_store[session_id]
