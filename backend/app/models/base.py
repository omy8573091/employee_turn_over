from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database.session import Base
import enum


class RiskZone(enum.Enum):
    """Risk zone enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategyStatus(enum.Enum):
    """Strategy status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    satisfaction_level = Column(Float, nullable=False)
    last_evaluation = Column(Float, nullable=False)
    number_project = Column(Integer, nullable=False)
    average_monthly_hours = Column(Integer, nullable=False)
    time_spend_company = Column(Integer, nullable=False)
    work_accident = Column(Integer, nullable=False)
    left = Column(Integer, nullable=False)  # 0: stayed, 1: left
    promotion_last_5years = Column(Integer, nullable=False)
    department = Column(String(50), nullable=False)
    salary = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    predictions = relationship("Prediction", back_populates="employee")
    retention_strategies = relationship("RetentionStrategy", back_populates="employee")


class Prediction(Base):
    """ML model predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    model_name = Column(String(50), nullable=False)
    turnover_probability = Column(Float, nullable=False)
    risk_zone = Column(Enum(RiskZone), nullable=False)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="predictions")


class RetentionStrategy(Base):
    """Retention strategies for employees"""
    __tablename__ = "retention_strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    risk_zone = Column(Enum(RiskZone), nullable=False)
    strategies = Column(Text, nullable=False)  # JSON string of strategies
    status = Column(Enum(StrategyStatus), default=StrategyStatus.PENDING)
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="retention_strategies")


class ModelPerformance(Base):
    """ML model performance metrics"""
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(50), nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    auc_score = Column(Float, nullable=False)
    training_date = Column(DateTime(timezone=True), server_default=func.now())
    model_version = Column(String(20), nullable=False)
