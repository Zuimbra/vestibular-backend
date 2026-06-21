from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.question import Question
from app.repositories.question_repository import (
    create_question,
    delete_question,
    get_question_by_id,
    get_questions,
    update_question,
)
from app.repositories.tag_repository import get_or_create_tag
from app.schemas.question_schema import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)
from app.schemas.tag_schema import QuestionTagsUpdate, TagResponse


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(question_data: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, question_data)


@router.get("", response_model=list[QuestionResponse])
def list_all(db: Session = Depends(get_db)):
    return get_questions(db)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_by_id(question_id: int, db: Session = Depends(get_db)):
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    return question


@router.patch("/{question_id}", response_model=QuestionResponse)
def update(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
):
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    return update_question(db, question, question_data)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(question_id: int, db: Session = Depends(get_db)):
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    delete_question(db, question)

    return None


@router.post("/{question_id}/tags", response_model=list[TagResponse])
def update_question_tags(
    question_id: int,
    payload: QuestionTagsUpdate,
    db: Session = Depends(get_db),
):
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    tags = [get_or_create_tag(db, tag_name) for tag_name in payload.tags]

    question.tags = tags

    db.commit()
    db.refresh(question)

    return question.tags