"""
Custom exception classes for the application.
"""
from fastapi import HTTPException, status


class EmployeeTurnoverException(Exception):
    """Base exception for employee turnover application."""
    pass


class DataValidationError(EmployeeTurnoverException):
    """Raised when data validation fails."""
    pass


class ModelNotFoundError(EmployeeTurnoverException):
    """Raised when a ML model is not found."""
    pass


class PredictionError(EmployeeTurnoverException):
    """Raised when prediction fails."""
    pass


class DataProcessingError(EmployeeTurnoverException):
    """Raised when data processing fails."""
    pass


class AuthenticationError(HTTPException):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """Raised when authorization fails."""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ResourceNotFoundError(HTTPException):
    """Raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ValidationError(HTTPException):
    """Raised when request validation fails."""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
