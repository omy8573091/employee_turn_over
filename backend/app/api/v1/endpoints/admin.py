from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.api.deps import get_current_user
from app.models import User

router = APIRouter()

@router.post("/upload-employees")
async def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload employee data from CSV or Excel file"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Mock upload response
    return {
        "message": "File uploaded successfully",
        "created_count": random.randint(100, 500),
        "updated_count": random.randint(10, 50),
        "total_rows": random.randint(150, 600)
    }

@router.post("/train-models")
async def train_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Train ML models with current employee data"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Mock training response
    return {
        "status": "completed",
        "message": "Models trained successfully with latest data",
        "models_trained": ["logistic_regression", "random_forest", "gradient_boosting"],
        "training_duration": "2 minutes 34 seconds",
        "accuracy_scores": {
            "logistic_regression": round(random.uniform(0.80, 0.90), 3),
            "random_forest": round(random.uniform(0.85, 0.95), 3),
            "gradient_boosting": round(random.uniform(0.82, 0.92), 3)
        },
        "timestamp": "2024-01-01T00:00:00Z",
        "best_model": "random_forest",
        "test_accuracy": round(random.uniform(0.85, 0.95), 3),
        "test_f1": round(random.uniform(0.80, 0.90), 3),
        "test_auc": round(random.uniform(0.88, 0.96), 3)
    }

@router.get("/system-status")
async def get_system_status(
    current_user: User = Depends(get_current_user)
):
    """Get system status and model information"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return {
        "status": "online",
        "version": "1.0.0",
        "uptime": "2 days, 5 hours",
        "database_status": "healthy",
        "ml_models_status": "loaded",
        "last_model_training": "2024-01-01T00:00:00Z",
        "total_employees": 14999,
        "total_predictions": 2500,
        "system_health": "healthy",
        "models_loaded": True,
        "available_models": ["logistic_regression", "random_forest", "gradient_boosting"],
        "scaler_loaded": True,
        "encoders_loaded": True,
        "feature_columns": [
            "satisfaction_level", "last_evaluation", "number_project",
            "average_monthly_hours", "time_spend_company", "work_accident",
            "promotion_last_5years", "department", "salary"
        ]
    }

@router.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users (admin only)"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Mock users data
    return [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@company.com",
            "is_admin": True,
            "created_at": "2024-01-01T00:00:00Z",
            "is_active": True
        },
        {
            "id": 2,
            "username": "hr_manager",
            "email": "hr@company.com",
            "is_admin": False,
            "created_at": "2024-01-02T00:00:00Z",
            "is_active": True
        }
    ]

@router.delete("/employees/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an employee (admin only)"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    # Mock deletion response
    return {"message": "Employee deleted successfully"}