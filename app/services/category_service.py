from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas


def _normalize_name(name: str) -> str:
    return name.strip().lower()


def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    normalized_name = _normalize_name(category.name)
    existing = (
        db.query(models.Category)
        .filter(models.Category.name.ilike(category.name))
        .first()
    )
    if existing is not None and _normalize_name(existing.name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{category.name}'.",
        )

    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Category]:
    return (
        db.query(models.Category)
        .order_by(models.Category.name.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
