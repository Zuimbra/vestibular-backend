from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.attempt_repository import create_attempt_and_update_review
from app.repositories.question_repository import get_question_by_id
from app.schemas.attempt_schema import AttemptCreate, AttemptFeedbackResponse


router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"],
)


@router.post(
    "",
    response_model=AttemptFeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_attempt(
    payload: AttemptCreate,
    db: Session = Depends(get_db),
):
    question = get_question_by_id(db, payload.question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    attempt, review_state = create_attempt_and_update_review(
        db=db,
        question=question,
        selected_answer=payload.selected_answer,
        confidence=payload.confidence,
    )

    return {
        "attempt": attempt,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "next_due_at": review_state.next_due_at,
    }