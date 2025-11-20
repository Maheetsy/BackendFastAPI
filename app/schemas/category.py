from pydantic import BaseModel, Field, field_validator, model_validator


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre de la categoría (mínimo 3 caracteres, máximo 100)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        if len(value) < 3:
            raise ValueError(
                "El nombre de la categoría debe tener al menos 3 caracteres."
            )
        if len(value) > 100:
            raise ValueError(
                "El nombre de la categoría no puede exceder 100 caracteres."
            )
        return value


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Nombre de la categoría (mínimo 3 caracteres, máximo 100)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("El nombre de la categoría no puede estar vacío.")
            if len(value) < 3:
                raise ValueError(
                    "El nombre de la categoría debe tener al menos 3 caracteres."
                )
            if len(value) > 100:
                raise ValueError(
                    "El nombre de la categoría no puede exceder 100 caracteres."
                )
        return value

    @model_validator(mode="after")
    def ensure_name_provided(self) -> "CategoryUpdate":
        if self.name is None:
            raise ValueError("Debe proporcionar el nombre para actualizar.")
        return self


class Category(CategoryBase):
    category_id: int

    model_config = {"from_attributes": True}