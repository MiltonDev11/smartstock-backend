"""Módulo `app.api.users`.

Contiene las rutas (endpoints) relacionadas con la gestión de usuarios:
- crear usuarios
- solicitudes de restablecimiento de contraseña

Este módulo documenta de forma concisa la intención de cada función y mantiene
comentarios en español coherentes con el estilo usado en `app/main.py`.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.esquemas.user import UserCreate, UserResponse
from passlib.context import CryptContext
from fastapi import Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Configuración para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    - Verifica si el correo ya está registrado y lanza un `HTTPException` si es así.
    - Hashea la contraseña y guarda el nuevo usuario en la DB.
    """
    # Verificar si el correo ya existe
    db_user = db.query(User).filter(User.correo == user.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    # Crear usuario
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

@router.post("/password-reset/request", response_class=HTMLResponse)
def request_password_reset(cedula: str = Form(...), db: Session = Depends(get_db)):
    """
    Solicita el restablecimiento de contraseña para un usuario identificado por su cédula.

    - Si el usuario existe, simula el envío de un correo y devuelve HTML informativo.
    - Si no existe, devuelve un HTML con mensaje de error.
    """
    user = db.query(User).filter(User.cedula == cedula).first()

    if user:
        # Simulamos envío de correo y respuesta HTML
        correo_oculto = user.correo[:3] + "***@" + user.correo.split("@")[1]
        return f"""
        <div style='background-color: #d1e7dd; color: #0f5132; padding: 10px; border-radius: 6px; text-align: center;'>
            Mensaje enviado. La validación fue enviada con éxito.<br>
            Revisa el correo: {correo_oculto}
        </div>
        """
    else:
        return """
        <div style='background-color: #f8d7da; color: #842029; padding: 10px; border-radius: 6px; text-align: center;'>
            Lo siento, no existe un usuario registrado con esa cédula.
        </div>
        """