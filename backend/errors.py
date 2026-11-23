"""Central error handling for the API.

Every error response has the same JSON shape, so the frontend can rely on it:

    {"detail": "Human-readable message", "error_code": "MACHINE_READABLE_CODE"}

The real cause is logged on the server and never sent to the client.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg import Error as PsycopgError
from psycopg import OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("lahore_api")


def error_response(status_code: int, detail: str, error_code: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail, "error_code": error_code},
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        codes = {
            400: "BAD_REQUEST",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
        }
        return error_response(
            exc.status_code,
            str(exc.detail),
            codes.get(exc.status_code, "HTTP_ERROR"),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        problems = "; ".join(
            f"{'.'.join(str(p) for p in err['loc'][1:])}: {err['msg']}"
            for err in exc.errors()
        )
        return error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Invalid request. {problems}",
            "VALIDATION_ERROR",
        )

    @app.exception_handler(OperationalError)
    async def database_unavailable(request: Request, exc: OperationalError):
        # Connection refused, wrong password, timeout, server down...
        logger.error("Database unavailable on %s: %s", request.url.path, exc)
        return error_response(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Database is temporarily unavailable. Please try again shortly.",
            "DATABASE_UNAVAILABLE",
        )

    @app.exception_handler(PsycopgError)
    async def database_error(request: Request, exc: PsycopgError):
        # Missing table, bad SQL, constraint violation... a bug, not an outage.
        logger.exception("Database query failed on %s", request.url.path)
        return error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "A database error occurred.",
            "DATABASE_ERROR",
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s", request.url.path)
        return error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred.",
            "INTERNAL_ERROR",
        )
