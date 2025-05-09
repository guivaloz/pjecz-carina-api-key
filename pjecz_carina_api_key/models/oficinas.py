"""
Oficinas, modelos
"""

from datetime import time
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Oficina(Base, UniversalMixin):
    """Oficina"""

    TIPOS = {
        "NO DEFINIDO": "NO DEFINIDO",
        "O.J. DE 1RA. INSTANCIA": "O.J. DE 1RA. INSTANCIA",
        "O.J. DE 2DA. INSTANCIA": "O.J. DE 2DA. INSTANCIA",
        "ADMINISTRATICO Y/O U. ADMIN.": "ADMINISTRATICO Y/O U. ADMIN.",
    }

    # Nombre de la tabla
    __tablename__ = "oficinas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Claves foráneas
    distrito_id: Mapped[int] = mapped_column(ForeignKey("distritos.id"))
    distrito: Mapped["Distrito"] = relationship(back_populates="oficinas")
    domicilio_id: Mapped[int] = mapped_column(ForeignKey("domicilios.id"))
    domicilio: Mapped["Domicilio"] = relationship(back_populates="oficinas")

    # Columnas
    clave: Mapped[str] = mapped_column(String(32), unique=True)
    descripcion: Mapped[str] = mapped_column(String(512))
    descripcion_corta: Mapped[str] = mapped_column(String(64))
    es_jurisdiccional: Mapped[bool] = mapped_column(default=False)
    apertura: Mapped[time]
    cierre: Mapped[time]
    limite_personas: Mapped[int]
    telefono: Mapped[str] = mapped_column(String(48))
    extension: Mapped[str] = mapped_column(String(24))

    # Hijos
    usuarios: Mapped[List["Usuario"]] = relationship("Usuario", back_populates="oficina")

    def __repr__(self):
        """Representación"""
        return f"<Oficina {self.id}>"
