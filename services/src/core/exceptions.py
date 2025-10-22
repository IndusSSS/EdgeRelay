"""
EdgeRelay Exception Handling
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import logging
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class EdgeRelayException(Exception):
    """
    Base exception for EdgeRelay.
    MESSS Compliant: Structured exception handling.
    """
    def __init__(self, message: str, status_code: int = 500, details: Dict[str, Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(EdgeRelayException):
    """Authentication related errors."""
    def __init__(self, message: str = "Authentication failed", details: Dict[str, Any] = None):
        super().__init__(message, 401, details)


class AuthorizationError(EdgeRelayException):
    """Authorization related errors."""
    def __init__(self, message: str = "Access denied", details: Dict[str, Any] = None):
        super().__init__(message, 403, details)


class ValidationError(EdgeRelayException):
    """Validation related errors."""
    def __init__(self, message: str = "Validation failed", details: Dict[str, Any] = None):
        super().__init__(message, 400, details)


class DatabaseError(EdgeRelayException):
    """Database related errors."""
    def __init__(self, message: str = "Database operation failed", details: Dict[str, Any] = None):
        super().__init__(message, 500, details)


class ServiceError(EdgeRelayException):
    """Service related errors."""
    def __init__(self, message: str = "Service operation failed", details: Dict[str, Any] = None):
        super().__init__(message, 500, details)


def setup_exception_handlers(app: FastAPI):
    """
    Setup exception handlers for the FastAPI application.
    MESSS Compliant: Comprehensive error handling.
    """
    
    @app.exception_handler(EdgeRelayException)
    async def edgerelay_exception_handler(request: Request, exc: EdgeRelayException):
        """Handle EdgeRelay exceptions."""
        logger.error(f"EdgeRelay exception: {exc.message}", extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method
        })
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "EdgeRelayException",
                "message": exc.message,
                "details": exc.details,
                "path": request.url.path,
                "method": request.method
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.error(f"HTTP exception: {exc.detail}", extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method
        })
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTPException",
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation exceptions."""
        logger.error(f"Validation error: {exc.errors()}", extra={
            "path": request.url.path,
            "method": request.method
        })
        
        return JSONResponse(
            status_code=422,
            content={
                "error": "ValidationError",
                "message": "Request validation failed",
                "details": exc.errors(),
                "path": request.url.path,
                "method": request.method
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}", extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__
        })
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An internal server error occurred",
                "path": request.url.path,
                "method": request.method
            }
        )
