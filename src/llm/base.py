from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> dict[str, str]:
        """
        Returns OpenAI-like response:
        {
            "content": str,
            "usage": {
                "prompt_tokens": int,
                "completion_tokens": int,
                "total_tokens": int
            }
        }
        """
        pass
