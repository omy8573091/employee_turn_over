from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://user:password@localhost/employee_turnover"
    database_url_test: str = "postgresql://user:password@localhost/employee_turnover_test"
    
    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API settings
    api_v1_str: str = "/api/v1"
    project_name: str = "Employee Turnover Analytics API"
    
    # CORS settings
    backend_cors_origins: list = ["http://localhost:3000", "http://localhost:3001"]
    
    # ML Model settings
    model_path: str = "models/"
    data_path: str = "data/"
    
    class Config:
        env_file = ".env"


settings = Settings()
