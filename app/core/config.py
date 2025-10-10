from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    FRONTEND_URL: str = ""

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: SecretStr = SecretStr("")
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = ""

    class Config:
        env_file = ".env"

settings = Settings()