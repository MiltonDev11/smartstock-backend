"""Módulo `app.models.material`.

Define el modelo `Material` que representa materiales en stock, incluyendo
sus atributos principales y métodos auxiliares como `calcular_ingreso`.
"""
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Material(Base):
    __tablename__ = "materiales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    material: Mapped[str] = mapped_column(String, nullable=False)
    medida: Mapped[str] = mapped_column(String, nullable=True)
    unidad: Mapped[str] = mapped_column(String, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    marca: Mapped[str] = mapped_column(String, nullable=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    def calcular_ingreso(self):
        return self.precio_unitario * self.cantidad
