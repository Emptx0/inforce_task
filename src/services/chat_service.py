from sqlalchemy.orm import Session

from src.db.models import ChatSession, Message
from src.llm import get_llm_client


llm_client = get_llm_client()


def create_session(db: Session) -> ChatSession:
    """
    Create new chat session
    """
    session = ChatSession()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def send_message(
    db: Session,
    session_id: int,
    user_message: str
) -> ChatSession:
    """
    Save user message, generate model response,
    update token usage and cost
    """
    chat = db.get(ChatSession, session_id)
    if not chat:
        raise ValueError("Chat session not found")

    # Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message,
        tokens=0,
        cost=0.0
    )
    db.add(user_msg)
    db.commit()

    # Prepare full conversation history
    messages = [
        {"role": m.role, "content": m.content}
        for m in chat.messages
    ] + [{"role": "user", "content": user_message}]

    # Call LLM
    llm_response = llm_client.chat(messages)
    usage = llm_response["usage"]

    total_tokens = usage["total_tokens"]
    total_cost = total_tokens

    # Save assistant message
    assistant_msg = Message(
        session_id=session_id,
        role="assistant",
        content=llm_response["content"],
        tokens=total_tokens,
        cost=total_cost
    )

    # Update session stats
    chat.total_tokens += total_tokens
    chat.total_cost += total_cost

    db.add(assistant_msg)
    db.commit()
    db.refresh(chat)

    return chat
