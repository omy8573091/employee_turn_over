"""
Prediction service for ML model predictions business logic.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.prediction_repository import PredictionRepository
from app.repositories.employee_repository import EmployeeRepository
from app.exceptions.custom_exceptions import DataValidationError, ResourceNotFoundError, PredictionError
from app.utils.validators import validate_prediction_data
from app.models.base import RiskZone
import joblib
import numpy as np
from datetime import datetime


class PredictionService:
    """Service for prediction business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model."""
        try:
            # This would load from the actual model file
            # For now, we'll use a placeholder
            self.model = None  # joblib.load('data/models/turnover_model.pkl')
        except Exception as e:
            # In production, you might want to log this and handle gracefully
            pass
    
    def create_prediction(self, employee_id: int, prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new prediction for an employee."""
        # Validate employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        # Validate prediction data
        validation_errors = validate_prediction_data(prediction_data)
        if validation_errors:
            raise DataValidationError(f"Validation errors: {', '.join(validation_errors)}")
        
        # Make prediction
        turnover_probability = self._make_prediction(prediction_data)
        risk_zone = self._determine_risk_zone(turnover_probability)
        
        # Create prediction record
        prediction_record = {
            'employee_id': employee_id,
            'model_name': prediction_data.get('model_name', 'default_model'),
            'turnover_probability': turnover_probability,
            'risk_zone': risk_zone
        }
        
        prediction = self.prediction_repo.create(prediction_record)
        return self._prediction_to_dict(prediction)
    
    def get_prediction(self, prediction_id: int) -> Dict[str, Any]:
        """Get prediction by ID."""
        prediction = self.prediction_repo.get_by_id(prediction_id)
        if not prediction:
            raise ResourceNotFoundError(f"Prediction with ID {prediction_id} not found")
        
        return self._prediction_to_dict(prediction)
    
    def get_employee_predictions(self, employee_id: int) -> List[Dict[str, Any]]:
        """Get all predictions for an employee."""
        predictions = self.prediction_repo.get_by_employee_id(employee_id)
        return [self._prediction_to_dict(pred) for pred in predictions]
    
    def get_latest_employee_prediction(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Get the latest prediction for an employee."""
        prediction = self.prediction_repo.get_latest_by_employee_id(employee_id)
        if prediction:
            return self._prediction_to_dict(prediction)
        return None
    
    def get_high_risk_predictions(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get high-risk predictions."""
        predictions = self.prediction_repo.get_high_risk_predictions(skip, limit)
        return [self._prediction_to_dict(pred) for pred in predictions]
    
    def get_predictions_by_risk_zone(self, risk_zone: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get predictions by risk zone."""
        try:
            risk_zone_enum = RiskZone(risk_zone.lower())
        except ValueError:
            raise DataValidationError(f"Invalid risk zone: {risk_zone}")
        
        predictions = self.prediction_repo.get_by_risk_zone(risk_zone_enum, skip, limit)
        return [self._prediction_to_dict(pred) for pred in predictions]
    
    def get_prediction_statistics(self) -> Dict[str, Any]:
        """Get prediction statistics."""
        return self.prediction_repo.get_prediction_statistics()
    
    def get_recent_predictions(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent predictions."""
        predictions = self.prediction_repo.get_recent_predictions(days, skip, limit)
        return [self._prediction_to_dict(pred) for pred in predictions]
    
    def batch_predict(self, employee_ids: List[int]) -> List[Dict[str, Any]]:
        """Make predictions for multiple employees."""
        results = []
        
        for employee_id in employee_ids:
            try:
                employee = self.employee_repo.get_by_id(employee_id)
                if not employee:
                    results.append({
                        'employee_id': employee_id,
                        'error': 'Employee not found'
                    })
                    continue
                
                # Convert employee data to prediction format
                prediction_data = self._employee_to_prediction_data(employee)
                turnover_probability = self._make_prediction(prediction_data)
                risk_zone = self._determine_risk_zone(turnover_probability)
                
                # Create prediction record
                prediction_record = {
                    'employee_id': employee_id,
                    'model_name': 'batch_model',
                    'turnover_probability': turnover_probability,
                    'risk_zone': risk_zone
                }
                
                prediction = self.prediction_repo.create(prediction_record)
                results.append(self._prediction_to_dict(prediction))
                
            except Exception as e:
                results.append({
                    'employee_id': employee_id,
                    'error': str(e)
                })
        
        return results
    
    def _make_prediction(self, data: Dict[str, Any]) -> float:
        """Make a prediction using the ML model."""
        if self.model is None:
            # Fallback prediction logic when model is not available
            # This is a simplified heuristic
            satisfaction = data.get('satisfaction_level', 0.5)
            last_eval = data.get('last_evaluation', 0.5)
            projects = data.get('number_project', 3)
            hours = data.get('average_monthly_hours', 200)
            time_at_company = data.get('time_spend_company', 3)
            
            # Simple heuristic-based prediction
            risk_score = (
                (1 - satisfaction) * 0.3 +
                (1 - last_eval) * 0.2 +
                (1 - min(projects / 5, 1)) * 0.1 +
                (1 - min(hours / 300, 1)) * 0.1 +
                (1 - min(time_at_company / 10, 1)) * 0.3
            )
            
            return min(max(risk_score, 0.0), 1.0)
        
        # Use actual model for prediction
        try:
            # Convert data to model input format
            features = self._prepare_features(data)
            prediction = self.model.predict_proba([features])[0][1]  # Probability of leaving
            return float(prediction)
        except Exception as e:
            raise PredictionError(f"Model prediction failed: {str(e)}")
    
    def _determine_risk_zone(self, probability: float) -> RiskZone:
        """Determine risk zone based on turnover probability."""
        if probability >= 0.8:
            return RiskZone.CRITICAL
        elif probability >= 0.6:
            return RiskZone.HIGH
        elif probability >= 0.4:
            return RiskZone.MEDIUM
        else:
            return RiskZone.LOW
    
    def _employee_to_prediction_data(self, employee) -> Dict[str, Any]:
        """Convert employee model to prediction data format."""
        return {
            'satisfaction_level': employee.satisfaction_level,
            'last_evaluation': employee.last_evaluation,
            'number_project': employee.number_project,
            'average_monthly_hours': employee.average_monthly_hours,
            'time_spend_company': employee.time_spend_company,
            'work_accident': employee.work_accident,
            'promotion_last_5years': employee.promotion_last_5years,
            'department': employee.department,
            'salary': employee.salary
        }
    
    def _prepare_features(self, data: Dict[str, Any]) -> List[float]:
        """Prepare features for model prediction."""
        # This would convert categorical variables to numerical
        # and normalize the data according to the model's requirements
        features = [
            data.get('satisfaction_level', 0.5),
            data.get('last_evaluation', 0.5),
            data.get('number_project', 3),
            data.get('average_monthly_hours', 200),
            data.get('time_spend_company', 3),
            data.get('work_accident', 0),
            data.get('promotion_last_5years', 0)
        ]
        
        # Add department encoding (simplified)
        department_encoding = {
            'IT': 0, 'RandD': 1, 'accounting': 2, 'hr': 3,
            'management': 4, 'marketing': 5, 'product_mng': 6,
            'sales': 7, 'support': 8, 'technical': 9
        }
        features.append(department_encoding.get(data.get('department', 'IT'), 0))
        
        # Add salary encoding
        salary_encoding = {'low': 0, 'medium': 1, 'high': 2}
        features.append(salary_encoding.get(data.get('salary', 'medium'), 1))
        
        return features
    
    def _prediction_to_dict(self, prediction) -> Dict[str, Any]:
        """Convert prediction model to dictionary."""
        return {
            'id': prediction.id,
            'employee_id': prediction.employee_id,
            'model_name': prediction.model_name,
            'turnover_probability': prediction.turnover_probability,
            'risk_zone': prediction.risk_zone.value,
            'prediction_date': prediction.prediction_date.isoformat()
        }
