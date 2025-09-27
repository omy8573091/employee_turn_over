"""
Data validation service for comprehensive data quality checks.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import logging
from scipy import stats
from app.exceptions.custom_exceptions import DataValidationError, DataProcessingError

logger = logging.getLogger(__name__)


class DataValidationService:
    """Service for comprehensive data validation and quality checks."""
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.quality_thresholds = self._load_quality_thresholds()
    
    def _load_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load validation rules for different data types."""
        return {
            'satisfaction_level': {
                'type': 'float',
                'min_value': 0.0,
                'max_value': 1.0,
                'required': True,
                'description': 'Employee satisfaction level (0-1)'
            },
            'last_evaluation': {
                'type': 'float',
                'min_value': 0.0,
                'max_value': 1.0,
                'required': True,
                'description': 'Last performance evaluation score (0-1)'
            },
            'number_project': {
                'type': 'int',
                'min_value': 1,
                'max_value': 10,
                'required': True,
                'description': 'Number of projects employee worked on'
            },
            'average_monthly_hours': {
                'type': 'int',
                'min_value': 50,
                'max_value': 400,
                'required': True,
                'description': 'Average monthly working hours'
            },
            'time_spend_company': {
                'type': 'int',
                'min_value': 1,
                'max_value': 15,
                'required': True,
                'description': 'Time spent at company in years'
            },
            'work_accident': {
                'type': 'int',
                'allowed_values': [0, 1],
                'required': True,
                'description': 'Work accident indicator (0/1)'
            },
            'left': {
                'type': 'int',
                'allowed_values': [0, 1],
                'required': True,
                'description': 'Employee left indicator (0/1)'
            },
            'promotion_last_5years': {
                'type': 'int',
                'allowed_values': [0, 1],
                'required': True,
                'description': 'Promotion in last 5 years (0/1)'
            },
            'department': {
                'type': 'str',
                'allowed_values': [
                    'IT', 'RandD', 'accounting', 'hr', 'management', 
                    'marketing', 'product_mng', 'sales', 'support', 'technical'
                ],
                'required': True,
                'description': 'Employee department'
            },
            'salary': {
                'type': 'str',
                'allowed_values': ['low', 'medium', 'high'],
                'required': True,
                'description': 'Salary level'
            }
        }
    
    def _load_quality_thresholds(self) -> Dict[str, float]:
        """Load data quality thresholds."""
        return {
            'max_missing_percentage': 5.0,  # Maximum 5% missing values
            'max_duplicate_percentage': 1.0,  # Maximum 1% duplicates
            'min_correlation_threshold': 0.1,  # Minimum correlation for feature relationships
            'max_outlier_percentage': 10.0,  # Maximum 10% outliers
            'min_data_consistency_score': 0.8,  # Minimum data consistency score
            'max_anomaly_percentage': 5.0  # Maximum 5% anomalies
        }
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive data quality validation."""
        try:
            logger.info("Starting comprehensive data quality validation")
            
            validation_results = {
                'timestamp': datetime.now().isoformat(),
                'dataset_shape': df.shape,
                'validation_summary': {},
                'field_validations': {},
                'data_quality_score': 0.0,
                'issues_found': [],
                'recommendations': [],
                'passed_validation': False
            }
            
            # 1. Basic data structure validation
            structure_validation = self._validate_data_structure(df)
            validation_results['structure_validation'] = structure_validation
            
            # 2. Field-level validation
            field_validations = self._validate_fields(df)
            validation_results['field_validations'] = field_validations
            
            # 3. Data completeness validation
            completeness_validation = self._validate_completeness(df)
            validation_results['completeness_validation'] = completeness_validation
            
            # 4. Data consistency validation
            consistency_validation = self._validate_consistency(df)
            validation_results['consistency_validation'] = consistency_validation
            
            # 5. Statistical validation
            statistical_validation = self._validate_statistics(df)
            validation_results['statistical_validation'] = statistical_validation
            
            # 6. Business rule validation
            business_validation = self._validate_business_rules(df)
            validation_results['business_validation'] = business_validation
            
            # 7. Anomaly detection
            anomaly_validation = self._detect_anomalies(df)
            validation_results['anomaly_validation'] = anomaly_validation
            
            # Calculate overall data quality score
            quality_score = self._calculate_quality_score(validation_results)
            validation_results['data_quality_score'] = quality_score
            
            # Determine if validation passed
            validation_results['passed_validation'] = quality_score >= self.quality_thresholds['min_data_consistency_score']
            
            # Generate recommendations
            recommendations = self._generate_recommendations(validation_results)
            validation_results['recommendations'] = recommendations
            
            # Generate summary
            summary = self._generate_validation_summary(validation_results)
            validation_results['validation_summary'] = summary
            
            logger.info(f"Data quality validation completed. Score: {quality_score:.2f}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error in data quality validation: {str(e)}")
            raise DataValidationError(f"Data quality validation failed: {str(e)}")
    
    def _validate_data_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate basic data structure."""
        structure_issues = []
        
        # Check if DataFrame is empty
        if df.empty:
            structure_issues.append("Dataset is empty")
        
        # Check minimum number of rows
        if len(df) < 10:
            structure_issues.append(f"Dataset has too few rows: {len(df)} (minimum: 10)")
        
        # Check for required columns
        required_columns = [col for col, rules in self.validation_rules.items() if rules.get('required', False)]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            structure_issues.append(f"Missing required columns: {missing_columns}")
        
        # Check for unexpected columns
        expected_columns = list(self.validation_rules.keys())
        unexpected_columns = [col for col in df.columns if col not in expected_columns]
        
        if unexpected_columns:
            structure_issues.append(f"Unexpected columns found: {unexpected_columns}")
        
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'required_columns_present': len(missing_columns) == 0,
            'missing_columns': missing_columns,
            'unexpected_columns': unexpected_columns,
            'issues': structure_issues,
            'passed': len(structure_issues) == 0
        }
    
    def _validate_fields(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate individual fields according to rules."""
        field_validations = {}
        
        for column, rules in self.validation_rules.items():
            if column not in df.columns:
                continue
            
            field_issues = []
            field_data = df[column]
            
            # Check data type
            expected_type = rules.get('type')
            if expected_type == 'int':
                if not pd.api.types.is_integer_dtype(field_data):
                    field_issues.append(f"Expected integer type, got {field_data.dtype}")
            elif expected_type == 'float':
                if not pd.api.types.is_numeric_dtype(field_data):
                    field_issues.append(f"Expected numeric type, got {field_data.dtype}")
            elif expected_type == 'str':
                if not pd.api.types.is_string_dtype(field_data) and not pd.api.types.is_object_dtype(field_data):
                    field_issues.append(f"Expected string type, got {field_data.dtype}")
            
            # Check value ranges
            if 'min_value' in rules:
                min_violations = (field_data < rules['min_value']).sum()
                if min_violations > 0:
                    field_issues.append(f"{min_violations} values below minimum ({rules['min_value']})")
            
            if 'max_value' in rules:
                max_violations = (field_data > rules['max_value']).sum()
                if max_violations > 0:
                    field_issues.append(f"{max_violations} values above maximum ({rules['max_value']})")
            
            # Check allowed values
            if 'allowed_values' in rules:
                invalid_values = field_data[~field_data.isin(rules['allowed_values'])].unique()
                if len(invalid_values) > 0:
                    field_issues.append(f"Invalid values found: {invalid_values.tolist()}")
            
            # Check for missing values
            missing_count = field_data.isnull().sum()
            missing_percentage = (missing_count / len(field_data)) * 100
            
            if missing_percentage > self.quality_thresholds['max_missing_percentage']:
                field_issues.append(f"Too many missing values: {missing_percentage:.1f}%")
            
            field_validations[column] = {
                'data_type': str(field_data.dtype),
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_percentage),
                'unique_values': int(field_data.nunique()),
                'issues': field_issues,
                'passed': len(field_issues) == 0
            }
        
        return field_validations
    
    def _validate_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data completeness."""
        completeness_issues = []
        
        # Check overall missing data
        total_missing = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        missing_percentage = (total_missing / total_cells) * 100
        
        if missing_percentage > self.quality_thresholds['max_missing_percentage']:
            completeness_issues.append(f"Overall missing data: {missing_percentage:.1f}%")
        
        # Check for completely empty columns
        empty_columns = df.columns[df.isnull().all()].tolist()
        if empty_columns:
            completeness_issues.append(f"Completely empty columns: {empty_columns}")
        
        # Check for completely empty rows
        empty_rows = df.isnull().all(axis=1).sum()
        if empty_rows > 0:
            completeness_issues.append(f"Completely empty rows: {empty_rows}")
        
        return {
            'total_missing_cells': int(total_missing),
            'missing_percentage': float(missing_percentage),
            'empty_columns': empty_columns,
            'empty_rows': int(empty_rows),
            'issues': completeness_issues,
            'passed': len(completeness_issues) == 0
        }
    
    def _validate_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data consistency."""
        consistency_issues = []
        
        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(df)) * 100
        
        if duplicate_percentage > self.quality_thresholds['max_duplicate_percentage']:
            consistency_issues.append(f"Too many duplicates: {duplicate_percentage:.1f}%")
        
        # Check logical consistency
        if 'satisfaction_level' in df.columns and 'last_evaluation' in df.columns:
            # Check for impossible combinations
            impossible_combinations = df[
                (df['satisfaction_level'] < 0.2) & (df['last_evaluation'] > 0.9)
            ]
            if len(impossible_combinations) > 0:
                consistency_issues.append(f"Impossible satisfaction-evaluation combinations: {len(impossible_combinations)}")
        
        # Check for negative values where not expected
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in ['satisfaction_level', 'last_evaluation']:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    consistency_issues.append(f"Negative values in {col}: {negative_count}")
        
        return {
            'duplicate_count': int(duplicate_count),
            'duplicate_percentage': float(duplicate_percentage),
            'issues': consistency_issues,
            'passed': len(consistency_issues) == 0
        }
    
    def _validate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate statistical properties of the data."""
        statistical_issues = []
        
        # Check for extreme outliers
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        outlier_summary = {}
        
        for col in numeric_columns:
            if col in ['left', 'work_accident', 'promotion_last_5years']:
                continue  # Skip binary columns
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR  # More conservative outlier detection
            upper_bound = Q3 + 3 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_percentage = (len(outliers) / len(df)) * 100
            
            outlier_summary[col] = {
                'count': len(outliers),
                'percentage': outlier_percentage
            }
            
            if outlier_percentage > self.quality_thresholds['max_outlier_percentage']:
                statistical_issues.append(f"Too many outliers in {col}: {outlier_percentage:.1f}%")
        
        # Check for normal distribution in key variables
        distribution_issues = []
        for col in ['satisfaction_level', 'last_evaluation']:
            if col in df.columns:
                # Shapiro-Wilk test for normality (on sample if too large)
                sample_size = min(1000, len(df))
                sample_data = df[col].dropna().sample(n=sample_size, random_state=42)
                
                if len(sample_data) > 3:
                    stat, p_value = stats.shapiro(sample_data)
                    if p_value < 0.05:  # Not normally distributed
                        distribution_issues.append(f"{col} is not normally distributed (p={p_value:.3f})")
        
        return {
            'outlier_summary': outlier_summary,
            'distribution_issues': distribution_issues,
            'issues': statistical_issues + distribution_issues,
            'passed': len(statistical_issues + distribution_issues) == 0
        }
    
    def _validate_business_rules(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate business rules and domain knowledge."""
        business_issues = []
        
        # Check turnover rate reasonableness
        if 'left' in df.columns:
            turnover_rate = df['left'].mean()
            if turnover_rate < 0.05 or turnover_rate > 0.5:
                business_issues.append(f"Unusual turnover rate: {turnover_rate:.1%}")
        
        # Check satisfaction vs turnover relationship
        if 'satisfaction_level' in df.columns and 'left' in df.columns:
            low_satisfaction_turnover = df[df['satisfaction_level'] < 0.3]['left'].mean()
            high_satisfaction_turnover = df[df['satisfaction_level'] > 0.7]['left'].mean()
            
            if low_satisfaction_turnover < high_satisfaction_turnover:
                business_issues.append("Counterintuitive: low satisfaction has lower turnover than high satisfaction")
        
        # Check working hours reasonableness
        if 'average_monthly_hours' in df.columns:
            avg_hours = df['average_monthly_hours'].mean()
            if avg_hours < 100 or avg_hours > 300:
                business_issues.append(f"Unusual average working hours: {avg_hours:.1f}")
        
        # Check project count vs time at company
        if 'number_project' in df.columns and 'time_spend_company' in df.columns:
            # New employees with too many projects
            new_employees_many_projects = df[
                (df['time_spend_company'] <= 1) & (df['number_project'] > 5)
            ]
            if len(new_employees_many_projects) > 0:
                business_issues.append(f"New employees with many projects: {len(new_employees_many_projects)}")
        
        return {
            'issues': business_issues,
            'passed': len(business_issues) == 0
        }
    
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect data anomalies."""
        anomalies = []
        
        # Extreme satisfaction levels
        if 'satisfaction_level' in df.columns:
            extreme_satisfaction = df[
                (df['satisfaction_level'] < 0.05) | (df['satisfaction_level'] > 0.95)
            ]
            if len(extreme_satisfaction) > 0:
                anomalies.append(f"Extreme satisfaction levels: {len(extreme_satisfaction)}")
        
        # Extreme working hours
        if 'average_monthly_hours' in df.columns:
            extreme_hours = df[
                (df['average_monthly_hours'] < 80) | (df['average_monthly_hours'] > 350)
            ]
            if len(extreme_hours) > 0:
                anomalies.append(f"Extreme working hours: {len(extreme_hours)}")
        
        # High evaluation but low satisfaction
        if 'last_evaluation' in df.columns and 'satisfaction_level' in df.columns:
            high_eval_low_satisfaction = df[
                (df['last_evaluation'] > 0.8) & (df['satisfaction_level'] < 0.3)
            ]
            if len(high_eval_low_satisfaction) > 0:
                anomalies.append(f"High evaluation but low satisfaction: {len(high_eval_low_satisfaction)}")
        
        # Long tenure but no promotion
        if 'time_spend_company' in df.columns and 'promotion_last_5years' in df.columns:
            long_tenure_no_promotion = df[
                (df['time_spend_company'] > 7) & (df['promotion_last_5years'] == 0)
            ]
            if len(long_tenure_no_promotion) > 0:
                anomalies.append(f"Long tenure but no promotion: {len(long_tenure_no_promotion)}")
        
        anomaly_percentage = (sum(len(df[condition]) for condition in [
            (df['satisfaction_level'] < 0.05) | (df['satisfaction_level'] > 0.95) if 'satisfaction_level' in df.columns else False,
            (df['average_monthly_hours'] < 80) | (df['average_monthly_hours'] > 350) if 'average_monthly_hours' in df.columns else False
        ]) / len(df)) * 100
        
        return {
            'anomalies': anomalies,
            'anomaly_percentage': float(anomaly_percentage),
            'passed': anomaly_percentage <= self.quality_thresholds['max_anomaly_percentage']
        }
    
    def _calculate_quality_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall data quality score."""
        scores = []
        
        # Structure validation score
        structure_passed = validation_results['structure_validation']['passed']
        scores.append(1.0 if structure_passed else 0.0)
        
        # Field validation score
        field_validations = validation_results['field_validations']
        field_scores = [1.0 if field['passed'] else 0.0 for field in field_validations.values()]
        scores.append(np.mean(field_scores) if field_scores else 0.0)
        
        # Completeness score
        completeness_passed = validation_results['completeness_validation']['passed']
        scores.append(1.0 if completeness_passed else 0.0)
        
        # Consistency score
        consistency_passed = validation_results['consistency_validation']['passed']
        scores.append(1.0 if consistency_passed else 0.0)
        
        # Statistical validation score
        statistical_passed = validation_results['statistical_validation']['passed']
        scores.append(1.0 if statistical_passed else 0.0)
        
        # Business validation score
        business_passed = validation_results['business_validation']['passed']
        scores.append(1.0 if business_passed else 0.0)
        
        # Anomaly detection score
        anomaly_passed = validation_results['anomaly_validation']['passed']
        scores.append(1.0 if anomaly_passed else 0.0)
        
        return float(np.mean(scores))
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        # Structure recommendations
        if not validation_results['structure_validation']['passed']:
            recommendations.append("Fix data structure issues before proceeding")
        
        # Field recommendations
        field_validations = validation_results['field_validations']
        for field, validation in field_validations.items():
            if not validation['passed']:
                recommendations.append(f"Review and fix issues in {field} field")
        
        # Completeness recommendations
        if not validation_results['completeness_validation']['passed']:
            recommendations.append("Address missing data issues")
        
        # Consistency recommendations
        if not validation_results['consistency_validation']['passed']:
            recommendations.append("Remove duplicates and fix consistency issues")
        
        # Statistical recommendations
        if not validation_results['statistical_validation']['passed']:
            recommendations.append("Review and handle outliers appropriately")
        
        # Business rule recommendations
        if not validation_results['business_validation']['passed']:
            recommendations.append("Review data for business rule violations")
        
        # Anomaly recommendations
        if not validation_results['anomaly_validation']['passed']:
            recommendations.append("Investigate and handle data anomalies")
        
        # General recommendations
        quality_score = validation_results['data_quality_score']
        if quality_score < 0.8:
            recommendations.append("Overall data quality is below acceptable threshold")
        elif quality_score < 0.9:
            recommendations.append("Data quality is acceptable but could be improved")
        
        return recommendations
    
    def _generate_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation summary."""
        total_issues = 0
        for section in ['structure_validation', 'completeness_validation', 'consistency_validation', 
                       'statistical_validation', 'business_validation', 'anomaly_validation']:
            if section in validation_results:
                total_issues += len(validation_results[section].get('issues', []))
        
        field_issues = sum(1 for field in validation_results['field_validations'].values() if not field['passed'])
        
        return {
            'total_issues_found': total_issues + field_issues,
            'quality_score': validation_results['data_quality_score'],
            'validation_passed': validation_results['passed_validation'],
            'critical_issues': total_issues,
            'field_issues': field_issues,
            'recommendations_count': len(validation_results['recommendations'])
        }
    
    def validate_single_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single employee record."""
        try:
            validation_results = {
                'record_id': record.get('employee_id', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'field_validations': {},
                'overall_passed': True,
                'issues': []
            }
            
            for field, rules in self.validation_rules.items():
                if field not in record:
                    if rules.get('required', False):
                        validation_results['field_validations'][field] = {
                            'passed': False,
                            'issue': 'Required field missing'
                        }
                        validation_results['overall_passed'] = False
                        validation_results['issues'].append(f"Missing required field: {field}")
                    continue
                
                value = record[field]
                field_issues = []
                
                # Type validation
                if rules.get('type') == 'int' and not isinstance(value, int):
                    field_issues.append(f"Expected integer, got {type(value).__name__}")
                elif rules.get('type') == 'float' and not isinstance(value, (int, float)):
                    field_issues.append(f"Expected number, got {type(value).__name__}")
                elif rules.get('type') == 'str' and not isinstance(value, str):
                    field_issues.append(f"Expected string, got {type(value).__name__}")
                
                # Range validation
                if 'min_value' in rules and value < rules['min_value']:
                    field_issues.append(f"Value below minimum: {value} < {rules['min_value']}")
                
                if 'max_value' in rules and value > rules['max_value']:
                    field_issues.append(f"Value above maximum: {value} > {rules['max_value']}")
                
                # Allowed values validation
                if 'allowed_values' in rules and value not in rules['allowed_values']:
                    field_issues.append(f"Invalid value: {value} not in {rules['allowed_values']}")
                
                validation_results['field_validations'][field] = {
                    'passed': len(field_issues) == 0,
                    'issues': field_issues
                }
                
                if field_issues:
                    validation_results['overall_passed'] = False
                    validation_results['issues'].extend([f"{field}: {issue}" for issue in field_issues])
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating single record: {str(e)}")
            raise DataValidationError(f"Single record validation failed: {str(e)}")
    
    def get_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable validation report."""
        report = []
        report.append("=" * 60)
        report.append("DATA QUALITY VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {validation_results['timestamp']}")
        report.append(f"Dataset Shape: {validation_results['dataset_shape']}")
        report.append(f"Quality Score: {validation_results['data_quality_score']:.2f}")
        report.append(f"Validation Passed: {'YES' if validation_results['passed_validation'] else 'NO'}")
        report.append("")
        
        # Summary
        summary = validation_results['validation_summary']
        report.append("SUMMARY:")
        report.append(f"  Total Issues: {summary['total_issues_found']}")
        report.append(f"  Critical Issues: {summary['critical_issues']}")
        report.append(f"  Field Issues: {summary['field_issues']}")
        report.append("")
        
        # Field validations
        report.append("FIELD VALIDATIONS:")
        for field, validation in validation_results['field_validations'].items():
            status = "PASS" if validation['passed'] else "FAIL"
            report.append(f"  {field}: {status}")
            if not validation['passed'] and validation.get('issues'):
                for issue in validation['issues']:
                    report.append(f"    - {issue}")
        report.append("")
        
        # Recommendations
        if validation_results['recommendations']:
            report.append("RECOMMENDATIONS:")
            for i, rec in enumerate(validation_results['recommendations'], 1):
                report.append(f"  {i}. {rec}")
        
        report.append("=" * 60)
        
        return "\n".join(report)
