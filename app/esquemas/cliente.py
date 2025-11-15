"""Módulo `app.esquemas.cliente`.

Define esquemas Pydantic para representar datos de clientes usados en la API.
"""
from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    cedula: str
    celular: str | None = None
    correo: EmailStr
