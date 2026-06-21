from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tag import Tag
from app.repositories.tag_repository import get_or_create_tag, get_tags
from app.schemas.tag_schema import TagCreate, TagResponse


router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("", response_model=list[TagResponse])
def list_all(db: Session = Depends(get_db)):
    return get_tags(db)


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(payload: TagCreate, db: Session = Depends(get_db)):
    return get_or_create_tag(db, payload.name)