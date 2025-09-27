#!/usr/bin/env python3
"""
Data setup script for employee turnover project.
"""
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.core.config.settings import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample employee turnover data for testing."""
    logger.info("Creating sample employee turnover data")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define departments and their characteristics
    departments = {
        'IT': {'base_turnover': 0.2, 'avg_satisfaction': 0.6, 'avg_evaluation': 0.7},
        'HR': {'base_turnover': 0.15, 'avg_satisfaction': 0.7, 'avg_evaluation': 0.75},
        'Sales': {'base_turnover': 0.35, 'avg_satisfaction': 0.5, 'avg_evaluation': 0.65},
        'Marketing': {'base_turnover': 0.25, 'avg_satisfaction': 0.65, 'avg_evaluation': 0.7},
        'Finance': {'base_turnover': 0.18, 'avg_satisfaction': 0.68, 'avg_evaluation': 0.72},
        'Engineering': {'base_turnover': 0.22, 'avg_satisfaction': 0.62, 'avg_evaluation': 0.75},
        'Support': {'base_turnover': 0.3, 'avg_satisfaction': 0.55, 'avg_evaluation': 0.6},
        'Management': {'base_turnover': 0.12, 'avg_satisfaction': 0.75, 'avg_evaluation': 0.8}
    }
    
    # Salary levels
    salary_levels = ['low', 'medium', 'high']
    
    # Generate data
    n_employees = 1000
    data = []
    
    for i in range(n_employees):
        # Select department
        dept = np.random.choice(list(departments.keys()))
        dept_info = departments[dept]
        
        # Generate employee characteristics
        satisfaction = np.random.normal(dept_info['avg_satisfaction'], 0.15)
        satisfaction = np.clip(satisfaction, 0.1, 1.0)
        
        last_evaluation = np.random.normal(dept_info['avg_evaluation'], 0.1)
        last_evaluation = np.clip(last_evaluation, 0.3, 1.0)
        
        number_project = np.random.randint(2, 8)
        average_monthly_hours = np.random.normal(200, 30)
        average_monthly_hours = np.clip(average_monthly_hours, 100, 350)
        
        time_spend_company = np.random.randint(1, 11)
        work_accident = np.random.choice([0, 1], p=[0.9, 0.1])
        promotion_last_5years = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # Salary based on department and performance
        if last_evaluation > 0.8 and time_spend_company > 3:
            salary = np.random.choice(['medium', 'high'], p=[0.3, 0.7])
        elif last_evaluation < 0.5:
            salary = np.random.choice(['low', 'medium'], p=[0.7, 0.3])
        else:
            salary = np.random.choice(salary_levels, p=[0.3, 0.5, 0.2])
        
        # Calculate turnover probability based on multiple factors
        base_turnover = dept_info['base_turnover']
        
        # Adjust based on satisfaction
        if satisfaction < 0.3:
            turnover_prob = base_turnover + 0.3
        elif satisfaction < 0.5:
            turnover_prob = base_turnover + 0.2
        elif satisfaction > 0.8:
            turnover_prob = base_turnover - 0.1
        else:
            turnover_prob = base_turnover
        
        # Adjust based on evaluation
        if last_evaluation < 0.4:
            turnover_prob += 0.15
        elif last_evaluation > 0.8:
            turnover_prob -= 0.1
        
        # Adjust based on workload
        if average_monthly_hours > 250:
            turnover_prob += 0.1
        elif average_monthly_hours < 150:
            turnover_prob += 0.05
        
        # Adjust based on projects
        if number_project > 6:
            turnover_prob += 0.1
        elif number_project < 3:
            turnover_prob += 0.05
        
        # Adjust based on time at company
        if time_spend_company < 2:
            turnover_prob += 0.1
        elif time_spend_company > 7:
            turnover_prob -= 0.05
        
        # Adjust based on salary
        if salary == 'low':
            turnover_prob += 0.1
        elif salary == 'high':
            turnover_prob -= 0.05
        
        # Adjust based on promotion
        if promotion_last_5years == 0 and time_spend_company > 3:
            turnover_prob += 0.1
        
        # Ensure probability is between 0 and 1
        turnover_prob = np.clip(turnover_prob, 0.05, 0.95)
        
        # Determine if employee left
        left = np.random.choice([0, 1], p=[1-turnover_prob, turnover_prob])
        
        employee_data = {
            'employee_id': f'EMP_{i+1:04d}',
            'satisfaction_level': round(satisfaction, 3),
            'last_evaluation': round(last_evaluation, 3),
            'number_project': number_project,
            'average_montly_hours': int(average_monthly_hours),
            'time_spend_company': time_spend_company,
            'Work_accident': work_accident,
            'left': left,
            'promotion_last_5years': promotion_last_5years,
            'sales': dept,
            'salary': salary
        }
        
        data.append(employee_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to raw data directory
    raw_data_path = Path(settings.DATA_PATH) / "raw"
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    output_file = raw_data_path / "sample_employee_data.csv"
    df.to_csv(output_file, index=False)
    
    logger.info(f"Sample data created: {output_file}")
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Turnover rate: {df['left'].mean():.1%}")
    
    # Print summary statistics
    print("\nDataset Summary:")
    print(f"Total employees: {len(df)}")
    print(f"Turnover rate: {df['left'].mean():.1%}")
    print(f"Departments: {df['sales'].nunique()}")
    print(f"Salary distribution: {df['salary'].value_counts().to_dict()}")
    
    return output_file


def create_test_data():
    """Create smaller test dataset for development."""
    logger.info("Creating test dataset")
    
    # Smaller dataset for testing
    np.random.seed(123)
    n_employees = 100
    
    data = []
    for i in range(n_employees):
        employee_data = {
            'employee_id': f'TEST_{i+1:03d}',
            'satisfaction_level': round(np.random.uniform(0.1, 1.0), 3),
            'last_evaluation': round(np.random.uniform(0.3, 1.0), 3),
            'number_project': np.random.randint(2, 7),
            'average_montly_hours': np.random.randint(120, 300),
            'time_spend_company': np.random.randint(1, 8),
            'Work_accident': np.random.choice([0, 1], p=[0.9, 0.1]),
            'left': np.random.choice([0, 1], p=[0.7, 0.3]),
            'promotion_last_5years': np.random.choice([0, 1], p=[0.8, 0.2]),
            'sales': np.random.choice(['IT', 'HR', 'Sales', 'Marketing']),
            'salary': np.random.choice(['low', 'medium', 'high'], p=[0.3, 0.5, 0.2])
        }
        data.append(employee_data)
    
    df = pd.DataFrame(data)
    
    # Save to raw data directory
    raw_data_path = Path(settings.DATA_PATH) / "raw"
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    output_file = raw_data_path / "test_employee_data.csv"
    df.to_csv(output_file, index=False)
    
    logger.info(f"Test data created: {output_file}")
    return output_file


def setup_directories():
    """Setup required directories."""
    logger.info("Setting up data directories")
    
    base_path = Path(settings.DATA_PATH)
    directories = ['raw', 'processed', 'models', 'exports', 'logs']
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")
    
    # Create .gitkeep files
    for directory in directories:
        gitkeep_file = base_path / directory / ".gitkeep"
        if not gitkeep_file.exists():
            gitkeep_file.touch()
    
    logger.info("Directory setup completed")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup data for employee turnover project")
    parser.add_argument("--sample", action="store_true", help="Create sample dataset")
    parser.add_argument("--test", action="store_true", help="Create test dataset")
    parser.add_argument("--directories", action="store_true", help="Setup directories only")
    parser.add_argument("--all", action="store_true", help="Setup everything")
    
    args = parser.parse_args()
    
    if args.all or args.directories:
        setup_directories()
    
    if args.all or args.sample:
        create_sample_data()
    
    if args.all or args.test:
        create_test_data()
    
    if not any([args.sample, args.test, args.directories, args.all]):
        print("No action specified. Use --help for options.")
        print("Recommended: python setup_data.py --all")


if __name__ == "__main__":
    main()
