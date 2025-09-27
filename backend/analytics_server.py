from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Employee Turnover Analytics API",
    description="Analytics API for Employee Turnover Prediction System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Analytics endpoints
@app.get("/api/v1/analytics/dashboard")
def get_dashboard():
    return {
        "total_employees": 14999,
        "employees_left": 3571,
        "turnover_rate": 0.238,
        "high_risk_employees": 3571,
        "safe_employees": 11428,
        "department_stats": [
            {"department": "sales", "total_employees": 4140, "employees_left": 1035, "turnover_rate": 0.25, "avg_satisfaction": 0.45},
            {"department": "technical", "total_employees": 2720, "employees_left": 544, "turnover_rate": 0.20, "avg_satisfaction": 0.55},
            {"department": "support", "total_employees": 2229, "employees_left": 669, "turnover_rate": 0.30, "avg_satisfaction": 0.35},
            {"department": "IT", "total_employees": 1227, "employees_left": 184, "turnover_rate": 0.15, "avg_satisfaction": 0.65},
            {"department": "product_mng", "total_employees": 902, "employees_left": 198, "turnover_rate": 0.22, "avg_satisfaction": 0.50},
            {"department": "marketing", "total_employees": 858, "employees_left": 240, "turnover_rate": 0.28, "avg_satisfaction": 0.42},
            {"department": "RandD", "total_employees": 787, "employees_left": 142, "turnover_rate": 0.18, "avg_satisfaction": 0.68},
            {"department": "accounting", "total_employees": 767, "employees_left": 184, "turnover_rate": 0.24, "avg_satisfaction": 0.48},
            {"department": "hr", "total_employees": 739, "employees_left": 192, "turnover_rate": 0.26, "avg_satisfaction": 0.40},
            {"department": "management", "total_employees": 630, "employees_left": 76, "turnover_rate": 0.12, "avg_satisfaction": 0.75}
        ]
    }

@app.get("/api/v1/analytics/risk-distribution")
def get_risk_distribution():
    return {
        "low": 11428,
        "medium": 3571,
        "high": 0,
        "critical": 0
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

@app.get("/api/v1/analytics/turnover-by-salary")
def get_turnover_by_salary():
    return [
        {"salary_level": "low", "turnover_rate": 0.35, "employee_count": 7316},
        {"salary_level": "medium", "turnover_rate": 0.18, "employee_count": 6446},
        {"salary_level": "high", "turnover_rate": 0.12, "employee_count": 1237}
    ]

@app.get("/api/v1/analytics/satisfaction-distribution")
def get_satisfaction_distribution():
    return [
        {"satisfaction_range": "0.0-0.2", "employee_count": 1200, "turnover_rate": 0.45},
        {"satisfaction_range": "0.2-0.4", "employee_count": 2100, "turnover_rate": 0.38},
        {"satisfaction_range": "0.4-0.6", "employee_count": 3500, "turnover_rate": 0.28},
        {"satisfaction_range": "0.6-0.8", "employee_count": 4200, "turnover_rate": 0.18},
        {"satisfaction_range": "0.8-1.0", "employee_count": 3999, "turnover_rate": 0.12}
    ]

@app.get("/api/v1/analytics/project-count-analysis")
def get_project_count_analysis():
    return [
        {"project_count": 2, "employee_count": 1200, "turnover_rate": 0.45, "avg_satisfaction": 0.35},
        {"project_count": 3, "employee_count": 2100, "turnover_rate": 0.38, "avg_satisfaction": 0.42},
        {"project_count": 4, "employee_count": 3500, "turnover_rate": 0.28, "avg_satisfaction": 0.55},
        {"project_count": 5, "employee_count": 4200, "turnover_rate": 0.18, "avg_satisfaction": 0.68},
        {"project_count": 6, "employee_count": 3999, "turnover_rate": 0.12, "avg_satisfaction": 0.78}
    ]

@app.get("/api/v1/analytics/clustering-analysis")
def get_clustering_analysis():
    return [
        {
            "cluster_id": 1,
            "cluster_name": "High Performers",
            "employee_count": 2500,
            "avg_satisfaction": 0.85,
            "avg_evaluation": 0.92,
            "turnover_rate": 0.08
        },
        {
            "cluster_id": 2,
            "cluster_name": "Satisfied Workers",
            "employee_count": 4200,
            "avg_satisfaction": 0.75,
            "avg_evaluation": 0.68,
            "turnover_rate": 0.15
        },
        {
            "cluster_id": 3,
            "cluster_name": "At Risk",
            "employee_count": 3800,
            "avg_satisfaction": 0.45,
            "avg_evaluation": 0.55,
            "turnover_rate": 0.35
        },
        {
            "cluster_id": 4,
            "cluster_name": "Disengaged",
            "employee_count": 4499,
            "avg_satisfaction": 0.25,
            "avg_evaluation": 0.42,
            "turnover_rate": 0.48
        }
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
        },
        {
            "employee_id": "EMP004",
            "employee_code": "EMP004",
            "department": "technical",
            "salary": "high",
            "risk_zone": "Medium Risk Zone (Orange)",
            "turnover_probability": 0.65,
            "prediction_date": "2024-01-15T10:30:00Z"
        },
        {
            "employee_id": "EMP005",
            "employee_code": "EMP005",
            "department": "IT",
            "salary": "medium",
            "risk_zone": "Medium Risk Zone (Orange)",
            "turnover_probability": 0.58,
            "prediction_date": "2024-01-15T10:30:00Z"
        }
    ]

if __name__ == "__main__":
    print("Starting Analytics Server on http://localhost:8000")
    uvicorn.run(
        "analytics_server:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
