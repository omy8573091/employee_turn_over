"""
Global exception handlers for the FastAPI application.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions.custom_exceptions import (
    EmployeeTurnoverException,
    DataValidationError,
    ModelNotFoundError,
    PredictionError,
    DataProcessingError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def employee_turnover_exception_handler(request: Request, exc: EmployeeTurnoverException):
    """Handle custom application exceptions."""
    logger.error(f"Employee turnover exception: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Application Error",
            "message": str(exc),
            "type": exc.__class__.__name__
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors()
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette HTTP exceptions."""
    logger.error(f"Starlette HTTP exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "type": exc.__class__.__name__
        }
    )


# Exception handler mapping
exception_handlers = {
    EmployeeTurnoverException: employee_turnover_exception_handler,
    DataValidationError: employee_turnover_exception_handler,
    ModelNotFoundError: employee_turnover_exception_handler,
    PredictionError: employee_turnover_exception_handler,
    DataProcessingError: employee_turnover_exception_handler,
    AuthenticationError: employee_turnover_exception_handler,
    AuthorizationError: employee_turnover_exception_handler,
    ResourceNotFoundError: employee_turnover_exception_handler,
    ValidationError: employee_turnover_exception_handler,
    RequestValidationError: validation_exception_handler,
    HTTPException: http_exception_handler,
    StarletteHTTPException: starlette_http_exception_handler,
    Exception: general_exception_handler,
}
