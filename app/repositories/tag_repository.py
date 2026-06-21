from sqlalchemy.orm import Session

from app.models.tag import Tag


def get_tags(db: Session) -> list[Tag]:
    return db.query(Tag).order_by(Tag.name.asc()).all()


def get_tag_by_name(db: Session, name: str) -> Tag | None:
    return db.query(Tag).filter(Tag.name == name).first()


def get_or_create_tag(db: Session, name: str) -> Tag:
    normalized_name = name.strip().lower()

    tag = get_tag_by_name(db, normalized_name)

    if tag:
        return tag

    tag = Tag(name=normalized_name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag