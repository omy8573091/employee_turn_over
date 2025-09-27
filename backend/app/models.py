from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    predictions = relationship("Prediction", back_populates="creator")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    satisfaction_level = Column(Float, nullable=False)
    last_evaluation = Column(Float, nullable=False)
    number_project = Column(Integer, nullable=False)
    average_monthly_hours = Column(Integer, nullable=False)
    time_spend_company = Column(Integer, nullable=False)
    work_accident = Column(Integer, nullable=False)
    promotion_last_5years = Column(Integer, nullable=False)
    sales = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    left = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    predictions = relationship("Prediction", back_populates="employee")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    turnover_probability = Column(Float, nullable=False)
    risk_zone = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
    prediction_confidence = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    employee = relationship("Employee", back_populates="predictions")
    creator = relationship("User", back_populates="predictions")

class RetentionStrategy(Base):
    __tablename__ = "retention_strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    strategy_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    success_probability = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    employee = relationship("Employee")
    creator = relationship("User")