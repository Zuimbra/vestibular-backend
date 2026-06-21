from sqlalchemy.orm import Session

from app.models.question import Question
from app.schemas.question_schema import QuestionCreate, QuestionUpdate


def create_question(db: Session, question_data: QuestionCreate) -> Question:
    question = Question(**question_data.model_dump())

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def get_questions(db: Session) -> list[Question]:
    return db.query(Question).order_by(Question.id.desc()).all()


def get_question_by_id(db: Session, question_id: int) -> Question | None:
    return db.query(Question).filter(Question.id == question_id).first()


def update_question(
    db: Session,
    question: Question,
    question_data: QuestionUpdate,
) -> Question:
    update_data = question_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)

    return question


def delete_question(db: Session, question: Question) -> None:
    db.delete(question)
    db.commit()