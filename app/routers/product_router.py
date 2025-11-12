from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies.auth import get_current_token
from ..schemas import product as product_schema
from ..services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=product_schema.Product,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_token)],
)
def create_product(
    product: product_schema.ProductCreate,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.create_product(db=db, product_in=product)


@router.get(
    "/",
    response_model=List[product_schema.Product],
)
def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=200),
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
) -> List[product_schema.Product]:
    return product_service.get_products(
        db=db,
        skip=skip,
        limit=limit,
        include_inactive=include_inactive,
    )


@router.get(
    "/{product_id}",
    response_model=product_schema.Product,
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.get_product(db=db, product_id=product_id)


@router.patch(
    "/{product_id}",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
)
def update_product(
    product_id: int,
    product: product_schema.ProductUpdate,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.update_product(
        db=db,
        product_id=product_id,
        product_update=product,
    )


@router.patch(
    "/{product_id}/stock",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
)
def increase_product_stock(
    product_id: int,
    payload: product_schema.StockAdjustment,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.increase_stock(
        db=db,
        product_id=product_id,
        quantity=payload.quantity,
    )


@router.delete(
    "/{product_id}",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.deactivate_product(db=db, product_id=product_id)


@router.post(
    "/{product_id}/activate",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
)
def activate_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    return product_service.activate_product(db=db, product_id=product_id)
