from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routes import router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=(
        "LegalEaseAI API for AI-assisted "
        "legal document drafting and export."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }