from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class QuestionReviewState(Base):
    __tablename__ = "question_review_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        unique=True,
        nullable=False
    )

    last_answered_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    times_answered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    times_correct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    times_wrong: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    next_due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    question = relationship("Question", back_populates="review_state")