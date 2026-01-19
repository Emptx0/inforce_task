import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    LLM_PROVIDER: str = os.getenv(
        "LLM_PROVIDER",
        "ollama"
    )

    OLLAMA_BASE_URL: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )
    OLLAMA_MODEL: str = os.getenv(
        "OLLAMA_MODEL",
        "gemma3:1b"
    )

    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
