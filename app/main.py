from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import health, questions, tags


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para um sistema individual de estudos com flashcards de questões de vestibular.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(questions.router)
app.include_router(tags.router)


@app.get("/")
def root():
    return {
        "message": "Vestibular Flashcards API",
        "docs": "/docs",
        "health": "/health",
    }