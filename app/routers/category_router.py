from typing import List

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies.auth import get_current_token
from ..schemas import category as category_schema
from ..services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "/",
    response_model=category_schema.Category,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_token)],
    summary="Crear una nueva categoría",
    description="Crea una nueva categoría. Requiere autenticación. El nombre debe ser único.",
)
def create_category(
    category: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
) -> category_schema.Category:
    """Crea una nueva categoría"""
    return category_service.create_category(db=db, category=category)


@router.get(
    "/",
    response_model=List[category_schema.Category],
    summary="Obtener todas las categorías",
    description="Obtiene una lista de categorías con paginación, ordenadas por nombre.",
)
def read_categories(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, gt=0, le=200, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db),
) -> List[category_schema.Category]:
    """Obtiene todas las categorías"""
    return category_service.get_categories(db=db, skip=skip, limit=limit)


@router.get(
    "/{category_id}",
    response_model=category_schema.Category,
    summary="Obtener una categoría por ID",
    description="Obtiene los detalles de una categoría específica por su ID.",
)
def read_category(
    category_id: int = Path(..., gt=0, description="ID de la categoría"),
    db: Session = Depends(get_db),
) -> category_schema.Category:
    """Obtiene una categoría por su ID"""
    return category_service.get_category(db=db, category_id=category_id)


@router.put(
    "/{category_id}",
    response_model=category_schema.Category,
    dependencies=[Depends(get_current_token)],
    summary="Actualizar completamente una categoría (PUT)",
    description="Actualiza todos los campos de una categoría. Requiere autenticación.",
)
def put_category(
    category_id: int,
    category: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
) -> category_schema.Category:
    """Actualiza completamente una categoría (PUT)"""
    return category_service.put_category(
        db=db,
        category_id=category_id,
        category_in=category,
    )


@router.patch(
    "/{category_id}",
    response_model=category_schema.Category,
    dependencies=[Depends(get_current_token)],
    summary="Actualizar parcialmente una categoría (PATCH)",
    description="Actualiza solo los campos proporcionados de una categoría. Requiere autenticación.",
)
def update_category(
    category_id: int,
    category: category_schema.CategoryUpdate,
    db: Session = Depends(get_db),
) -> category_schema.Category:
    """Actualiza parcialmente una categoría (PATCH)"""
    return category_service.update_category(
        db=db,
        category_id=category_id,
        category_update=category,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_token)],
    summary="Eliminar físicamente una categoría (DELETE)",
    description="Elimina permanentemente una categoría de la base de datos. No se puede eliminar si tiene productos asociados. Requiere autenticación.",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Elimina físicamente una categoría"""
    category_service.delete_category(db=db, category_id=category_id)
