from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttemptCreate(BaseModel):
    question_id: int
    selected_answer: str | None = None
    confidence: str | None = None


class AttemptResponse(BaseModel):
    id: int
    question_id: int
    selected_answer: str | None
    is_correct: bool
    confidence: str | None
    answered_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttemptFeedbackResponse(BaseModel):
    attempt: AttemptResponse
    correct_answer: str | None
    explanation: str | None
    next_due_at: datetime | None