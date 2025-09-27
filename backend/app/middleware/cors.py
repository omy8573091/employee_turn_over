"""
CORS middleware configuration.
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.config.settings import settings


def setup_cors(app: FastAPI) -> None:
    """Setup CORS middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
