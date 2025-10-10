from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    cedula: str
    nombre: str
    celular: Optional[str] = None
    correo: EmailStr
    role: str

class UserCreate(UserBase):
    cedula: str
    nombre: str
    celular: Optional[str] = None
    correo: EmailStr
    password: str   # recibimos la contraseña en texto plano
    role: str = "user"   # por defecto "user"

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
class UserResponse(BaseModel):
    id: int
    cedula: str
    nombre: str
    celular: Optional[str]
    correo: EmailStr
    role: str
    is_active: Optional[bool]
    created_at: datetime

    class Config:
        orm_mode = True
