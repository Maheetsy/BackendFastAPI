from typing import List

from fastapi import APIRouter, Depends, Path, Query, status
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
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto. Requiere autenticación. El stock se inicializa en 0.",
)
def create_product(
    product: product_schema.ProductCreate,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Crea un nuevo producto"""
    return product_service.create_product(db=db, product_in=product)


@router.get(
    "/",
    response_model=List[product_schema.Product],
    summary="Obtener todos los productos",
    description="Obtiene una lista de productos con paginación. Por defecto solo muestra productos activos.",
)
def read_products(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, gt=0, le=200, description="Número máximo de registros a retornar"),
    include_inactive: bool = Query(
        False, description="Incluir productos inactivos en los resultados"
    ),
    db: Session = Depends(get_db),
) -> List[product_schema.Product]:
    """Obtiene todos los productos"""
    return product_service.get_products(
        db=db,
        skip=skip,
        limit=limit,
        include_inactive=include_inactive,
    )


@router.get(
    "/{product_id}",
    response_model=product_schema.Product,
    summary="Obtener un producto por ID",
    description="Obtiene los detalles de un producto específico por su ID.",
)
def read_product(
    product_id: int = Path(..., gt=0, description="ID del producto"),
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Obtiene un producto por su ID"""
    return product_service.get_product(db=db, product_id=product_id)


@router.put(
    "/{product_id}",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
    summary="Actualizar completamente un producto (PUT)",
    description="Actualiza todos los campos de un producto. Requiere autenticación.",
)
def put_product(
    product_id: int,
    product: product_schema.ProductCreate,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Actualiza completamente un producto (PUT)"""
    return product_service.put_product(
        db=db,
        product_id=product_id,
        product_in=product,
    )


@router.patch(
    "/{product_id}",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
    summary="Actualizar parcialmente un producto (PATCH)",
    description="Actualiza solo los campos proporcionados de un producto. Requiere autenticación.",
)
def update_product(
    product_id: int,
    product: product_schema.ProductUpdate,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Actualiza parcialmente un producto (PATCH)"""
    return product_service.update_product(
        db=db,
        product_id=product_id,
        product_update=product,
    )


@router.patch(
    "/{product_id}/stock",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
    summary="Aumentar el stock de un producto",
    description="Aumenta el stock de un producto agregando la cantidad especificada. Requiere autenticación.",
)
def increase_product_stock(
    product_id: int,
    payload: product_schema.StockAdjustment,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Aumenta el stock de un producto"""
    return product_service.increase_stock(
        db=db,
        product_id=product_id,
        quantity=payload.quantity,
    )


@router.patch(
    "/{product_id}/deactivate",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
    summary="Desactivar un producto (soft delete)",
    description="Desactiva un producto sin eliminarlo físicamente. Requiere autenticación.",
)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Desactiva un producto (soft delete)"""
    return product_service.deactivate_product(db=db, product_id=product_id)


@router.post(
    "/{product_id}/activate",
    response_model=product_schema.Product,
    dependencies=[Depends(get_current_token)],
    summary="Activar un producto",
    description="Activa un producto previamente desactivado. Requiere autenticación.",
)
def activate_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> product_schema.Product:
    """Activa un producto"""
    return product_service.activate_product(db=db, product_id=product_id)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_token)],
    summary="Eliminar físicamente un producto (DELETE)",
    description="Elimina permanentemente un producto de la base de datos. Requiere autenticación.",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Elimina físicamente un producto"""
    product_service.delete_product(db=db, product_id=product_id)
