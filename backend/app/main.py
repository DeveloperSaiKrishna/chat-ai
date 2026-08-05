from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat_route, lang_chain_route, health_ai_route, notes_route, image_to_text_route

from app.db.sqlite_db import init_db

app = FastAPI()

app.include_router(chat_route.router)
app.include_router(lang_chain_route.router)
app.include_router(health_ai_route.router)
app.include_router(notes_route.router)
app.include_router(image_to_text_route.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/")
def root():
    return {"status": "running"}
