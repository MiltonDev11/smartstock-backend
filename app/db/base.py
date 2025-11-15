"""Módulo `app.db.base`.

Este módulo importa todos los modelos para que SQLAlchemy pueda
registrarlos en la metadata. Se utiliza por Alembic y por la inicialización
de la base de datos.
"""
from app.models.user import User  # importa cada modelo aquí
from app.db.session import Base
from app.models.material import Material
from app.models.solicitud import Solicitud, SolicitudItem