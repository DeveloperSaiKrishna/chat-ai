from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "notes"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_vectorstore():
    return Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )


def add_chunks(chunks, note_id, filename):
    db = get_vectorstore()

    ids = [f"{note_id}_{i}" for i in range(len(chunks))]

    metadatas = [
        {"note_id": note_id, "filename": filename, "chunk_id": i}
        for i in range(len(chunks))
    ]

    db.add_texts(texts=chunks, metadatas=metadatas, ids=ids)


def search(query, k=4):
    db = get_vectorstore()
    return db.similarity_search(query, k=k)
