"""
Materias, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_list import CustomList
from ..dependencies.safe_string import safe_clave
from ..models.materias import Materia
from ..models.permisos import Permiso
from ..schemas.materias import MateriaOut, OneMateriaOut

materias = APIRouter(prefix="/api/v5/materias")


@materias.get("/{clave}", response_model=OneMateriaOut)
async def detalle_materia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una materia a partir de su clave"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        materia = database.query(Materia).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneMateriaOut(success=False, message="No existe esa materia", errors=[str(error)])
    if materia.estatus != "A":
        message = "No está activa esa materia, está eliminada"
        return OneMateriaOut(success=False, message=message, errors=[message])
    if materia.en_exh_exhortos is False:
        message = "No está habilitada esa materia para exhortos"
        return OneMateriaOut(success=False, message=message, errors=[message])
    return OneMateriaOut(success=True, message=f"Detalle de {clave}", data=MateriaOut.model_validate(materia))


@materias.get("", response_model=CustomList[MateriaOut])
async def listado_materias(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Listado de materias"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Materia).filter_by(en_exh_exhortos=True).filter_by(estatus="A").order_by(Materia.nombre))
