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


def get_category(db: Session, category_id: int) -> models.Category:
    category = (
        db.query(models.Category)
        .filter(models.Category.category_id == category_id)
        .first()
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {category_id} no encontrada.",
        )
    return category


def update_category(
    db: Session, category_id: int, category_update: schemas.CategoryUpdate
) -> models.Category:
    category = get_category(db, category_id)
    normalized_name = _normalize_name(category_update.name)
    
    # Verificar si existe otra categoría con el mismo nombre
    existing = (
        db.query(models.Category)
        .filter(
            models.Category.name.ilike(category_update.name),
            models.Category.category_id != category_id,
        )
        .first()
    )
    if existing is not None and _normalize_name(existing.name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{category_update.name}'.",
        )

    category.name = category_update.name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def put_category(
    db: Session, category_id: int, category_in: schemas.CategoryCreate
) -> models.Category:
    """Actualiza completamente una categoría (PUT)"""
    category = get_category(db, category_id)
    normalized_name = _normalize_name(category_in.name)
    
    # Verificar si existe otra categoría con el mismo nombre
    existing = (
        db.query(models.Category)
        .filter(
            models.Category.name.ilike(category_in.name),
            models.Category.category_id != category_id,
        )
        .first()
    )
    if existing is not None and _normalize_name(existing.name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{category_in.name}'.",
        )

    category.name = category_in.name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    """Elimina físicamente una categoría de la base de datos"""
    category = get_category(db, category_id)
    
    # Verificar si hay productos asociados
    from ..models import Product
    products_count = (
        db.query(Product)
        .filter(Product.category_id == category_id)
        .count()
    )
    if products_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar la categoría porque tiene {products_count} producto(s) asociado(s).",
        )
    
    db.delete(category)
    db.commit()
