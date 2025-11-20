from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl, condecimal, field_validator, model_validator


def _quantize_price(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nombre del producto (mínimo 3 caracteres, máximo 255)",
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Descripción del producto (máximo 2000 caracteres)",
    )
    price: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(
        ...,
        description="Precio del producto (debe ser mayor a 0, máximo 2 decimales)",
    )
    imagen_url: HttpUrl | None = Field(
        default=None, description="URL de la imagen del producto"
    )
    category_id: int = Field(
        ..., gt=0, description="ID de la categoría (debe ser un número positivo)"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError(
                "El nombre del producto debe tener al menos 3 caracteres."
            )
        if len(value) > 255:
            raise ValueError("El nombre del producto no puede exceder 255 caracteres.")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if len(value) > 2000:
                raise ValueError(
                    "La descripción no puede exceder 2000 caracteres."
                )
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return _quantize_price(value)

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("El ID de categoría debe ser un número positivo.")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Nombre del producto (mínimo 3 caracteres, máximo 255)",
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Descripción del producto (máximo 2000 caracteres)",
    )
    price: condecimal(max_digits=10, decimal_places=2, gt=0) | None = Field(
        default=None,
        description="Precio del producto (debe ser mayor a 0, máximo 2 decimales)",
    )
    imagen_url: HttpUrl | None = Field(
        default=None, description="URL de la imagen del producto"
    )
    category_id: int | None = Field(
        default=None, gt=0, description="ID de la categoría (debe ser un número positivo)"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if len(value) < 3:
                raise ValueError(
                    "El nombre del producto debe tener al menos 3 caracteres."
                )
            if len(value) > 255:
                raise ValueError(
                    "El nombre del producto no puede exceder 255 caracteres."
                )
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if len(value) > 2000:
                raise ValueError(
                    "La descripción no puede exceder 2000 caracteres."
                )
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and value <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        if value is not None:
            return _quantize_price(value)
        return value

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("El ID de categoría debe ser un número positivo.")
        return value

    @model_validator(mode="after")
    def ensure_any_field(self) -> "ProductUpdate":
        if not any(
            getattr(self, field) is not None
            for field in ("name", "description", "price", "imagen_url", "category_id")
        ):
            raise ValueError("Debe proporcionar al menos un campo para actualizar.")
        return self


class StockAdjustment(BaseModel):
    quantity: int = Field(
        ...,
        gt=0,
        description="Cantidad a agregar al stock (debe ser un número positivo)",
    )

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        return value


class Product(ProductBase):
    product_id: int
    stock: int = Field(..., ge=0, description="Stock disponible del producto")
    active: bool = Field(..., description="Estado activo/inactivo del producto")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
