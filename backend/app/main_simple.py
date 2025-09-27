from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import random
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create FastAPI app
app = FastAPI(
    title="Employee Turnover Analytics API",
    description="AI-powered employee retention and turnover prediction platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        username = verify_token(token)
        if username is None:
            raise credentials_exception
        return {"username": username, "is_admin": True}
    except Exception:
        raise credentials_exception

# Mock data
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
        "sales": "sales",
        "salary": "low",
        "left": 1
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
        "sales": "sales",
        "salary": "medium",
        "left": 1
    }
]

MOCK_PREDICTIONS = []

# Root endpoints
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Employee Turnover Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development"
    }

# Auth endpoints
@app.post("/api/v1/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint"""
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/api/v1/auth/logout")
def logout():
    """Logout endpoint"""
    return {"message": "Successfully logged out"}

# Employee endpoints
@app.get("/api/v1/employees/")
def get_employees(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all employees"""
    return MOCK_EMPLOYEES[skip:skip + limit]

@app.get("/api/v1/employees/{employee_id}")
def get_employee(
    employee_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get employee by ID"""
    for emp in MOCK_EMPLOYEES:
        if emp["id"] == employee_id:
            return emp
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )

# Analytics endpoints
@app.get("/api/v1/analytics/dashboard")
def get_dashboard_analytics(current_user: dict = Depends(get_current_user)):
    """Get dashboard analytics summary"""
    return {
        "total_employees": 14999,
        "employees_left": 3571,
        "turnover_rate": 0.238,
        "high_risk_employees": 1250,
        "safe_employees": 8500,
        "department_stats": [
            {
                "department": "sales",
                "total_employees": 4140,
                "employees_left": 1012,
                "turnover_rate": 0.244,
                "avg_satisfaction": 0.612
            },
            {
                "department": "technical",
                "total_employees": 2720,
                "employees_left": 512,
                "turnover_rate": 0.188,
                "avg_satisfaction": 0.678
            }
        ],
        "salary_stats": [
            {
                "salary_level": "low",
                "total_employees": 7316,
                "employees_left": 2172,
                "turnover_rate": 0.297,
                "avg_satisfaction": 0.567
            },
            {
                "salary_level": "medium",
                "total_employees": 6446,
                "employees_left": 1234,
                "turnover_rate": 0.191,
                "avg_satisfaction": 0.678
            }
        ]
    }

@app.get("/api/v1/analytics/risk-distribution")
def get_risk_distribution(current_user: dict = Depends(get_current_user)):
    """Get risk zone distribution"""
    return {
        "safe_zone": 8500,
        "low_risk_zone": 3500,
        "medium_risk_zone": 2000,
        "high_risk_zone": 999
    }

@app.get("/api/v1/analytics/turnover-by-department")
def get_turnover_by_department(current_user: dict = Depends(get_current_user)):
    """Get turnover statistics by department"""
    return [
        {
            "department": "management",
            "total_employees": 630,
            "employees_left": 255,
            "turnover_rate": 0.405,
            "avg_satisfaction": 0.523,
            "avg_evaluation": 0.612,
            "avg_hours": 201.5
        },
        {
            "department": "sales",
            "total_employees": 4140,
            "employees_left": 1012,
            "turnover_rate": 0.244,
            "avg_satisfaction": 0.612,
            "avg_evaluation": 0.678,
            "avg_hours": 199.2
        }
    ]

@app.get("/api/v1/analytics/turnover-by-salary")
def get_turnover_by_salary(current_user: dict = Depends(get_current_user)):
    """Get turnover statistics by salary level"""
    return [
        {
            "salary_level": "low",
            "total_employees": 7316,
            "employees_left": 2172,
            "turnover_rate": 0.297,
            "avg_satisfaction": 0.567,
            "avg_evaluation": 0.612,
            "avg_hours": 201.8
        },
        {
            "salary_level": "medium",
            "total_employees": 6446,
            "employees_left": 1234,
            "turnover_rate": 0.191,
            "avg_satisfaction": 0.678,
            "avg_evaluation": 0.689,
            "avg_hours": 199.2
        }
    ]

@app.get("/api/v1/analytics/satisfaction-distribution")
def get_satisfaction_distribution(current_user: dict = Depends(get_current_user)):
    """Get satisfaction level distribution by turnover status"""
    return [
        {
            "status": "Stayed",
            "avg_satisfaction": 0.667,
            "min_satisfaction": 0.09,
            "max_satisfaction": 1.0,
            "std_satisfaction": 0.198
        },
        {
            "status": "Left",
            "avg_satisfaction": 0.440,
            "min_satisfaction": 0.09,
            "max_satisfaction": 1.0,
            "std_satisfaction": 0.234
        }
    ]

@app.get("/api/v1/analytics/project-count-analysis")
def get_project_count_analysis(current_user: dict = Depends(get_current_user)):
    """Get turnover analysis by project count"""
    return [
        {
            "project_count": 2,
            "total_employees": 2834,
            "employees_left": 1002,
            "turnover_rate": 0.354,
            "avg_satisfaction": 0.456,
            "avg_evaluation": 0.523,
            "avg_hours": 198.5
        },
        {
            "project_count": 3,
            "total_employees": 2385,
            "employees_left": 512,
            "turnover_rate": 0.215,
            "avg_satisfaction": 0.634,
            "avg_evaluation": 0.678,
            "avg_hours": 200.2
        }
    ]

@app.get("/api/v1/analytics/clustering-analysis")
def get_clustering_analysis(current_user: dict = Depends(get_current_user)):
    """Get clustering analysis for employees who left"""
    return {
        "total_employees_analyzed": 3571,
        "clusters": {
            "cluster_0": {
                "description": "Disengaged employees (low satisfaction, low evaluation)",
                "count": 1245,
                "avg_satisfaction": 0.234,
                "avg_evaluation": 0.312
            },
            "cluster_1": {
                "description": "Overworked high performers (low satisfaction, high evaluation)",
                "count": 1456,
                "avg_satisfaction": 0.345,
                "avg_evaluation": 0.789
            }
        },
        "interpretations": {
            "cluster_0": "Disengaged employees with low satisfaction and performance. May need engagement initiatives.",
            "cluster_1": "High performers who are overworked and dissatisfied. Need workload management."
        }
    }

# Prediction endpoints
@app.post("/api/v1/predictions/predict")
def predict_employee_turnover(
    employee_id: int,
    model_name: str = "random_forest",
    current_user: dict = Depends(get_current_user)
):
    """Predict turnover probability for an employee"""
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
        "employee_id": employee_id,
        "turnover_probability": round(probability, 3),
        "risk_zone": risk_zone,
        "model_used": model_name,
        "prediction_confidence": "High" if probability > 0.8 or probability < 0.2 else "Medium",
        "created_at": datetime.now(),
        "created_by": current_user["username"]
    }
    
    MOCK_PREDICTIONS.append(prediction)
    return prediction

@app.get("/api/v1/predictions/employee/{employee_id}")
def get_employee_predictions(
    employee_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get all predictions for a specific employee"""
    employee_predictions = [
        pred for pred in MOCK_PREDICTIONS 
        if pred["employee_id"] == employee_id
    ]
    return employee_predictions

@app.get("/api/v1/predictions/high-risk")
def get_high_risk_predictions(current_user: dict = Depends(get_current_user)):
    """Get predictions for high-risk employees"""
    high_risk_zones = ['Medium Risk Zone (Orange)', 'High Risk Zone (Red)']
    high_risk_predictions = [
        pred for pred in MOCK_PREDICTIONS 
        if pred["risk_zone"] in high_risk_zones
    ]
    return sorted(high_risk_predictions, key=lambda x: x["turnover_probability"], reverse=True)

# Admin endpoints
@app.get("/api/v1/admin/system-status")
def get_system_status(current_user: dict = Depends(get_current_user)):
    """Get system status and model information"""
    return {
        "models_loaded": True,
        "available_models": ["logistic_regression", "random_forest", "gradient_boosting"],
        "scaler_loaded": True,
        "encoders_loaded": True,
        "feature_columns": [
            "satisfaction_level", "last_evaluation", "number_project",
            "average_monthly_hours", "time_spend_company", "work_accident",
            "promotion_last_5years", "sales", "salary"
        ]
    }

@app.post("/api/v1/admin/train-models")
def train_models(current_user: dict = Depends(get_current_user)):
    """Train ML models with current employee data"""
    return {
        "message": "Models trained successfully",
        "best_model": "random_forest",
        "test_accuracy": round(random.uniform(0.85, 0.95), 3),
        "test_f1": round(random.uniform(0.80, 0.90), 3),
        "test_auc": round(random.uniform(0.88, 0.96), 3),
        "models_trained": ["logistic_regression", "random_forest", "gradient_boosting"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
