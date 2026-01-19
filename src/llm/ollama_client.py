from src.llm.base import LLMClient

import requests


class OllamaClient(LLMClient):
    def __init__(
        self,
        model: str = "gemma3:1b",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url

    def chat(self, messages: list[dict[str, str]]) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        response_data = response.json()
        answer = response_data["message"]["content"]

        usage = self._estimate_usage(response_data)

        return {
            "content": answer,
            "usage": usage
        }

    def _estimate_usage(self, response_data: dict) -> dict[str, int]:
        usage = {
            "prompt_tokens": response_data["prompt_eval_count"],
            "completion_tokens": response_data["eval_count"],
            "total_tokens": response_data["prompt_eval_count"] + response_data["eval_count"]
        }

        return usage



def main():  # Simple test
    client = OllamaClient(model="gemma3:1b")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what REST API is in simple words. Give one short sentence answer."}
    ]

    result = client.chat(messages)

    print("=== MODEL ANSWER ===")
    print(result["content"])

    print("=== TOKEN USAGE ===")
    print(result["usage"])


if __name__ == "__main__":
    main()
