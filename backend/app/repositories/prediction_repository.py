"""
Prediction repository for ML model predictions data access.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from app.models.base import Prediction, Employee, RiskZone
from app.exceptions.custom_exceptions import ResourceNotFoundError


class PredictionRepository:
    """Repository for prediction data operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, prediction_data: Dict[str, Any]) -> Prediction:
        """Create a new prediction."""
        prediction = Prediction(**prediction_data)
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction
    
    def get_by_id(self, prediction_id: int) -> Optional[Prediction]:
        """Get prediction by ID."""
        return self.db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    def get_by_employee_id(self, employee_id: int) -> List[Prediction]:
        """Get all predictions for an employee."""
        return (
            self.db.query(Prediction)
            .filter(Prediction.employee_id == employee_id)
            .order_by(desc(Prediction.prediction_date))
            .all()
        )
    
    def get_latest_by_employee_id(self, employee_id: int) -> Optional[Prediction]:
        """Get the latest prediction for an employee."""
        return (
            self.db.query(Prediction)
            .filter(Prediction.employee_id == employee_id)
            .order_by(desc(Prediction.prediction_date))
            .first()
        )
    
    def get_by_risk_zone(self, risk_zone: RiskZone, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get predictions by risk zone."""
        return (
            self.db.query(Prediction)
            .filter(Prediction.risk_zone == risk_zone)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_high_risk_predictions(self, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get high and critical risk predictions."""
        return (
            self.db.query(Prediction)
            .filter(
                or_(
                    Prediction.risk_zone == RiskZone.HIGH,
                    Prediction.risk_zone == RiskZone.CRITICAL
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_predictions_with_employees(self, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get predictions with employee information."""
        return (
            self.db.query(Prediction)
            .join(Employee)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_prediction_statistics(self) -> Dict[str, Any]:
        """Get prediction statistics."""
        total_predictions = self.db.query(Prediction).count()
        
        # Risk zone breakdown
        risk_zone_stats = (
            self.db.query(
                Prediction.risk_zone,
                func.count(Prediction.id)
            )
            .group_by(Prediction.risk_zone)
            .all()
        )
        
        # Average turnover probability by risk zone
        avg_probability_by_risk = (
            self.db.query(
                Prediction.risk_zone,
                func.avg(Prediction.turnover_probability)
            )
            .group_by(Prediction.risk_zone)
            .all()
        )
        
        # Model performance
        model_stats = (
            self.db.query(
                Prediction.model_name,
                func.count(Prediction.id),
                func.avg(Prediction.turnover_probability)
            )
            .group_by(Prediction.model_name)
            .all()
        )
        
        return {
            'total_predictions': total_predictions,
            'risk_zone_breakdown': dict(risk_zone_stats),
            'avg_probability_by_risk': dict(avg_probability_by_risk),
            'model_performance': [
                {
                    'model_name': stat[0],
                    'prediction_count': stat[1],
                    'avg_probability': float(stat[2]) if stat[2] else 0
                }
                for stat in model_stats
            ]
        }
    
    def get_recent_predictions(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """Get recent predictions within specified days."""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return (
            self.db.query(Prediction)
            .filter(Prediction.prediction_date >= cutoff_date)
            .order_by(desc(Prediction.prediction_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self, prediction_id: int, update_data: Dict[str, Any]) -> Optional[Prediction]:
        """Update prediction data."""
        prediction = self.get_by_id(prediction_id)
        if not prediction:
            raise ResourceNotFoundError(f"Prediction with ID {prediction_id} not found")
        
        for key, value in update_data.items():
            if hasattr(prediction, key):
                setattr(prediction, key, value)
        
        self.db.commit()
        self.db.refresh(prediction)
        return prediction
    
    def delete(self, prediction_id: int) -> bool:
        """Delete a prediction."""
        prediction = self.get_by_id(prediction_id)
        if not prediction:
            raise ResourceNotFoundError(f"Prediction with ID {prediction_id} not found")
        
        self.db.delete(prediction)
        self.db.commit()
        return True
