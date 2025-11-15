"""Módulo `app.api.admin_users`.

Provee endpoints que permiten al administrador crear usuarios (vendedores)
y enviarles credenciales por correo. Incluye utilidades para generar
contraseñas seguras.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password
from app.core.email_config import conf   # tu conf de FastMail
from fastapi_mail import FastMail, MessageSchema
from fastapi_mail import MessageType
import secrets
import string
from typing import Optional

router = APIRouter(prefix="/admin", tags=["AdminUsers"])

# Pydantic schema para la petición (solo los campos que el admin envía)
class AdminCreateUserIn(BaseModel):
    nombre: str = Field(..., min_length=1)
    cedula: str = Field(..., min_length=4)
    celular: Optional[str] = Field(None, min_length=7)
    correo: EmailStr

def generate_random_password(length: int = 10) -> str:
    # caracteres seguros, evita símbolos problemáticos
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@router.post("/register-user")
async def register_user_admin(payload: AdminCreateUserIn, db: Session = Depends(get_db)):
    # 1) Validaciones: cedula o correo duplicados
    existing = db.query(User).filter((User.cedula == payload.cedula) | (User.correo == payload.correo)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con esa cédula o correo.")

    # 2) Generar contraseña y hashearla
    password_plain = generate_random_password(10)  # máximo 10 caracteres
    password_hashed = hash_password(password_plain)

    # 3) Crear usuario con role 'vendedor'
    new_user = User(
        cedula = payload.cedula,
        nombre = payload.nombre,
        celular = payload.celular,
        correo = str(payload.correo),
        password_hash = password_hashed,
        role = "vendedor",
        is_active = True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4) Enviar correo al usuario con la contraseña (HTML)
    fm = FastMail(conf)
    censurado = (
        lambda email: f"{email.split('@')[0][:3]}***@***{email.split('@')[1][-4:]}"
    )(payload.correo)

    message = MessageSchema(
        subject="Bienvenido a SmartStock — tus credenciales",
        recipients=[str(payload.correo)],
        body=f"""
            <p>Hola {payload.nombre},</p>
            <p>Has sido registrado en la plataforma SmartStock como <strong>vendedor</strong>.</p>
            <p>Tu contraseña temporal es: <strong>{password_plain}</strong></p>
            <p>Por seguridad, al iniciar sesión podrás cambiarla desde tu perfil.</p>
            <hr>
            <p>Si no solicitaste este acceso, informa al administrador.</p>
        """,
        subtype=MessageType.html
    )
    try:
        await fm.send_message(message)
    except Exception as e:
        # Si falla el envío, podrías borrar el usuario o marcarlo con is_active=False.
        # Aquí devolvemos el error al frontend para que el admin lo vea.
        raise HTTPException(status_code=500, detail=f"Error al enviar correo: {str(e)}")

    # 5) Respuesta al admin (incluimos email censurado para mostrar)
    return {"msg": "Usuario creado y correo enviado", "user_id": new_user.id, "correo": censurado}
