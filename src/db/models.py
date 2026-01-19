from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone


Base = declarative_base()


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    role = Column(String(20))  # user / assistant
    content = Column(Text)

    tokens = Column(Integer)
    cost = Column(Float)

    session = relationship("ChatSession", back_populates="messages")
