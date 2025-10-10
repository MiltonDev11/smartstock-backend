from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    celular = Column(String, nullable=True)
    correo = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, vendedor, trabajador
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserCreate(BaseModel):
    cedula: str
    nombre: str
    celular: Optional[str]
    correo: EmailStr
    password: str
    role: str = "user"
