from typing import List

from fastapi import APIRouter, Depends, Query, status
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
)
def create_category(
    category: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
) -> category_schema.Category:
    return category_service.create_category(db=db, category=category)


@router.get(
    "/",
    response_model=List[category_schema.Category],
)
def read_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=200),
    db: Session = Depends(get_db),
) -> List[category_schema.Category]:
    return category_service.get_categories(db=db, skip=skip, limit=limit)
