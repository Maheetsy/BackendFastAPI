from pydantic import BaseModel, Field, field_validator


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        return value


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    category_id: int

    model_config = {"from_attributes": True}