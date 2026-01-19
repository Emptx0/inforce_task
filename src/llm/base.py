from abc import ABC, abstractmethod
from typing import List, Dict


class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> Dict:
        """
        Must return OpenAI-like response:
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
