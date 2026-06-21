from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.question_review_state import QuestionReviewState


def calculate_next_due_at(is_correct: bool, confidence: str | None) -> datetime:
    now = datetime.utcnow()

    if not is_correct:
        return now + timedelta(days=1)

    if confidence == "low":
        return now + timedelta(days=2)

    if confidence == "medium":
        return now + timedelta(days=5)

    if confidence == "high":
        return now + timedelta(days=10)

    return now + timedelta(days=3)


def update_review_state(
    db: Session,
    question_id: int,
    is_correct: bool,
    answered_at: datetime,
    confidence: str | None,
) -> QuestionReviewState:
    review_state = (
        db.query(QuestionReviewState)
        .filter(QuestionReviewState.question_id == question_id)
        .first()
    )

    if not review_state:
        review_state = QuestionReviewState(
            question_id=question_id,
            times_answered=0,
            times_correct=0,
            times_wrong=0,
        )

        db.add(review_state)

    review_state.last_answered_at = answered_at
    review_state.times_answered += 1

    if is_correct:
        review_state.times_correct += 1
    else:
        review_state.times_wrong += 1

    review_state.next_due_at = calculate_next_due_at(
        is_correct=is_correct,
        confidence=confidence,
    )

    return review_state