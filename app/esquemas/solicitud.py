# app/esquemas/solicitud.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ItemCreate(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float

class SolicitudCreate(BaseModel):
    cliente_cedula: str
    items: List[ItemCreate]

class ItemOut(BaseModel):
    id: int
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        orm_mode = True

class SolicitudOut(BaseModel):
    id: int
    cliente_cedula: str
    created_at: datetime
    delivery_date: Optional[datetime]
    status: str
    items: List[ItemOut]

    class Config:
        orm_mode = True
