"""
Data validation utilities.
"""
import re
from typing import Any, Dict, List, Optional
from datetime import datetime, date
import pandas as pd


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def validate_date_range(start_date: date, end_date: date) -> bool:
    """Validate that start date is before end date."""
    return start_date <= end_date


def validate_employee_data(data: Dict[str, Any]) -> List[str]:
    """Validate employee data and return list of errors."""
    errors = []
    
    # Required fields
    required_fields = ['employee_id', 'name', 'email', 'department', 'position']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Email validation
    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors.append("Invalid email format")
    
    # Phone validation
    if 'phone' in data and data['phone']:
        if not validate_phone(data['phone']):
            errors.append("Invalid phone number format")
    
    # Numeric validations
    numeric_fields = ['age', 'salary', 'years_at_company']
    for field in numeric_fields:
        if field in data and data[field] is not None:
            try:
                value = float(data[field])
                if value < 0:
                    errors.append(f"{field} must be non-negative")
            except (ValueError, TypeError):
                errors.append(f"{field} must be a valid number")
    
    return errors


def validate_prediction_data(data: Dict[str, Any]) -> List[str]:
    """Validate data for prediction and return list of errors."""
    errors = []
    
    # Required features for prediction
    required_features = [
        'age', 'department', 'education', 'job_level', 'salary',
        'years_at_company', 'work_life_balance', 'job_satisfaction'
    ]
    
    for feature in required_features:
        if feature not in data or data[feature] is None:
            errors.append(f"Missing required feature: {feature}")
    
    return errors


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    return filename
