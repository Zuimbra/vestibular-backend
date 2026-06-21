from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        nullable=False
    )

    selected_answer: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    confidence: Mapped[str | None] = mapped_column(String(30), nullable=True)

    answered_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    question = relationship("Question", back_populates="attempts")