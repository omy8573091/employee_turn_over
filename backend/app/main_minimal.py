"""
Minimal FastAPI application for testing the basic setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Employee Turnover Prediction API for HR departments",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Employee Turnover Prediction API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR,
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

@app.get("/info")
def app_info():
    """Application information endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "api_version": settings.API_V1_STR,
        "database_url": settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else "configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_minimal:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
