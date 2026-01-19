from typing import Any

import requests


BASE_URL = "http://127.0.0.1:8000"


def start_session() -> int:
    resp = requests.post(f"{BASE_URL}/sessions")
    resp.raise_for_status()
    return resp.json()["session_id"]


def send_message(session_id: int, message: str) -> tuple:
    resp = requests.post(
        f"{BASE_URL}/sessions/{session_id}/messages",
        json={"message": message}
    )
    resp.raise_for_status()

    data = resp.json()
    return (
        data["messages"][-1]["content"],
        data["messages"][-1]["tokens"],
        data["messages"][-1]["cost"]
    )


def main():
    print("CLI Chat (type 'exit' to quit)\n")

    session_id = start_session()
    print(f"Session started: {session_id}\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        try:
            answer, tokens, cost = send_message(session_id, user_input)
            print(f"Bot: {answer}\n\n"
                  f"Tokens: {tokens}\n"
                  f"Cost: {cost}\n")
        except Exception as e:
            print("Error:", e)
            break


if __name__ == "__main__":
    main()
