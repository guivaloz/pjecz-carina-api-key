"""
Oficinas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int | None = None
    clave: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneOficinaOut(OneBaseOut):
    """Esquema para entregar un oficina"""

    data: OficinaOut | None = None
