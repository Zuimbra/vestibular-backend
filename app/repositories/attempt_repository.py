from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.question import Question
from app.models.question_review_state import QuestionReviewState
from app.services.review_service import update_review_state


def normalize_answer(answer: str | None) -> str | None:
    if answer is None:
        return None

    return answer.strip().upper()


def check_answer(question: Question, selected_answer: str | None) -> bool:
    normalized_selected = normalize_answer(selected_answer)
    normalized_correct = normalize_answer(question.correct_answer)

    if normalized_selected is None:
        return False

    if normalized_correct is None:
        return False

    return normalized_selected == normalized_correct


def create_attempt_and_update_review(
    db: Session,
    question: Question,
    selected_answer: str | None,
    confidence: str | None,
) -> tuple[Attempt, QuestionReviewState]:
    answered_at = datetime.utcnow()

    is_correct = check_answer(
        question=question,
        selected_answer=selected_answer,
    )

    attempt = Attempt(
        question_id=question.id,
        selected_answer=normalize_answer(selected_answer),
        is_correct=is_correct,
        confidence=confidence,
        answered_at=answered_at,
    )

    db.add(attempt)

    review_state = update_review_state(
        db=db,
        question_id=question.id,
        is_correct=is_correct,
        answered_at=answered_at,
        confidence=confidence,
    )

    db.commit()
    db.refresh(attempt)
    db.refresh(review_state)

    return attempt, review_state