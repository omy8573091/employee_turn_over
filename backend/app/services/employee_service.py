"""
Employee service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.prediction_repository import PredictionRepository
from app.exceptions.custom_exceptions import DataValidationError, ResourceNotFoundError
from app.utils.validators import validate_employee_data


class EmployeeService:
    """Service for employee business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.prediction_repo = PredictionRepository(db)
    
    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new employee with validation."""
        # Validate employee data
        validation_errors = validate_employee_data(employee_data)
        if validation_errors:
            raise DataValidationError(f"Validation errors: {', '.join(validation_errors)}")
        
        # Check if employee ID already exists
        existing_employee = self.employee_repo.get_by_employee_id(employee_data.get('employee_id'))
        if existing_employee:
            raise DataValidationError("Employee ID already exists")
        
        # Create employee
        employee = self.employee_repo.create(employee_data)
        return self._employee_to_dict(employee)
    
    def get_employee(self, employee_id: int) -> Dict[str, Any]:
        """Get employee by ID."""
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        return self._employee_to_dict(employee)
    
    def get_employee_by_employee_id(self, employee_id: str) -> Dict[str, Any]:
        """Get employee by employee ID."""
        employee = self.employee_repo.get_by_employee_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        return self._employee_to_dict(employee)
    
    def get_employees(self, skip: int = 0, limit: int = 100, department: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get employees with optional filtering."""
        if department:
            employees = self.employee_repo.get_by_department(department, skip, limit)
        else:
            employees = self.employee_repo.get_all(skip, limit)
        
        return [self._employee_to_dict(emp) for emp in employees]
    
    def get_high_risk_employees(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get high-risk employees."""
        employees = self.employee_repo.get_high_risk_employees(skip, limit)
        return [self._employee_to_dict(emp) for emp in employees]
    
    def update_employee(self, employee_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update employee data."""
        # Validate update data
        validation_errors = validate_employee_data(update_data)
        if validation_errors:
            raise DataValidationError(f"Validation errors: {', '.join(validation_errors)}")
        
        employee = self.employee_repo.update(employee_id, update_data)
        return self._employee_to_dict(employee)
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee."""
        return self.employee_repo.delete(employee_id)
    
    def search_employees(self, search_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search employees with various criteria."""
        employees = self.employee_repo.search(search_params, skip, limit)
        return [self._employee_to_dict(emp) for emp in employees]
    
    def get_employee_with_predictions(self, employee_id: int) -> Dict[str, Any]:
        """Get employee with their prediction history."""
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        predictions = self.prediction_repo.get_by_employee_id(employee_id)
        
        employee_dict = self._employee_to_dict(employee)
        employee_dict['predictions'] = [
            {
                'id': pred.id,
                'model_name': pred.model_name,
                'turnover_probability': pred.turnover_probability,
                'risk_zone': pred.risk_zone.value,
                'prediction_date': pred.prediction_date.isoformat()
            }
            for pred in predictions
        ]
        
        return employee_dict
    
    def get_employee_statistics(self) -> Dict[str, Any]:
        """Get employee statistics."""
        return self.employee_repo.get_employee_statistics()
    
    def _employee_to_dict(self, employee) -> Dict[str, Any]:
        """Convert employee model to dictionary."""
        return {
            'id': employee.id,
            'employee_id': employee.employee_id,
            'satisfaction_level': employee.satisfaction_level,
            'last_evaluation': employee.last_evaluation,
            'number_project': employee.number_project,
            'average_monthly_hours': employee.average_monthly_hours,
            'time_spend_company': employee.time_spend_company,
            'work_accident': employee.work_accident,
            'left': employee.left,
            'promotion_last_5years': employee.promotion_last_5years,
            'department': employee.department,
            'salary': employee.salary,
            'created_at': employee.created_at.isoformat() if employee.created_at else None,
            'updated_at': employee.updated_at.isoformat() if employee.updated_at else None
        }
