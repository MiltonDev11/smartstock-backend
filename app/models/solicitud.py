"""Módulo `app.models.solicitud`.

Define los modelos `Solicitud` y `SolicitudItem` y el enum de estado
(`SolicitudStatus`) para representar solicitudes de materiales.

Incluye relaciones entre solicitudes y sus ítems, así como propiedades
útiles como `subtotal` en `SolicitudItem`.
"""
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.db.session import Base
import enum

class SolicitudStatus(str, enum.Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    completado = "completado"

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    cliente_cedula: Mapped[str] = mapped_column(
        String, ForeignKey("users.cedula"),
        nullable=False, index=True
    )

    # FECHA DE CREACIÓN → timezone-aware y usando func.now()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # FECHA DE ENTREGA (nullable)
    delivery_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[SolicitudStatus] = mapped_column(
        Enum(SolicitudStatus),
        default=SolicitudStatus.pendiente
    )

    items = relationship(
        "SolicitudItem",
        back_populates="solicitud",
        cascade="all, delete-orphan"
    )


class SolicitudItem(Base):
    __tablename__ = "solicitud_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    solicitud_id: Mapped[int] = mapped_column(Integer, ForeignKey("solicitudes.id"), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    solicitud = relationship("Solicitud", back_populates="items")

    @property
    def subtotal(self):
        return (self.precio_unitario or 0) * (self.cantidad or 0)

