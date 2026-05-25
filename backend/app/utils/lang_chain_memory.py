from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

memory_store = {}

# Create model ONCE globally
llm = ChatOllama(model="llama3", streaming=True)


def get_session_history(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = InMemoryChatMessageHistory()

    return memory_store[session_id]


chat_chain = RunnableWithMessageHistory(llm, get_session_history)
