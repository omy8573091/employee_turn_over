"""
Employee repository for data access operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app.models.base import Employee, Prediction, RetentionStrategy
from app.exceptions.custom_exceptions import ResourceNotFoundError


class EmployeeRepository:
    """Repository for employee data operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, employee_data: Dict[str, Any]) -> Employee:
        """Create a new employee."""
        employee = Employee(**employee_data)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
    
    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID."""
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def get_by_employee_id(self, employee_id: str) -> Optional[Employee]:
        """Get employee by employee ID."""
        return self.db.query(Employee).filter(Employee.employee_id == employee_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination."""
        return self.db.query(Employee).offset(skip).limit(limit).all()
    
    def get_by_department(self, department: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get employees by department."""
        return (
            self.db.query(Employee)
            .filter(Employee.department == department)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_high_risk_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get employees with high turnover risk."""
        # This would typically join with predictions table
        # For now, using basic criteria
        return (
            self.db.query(Employee)
            .filter(
                and_(
                    Employee.satisfaction_level < 0.5,
                    Employee.left == 0  # Still employed
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self, employee_id: int, update_data: Dict[str, Any]) -> Optional[Employee]:
        """Update employee data."""
        employee = self.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        for key, value in update_data.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        
        self.db.commit()
        self.db.refresh(employee)
        return employee
    
    def delete(self, employee_id: int) -> bool:
        """Delete an employee."""
        employee = self.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found")
        
        self.db.delete(employee)
        self.db.commit()
        return True
    
    def search(self, search_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Employee]:
        """Search employees with various criteria."""
        query = self.db.query(Employee)
        
        if 'department' in search_params:
            query = query.filter(Employee.department == search_params['department'])
        
        if 'salary_range' in search_params:
            salary_range = search_params['salary_range']
            if salary_range == 'low':
                query = query.filter(Employee.salary == 'low')
            elif salary_range == 'medium':
                query = query.filter(Employee.salary == 'medium')
            elif salary_range == 'high':
                query = query.filter(Employee.salary == 'high')
        
        if 'min_satisfaction' in search_params:
            query = query.filter(Employee.satisfaction_level >= search_params['min_satisfaction'])
        
        if 'max_satisfaction' in search_params:
            query = query.filter(Employee.satisfaction_level <= search_params['max_satisfaction'])
        
        return query.offset(skip).limit(limit).all()
    
    def get_employee_with_predictions(self, employee_id: int) -> Optional[Employee]:
        """Get employee with their prediction history."""
        return (
            self.db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )
    
    def get_employee_statistics(self) -> Dict[str, Any]:
        """Get employee statistics."""
        total_employees = self.db.query(Employee).count()
        employees_left = self.db.query(Employee).filter(Employee.left == 1).count()
        employees_stayed = self.db.query(Employee).filter(Employee.left == 0).count()
        
        # Department statistics
        dept_stats = (
            self.db.query(Employee.department, self.db.func.count(Employee.id))
            .group_by(Employee.department)
            .all()
        )
        
        return {
            'total_employees': total_employees,
            'employees_left': employees_left,
            'employees_stayed': employees_stayed,
            'turnover_rate': (employees_left / total_employees * 100) if total_employees > 0 else 0,
            'department_breakdown': dict(dept_stats)
        }
