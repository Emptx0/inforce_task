from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.db import SessionLocal
from src.services.chat_service import create_session, send_message
from src.schemas import MessageCreate, ChatSessionResponse
from src.db.models import ChatSession


router = APIRouter(prefix="/sessions", tags=["chat"])


# Dependency для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ChatSessionResponse)
def start_session(db: Session = Depends(get_db)):
    """
    Create new chat session
    """
    chat = create_session(db)

    return ChatSessionResponse(
        session_id=chat.id,
        total_tokens=chat.total_tokens,
        total_cost=chat.total_cost,
        messages=[]
    )


@router.post("/{session_id}/messages", response_model=ChatSessionResponse)
def send_chat_message(
    session_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Send message to chat session
    """
    try:
        chat = send_message(db, session_id, payload.message)
    except ValueError:
        raise HTTPException(status_code=404, detail="Chat session not found")

    return ChatSessionResponse(
        session_id=chat.id,
        total_tokens=chat.total_tokens,
        total_cost=chat.total_cost,
        messages=chat.messages
    )


@router.get("/{session_id}", response_model=ChatSessionResponse)
def get_chat_history(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get full chat history
    """
    chat = db.get(ChatSession, session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")

    return ChatSessionResponse(
        session_id=chat.id,
        total_tokens=chat.total_tokens,
        total_cost=chat.total_cost,
        messages=chat.messages
    )
