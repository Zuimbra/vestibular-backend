from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.question_tag import question_tags


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    source_id: Mapped[int | None] = mapped_column(
        ForeignKey("sources.id"),
        nullable=True
    )

    area: Mapped[str] = mapped_column(String(50), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)

    statement: Mapped[str] = mapped_column(Text, nullable=False)
    alternatives: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    correct_answer: Mapped[str | None] = mapped_column(String(10), nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    difficulty: Mapped[str | None] = mapped_column(String(30), nullable=True)
    original_page: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    source = relationship("Source", back_populates="questions")

    tags = relationship(
        "Tag",
        secondary=question_tags,
        back_populates="questions"
    )

    attempts = relationship("Attempt", back_populates="question")

    review_state = relationship(
        "QuestionReviewState",
        back_populates="question",
        uselist=False
    )