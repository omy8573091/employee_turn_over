"""
Machine Learning models service for employee turnover prediction.
"""
import pandas as pd
import numpy as np
import joblib
import json
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, precision_recall_curve, f1_score, accuracy_score
)
from sklearn.cluster import KMeans
from imblearn.over_sampling import SMOTE
from app.core.config.settings import settings
from app.exceptions.custom_exceptions import ModelNotFoundError, PredictionError, DataProcessingError

logger = logging.getLogger(__name__)


class MLModelsService:
    """Service for machine learning models and predictions."""
    
    def __init__(self):
        self.models_path = Path(settings.MODEL_PATH)
        self.models_path.mkdir(parents=True, exist_ok=True)
        
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.model_metadata = {}
        
        # Load existing models
        self._load_models()
    
    def train_models(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
        """Train multiple ML models for turnover prediction."""
        try:
            logger.info("Starting model training pipeline")
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Handle class imbalance with SMOTE
            smote = SMOTE(random_state=42)
            X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_balanced)
            X_test_scaled = scaler.transform(X_test)
            
            # Define models to train
            models_config = {
                'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
                'random_forest': RandomForestClassifier(
                    n_estimators=100, random_state=42, max_depth=10
                ),
                'gradient_boosting': GradientBoostingClassifier(
                    n_estimators=100, random_state=42, max_depth=6
                )
            }
            
            training_results = {
                'timestamp': datetime.now().isoformat(),
                'data_shape': {
                    'X_train': X_train.shape,
                    'X_test': X_test.shape,
                    'y_train': y_train.shape,
                    'y_test': y_test.shape
                },
                'models_performance': {},
                'best_model': None,
                'best_score': 0
            }
            
            # Train each model
            for model_name, model in models_config.items():
                logger.info(f"Training {model_name}")
                
                # Train model
                model.fit(X_train_scaled, y_train_balanced)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                
                # Calculate metrics
                metrics = self._calculate_metrics(y_test, y_pred, y_pred_proba)
                
                # Cross-validation score
                cv_scores = cross_val_score(
                    model, X_train_scaled, y_train_balanced, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
                    scoring='roc_auc'
                )
                
                model_performance = {
                    'metrics': metrics,
                    'cv_scores': {
                        'mean': float(cv_scores.mean()),
                        'std': float(cv_scores.std()),
                        'scores': cv_scores.tolist()
                    },
                    'feature_importance': self._get_feature_importance(model, X.columns)
                }
                
                training_results['models_performance'][model_name] = model_performance
                
                # Update best model
                if metrics['roc_auc'] > training_results['best_score']:
                    training_results['best_model'] = model_name
                    training_results['best_score'] = metrics['roc_auc']
                
                # Save model
                self._save_model(model_name, model, scaler, X.columns.tolist())
            
            # Save training results
            self._save_training_results(training_results)
            
            logger.info(f"Model training completed. Best model: {training_results['best_model']}")
            return training_results
            
        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise DataProcessingError(f"Model training failed: {str(e)}")
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray) -> Dict[str, float]:
        """Calculate comprehensive model metrics."""
        return {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(f1_score(y_true, y_pred, average='weighted')),
            'recall': float(f1_score(y_true, y_pred, average='weighted')),
            'f1_score': float(f1_score(y_true, y_pred, average='weighted')),
            'roc_auc': float(roc_auc_score(y_true, y_pred_proba)),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
    
    def _get_feature_importance(self, model, feature_names: List[str]) -> Dict[str, float]:
        """Get feature importance from model."""
        try:
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(feature_names, model.feature_importances_))
                # Sort by importance
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            elif hasattr(model, 'coef_'):
                # For logistic regression
                importance_dict = dict(zip(feature_names, abs(model.coef_[0])))
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            else:
                return {}
        except Exception as e:
            logger.warning(f"Could not extract feature importance: {str(e)}")
            return {}
    
    def _save_model(self, model_name: str, model, scaler, feature_names: List[str]):
        """Save trained model and metadata."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save model
            model_filename = f"{model_name}_{timestamp}.joblib"
            model_path = self.models_path / model_filename
            joblib.dump(model, model_path)
            
            # Save scaler
            scaler_filename = f"{model_name}_scaler_{timestamp}.joblib"
            scaler_path = self.models_path / scaler_filename
            joblib.dump(scaler, scaler_path)
            
            # Save metadata
            metadata = {
                'model_name': model_name,
                'timestamp': timestamp,
                'feature_names': feature_names,
                'model_path': str(model_path),
                'scaler_path': str(scaler_path),
                'version': settings.MODEL_VERSION
            }
            
            metadata_filename = f"{model_name}_metadata_{timestamp}.json"
            metadata_path = self.models_path / metadata_filename
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Update in-memory models
            self.models[model_name] = {
                'model': model,
                'scaler': scaler,
                'feature_names': feature_names,
                'metadata': metadata
            }
            
            logger.info(f"Model {model_name} saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {str(e)}")
            raise DataProcessingError(f"Failed to save model: {str(e)}")
    
    def _save_training_results(self, results: Dict[str, Any]):
        """Save training results to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_filename = f"training_results_{timestamp}.json"
            results_path = self.models_path / results_filename
            
            with open(results_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Training results saved: {results_path}")
            
        except Exception as e:
            logger.error(f"Error saving training results: {str(e)}")
    
    def _load_models(self):
        """Load existing models from disk."""
        try:
            model_files = list(self.models_path.glob("*_metadata_*.json"))
            
            for metadata_file in model_files:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                model_name = metadata['model_name']
                
                # Load model and scaler
                model = joblib.load(metadata['model_path'])
                scaler = joblib.load(metadata['scaler_path'])
                
                self.models[model_name] = {
                    'model': model,
                    'scaler': scaler,
                    'feature_names': metadata['feature_names'],
                    'metadata': metadata
                }
                
                logger.info(f"Loaded model: {model_name}")
            
        except Exception as e:
            logger.warning(f"Could not load existing models: {str(e)}")
    
    def predict_turnover(self, employee_data: Dict[str, Any], model_name: str = None) -> Dict[str, Any]:
        """Predict employee turnover probability."""
        try:
            # Use best model if no specific model requested
            if model_name is None:
                model_name = self._get_best_model()
            
            if model_name not in self.models:
                raise ModelNotFoundError(f"Model {model_name} not found")
            
            model_info = self.models[model_name]
            model = model_info['model']
            scaler = model_info['scaler']
            feature_names = model_info['feature_names']
            
            # Prepare features
            features = self._prepare_features(employee_data, feature_names)
            
            # Scale features
            features_scaled = scaler.transform([features])
            
            # Make prediction
            turnover_probability = float(model.predict_proba(features_scaled)[0][1])
            risk_zone = self._determine_risk_zone(turnover_probability)
            
            # Get feature importance for this prediction
            feature_importance = self._get_prediction_feature_importance(
                model, features, feature_names
            )
            
            prediction_result = {
                'turnover_probability': turnover_probability,
                'risk_zone': risk_zone,
                'model_used': model_name,
                'prediction_confidence': self._calculate_prediction_confidence(turnover_probability),
                'feature_importance': feature_importance,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Prediction completed: {turnover_probability:.3f} ({risk_zone})")
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error in turnover prediction: {str(e)}")
            raise PredictionError(f"Turnover prediction failed: {str(e)}")
    
    def _prepare_features(self, employee_data: Dict[str, Any], feature_names: List[str]) -> List[float]:
        """Prepare features for prediction."""
        features = []
        
        for feature_name in feature_names:
            if feature_name in employee_data:
                features.append(float(employee_data[feature_name]))
            elif feature_name.startswith('dept_'):
                # Handle department dummy variables
                dept_name = feature_name.replace('dept_', '')
                features.append(1.0 if employee_data.get('department') == dept_name else 0.0)
            elif feature_name == 'salary_encoded':
                # Handle salary encoding
                salary_mapping = {'low': 0, 'medium': 1, 'high': 2}
                features.append(float(salary_mapping.get(employee_data.get('salary', 'medium'), 1)))
            else:
                # Default value for missing features
                features.append(0.0)
        
        return features
    
    def _determine_risk_zone(self, probability: float) -> str:
        """Determine risk zone based on turnover probability."""
        if probability >= 0.8:
            return 'critical'
        elif probability >= 0.6:
            return 'high'
        elif probability >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_prediction_confidence(self, probability: float) -> str:
        """Calculate prediction confidence level."""
        distance_from_0_5 = abs(probability - 0.5)
        
        if distance_from_0_5 >= 0.3:
            return 'high'
        elif distance_from_0_5 >= 0.2:
            return 'medium'
        else:
            return 'low'
    
    def _get_prediction_feature_importance(self, model, features: List[float], feature_names: List[str]) -> Dict[str, float]:
        """Get feature importance for specific prediction."""
        try:
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(feature_names, model.feature_importances_))
                # Weight by actual feature values
                weighted_importance = {
                    name: importance * abs(features[i]) 
                    for i, (name, importance) in enumerate(importance_dict.items())
                }
                return dict(sorted(weighted_importance.items(), key=lambda x: x[1], reverse=True))
            else:
                return {}
        except Exception as e:
            logger.warning(f"Could not calculate prediction feature importance: {str(e)}")
            return {}
    
    def _get_best_model(self) -> str:
        """Get the best performing model."""
        if not self.models:
            raise ModelNotFoundError("No models available")
        
        # For now, return the first available model
        # In production, this would check performance metrics
        return list(self.models.keys())[0]
    
    def batch_predict(self, employees_data: List[Dict[str, Any]], model_name: str = None) -> List[Dict[str, Any]]:
        """Make batch predictions for multiple employees."""
        try:
            results = []
            
            for i, employee_data in enumerate(employees_data):
                try:
                    prediction = self.predict_turnover(employee_data, model_name)
                    prediction['employee_index'] = i
                    results.append(prediction)
                except Exception as e:
                    logger.error(f"Error predicting for employee {i}: {str(e)}")
                    results.append({
                        'employee_index': i,
                        'error': str(e),
                        'turnover_probability': None,
                        'risk_zone': None
                    })
            
            logger.info(f"Batch prediction completed: {len(results)} employees")
            return results
            
        except Exception as e:
            logger.error(f"Error in batch prediction: {str(e)}")
            raise PredictionError(f"Batch prediction failed: {str(e)}")
    
    def get_model_performance(self, model_name: str = None) -> Dict[str, Any]:
        """Get model performance metrics."""
        try:
            if model_name is None:
                model_name = self._get_best_model()
            
            if model_name not in self.models:
                raise ModelNotFoundError(f"Model {model_name} not found")
            
            # Load training results
            results_files = list(self.models_path.glob("training_results_*.json"))
            if not results_files:
                return {"error": "No training results found"}
            
            # Get latest results
            latest_results = max(results_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_results, 'r') as f:
                training_results = json.load(f)
            
            if model_name in training_results.get('models_performance', {}):
                return training_results['models_performance'][model_name]
            else:
                return {"error": f"No performance data for model {model_name}"}
                
        except Exception as e:
            logger.error(f"Error getting model performance: {str(e)}")
            return {"error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models."""
        models_info = []
        
        for model_name, model_info in self.models.items():
            models_info.append({
                'name': model_name,
                'version': model_info['metadata'].get('version', '1.0'),
                'timestamp': model_info['metadata'].get('timestamp'),
                'feature_count': len(model_info['feature_names']),
                'features': model_info['feature_names']
            })
        
        return models_info
    
    def retrain_model(self, X: pd.DataFrame, y: pd.Series, model_name: str) -> Dict[str, Any]:
        """Retrain a specific model with new data."""
        try:
            logger.info(f"Retraining model: {model_name}")
            
            # Train the model
            results = self.train_models(X, y)
            
            if model_name in results['models_performance']:
                logger.info(f"Model {model_name} retrained successfully")
                return {
                    'status': 'success',
                    'model_name': model_name,
                    'performance': results['models_performance'][model_name]
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Model {model_name} not found in training results'
                }
                
        except Exception as e:
            logger.error(f"Error retraining model {model_name}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
