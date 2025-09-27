from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Employee Turnover Prediction API",
    description="Employee Turnover Prediction API for HR departments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Employee Turnover Prediction API",
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

# Mock endpoints for frontend
@app.get("/api/v1/analytics/dashboard")
def get_dashboard():
    return {
        "total_employees": 14999,
        "turnover_rate": 0.238,
        "high_risk_employees": 3571,
        "safe_employees": 11428
    }

@app.get("/api/v1/analytics/risk-distribution")
def get_risk_distribution():
    return {
        "Low Risk Zone (Green)": 11428,
        "Medium Risk Zone (Orange)": 3571,
        "High Risk Zone (Red)": 0
    }

@app.get("/api/v1/analytics/turnover-by-department")
def get_turnover_by_department():
    return [
        {"department": "sales", "turnover_rate": 0.25, "employee_count": 4140},
        {"department": "technical", "turnover_rate": 0.20, "employee_count": 2720},
        {"department": "support", "turnover_rate": 0.30, "employee_count": 2229},
        {"department": "IT", "turnover_rate": 0.15, "employee_count": 1227},
        {"department": "product_mng", "turnover_rate": 0.22, "employee_count": 902},
        {"department": "marketing", "turnover_rate": 0.28, "employee_count": 858},
        {"department": "RandD", "turnover_rate": 0.18, "employee_count": 787},
        {"department": "accounting", "turnover_rate": 0.24, "employee_count": 767},
        {"department": "hr", "turnover_rate": 0.26, "employee_count": 739},
        {"department": "management", "turnover_rate": 0.12, "employee_count": 630}
    ]

@app.get("/api/v1/predictions/high-risk-employees")
def get_high_risk_employees():
    return [
        {
            "employee_id": "EMP001",
            "employee_code": "EMP001",
            "department": "sales",
            "salary": "medium",
            "risk_zone": "High Risk Zone (Red)",
            "turnover_probability": 0.85,
            "prediction_date": "2024-01-15T10:30:00Z"
        },
        {
            "employee_id": "EMP002",
            "employee_code": "EMP002",
            "department": "support",
            "salary": "low",
            "risk_zone": "High Risk Zone (Red)",
            "turnover_probability": 0.78,
            "prediction_date": "2024-01-15T10:30:00Z"
        },
        {
            "employee_id": "EMP003",
            "employee_code": "EMP003",
            "department": "marketing",
            "salary": "medium",
            "risk_zone": "High Risk Zone (Red)",
            "turnover_probability": 0.72,
            "prediction_date": "2024-01-15T10:30:00Z"
        }
    ]

if __name__ == "__main__":
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
