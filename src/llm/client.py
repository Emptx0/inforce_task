import requests

from typing import List, Dict


class OllamaClient:
    def __init__(
        self,
        model: str = "gemma3:1b",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url

    def chat(self, messages: List[Dict[str, str]]) -> Dict:
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

        data = response.json()
        answer = data["message"]["content"]

        usage = self._estimate_usage(data)

        return {
            "content": answer,
            "usage": usage
        }

    def _estimate_usage(self, data: Dict) -> Dict[str, int]:
        usage = {
            "prompt_tokens": data["prompt_eval_count"],
            "completion_tokens": data["eval_count"],
            "total_tokens": data["prompt_eval_count"] + data["eval_count"]
        }

        return usage


def main():
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
