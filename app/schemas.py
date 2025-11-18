from pydantic import BaseModel, Field, validator
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, example="Laptop Gaming")
    precio: float = Field(
        ..., gt=0, description="Precio debe ser mayor a 0", example=999.99
    )

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None, min_length=1, max_length=100, example="Laptop Gaming Pro"
    )
    precio: Optional[float] = Field(
        None, gt=0, description="Precio debe ser mayor a 0", example=1299.99
    )

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v


class Producto(ProductoBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
