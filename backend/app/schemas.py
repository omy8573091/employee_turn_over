from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Employee schemas
class EmployeeBase(BaseModel):
    employee_id: str
    satisfaction_level: float
    last_evaluation: float
    number_project: int
    average_monthly_hours: int
    time_spend_company: int
    work_accident: int
    promotion_last_5years: int
    department: str
    salary: str
    left: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    satisfaction_level: Optional[float] = None
    last_evaluation: Optional[float] = None
    number_project: Optional[int] = None
    average_monthly_hours: Optional[int] = None
    time_spend_company: Optional[int] = None
    work_accident: Optional[int] = None
    promotion_last_5years: Optional[int] = None
    department: Optional[str] = None
    salary: Optional[str] = None
    left: Optional[int] = None

# Prediction schemas
class PredictionBase(BaseModel):
    turnover_probability: float
    risk_zone: str
    model_used: str
    prediction_confidence: str

class PredictionCreate(PredictionBase):
    employee_id: int

class Prediction(PredictionBase):
    id: int
    employee_id: str
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    employee_id: int
    model_name: Optional[str] = "random_forest"

class EmployeePredictionRequest(BaseModel):
    employee_id: str
    satisfaction_level: float
    last_evaluation: float
    number_project: int
    average_monthly_hours: int
    time_spend_company: int
    work_accident: int
    promotion_last_5years: int
    department: str
    salary: str
    left: int
    model_name: Optional[str] = "random_forest"

class PredictionResponse(Prediction):
    pass

# Retention Strategy schemas
class RetentionStrategyBase(BaseModel):
    strategy_type: str
    description: str
    priority: str
    estimated_cost: float
    success_probability: float

class RetentionStrategyCreate(RetentionStrategyBase):
    employee_id: int

class RetentionStrategy(RetentionStrategyBase):
    id: int
    employee_id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

# Analytics schemas
class DepartmentStats(BaseModel):
    department: str
    total_employees: int
    employees_left: int
    turnover_rate: float
    avg_satisfaction: float

class SalaryStats(BaseModel):
    salary_level: str
    total_employees: int
    employees_left: int
    turnover_rate: float
    avg_satisfaction: float

class AnalyticsSummary(BaseModel):
    total_employees: int
    employees_left: int
    turnover_rate: float
    high_risk_employees: int
    safe_employees: int
    department_stats: List[DepartmentStats]
    salary_stats: List[SalaryStats]

class RiskZoneDistribution(BaseModel):
    safe_zone: int
    low_risk_zone: int
    medium_risk_zone: int
    high_risk_zone: int

class TurnoverByDepartment(BaseModel):
    department: str
    total_employees: int
    employees_left: int
    turnover_rate: float
    avg_satisfaction: float
    avg_evaluation: float
    avg_hours: float

class TurnoverBySalary(BaseModel):
    salary_level: str
    total_employees: int
    employees_left: int
    turnover_rate: float
    avg_satisfaction: float
    avg_evaluation: float
    avg_hours: float

class SatisfactionDistribution(BaseModel):
    status: str
    avg_satisfaction: float
    min_satisfaction: float
    max_satisfaction: float
    std_satisfaction: float

class ProjectCountAnalysis(BaseModel):
    project_count: int
    total_employees: int
    employees_left: int
    turnover_rate: float
    avg_satisfaction: float
    avg_evaluation: float
    avg_hours: float

class ClusteringAnalysis(BaseModel):
    total_employees_analyzed: int
    clusters: dict
    interpretations: dict
    error: Optional[str] = None