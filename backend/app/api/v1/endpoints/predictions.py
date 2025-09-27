from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random
from datetime import datetime

from app.database import get_db
from app.api.deps import get_current_user
from app.models import User
from app.schemas import PredictionRequest, PredictionResponse, EmployeePredictionRequest

router = APIRouter()

# Mock predictions data
MOCK_PREDICTIONS = []

@router.post("/predict", response_model=PredictionResponse)
async def predict_employee_turnover(
    prediction_request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict turnover probability for an employee"""
    # Generate mock prediction
    probability = random.uniform(0.1, 0.95)
    
    if probability < 0.2:
        risk_zone = 'Safe Zone (Green)'
    elif probability < 0.6:
        risk_zone = 'Low Risk Zone (Yellow)'
    elif probability < 0.9:
        risk_zone = 'Medium Risk Zone (Orange)'
    else:
        risk_zone = 'High Risk Zone (Red)'
    
    prediction = {
        "id": len(MOCK_PREDICTIONS) + 1,
        "employee_id": prediction_request.employee_id,
        "turnover_probability": round(probability, 3),
        "risk_zone": risk_zone,
        "model_used": prediction_request.model_name or "random_forest",
        "prediction_confidence": "High" if probability > 0.8 or probability < 0.2 else "Medium",
        "created_at": datetime.now(),
        "created_by": current_user.id
    }
    
    MOCK_PREDICTIONS.append(prediction)
    return prediction

@router.post("/predict-employee", response_model=PredictionResponse)
async def predict_employee_turnover_with_data(
    employee_data: EmployeePredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict turnover probability for an employee using provided data"""
    # Generate mock prediction based on employee data
    # In a real implementation, this would use the ML model
    
    # Simple heuristic-based prediction for demo
    risk_factors = 0
    
    # Satisfaction level (lower = higher risk)
    if employee_data.satisfaction_level < 0.3:
        risk_factors += 0.3
    elif employee_data.satisfaction_level < 0.6:
        risk_factors += 0.1
    
    # Last evaluation (lower = higher risk)
    if employee_data.last_evaluation < 0.4:
        risk_factors += 0.2
    elif employee_data.last_evaluation < 0.7:
        risk_factors += 0.1
    
    # Number of projects (too few or too many = higher risk)
    if employee_data.number_project < 2 or employee_data.number_project > 6:
        risk_factors += 0.15
    
    # Average monthly hours (too many = higher risk)
    if employee_data.average_monthly_hours > 250:
        risk_factors += 0.2
    elif employee_data.average_monthly_hours > 200:
        risk_factors += 0.1
    
    # Time at company (very short or very long = higher risk)
    if employee_data.time_spend_company < 2 or employee_data.time_spend_company > 8:
        risk_factors += 0.1
    
    # Work accident (having one = slightly higher risk)
    if employee_data.work_accident == 1:
        risk_factors += 0.05
    
    # No promotion in 5 years = higher risk
    if employee_data.promotion_last_5years == 0 and employee_data.time_spend_company >= 5:
        risk_factors += 0.15
    
    # Department risk (some departments have higher turnover)
    high_turnover_depts = ['sales', 'support', 'hr']
    if employee_data.department in high_turnover_depts:
        risk_factors += 0.1
    
    # Salary level (lower salary = higher risk)
    if employee_data.salary == 'low':
        risk_factors += 0.1
    
    # Base probability + risk factors
    base_probability = 0.1
    probability = min(0.95, base_probability + risk_factors)
    
    # Add some randomness for demo purposes
    import random
    probability += random.uniform(-0.1, 0.1)
    probability = max(0.05, min(0.95, probability))
    
    # Determine risk zone
    if probability < 0.2:
        risk_zone = 'Safe Zone (Green)'
    elif probability < 0.6:
        risk_zone = 'Low Risk Zone (Yellow)'
    elif probability < 0.9:
        risk_zone = 'Medium Risk Zone (Orange)'
    else:
        risk_zone = 'High Risk Zone (Red)'
    
    prediction = {
        "id": len(MOCK_PREDICTIONS) + 1,
        "employee_id": employee_data.employee_id,
        "turnover_probability": round(probability, 3),
        "risk_zone": risk_zone,
        "model_used": employee_data.model_name or "random_forest",
        "prediction_confidence": "High" if probability > 0.8 or probability < 0.2 else "Medium",
        "created_at": datetime.now(),
        "created_by": current_user.id
    }
    
    MOCK_PREDICTIONS.append(prediction)
    return prediction

@router.get("/employee/{employee_id}")
async def get_employee_predictions(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all predictions for a specific employee"""
    employee_predictions = [
        pred for pred in MOCK_PREDICTIONS 
        if pred["employee_id"] == employee_id
    ]
    
    # If no predictions exist, generate some mock data
    if not employee_predictions:
        # Generate mock predictions based on employee_id
        mock_predictions = []
        for i in range(3):
            probability = random.uniform(0.1, 0.95)
            if probability < 0.2:
                risk_zone = 'low'
            elif probability < 0.6:
                risk_zone = 'medium'
            elif probability < 0.9:
                risk_zone = 'high'
            else:
                risk_zone = 'critical'
            
            mock_predictions.append({
                "employee_id": employee_id,
                "turnover_probability": round(probability, 3),
                "risk_zone": risk_zone,
                "prediction_date": f"2024-01-{i+1:02d}T00:00:00Z",
                "model_used": "random_forest",
                "confidence_score": round(random.uniform(0.7, 0.95), 3)
            })
        return mock_predictions
    
    return employee_predictions

@router.get("/latest", response_model=List[PredictionResponse])
async def get_latest_predictions(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get latest predictions across all employees"""
    return MOCK_PREDICTIONS[-limit:] if MOCK_PREDICTIONS else []

@router.get("/high-risk", response_model=List[PredictionResponse])
async def get_high_risk_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get predictions for high-risk employees"""
    high_risk_zones = ['Medium Risk Zone (Orange)', 'High Risk Zone (Red)']
    high_risk_predictions = [
        pred for pred in MOCK_PREDICTIONS 
        if pred["risk_zone"] in high_risk_zones
    ]
    return sorted(high_risk_predictions, key=lambda x: x["turnover_probability"], reverse=True)

@router.delete("/{prediction_id}")
async def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a prediction record"""
    for i, pred in enumerate(MOCK_PREDICTIONS):
        if pred["id"] == prediction_id:
            del MOCK_PREDICTIONS[i]
            return {"message": "Prediction deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Prediction not found"
    )

@router.get("/feature-importance")
async def get_feature_importance(
    model_name: str = 'random_forest',
    current_user: User = Depends(get_current_user)
):
    """Get feature importance from the trained model"""
    # Mock feature importance data
    feature_importance = [
        {"feature": "satisfaction_level", "importance": 0.342},
        {"feature": "last_evaluation", "importance": 0.198},
        {"feature": "number_project", "importance": 0.156},
        {"feature": "average_monthly_hours", "importance": 0.134},
        {"feature": "time_spend_company", "importance": 0.089},
        {"feature": "salary", "importance": 0.045},
        {"feature": "sales", "importance": 0.023},
        {"feature": "work_accident", "importance": 0.008},
        {"feature": "promotion_last_5years", "importance": 0.005}
    ]
    
    return {
        "model_name": model_name,
        "feature_importance": feature_importance
    }