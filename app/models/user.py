from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cedula: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    celular: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    correo: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)  # admin, vendedor, trabajador
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_reset_token: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)

class UserCreate(BaseModel):
    cedula: str
    nombre: str
    celular: Optional[str]
    correo: EmailStr
    password: str
    role: str = "user"
