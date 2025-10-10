# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.esquemas.user import UserCreate, UserResponse
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

# Configuración para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # ✅ Verificar si el correo ya existe
    db_user = db.query(User).filter(User.correo == user.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    # ✅ Crear usuario
    hashed_password = pwd_context.hash(user.password)  # encriptamos
    new_user = User(
        cedula=user.cedula,
        nombre=user.nombre,
        celular=user.celular,
        correo=user.correo,
        password_hash=hashed_password,
        role=user.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
