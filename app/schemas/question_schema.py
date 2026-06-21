from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    area: str
    subject: str
    statement: str
    alternatives: dict | None = None
    correct_answer: str | None = None
    explanation: str | None = None
    difficulty: str | None = None
    original_page: int | None = None
    source_id: int | None = None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    area: str | None = None
    subject: str | None = None
    statement: str | None = None
    alternatives: dict | None = None
    correct_answer: str | None = None
    explanation: str | None = None
    difficulty: str | None = None
    original_page: int | None = None
    source_id: int | None = None


class QuestionResponse(QuestionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)