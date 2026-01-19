from src.llm.ollama_client import OllamaClient
from src.llm.base import LLMClient

from src.config import settings


def get_llm_client() -> LLMClient:
    provider = settings.LLM_PROVIDER
    if provider == "ollama":
        try:
            return OllamaClient()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize OllamaClient: {e}"
            ) from e

    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider}'."
        )


if __name__ == "__main__":
    llm_client = get_llm_client()
    print(llm_client)