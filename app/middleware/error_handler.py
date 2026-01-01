"""
Middleware global para tratamento consistente de erros.
Captura exceções não tratadas e formata respostas padronizadas.
"""

import logging
import traceback
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from app.exceptions import BaseAPIException, DatabaseException

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware que captura todas as exceções e retorna respostas formatadas.

    Hierarquia de tratamento:
    1. BaseAPIException (nossas exceções customizadas)
    2. ValidationError (Pydantic)
    3. SQLAlchemyError (erros de banco)
    4. Exception (qualquer outro erro)
    """
    try:
        response = await call_next(request)
        return response

    except BaseAPIException as exc:
        # Nossas exceções customizadas já estão formatadas
        logger.warning(
            f"API Exception: {exc.error_code} - {exc.detail}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_code": exc.error_code
            }
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    except ValidationError as exc:
        # Erros de validação do Pydantic
        logger.warning(
            f"Validation Error: {str(exc)}",
            extra={"path": request.url.path, "method": request.method}
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Dados de entrada inválidos.",
                "error_code": "VALIDATION_ERROR",
                "extra": {"errors": exc.errors()}
            }
        )

    except IntegrityError as exc:
        # Violação de constraints do banco (FK, unique, etc)
        logger.error(
            f"Database Integrity Error: {str(exc.orig)}",
            extra={"path": request.url.path, "method": request.method}
        )

        # Tenta identificar o tipo de violação
        error_msg = str(exc.orig).lower()
        if "foreign key" in error_msg:
            detail = "Referência inválida: o recurso relacionado não existe."
            error_code = "FOREIGN_KEY_VIOLATION"
        elif "unique" in error_msg or "duplicate" in error_msg:
            detail = "Já existe um registro com estes dados."
            error_code = "DUPLICATE_ENTRY"
        else:
            detail = "Violação de restrição do banco de dados."
            error_code = "INTEGRITY_ERROR"

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": detail,
                "error_code": error_code,
                "extra": {}
            }
        )

    except SQLAlchemyError as exc:
        # Outros erros do SQLAlchemy
        logger.error(
            f"Database Error: {str(exc)}",
            extra={"path": request.url.path, "method": request.method}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao acessar o banco de dados.",
                "error_code": "DATABASE_ERROR",
                "extra": {}
            }
        )

    except Exception as exc:
        # Qualquer outro erro não previsto
        logger.critical(
            f"Unhandled Exception: {str(exc)}\n{traceback.format_exc()}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "exception_type": type(exc).__name__
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro interno do servidor. Nossa equipe foi notificada.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "extra": {"type": type(exc).__name__}
            }
        )


def setup_error_handlers(app):
    """
    Configura handlers de erro específicos para a aplicação FastAPI.
    """
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handler específico para erros de validação do FastAPI."""
        logger.warning(
            f"Request Validation Error: {exc.errors()}",
            extra={"path": request.url.path, "method": request.method}
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Dados da requisição inválidos.",
                "error_code": "REQUEST_VALIDATION_ERROR",
                "extra": {"errors": exc.errors()}
            }
        )

    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        """Handler para nossas exceções customizadas."""
        logger.warning(
            f"API Exception: {exc.error_code}",
            extra={
                "path": request.url.path,
                "error_code": exc.error_code
            }
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )