"""Módulo `app.esquemas.material`.

Esquemas Pydantic para crear y representar materiales (entrada y salida).
"""
from pydantic import BaseModel

class MaterialCreate(BaseModel):
    material: str
    medida: str | None = None
    unidad: str | None = None
    precio_unitario: float
    marca: str | None = None
    cantidad: int

class MaterialOut(BaseModel):
    id: int
    material: str
    medida: str | None
    unidad: str | None
    precio_unitario: float
    marca: str | None
    cantidad: int
    ingreso: float

    class Config:
        orm_mode = True
