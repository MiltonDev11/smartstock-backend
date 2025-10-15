from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.core.config import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generate_token(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})

def verify_token(token: str, max_age: int = 900) -> int:
    try:
        data = serializer.loads(token, max_age=max_age)
        return data["user_id"]
    except SignatureExpired:
        raise ValueError("El enlace ha expirado.")
    except BadSignature:
        raise ValueError("Token inválido o manipulado.")