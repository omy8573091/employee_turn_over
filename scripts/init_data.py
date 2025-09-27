#!/usr/bin/env python3
"""
Data initialization script for Employee Turnover Analytics Platform
This script loads the HR dataset and creates initial admin user
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

from app.database import SessionLocal, engine
from app.models import Base, User, Employee
from app.auth import get_password_hash
from app.ml_models import turnover_predictor

def create_tables():
    """Create database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    db = SessionLocal()
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("✅ Admin user already exists")
        db.close()
        return
    
    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@company.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    db.close()
    print("✅ Admin user created (username: admin, password: admin123)")

def load_employee_data():
    """Load employee data from Excel file"""
    print("Loading employee data...")
    
    # Check if data file exists
    data_file = Path(__file__).parent.parent / "1688640705_hr_comma_sep.xlsx"
    if not data_file.exists():
        print("❌ Data file not found. Please ensure 1688640705_hr_comma_sep.xlsx is in the project root.")
        return
    
    # Load data
    df = pd.read_excel(data_file)
    print(f"📊 Loaded {len(df)} employee records")
    
    db = SessionLocal()
    
    # Check if data already exists
    existing_count = db.query(Employee).count()
    if existing_count > 0:
        print(f"✅ Employee data already loaded ({existing_count} records)")
        db.close()
        return
    
    # Insert employee data
    for index, row in df.iterrows():
        employee = Employee(
            employee_id=f"EMP_{index + 1:06d}",
            satisfaction_level=float(row['satisfaction_level']),
            last_evaluation=float(row['last_evaluation']),
            number_project=int(row['number_project']),
            average_monthly_hours=int(row['average_montly_hours']),
            time_spend_company=int(row['time_spend_company']),
            work_accident=int(row['Work_accident']),
            left=int(row['left']),
            promotion_last_5years=int(row['promotion_last_5years']),
            department=str(row['sales']),
            salary=str(row['salary'])
        )
        db.add(employee)
    
    db.commit()
    db.close()
    print(f"✅ Loaded {len(df)} employee records")

def train_models():
    """Train ML models"""
    print("Training ML models...")
    
    db = SessionLocal()
    employees = db.query(Employee).all()
    
    if len(employees) < 100:
        print("❌ Insufficient data for training. Need at least 100 employees.")
        db.close()
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'satisfaction_level': emp.satisfaction_level,
            'last_evaluation': emp.last_evaluation,
            'number_project': emp.number_project,
            'average_montly_hours': emp.average_monthly_hours,
            'time_spend_company': emp.time_spend_company,
            'Work_accident': emp.work_accident,
            'left': emp.left,
            'promotion_last_5years': emp.promotion_last_5years,
            'sales': emp.department,
            'salary': emp.salary
        }
        for emp in employees
    ])
    
    # Train models
    training_result = turnover_predictor.train_models(df)
    print(f"✅ Models trained successfully. Best model: {training_result['best_model']}")
    
    db.close()

def main():
    """Main initialization function"""
    print("🚀 Initializing Employee Turnover Analytics Platform...")
    print("=" * 60)
    
    try:
        create_tables()
        create_admin_user()
        load_employee_data()
        train_models()
        
        print("=" * 60)
        print("🎉 Initialization complete!")
        print("")
        print("📊 Access the application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Documentation: http://localhost:8000/docs")
        print("")
        print("🔐 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
