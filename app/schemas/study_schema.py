from pydantic import BaseModel, ConfigDict

from app.schemas.tag_schema import TagResponse


class StudyQuestionResponse(BaseModel):
    id: int
    area: str
    subject: str
    statement: str
    alternatives: dict | None = None
    difficulty: str | None = None
    original_page: int | None = None
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)