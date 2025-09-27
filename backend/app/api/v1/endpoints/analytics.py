from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.api.deps import get_current_user
from app.models import User
from app.schemas import (
    AnalyticsSummary, RiskZoneDistribution, TurnoverByDepartment,
    TurnoverBySalary, SatisfactionDistribution, ProjectCountAnalysis,
    ClusteringAnalysis, DepartmentStats, SalaryStats
)

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsSummary)
async def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard analytics summary"""
    # Mock data for demo
    return AnalyticsSummary(
        total_employees=14999,
        employees_left=3571,
        turnover_rate=0.238,
        high_risk_employees=1250,
        safe_employees=8500,
        department_stats=[
            DepartmentStats(
                department="sales",
                total_employees=4140,
                employees_left=1012,
                turnover_rate=0.244,
                avg_satisfaction=0.612
            ),
            DepartmentStats(
                department="technical",
                total_employees=2720,
                employees_left=512,
                turnover_rate=0.188,
                avg_satisfaction=0.678
            ),
            DepartmentStats(
                department="support",
                total_employees=2229,
                employees_left=555,
                turnover_rate=0.249,
                avg_satisfaction=0.589
            ),
            DepartmentStats(
                department="IT",
                total_employees=1227,
                employees_left=276,
                turnover_rate=0.225,
                avg_satisfaction=0.634
            ),
            DepartmentStats(
                department="product_mng",
                total_employees=902,
                employees_left=198,
                turnover_rate=0.219,
                avg_satisfaction=0.645
            ),
            DepartmentStats(
                department="marketing",
                total_employees=857,
                employees_left=205,
                turnover_rate=0.239,
                avg_satisfaction=0.612
            ),
            DepartmentStats(
                department="RandD",
                total_employees=787,
                employees_left=175,
                turnover_rate=0.222,
                avg_satisfaction=0.656
            ),
            DepartmentStats(
                department="accounting",
                total_employees=767,
                employees_left=204,
                turnover_rate=0.266,
                avg_satisfaction=0.587
            ),
            DepartmentStats(
                department="hr",
                total_employees=739,
                employees_left=179,
                turnover_rate=0.242,
                avg_satisfaction=0.601
            ),
            DepartmentStats(
                department="management",
                total_employees=630,
                employees_left=255,
                turnover_rate=0.405,
                avg_satisfaction=0.523
            )
        ],
        salary_stats=[
            SalaryStats(
                salary_level="low",
                total_employees=7316,
                employees_left=2172,
                turnover_rate=0.297,
                avg_satisfaction=0.567
            ),
            SalaryStats(
                salary_level="medium",
                total_employees=6446,
                employees_left=1234,
                turnover_rate=0.191,
                avg_satisfaction=0.678
            ),
            SalaryStats(
                salary_level="high",
                total_employees=1237,
                employees_left=165,
                turnover_rate=0.133,
                avg_satisfaction=0.745
            )
        ]
    )

@router.get("/risk-distribution")
async def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get risk zone distribution"""
    return {
        "low": 3500,
        "medium": 2000,
        "high": 999,
        "critical": 500
    }

@router.get("/turnover-by-department")
async def get_turnover_by_department(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get turnover statistics by department"""
    return [
        {
            "department": "management",
            "employee_count": 630,
            "turnover_rate": 0.405
        },
        {
            "department": "sales",
            "employee_count": 4140,
            "turnover_rate": 0.244
        },
        {
            "department": "support",
            "employee_count": 2229,
            "turnover_rate": 0.249
        },
        {
            "department": "marketing",
            "employee_count": 857,
            "turnover_rate": 0.239
        },
        {
            "department": "accounting",
            "employee_count": 767,
            "turnover_rate": 0.266
        },
        {
            "department": "hr",
            "employee_count": 739,
            "turnover_rate": 0.242
        },
        {
            "department": "product_mng",
            "employee_count": 902,
            "turnover_rate": 0.219
        },
        {
            "department": "RandD",
            "employee_count": 787,
            "turnover_rate": 0.222
        },
        {
            "department": "IT",
            "employee_count": 1227,
            "turnover_rate": 0.225
        },
        {
            "department": "technical",
            "employee_count": 2720,
            "turnover_rate": 0.188
        }
    ]

@router.get("/turnover-by-salary")
async def get_turnover_by_salary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get turnover statistics by salary level"""
    return [
        {
            "salary_level": "low",
            "employee_count": 7316,
            "turnover_rate": 0.297
        },
        {
            "salary_level": "medium",
            "employee_count": 6446,
            "turnover_rate": 0.191
        },
        {
            "salary_level": "high",
            "employee_count": 1237,
            "turnover_rate": 0.133
        }
    ]

@router.get("/satisfaction-distribution")
async def get_satisfaction_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get satisfaction level distribution by turnover status"""
    return [
        {
            "satisfaction_range": "0.0-0.2",
            "employee_count": 1200,
            "turnover_rate": 0.85
        },
        {
            "satisfaction_range": "0.2-0.4",
            "employee_count": 1800,
            "turnover_rate": 0.72
        },
        {
            "satisfaction_range": "0.4-0.6",
            "employee_count": 2500,
            "turnover_rate": 0.45
        },
        {
            "satisfaction_range": "0.6-0.8",
            "employee_count": 3200,
            "turnover_rate": 0.25
        },
        {
            "satisfaction_range": "0.8-1.0",
            "employee_count": 2800,
            "turnover_rate": 0.12
        }
    ]

@router.get("/project-count-analysis")
async def get_project_count_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get turnover analysis by project count"""
    return [
        {
            "project_count": 2,
            "employee_count": 2834,
            "turnover_rate": 0.354,
            "avg_satisfaction": 0.456
        },
        {
            "project_count": 3,
            "employee_count": 2385,
            "turnover_rate": 0.215,
            "avg_satisfaction": 0.634
        },
        {
            "project_count": 4,
            "employee_count": 2156,
            "turnover_rate": 0.206,
            "avg_satisfaction": 0.689
        },
        {
            "project_count": 5,
            "employee_count": 1987,
            "turnover_rate": 0.213,
            "avg_satisfaction": 0.667
        },
        {
            "project_count": 6,
            "employee_count": 1876,
            "turnover_rate": 0.243,
            "avg_satisfaction": 0.612
        },
        {
            "project_count": 7,
            "employee_count": 3761,
            "turnover_rate": 0.195,
            "avg_satisfaction": 0.678
        }
    ]

@router.get("/clustering-analysis")
async def get_clustering_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get clustering analysis for employees who left"""
    return [
        {
            "cluster_id": 0,
            "cluster_name": "Disengaged Employees",
            "employee_count": 1245,
            "avg_satisfaction": 0.234,
            "avg_evaluation": 0.312,
            "turnover_rate": 0.89
        },
        {
            "cluster_id": 1,
            "cluster_name": "Overworked High Performers",
            "employee_count": 1456,
            "avg_satisfaction": 0.345,
            "avg_evaluation": 0.789,
            "turnover_rate": 0.76
        },
        {
            "cluster_id": 2,
            "cluster_name": "Underperformers",
            "employee_count": 870,
            "avg_satisfaction": 0.678,
            "avg_evaluation": 0.423,
            "turnover_rate": 0.45
        }
    ]