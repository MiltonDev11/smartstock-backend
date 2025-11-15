"""Módulo `app.db.session`.

Configura la conexión a la base de datos SQLAlchemy y provee
la fábrica de sesiones `SessionLocal` y una dependencia `get_db`.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Provee una sesión de base de datos para usar como dependencia en rutas.

    La sesión se cierra automáticamente en el bloque `finally`.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()