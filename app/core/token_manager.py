"""Módulo `app.core.token_manager`.

Provee utilidades para generar y verificar tokens temporales (p. ej. para
restablecimiento de contraseñas) usando `itsdangerous`.
"""
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.core.config import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


def generate_token(user_id: int) -> str:
    """Genera un token seguro que contiene el `user_id`."""
    return serializer.dumps({"user_id": user_id})


def verify_token(token: str, max_age: int = 900) -> int:
    """Verifica y decodifica un token, devolviendo el `user_id`.

    - `max_age` se expresa en segundos; por defecto 900s (15 minutos).
    - Lanza `ValueError` con mensaje en español si el token expira o es inválido.
    """
    try:
        data = serializer.loads(token, max_age=max_age)
        return data["user_id"]
    except SignatureExpired:
        raise ValueError("El enlace ha expirado.")
    except BadSignature:
        raise ValueError("Token inválido o manipulado.")