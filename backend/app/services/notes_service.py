from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vectorstore.chroma_store import search
from app.utils.build_search_chain import build_search_chain
from app.db.sqlite_db import insert_note, get_notes
from app.vectorstore.chroma_store import add_chunks


def format_context(results, limit=4):
    results = results[:limit]
    # return "\n\n".join([r.page_content for r in results])
    context = "\n\n".join(
        [f"Source: {r.metadata.get('filename')}\n{r.page_content}" for r in results]
    )
    return context


# def format_context(results, limit=4):
#     results = results[:limit]
#     formatted_chunks = []

#     for r in results:
#         filename = r.metadata.get("filename", "unknown")
#         formatted_chunks.append(f"Source: {filename}\n{r.page_content}")

#     return "\n\n".join(formatted_chunks)


# def format_context(results, limit=4):

#     results = results[:limit]

#     return "\n\n".join([r.page_content for r in results])


async def search_notes_service_stream(query: str, session_id: str, model: str):

    # 1. Vector search (RAG)
    results = search(query, k=5)

    context = format_context(results) if results else "No relevant notes found."

    # 2. Build chat chain
    chain = build_search_chain(model)

    # 3. Stream response
    async for chunk in chain.astream(
        {"input": query, "context": context},
        config={"configurable": {"session_id": session_id}},
    ):
        if chunk.content:
            yield chunk.content


"""
CHUNK_SIZE & OVERLAP
Are answers missing context? → increase chunk size
Are answers irrelevant? → decrease chunk size
Are boundaries cutting info? → increase overlap
"""
def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    return splitter.split_text(text)


def add_note_service(filename: str, content: str):

    # 1. Save raw note in SQLite (source of truth)
    note_id = insert_note(filename, content)

    # 2. Chunk text for embeddings
    chunks = chunk_text(content)

    if not chunks:
        return {"status": "failed", "message": "Empty or invalid content"}

    # 3. Store in vector DB (Chroma)
    add_chunks(chunks=chunks, note_id=note_id, filename=filename)

    return {
        "status": "success",
        "note_id": note_id,
        "filename": filename,
        "chunks_added": len(chunks),
    }


def get_all_notes():
    return get_notes()
