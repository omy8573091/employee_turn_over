from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.api.deps import get_current_user
from app.models import User, Employee
from app.schemas import EmployeeCreate, EmployeeUpdate, Employee as EmployeeSchema

router = APIRouter()

# Mock data for demo purposes
MOCK_EMPLOYEES = [
    {
        "id": 1,
        "employee_id": "EMP001",
        "satisfaction_level": 0.38,
        "last_evaluation": 0.53,
        "number_project": 2,
        "average_monthly_hours": 157,
        "time_spend_company": 3,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "sales",
        "salary": "low",
        "left": 1,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "employee_id": "EMP002",
        "satisfaction_level": 0.80,
        "last_evaluation": 0.86,
        "number_project": 5,
        "average_monthly_hours": 262,
        "time_spend_company": 6,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "technical",
        "salary": "medium",
        "left": 0,
        "created_at": "2024-01-02T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z"
    },
    {
        "id": 3,
        "employee_id": "EMP003",
        "satisfaction_level": 0.11,
        "last_evaluation": 0.88,
        "number_project": 7,
        "average_monthly_hours": 272,
        "time_spend_company": 4,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "support",
        "salary": "medium",
        "left": 1,
        "created_at": "2024-01-03T00:00:00Z",
        "updated_at": "2024-01-03T00:00:00Z"
    },
    {
        "id": 4,
        "employee_id": "EMP004",
        "satisfaction_level": 0.72,
        "last_evaluation": 0.87,
        "number_project": 5,
        "average_monthly_hours": 223,
        "time_spend_company": 5,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "IT",
        "salary": "low",
        "left": 0,
        "created_at": "2024-01-04T00:00:00Z",
        "updated_at": "2024-01-04T00:00:00Z"
    },
    {
        "id": 5,
        "employee_id": "EMP005",
        "satisfaction_level": 0.37,
        "last_evaluation": 0.52,
        "number_project": 2,
        "average_monthly_hours": 159,
        "time_spend_company": 3,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "hr",
        "salary": "low",
        "left": 1,
        "created_at": "2024-01-05T00:00:00Z",
        "updated_at": "2024-01-05T00:00:00Z"
    },
    {
        "id": 6,
        "employee_id": "EMP006",
        "satisfaction_level": 0.85,
        "last_evaluation": 0.92,
        "number_project": 4,
        "average_monthly_hours": 200,
        "time_spend_company": 8,
        "work_accident": 0,
        "promotion_last_5years": 1,
        "department": "marketing",
        "salary": "high",
        "left": 0,
        "created_at": "2024-01-06T00:00:00Z",
        "updated_at": "2024-01-06T00:00:00Z"
    },
    {
        "id": 7,
        "employee_id": "EMP007",
        "satisfaction_level": 0.45,
        "last_evaluation": 0.65,
        "number_project": 3,
        "average_monthly_hours": 180,
        "time_spend_company": 2,
        "work_accident": 1,
        "promotion_last_5years": 0,
        "department": "accounting",
        "salary": "medium",
        "left": 0,
        "created_at": "2024-01-07T00:00:00Z",
        "updated_at": "2024-01-07T00:00:00Z"
    },
    {
        "id": 8,
        "employee_id": "EMP008",
        "satisfaction_level": 0.92,
        "last_evaluation": 0.78,
        "number_project": 6,
        "average_monthly_hours": 250,
        "time_spend_company": 10,
        "work_accident": 0,
        "promotion_last_5years": 2,
        "department": "RandD",
        "salary": "high",
        "left": 0,
        "created_at": "2024-01-08T00:00:00Z",
        "updated_at": "2024-01-08T00:00:00Z"
    }
]

@router.get("/")
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all employees"""
    # Return mock data for demo with proper structure
    employees = MOCK_EMPLOYEES[skip:skip + limit]
    return {"employees": employees, "total": len(MOCK_EMPLOYEES)}

@router.get("/{employee_id}")
async def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get employee by employee_id"""
    for emp in MOCK_EMPLOYEES:
        if emp["employee_id"] == employee_id:
            return emp
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

@router.post("/")
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new employee"""
    new_employee = {
        "id": len(MOCK_EMPLOYEES) + 1,
        "employee_id": f"EMP{len(MOCK_EMPLOYEES) + 1:03d}",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        **employee.dict()
    }
    MOCK_EMPLOYEES.append(new_employee)
    return new_employee

@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update employee"""
    for i, emp in enumerate(MOCK_EMPLOYEES):
        if emp["employee_id"] == employee_id:
            update_data = employee_update.dict(exclude_unset=True)
            MOCK_EMPLOYEES[i].update(update_data)
            MOCK_EMPLOYEES[i]["updated_at"] = "2024-01-01T00:00:00Z"
            return MOCK_EMPLOYEES[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete employee"""
    for i, emp in enumerate(MOCK_EMPLOYEES):
        if emp["employee_id"] == employee_id:
            del MOCK_EMPLOYEES[i]
            return {"message": "Employee deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

@router.get("/{employee_id}/retention-strategies")
async def get_employee_retention_strategies(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get retention strategies for a specific employee"""
    # Check if employee exists
    employee = None
    for emp in MOCK_EMPLOYEES:
        if emp["employee_id"] == employee_id:
            employee = emp
            break
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Mock retention strategies based on employee data
    strategies = []
    
    # Generate strategies based on employee risk factors
    if employee["satisfaction_level"] < 0.5:
        strategies.append({
            "strategy_id": f"STRAT_{employee_id}_001",
            "employee_id": employee_id,
            "risk_zone": "high",
            "strategy_type": "Satisfaction Improvement",
            "description": "Implement regular check-ins and feedback sessions to improve job satisfaction",
            "estimated_cost": 5000,
            "success_probability": 0.7,
            "status": "pending",
            "created_at": "2024-01-01T00:00:00Z"
        })
    
    if employee["number_project"] > 5:
        strategies.append({
            "strategy_id": f"STRAT_{employee_id}_002",
            "employee_id": employee_id,
            "risk_zone": "medium",
            "strategy_type": "Workload Management",
            "description": "Redistribute projects to reduce workload and prevent burnout",
            "estimated_cost": 3000,
            "success_probability": 0.8,
            "status": "in_progress",
            "created_at": "2024-01-01T00:00:00Z"
        })
    
    if employee["promotion_last_5years"] == 0 and employee["time_spend_company"] > 3:
        strategies.append({
            "strategy_id": f"STRAT_{employee_id}_003",
            "employee_id": employee_id,
            "risk_zone": "medium",
            "strategy_type": "Career Development",
            "description": "Create a career development plan with clear promotion path",
            "estimated_cost": 8000,
            "success_probability": 0.6,
            "status": "pending",
            "created_at": "2024-01-01T00:00:00Z"
        })
    
    if employee["average_monthly_hours"] > 250:
        strategies.append({
            "strategy_id": f"STRAT_{employee_id}_004",
            "employee_id": employee_id,
            "risk_zone": "high",
            "strategy_type": "Work-Life Balance",
            "description": "Implement flexible working hours and remote work options",
            "estimated_cost": 2000,
            "success_probability": 0.75,
            "status": "completed",
            "created_at": "2024-01-01T00:00:00Z"
        })
    
    return {"strategies": strategies}