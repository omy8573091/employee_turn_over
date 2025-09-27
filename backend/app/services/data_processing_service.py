"""
Data processing service for employee turnover data.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import logging
from datetime import datetime
from app.core.config.settings import settings
from app.exceptions.custom_exceptions import DataProcessingError, DataValidationError

logger = logging.getLogger(__name__)


class DataProcessingService:
    """Service for processing employee turnover data."""
    
    def __init__(self):
        self.data_path = Path(settings.DATA_PATH)
        self.raw_path = self.data_path / "raw"
        self.processed_path = self.data_path / "processed"
        self.logs_path = self.data_path / "logs"
        
        # Ensure directories exist
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
    
    def load_raw_data(self, filename: str) -> pd.DataFrame:
        """Load raw data from file."""
        try:
            file_path = self.raw_path / filename
            
            if not file_path.exists():
                raise DataProcessingError(f"File not found: {filename}")
            
            # Determine file type and load accordingly
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif filename.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                raise DataProcessingError(f"Unsupported file format: {filename}")
            
            logger.info(f"Loaded raw data: {df.shape} from {filename}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading raw data: {str(e)}")
            raise DataProcessingError(f"Failed to load raw data: {str(e)}")
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and return quality report."""
        try:
            quality_report = {
                "timestamp": datetime.now().isoformat(),
                "shape": df.shape,
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
                "missing_values": {},
                "duplicates": df.duplicated().sum(),
                "data_types": {},
                "anomalies": {},
                "statistics": {}
            }
            
            # Missing values analysis
            missing_data = df.isnull().sum()
            quality_report["missing_values"] = {
                col: {
                    "count": int(missing_data[col]),
                    "percentage": float((missing_data[col] / len(df)) * 100)
                }
                for col in df.columns
            }
            
            # Data types
            quality_report["data_types"] = {
                col: str(dtype) for col, dtype in df.dtypes.items()
            }
            
            # Statistical summary for numerical columns
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            quality_report["statistics"] = df[numerical_cols].describe().to_dict()
            
            # Anomaly detection
            quality_report["anomalies"] = self._detect_anomalies(df)
            
            logger.info("Data quality validation completed")
            return quality_report
            
        except Exception as e:
            logger.error(f"Error in data quality validation: {str(e)}")
            raise DataProcessingError(f"Data quality validation failed: {str(e)}")
    
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect data anomalies."""
        anomalies = {}
        
        # Satisfaction level anomalies
        if 'satisfaction_level' in df.columns:
            extreme_satisfaction = df[
                (df['satisfaction_level'] < 0.1) | (df['satisfaction_level'] > 0.9)
            ]
            anomalies["extreme_satisfaction"] = {
                "count": len(extreme_satisfaction),
                "percentage": len(extreme_satisfaction) / len(df) * 100
            }
        
        # Working hours anomalies
        if 'average_montly_hours' in df.columns:
            extreme_hours = df[
                (df['average_montly_hours'] < 100) | (df['average_montly_hours'] > 350)
            ]
            anomalies["extreme_working_hours"] = {
                "count": len(extreme_hours),
                "percentage": len(extreme_hours) / len(df) * 100
            }
        
        # High evaluation but low satisfaction
        if 'last_evaluation' in df.columns and 'satisfaction_level' in df.columns:
            high_eval_low_satisfaction = df[
                (df['last_evaluation'] > 0.8) & (df['satisfaction_level'] < 0.3)
            ]
            anomalies["high_eval_low_satisfaction"] = {
                "count": len(high_eval_low_satisfaction),
                "percentage": len(high_eval_low_satisfaction) / len(df) * 100
            }
        
        return anomalies
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
        try:
            df_cleaned = df.copy()
            
            # Handle missing values
            df_cleaned = self._handle_missing_values(df_cleaned)
            
            # Handle outliers
            df_cleaned = self._handle_outliers(df_cleaned)
            
            # Standardize column names
            df_cleaned = self._standardize_column_names(df_cleaned)
            
            # Data type conversions
            df_cleaned = self._convert_data_types(df_cleaned)
            
            # Remove duplicates
            initial_count = len(df_cleaned)
            df_cleaned = df_cleaned.drop_duplicates()
            removed_duplicates = initial_count - len(df_cleaned)
            
            if removed_duplicates > 0:
                logger.info(f"Removed {removed_duplicates} duplicate records")
            
            logger.info(f"Data cleaning completed: {df_cleaned.shape}")
            return df_cleaned
            
        except Exception as e:
            logger.error(f"Error in data cleaning: {str(e)}")
            raise DataProcessingError(f"Data cleaning failed: {str(e)}")
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # For numerical columns, use median imputation
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        # For categorical columns, use mode imputation
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                df[col].fillna(mode_value, inplace=True)
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using IQR method."""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col in ['left', 'Work_accident', 'promotion_last_5years']:
                continue  # Skip binary columns
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names."""
        column_mapping = {
            'average_montly_hours': 'average_monthly_hours',
            'Work_accident': 'work_accident',
            'sales': 'department',
            'time_spend_company': 'time_spend_company'
        }
        
        df = df.rename(columns=column_mapping)
        return df
    
    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert data types appropriately."""
        # Ensure binary columns are integers
        binary_cols = ['left', 'work_accident', 'promotion_last_5years']
        for col in binary_cols:
            if col in df.columns:
                df[col] = df[col].astype(int)
        
        # Ensure satisfaction and evaluation are floats
        float_cols = ['satisfaction_level', 'last_evaluation']
        for col in float_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer new features for ML models."""
        try:
            df_features = df.copy()
            
            # Workload intensity (projects per month)
            if 'number_project' in df.columns and 'average_monthly_hours' in df.columns:
                df_features['workload_intensity'] = (
                    df_features['number_project'] / (df_features['average_monthly_hours'] / 160)
                )
            
            # Performance vs satisfaction ratio
            if 'last_evaluation' in df.columns and 'satisfaction_level' in df.columns:
                df_features['performance_satisfaction_ratio'] = (
                    df_features['last_evaluation'] / (df_features['satisfaction_level'] + 0.001)
                )
            
            # Risk score based on multiple factors
            risk_factors = []
            if 'satisfaction_level' in df.columns:
                risk_factors.append(1 - df_features['satisfaction_level'])
            if 'last_evaluation' in df.columns:
                risk_factors.append(1 - df_features['last_evaluation'])
            if 'promotion_last_5years' in df.columns:
                risk_factors.append(1 - df_features['promotion_last_5years'])
            
            if risk_factors:
                df_features['risk_score'] = np.mean(risk_factors, axis=0)
            
            # Department risk encoding
            if 'department' in df.columns:
                dept_turnover_rates = df_features.groupby('department')['left'].mean()
                df_features['department_risk'] = df_features['department'].map(dept_turnover_rates)
            
            # Salary risk encoding
            if 'salary' in df.columns:
                salary_mapping = {'low': 0.3, 'medium': 0.2, 'high': 0.1}
                df_features['salary_risk'] = df_features['salary'].map(salary_mapping)
            
            logger.info(f"Feature engineering completed: {df_features.shape}")
            return df_features
            
        except Exception as e:
            logger.error(f"Error in feature engineering: {str(e)}")
            raise DataProcessingError(f"Feature engineering failed: {str(e)}")
    
    def prepare_ml_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        """Prepare data for machine learning."""
        try:
            # Select features for ML
            feature_columns = [
                'satisfaction_level', 'last_evaluation', 'number_project',
                'average_monthly_hours', 'time_spend_company', 'work_accident',
                'promotion_last_5years'
            ]
            
            # Add engineered features if they exist
            engineered_features = [
                'workload_intensity', 'performance_satisfaction_ratio',
                'risk_score', 'department_risk', 'salary_risk'
            ]
            
            for feature in engineered_features:
                if feature in df.columns:
                    feature_columns.append(feature)
            
            # Handle categorical variables
            if 'department' in df.columns:
                df_encoded = pd.get_dummies(df, columns=['department'], prefix='dept')
                dept_columns = [col for col in df_encoded.columns if col.startswith('dept_')]
                feature_columns.extend(dept_columns)
            else:
                df_encoded = df.copy()
            
            if 'salary' in df.columns:
                salary_mapping = {'low': 0, 'medium': 1, 'high': 2}
                df_encoded['salary_encoded'] = df_encoded['salary'].map(salary_mapping)
                feature_columns.append('salary_encoded')
            
            # Prepare X and y
            X = df_encoded[feature_columns].copy()
            y = df_encoded['left'].copy()
            
            # Handle any remaining missing values
            X = X.fillna(X.median())
            
            logger.info(f"ML data prepared: X={X.shape}, y={y.shape}")
            return X, y, feature_columns
            
        except Exception as e:
            logger.error(f"Error preparing ML data: {str(e)}")
            raise DataProcessingError(f"ML data preparation failed: {str(e)}")
    
    def save_processed_data(self, df: pd.DataFrame, filename: str) -> str:
        """Save processed data to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            processed_filename = f"{timestamp}_{filename}"
            file_path = self.processed_path / processed_filename
            
            if filename.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif filename.endswith('.parquet'):
                df.to_parquet(file_path, index=False)
            else:
                df.to_csv(file_path, index=False)  # Default to CSV
            
            logger.info(f"Processed data saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            raise DataProcessingError(f"Failed to save processed data: {str(e)}")
    
    def process_data_pipeline(self, input_filename: str, output_filename: str = None) -> Dict[str, Any]:
        """Run the complete data processing pipeline."""
        try:
            pipeline_results = {
                "timestamp": datetime.now().isoformat(),
                "input_file": input_filename,
                "steps_completed": [],
                "quality_report": None,
                "output_file": None,
                "feature_columns": None,
                "data_shape": None
            }
            
            # Step 1: Load raw data
            logger.info("Step 1: Loading raw data")
            df = self.load_raw_data(input_filename)
            pipeline_results["steps_completed"].append("load_raw_data")
            
            # Step 2: Validate data quality
            logger.info("Step 2: Validating data quality")
            quality_report = self.validate_data_quality(df)
            pipeline_results["quality_report"] = quality_report
            pipeline_results["steps_completed"].append("validate_data_quality")
            
            # Step 3: Clean data
            logger.info("Step 3: Cleaning data")
            df_cleaned = self.clean_data(df)
            pipeline_results["steps_completed"].append("clean_data")
            
            # Step 4: Engineer features
            logger.info("Step 4: Engineering features")
            df_features = self.engineer_features(df_cleaned)
            pipeline_results["steps_completed"].append("engineer_features")
            
            # Step 5: Prepare ML data
            logger.info("Step 5: Preparing ML data")
            X, y, feature_columns = self.prepare_ml_data(df_features)
            pipeline_results["feature_columns"] = feature_columns
            pipeline_results["data_shape"] = {"X": X.shape, "y": y.shape}
            pipeline_results["steps_completed"].append("prepare_ml_data")
            
            # Step 6: Save processed data
            logger.info("Step 6: Saving processed data")
            if output_filename is None:
                output_filename = f"processed_{input_filename}"
            
            output_path = self.save_processed_data(df_features, output_filename)
            pipeline_results["output_file"] = output_path
            pipeline_results["steps_completed"].append("save_processed_data")
            
            logger.info("Data processing pipeline completed successfully")
            return pipeline_results
            
        except Exception as e:
            logger.error(f"Data processing pipeline failed: {str(e)}")
            raise DataProcessingError(f"Pipeline failed: {str(e)}")
    
    def get_processing_logs(self) -> List[Dict[str, Any]]:
        """Get processing logs."""
        try:
            log_files = list(self.logs_path.glob("*.log"))
            logs = []
            
            for log_file in log_files:
                with open(log_file, 'r') as f:
                    content = f.read()
                    logs.append({
                        "filename": log_file.name,
                        "size": log_file.stat().st_size,
                        "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat(),
                        "content": content[-1000:]  # Last 1000 characters
                    })
            
            return logs
            
        except Exception as e:
            logger.error(f"Error reading processing logs: {str(e)}")
            return []
