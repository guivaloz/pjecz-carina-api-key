"""
Exh Exhortos v4, esquemas de pydantic
"""

from pydantic import BaseModel

from ..dependencies.schemas_base import OneBaseOut
from .exh_exhortos_archivos import ExhExhortoArchivoItem
from .exh_exhortos_partes import ExhExhortoParteItem
from .exh_exhortos_videos import ExhExhortoVideoItem


class ExhExhortoIn(BaseModel):
    """Esquema para recibir un exhorto"""

    exhortoOrigenId: str
    municipioDestinoId: int
    materiaClave: str
    estadoOrigenId: int
    municipioOrigenId: int
    juzgadoOrigenId: str | None
    juzgadoOrigenNombre: str
    numeroExpedienteOrigen: str
    numeroOficioOrigen: str | None
    tipoJuicioAsuntoDelitos: str
    juezExhortante: str | None
    partes: list[ExhExhortoParteItem] | None
    fojas: int
    diasResponder: int
    tipoDiligenciacionNombre: str | None
    fechaOrigen: str | None  # YYYY-MM-DD HH:mm:ss
    observaciones: str | None
    archivos: list[ExhExhortoArchivoItem]


class ExhExhortoOut(BaseModel):
    """Esquema para confirmar la recepción de un exhorto"""

    exhortoOrigenId: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoOut(OneBaseOut):
    """Esquema para entregar una confirmación de la recepción de un exhorto"""

    data: ExhExhortoOut | None = None


class ExhExhortoConsultaOut(ExhExhortoIn):
    """Esquema para consultar un exhorto"""

    folioSeguimiento: str
    estadoDestinoId: int
    estadoDestinoNombre: str
    municipioDestinoNombre: str
    materiaNombre: str
    estadoOrigenNombre: str
    municipioOrigenNombre: str
    fechaHoraRecepcion: str  # YYYY-MM-DD HH:mm:ss
    municipioTurnadoId: int
    municipioTurnadoNombre: str
    areaTurnadoId: str
    areaTurnadoNombre: str
    numeroExhorto: str
    urlInfo: str
    respuestaOrigenId: str


class OneExhExhortoConsultaOut(OneBaseOut):
    """Esquema para entregar la consulta de un exhorto"""

    data: ExhExhortoConsultaOut | None = None


class ExhExhortoRespuestaIn(BaseModel):
    """Esquema para recibir la respuesta"""

    exhortoId: str
    respuestaOrigenId: str
    municipioTurnadoId: int
    areaTurnadoId: str | None
    areaTurnadoNombre: str
    numeroExhorto: str | None
    tipoDiligenciado: int  # 0 = No Diligenciado, 1 = Parcialmente Dilgenciado, 2 = Diligenciado
    observaciones: str | None
    archivos: list[ExhExhortoArchivoItem]
    videos: list[ExhExhortoVideoItem] | None


class ExhExhortoRespuestaOut(BaseModel):
    """Esquema para confirmar la recepción de la respuesta"""

    exhortoId: str
    respuestaOrigenId: str
    fechaHora: str  # YYYY-MM-DD HH:mm:ss


class OneExhExhortoRespuestaOut(OneBaseOut):
    """Esquema para entregar la confirmación de la recepción de la respuesta"""

    data: ExhExhortoRespuestaOut | None = None
