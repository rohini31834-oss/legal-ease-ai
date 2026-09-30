import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    APP_NAME = os.getenv("APP_NAME", "LegalEaseAI")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3-flash-preview"
    ).strip()

    AI_PROVIDER = os.getenv(
        "AI_PROVIDER",
        "gemini"
    ).strip().lower()

    MOCK_ON_MISSING_KEY = (
        os.getenv(
            "MOCK_ON_MISSING_KEY",
            "true"
        ).lower()
        == "true"
    )

    BACKEND_HOST = os.getenv(
        "BACKEND_HOST",
        "127.0.0.1"
    )

    BACKEND_PORT = int(
        os.getenv(
            "BACKEND_PORT",
            "8000"
        )
    )

    MAX_INPUT_CHARS = int(
        os.getenv(
            "MAX_INPUT_CHARS",
            "12000"
        )
    )

    REQUEST_TIMEOUT_SECONDS = int(
        os.getenv(
            "REQUEST_TIMEOUT_SECONDS",
            "120"
        )
    )

    TEMPERATURE = float(
        os.getenv(
            "TEMPERATURE",
            "0.4"
        )
    )


settings = Settings()