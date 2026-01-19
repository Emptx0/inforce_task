from pydantic import BaseModel
from typing import List
from datetime import datetime


class MessageCreate(BaseModel):
    """
    Payload sent by the user when submitting a new message
    """
    message: str


class MessageResponse(BaseModel):
    """
    Representation of a single chat message returned by the API
    """
    role: str  # "user" or "assistant"
    content: str
    tokens: int
    cost: float
    created_at: datetime

    class Config:
        # Allows Pydantic to read data directly from SQLAlchemy ORM objects
        from_attributes = True


class ChatSessionResponse(BaseModel):
    """
    Full chat session response including message history and usage statistics
    """
    session_id: int
    total_tokens: int
    total_cost: float
    messages: List[MessageResponse]
