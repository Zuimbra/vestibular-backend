from datetime import datetime

from sqlalchemy import case, or_
from sqlalchemy.orm import Session, joinedload

from app.models.question import Question
from app.models.question_review_state import QuestionReviewState
from app.models.tag import Tag


def get_next_questions(
    db: Session,
    area: str | None = None,
    subject: str | None = None,
    tag: str | None = None,
    limit: int = 10,
) -> list[Question]:
    now = datetime.utcnow()

    query = (
        db.query(Question)
        .outerjoin(
            QuestionReviewState,
            Question.id == QuestionReviewState.question_id,
        )
        .options(joinedload(Question.tags))
    )

    if area:
        query = query.filter(Question.area == area.strip().lower())

    if subject:
        query = query.filter(Question.subject == subject.strip().lower())

    if tag:
        normalized_tag = tag.strip().lower()
        query = query.filter(Question.tags.any(Tag.name == normalized_tag))

    query = query.filter(
        or_(
            QuestionReviewState.id.is_(None),
            QuestionReviewState.next_due_at.is_(None),
            QuestionReviewState.next_due_at <= now,
        )
    )

    query = query.order_by(
        case(
            (QuestionReviewState.id.is_(None), 0),
            (QuestionReviewState.next_due_at.is_(None), 0),
            else_=1,
        ),
        QuestionReviewState.next_due_at.asc(),
        QuestionReviewState.last_answered_at.asc(),
        Question.id.asc(),
    )

    return query.limit(limit).all()