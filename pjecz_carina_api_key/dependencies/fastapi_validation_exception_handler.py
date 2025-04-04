"""
FastAPI Validation Exception Handler
"""

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador de excepciones de validación"""
    errors = list()
    payload = {
        "success": False,
        "message": "Error de validación",
        "errors": errors,
        "data": None,
    }
    return JSONResponse(
        content=jsonable_encoder(payload),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
