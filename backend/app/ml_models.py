import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os
import logging

logger = logging.getLogger(__name__)

class MLModelManager:
    def __init__(self):
        self.models = {}
        self.scaler = None
        self.label_encoders = {}
        self.feature_columns = []
        self.model_path = "models/"
        os.makedirs(self.model_path, exist_ok=True)
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load employee data from file"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
            
            logger.info(f"Loaded data with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess data for model training"""
        try:
            # Separate features and target
            target_column = 'left'
            if target_column not in df.columns:
                raise ValueError(f"Target column '{target_column}' not found")
            
            # Separate categorical and numerical columns
            categorical_columns = ['sales', 'salary']
            numerical_columns = [col for col in df.columns if col not in categorical_columns + [target_column]]
            
            # Encode categorical variables
            df_processed = df.copy()
            for col in categorical_columns:
                if col in df.columns:
                    le = LabelEncoder()
                    df_processed[col] = le.fit_transform(df_processed[col])
                    self.label_encoders[col] = le
            
            # Prepare features and target
            X = df_processed.drop(columns=[target_column])
            y = df_processed[target_column]
            
            # Store feature columns
            self.feature_columns = X.columns.tolist()
            
            return X.values, y.values
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            raise
    
    def train_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Train multiple ML models"""
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Apply SMOTE to handle class imbalance
            smote = SMOTE(random_state=42, k_neighbors=3)
            X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train_smote)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Define models
            models = {
                'logistic_regression': LogisticRegression(
                    random_state=42, max_iter=1000, C=1.0, penalty='l2'
                ),
                'random_forest': RandomForestClassifier(
                    n_estimators=100, random_state=42, max_depth=10, 
                    min_samples_split=5, class_weight='balanced'
                ),
                'gradient_boosting': GradientBoostingClassifier(
                    n_estimators=100, random_state=42, learning_rate=0.1, 
                    max_depth=6, min_samples_split=5
                )
            }
            
            # Train models
            results = {}
            for name, model in models.items():
                logger.info(f"Training {name}...")
                model.fit(X_train_scaled, y_train_smote)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                
                # Calculate metrics
                from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
                
                results[name] = {
                    'model': model,
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred),
                    'recall': recall_score(y_test, y_pred),
                    'f1_score': f1_score(y_test, y_pred),
                    'auc_score': roc_auc_score(y_test, y_pred_proba)
                }
                
                # Save model
                model_path = os.path.join(self.model_path, f"{name}_model.joblib")
                joblib.dump(model, model_path)
                logger.info(f"Saved {name} model to {model_path}")
            
            # Save scaler and encoders
            joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.joblib"))
            joblib.dump(self.label_encoders, os.path.join(self.model_path, "label_encoders.joblib"))
            joblib.dump(self.feature_columns, os.path.join(self.model_path, "feature_columns.joblib"))
            
            # Find best model
            best_model = max(results.keys(), key=lambda x: results[x]['f1_score'])
            
            return {
                'results': results,
                'best_model': best_model,
                'test_accuracy': results[best_model]['accuracy'],
                'test_f1': results[best_model]['f1_score'],
                'test_auc': results[best_model]['auc_score']
            }
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            raise
    
    def load_trained_models(self) -> bool:
        """Load pre-trained models"""
        try:
            # Load scaler and encoders
            scaler_path = os.path.join(self.model_path, "scaler.joblib")
            encoders_path = os.path.join(self.model_path, "label_encoders.joblib")
            features_path = os.path.join(self.model_path, "feature_columns.joblib")
            
            if not all(os.path.exists(p) for p in [scaler_path, encoders_path, features_path]):
                logger.warning("Trained models not found")
                return False
            
            self.scaler = joblib.load(scaler_path)
            self.label_encoders = joblib.load(encoders_path)
            self.feature_columns = joblib.load(features_path)
            
            # Load models
            model_files = {
                'logistic_regression': 'logistic_regression_model.joblib',
                'random_forest': 'random_forest_model.joblib',
                'gradient_boosting': 'gradient_boosting_model.joblib'
            }
            
            for name, filename in model_files.items():
                model_path = os.path.join(self.model_path, filename)
                if os.path.exists(model_path):
                    self.models[name] = joblib.load(model_path)
                    logger.info(f"Loaded {name} model")
            
            return len(self.models) > 0
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def predict_turnover(self, employee_data: Dict[str, Any], model_name: str = 'random_forest') -> Dict[str, Any]:
        """Predict turnover probability for an employee"""
        try:
            if not self.models or model_name not in self.models:
                raise ValueError(f"Model {model_name} not found. Please train models first.")
            
            # Convert employee data to DataFrame
            df = pd.DataFrame([employee_data])
            
            # Preprocess data
            df_processed = df.copy()
            for col, encoder in self.label_encoders.items():
                if col in df_processed.columns:
                    df_processed[col] = encoder.transform(df_processed[col])
            
            # Ensure all required features are present
            for col in self.feature_columns:
                if col not in df_processed.columns:
                    df_processed[col] = 0  # Default value for missing features
            
            # Reorder columns to match training data
            X = df_processed[self.feature_columns]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            model = self.models[model_name]
            probability = model.predict_proba(X_scaled)[0, 1]
            
            # Determine risk zone
            if probability < 0.2:
                risk_zone = 'Safe Zone (Green)'
            elif probability < 0.6:
                risk_zone = 'Low Risk Zone (Yellow)'
            elif probability < 0.9:
                risk_zone = 'Medium Risk Zone (Orange)'
            else:
                risk_zone = 'High Risk Zone (Red)'
            
            return {
                'turnover_probability': float(probability),
                'risk_zone': risk_zone,
                'model_used': model_name,
                'prediction_confidence': 'High' if probability > 0.8 or probability < 0.2 else 'Medium'
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def get_feature_importance(self, model_name: str = 'random_forest') -> List[Dict[str, Any]]:
        """Get feature importance from tree-based models"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                feature_importance = [
                    {
                        'feature': feature,
                        'importance': float(importance)
                    }
                    for feature, importance in zip(self.feature_columns, importances)
                ]
                return sorted(feature_importance, key=lambda x: x['importance'], reverse=True)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            return []

# Global instance
ml_manager = MLModelManager()