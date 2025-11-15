"""Módulo `app.core.security`.

Provee utilidades para hashing y verificación de contraseñas usando
`passlib`. Las funciones expuestas son `hash_password` y `verify_password`.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Devuelve el hash seguro de la contraseña proporcionada."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincida con un hash."""
    return pwd_context.verify(plain_password, hashed_password)