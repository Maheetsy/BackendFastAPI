from collections.abc import Sequence
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas


def _get_category_or_404(db: Session, category_id: int) -> models.Category:
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


def _get_product_or_404(db: Session, product_id: int) -> models.Product:
    product = (
        db.query(models.Product)
        .options(joinedload(models.Product.category))
        .filter(models.Product.product_id == product_id)
        .first()
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {product_id} no encontrado.",
        )
    return product


def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    _get_category_or_404(db, product_in.category_id)

    db_product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=Decimal(product_in.price),
        imagen_url=str(product_in.imagen_url) if product_in.imagen_url else None,
        category_id=product_in.category_id,
        stock=0,
        active=True,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
) -> Sequence[models.Product]:
    query = db.query(models.Product).options(joinedload(models.Product.category))
    
    if not include_inactive:
        query = query.filter(models.Product.active.is_(True))
    
    query = query.offset(skip).limit(limit)
    return query.all()


def get_product(db: Session, product_id: int) -> models.Product:
    return _get_product_or_404(db, product_id)


def update_product(
    db: Session,
    product_id: int,
    product_update: schemas.ProductUpdate,
) -> models.Product:
    product = _get_product_or_404(db, product_id)

    update_data = product_update.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        _get_category_or_404(db, update_data["category_id"])

    for field, value in update_data.items():
        if field == "imagen_url" and value is not None:
            setattr(product, field, str(value))
        elif field == "price" and value is not None:
            setattr(product, field, Decimal(value))
        else:
            setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def increase_stock(db: Session, product_id: int, quantity: int) -> models.Product:
    product = _get_product_or_404(db, product_id)
    if not product.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No es posible modificar el stock de un producto inactivo.",
        )
    product.stock += quantity
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def deactivate_product(db: Session, product_id: int) -> models.Product:
    product = _get_product_or_404(db, product_id)
    if not product.active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya se encuentra inactivo.",
        )
    product.active = False
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def activate_product(db: Session, product_id: int) -> models.Product:
    product = _get_product_or_404(db, product_id)
    if product.active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya se encuentra activo.",
        )
    product.active = True
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def put_product(
    db: Session, product_id: int, product_in: schemas.ProductCreate
) -> models.Product:
    """Actualiza completamente un producto (PUT)"""
    product = _get_product_or_404(db, product_id)
    _get_category_or_404(db, product_in.category_id)

    product.name = product_in.name
    product.description = product_in.description
    product.price = Decimal(product_in.price)
    product.imagen_url = str(product_in.imagen_url) if product_in.imagen_url else None
    product.category_id = product_in.category_id

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    """Elimina físicamente un producto de la base de datos"""
    product = _get_product_or_404(db, product_id)
    db.delete(product)
    db.commit()
