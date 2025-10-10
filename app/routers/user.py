from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.esquemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password
from app.db.session import get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validar que no exista el correo o cédula
    existing_user = db.query(User).filter((User.correo == user.correo) | (User.cedula == user.cedula)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe con ese correo o cédula")

    # Crear nuevo usuario
    new_user = User(
        cedula=user.cedula,
        nombre=user.nombre,
        celular=user.celular,
        correo=user.correo,
        password_hash=hash_password(user.password),
        role=user.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Usuario registrado con éxito", "user_id": new_user.id}
