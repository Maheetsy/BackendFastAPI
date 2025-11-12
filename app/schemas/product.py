from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl, condecimal, field_validator, model_validator


def _quantize_price(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    price: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(...)
    imagen_url: HttpUrl | None = None
    category_id: int = Field(..., gt=0)

    @field_validator("name")
    @classmethod
    def trim_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("description")
    @classmethod
    def trim_description(cls, value: str | None) -> str | None:
        return value.strip() if value else value

    @field_validator("price")
    @classmethod
    def normalize_price(cls, value: Decimal) -> Decimal:
        return _quantize_price(value)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    price: condecimal(max_digits=10, decimal_places=2, gt=0) | None = None
    imagen_url: HttpUrl | None = None
    category_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def ensure_any_field(self) -> "ProductUpdate":
        if not any(
            getattr(self, field) is not None
            for field in ("name", "description", "price", "imagen_url", "category_id")
        ):
            raise ValueError("Debe proporcionar al menos un dato para actualizar.")
        return self


class StockAdjustment(BaseModel):
    quantity: int = Field(..., gt=0, description="Cantidad a agregar al stock")


class Product(ProductBase):
    product_id: int
    stock: int
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
