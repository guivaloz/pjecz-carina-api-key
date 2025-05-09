"""
Exh Exhortos Partes, esquemas de pydantic
"""

from pydantic import BaseModel


class ExhExhortoParteItem(BaseModel):
    """Esquema para recibir los metadatos de una parte"""

    nombre: str
    apellidoPaterno: str | None
    apellidoMaterno: str | None
    genero: str | None
    esPersonaMoral: bool
    tipoParte: int
    tipoParteNombre: str | None
    correoElectronico: str | None  # Agregado en 2023-02
    telefono: str | None  # Agregado en 2023-02
