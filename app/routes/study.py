from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.study_repository import get_next_questions
from app.schemas.study_schema import StudyQuestionResponse


router = APIRouter(
    prefix="/study",
    tags=["Study"],
)


@router.get("/next", response_model=list[StudyQuestionResponse])
def next_questions(
    area: str | None = None,
    subject: str | None = None,
    tag: str | None = None,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return get_next_questions(
        db=db,
        area=area,
        subject=subject,
        tag=tag,
        limit=limit,
    )