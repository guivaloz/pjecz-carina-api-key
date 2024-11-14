"""
Materias, modelos
"""

from typing import List

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Materia(Base, UniversalMixin):
    """Materia"""

    # Nombre de la tabla
    __tablename__ = "materias"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    nombre: Mapped[str] = mapped_column(String(256))
    descripcion: Mapped[str] = mapped_column(String(1024))
    en_sentencias: Mapped[bool] = mapped_column(Boolean, default=False)
    en_exh_exhortos: Mapped[bool] = mapped_column(Boolean, default=False)

    # Hijos
    autoridades: Mapped[List["Autoridad"]] = relationship("Autoridad", back_populates="materia")

    def __repr__(self):
        """Representación"""
        return f"<Materia {self.nombre}>"
