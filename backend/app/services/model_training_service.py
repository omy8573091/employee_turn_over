"""
Model training service for comprehensive ML pipeline.
"""
import pandas as pd
import numpy as np
import joblib
import json
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, precision_recall_curve, f1_score, accuracy_score,
    precision_score, recall_score
)
from sklearn.cluster import KMeans
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import matplotlib.pyplot as plt
import seaborn as sns
from app.core.config.settings import settings
from app.exceptions.custom_exceptions import ModelNotFoundError, DataProcessingError

logger = logging.getLogger(__name__)


class ModelTrainingService:
    """Service for comprehensive model training and evaluation."""
    
    def __init__(self):
        self.models_path = Path(settings.MODEL_PATH)
        self.models_path.mkdir(parents=True, exist_ok=True)
        
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.model_metadata = {}
        self.training_history = []
        
        # Load existing models
        self._load_models()
    
    def train_comprehensive_models(
        self, 
        X: pd.DataFrame, 
        y: pd.Series, 
        test_size: float = 0.2,
        validation_size: float = 0.1
    ) -> Dict[str, Any]:
        """Train comprehensive set of models with hyperparameter tuning."""
        try:
            logger.info("Starting comprehensive model training pipeline")
            
            # Split data into train, validation, and test sets
            X_temp, X_test, y_temp, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            X_train, X_val, y_train, y_val = train_test_split(
                X_temp, y_temp, test_size=validation_size/(1-test_size), 
                random_state=42, stratify=y_temp
            )
            
            # Handle class imbalance
            X_train_balanced, y_train_balanced = self._handle_class_imbalance(X_train, y_train)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_balanced)
            X_val_scaled = scaler.transform(X_val)
            X_test_scaled = scaler.transform(X_test)
            
            # Define models with hyperparameter grids
            models_config = self._get_models_config()
            
            training_results = {
                'timestamp': datetime.now().isoformat(),
                'data_shape': {
                    'X_train': X_train.shape,
                    'X_val': X_val.shape,
                    'X_test': X_test.shape,
                    'y_train': y_train.shape,
                    'y_val': y_val.shape,
                    'y_test': y_test.shape
                },
                'class_distribution': {
                    'train': y_train.value_counts().to_dict(),
                    'test': y_test.value_counts().to_dict()
                },
                'models_performance': {},
                'best_model': None,
                'best_score': 0,
                'feature_importance': {},
                'hyperparameter_tuning': {}
            }
            
            # Train each model with hyperparameter tuning
            for model_name, config in models_config.items():
                logger.info(f"Training {model_name} with hyperparameter tuning")
                
                # Hyperparameter tuning
                best_model, best_params = self._tune_hyperparameters(
                    config['model'], config['param_grid'], 
                    X_train_scaled, y_train_balanced
                )
                
                # Train final model
                best_model.fit(X_train_scaled, y_train_balanced)
                
                # Evaluate on validation set
                val_pred = best_model.predict(X_val_scaled)
                val_pred_proba = best_model.predict_proba(X_val_scaled)[:, 1]
                
                # Evaluate on test set
                test_pred = best_model.predict(X_test_scaled)
                test_pred_proba = best_model.predict_proba(X_test_scaled)[:, 1]
                
                # Calculate comprehensive metrics
                val_metrics = self._calculate_comprehensive_metrics(y_val, val_pred, val_pred_proba)
                test_metrics = self._calculate_comprehensive_metrics(y_test, test_pred, test_pred_proba)
                
                # Cross-validation scores
                cv_scores = cross_val_score(
                    best_model, X_train_scaled, y_train_balanced, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
                    scoring='roc_auc'
                )
                
                # Feature importance
                feature_importance = self._get_feature_importance(best_model, X.columns)
                
                model_performance = {
                    'validation_metrics': val_metrics,
                    'test_metrics': test_metrics,
                    'cv_scores': {
                        'mean': float(cv_scores.mean()),
                        'std': float(cv_scores.std()),
                        'scores': cv_scores.tolist()
                    },
                    'feature_importance': feature_importance,
                    'best_hyperparameters': best_params,
                    'model_type': config['type']
                }
                
                training_results['models_performance'][model_name] = model_performance
                training_results['hyperparameter_tuning'][model_name] = best_params
                
                # Update best model
                if test_metrics['roc_auc'] > training_results['best_score']:
                    training_results['best_model'] = model_name
                    training_results['best_score'] = test_metrics['roc_auc']
                
                # Save model
                self._save_model(model_name, best_model, scaler, X.columns.tolist(), model_performance)
            
            # Train ensemble model
            ensemble_model = self._train_ensemble_model(models_config, X_train_scaled, y_train_balanced)
            ensemble_pred = ensemble_model.predict(X_test_scaled)
            ensemble_pred_proba = ensemble_model.predict_proba(X_test_scaled)[:, 1]
            ensemble_metrics = self._calculate_comprehensive_metrics(y_test, ensemble_pred, ensemble_pred_proba)
            
            training_results['models_performance']['ensemble'] = {
                'test_metrics': ensemble_metrics,
                'model_type': 'ensemble'
            }
            
            # Save ensemble model
            self._save_model('ensemble', ensemble_model, scaler, X.columns.tolist(), 
                           {'test_metrics': ensemble_metrics})
            
            # Generate model comparison report
            comparison_report = self._generate_model_comparison_report(training_results)
            training_results['model_comparison'] = comparison_report
            
            # Save training results
            self._save_training_results(training_results)
            
            # Generate visualizations
            self._generate_training_visualizations(training_results, X_test_scaled, y_test)
            
            logger.info(f"Comprehensive model training completed. Best model: {training_results['best_model']}")
            return training_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive model training: {str(e)}")
            raise DataProcessingError(f"Model training failed: {str(e)}")
    
    def _get_models_config(self) -> Dict[str, Dict[str, Any]]:
        """Get models configuration with hyperparameter grids."""
        return {
            'logistic_regression': {
                'model': LogisticRegression(random_state=42, max_iter=1000),
                'param_grid': {
                    'C': [0.1, 1, 10, 100],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear', 'saga']
                },
                'type': 'linear'
            },
            'random_forest': {
                'model': RandomForestClassifier(random_state=42),
                'param_grid': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [5, 10, 15, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'type': 'ensemble'
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(random_state=42),
                'param_grid': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'subsample': [0.8, 0.9, 1.0]
                },
                'type': 'ensemble'
            },
            'svm': {
                'model': SVC(random_state=42, probability=True),
                'param_grid': {
                    'C': [0.1, 1, 10],
                    'kernel': ['rbf', 'linear'],
                    'gamma': ['scale', 'auto', 0.001, 0.01]
                },
                'type': 'kernel'
            }
        }
    
    def _tune_hyperparameters(
        self, 
        model, 
        param_grid: Dict[str, List], 
        X_train: np.ndarray, 
        y_train: np.ndarray
    ) -> Tuple[Any, Dict[str, Any]]:
        """Perform hyperparameter tuning using GridSearchCV."""
        try:
            grid_search = GridSearchCV(
                model, param_grid, cv=3, scoring='roc_auc', 
                n_jobs=-1, verbose=0
            )
            grid_search.fit(X_train, y_train)
            
            return grid_search.best_estimator_, grid_search.best_params_
            
        except Exception as e:
            logger.warning(f"Hyperparameter tuning failed: {str(e)}")
            return model, {}
    
    def _handle_class_imbalance(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Handle class imbalance using SMOTE."""
        try:
            # Check if imbalance exists
            class_counts = np.bincount(y)
            imbalance_ratio = class_counts[0] / class_counts[1] if len(class_counts) > 1 else 1
            
            if imbalance_ratio > 2:  # Significant imbalance
                smote = SMOTE(random_state=42)
                X_balanced, y_balanced = smote.fit_resample(X, y)
                logger.info(f"Applied SMOTE. Original shape: {X.shape}, Balanced shape: {X_balanced.shape}")
                return X_balanced, y_balanced
            else:
                logger.info("No significant class imbalance detected")
                return X, y
                
        except Exception as e:
            logger.warning(f"SMOTE failed: {str(e)}")
            return X, y
    
    def _calculate_comprehensive_metrics(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        y_pred_proba: np.ndarray
    ) -> Dict[str, Any]:
        """Calculate comprehensive model metrics."""
        return {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, average='weighted')),
            'recall': float(recall_score(y_true, y_pred, average='weighted')),
            'f1_score': float(f1_score(y_true, y_pred, average='weighted')),
            'roc_auc': float(roc_auc_score(y_true, y_pred_proba)),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'classification_report': classification_report(y_true, y_pred, output_dict=True)
        }
    
    def _get_feature_importance(self, model, feature_names: List[str]) -> Dict[str, float]:
        """Get feature importance from model."""
        try:
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(feature_names, model.feature_importances_))
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            elif hasattr(model, 'coef_'):
                importance_dict = dict(zip(feature_names, abs(model.coef_[0])))
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            else:
                return {}
        except Exception as e:
            logger.warning(f"Could not extract feature importance: {str(e)}")
            return {}
    
    def _train_ensemble_model(
        self, 
        models_config: Dict[str, Dict[str, Any]], 
        X_train: np.ndarray, 
        y_train: np.ndarray
    ) -> VotingClassifier:
        """Train ensemble model using voting classifier."""
        try:
            # Select top models for ensemble
            estimators = []
            
            # Add logistic regression
            if 'logistic_regression' in models_config:
                lr = LogisticRegression(random_state=42, max_iter=1000)
                lr.fit(X_train, y_train)
                estimators.append(('lr', lr))
            
            # Add random forest
            if 'random_forest' in models_config:
                rf = RandomForestClassifier(n_estimators=100, random_state=42)
                rf.fit(X_train, y_train)
                estimators.append(('rf', rf))
            
            # Add gradient boosting
            if 'gradient_boosting' in models_config:
                gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
                gb.fit(X_train, y_train)
                estimators.append(('gb', gb))
            
            # Create voting classifier
            ensemble = VotingClassifier(estimators=estimators, voting='soft')
            ensemble.fit(X_train, y_train)
            
            logger.info(f"Ensemble model trained with {len(estimators)} base models")
            return ensemble
            
        except Exception as e:
            logger.error(f"Ensemble training failed: {str(e)}")
            raise DataProcessingError(f"Ensemble training failed: {str(e)}")
    
    def _generate_model_comparison_report(self, training_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive model comparison report."""
        models_performance = training_results['models_performance']
        
        comparison_data = []
        for model_name, performance in models_performance.items():
            if 'test_metrics' in performance:
                metrics = performance['test_metrics']
                comparison_data.append({
                    'model': model_name,
                    'accuracy': metrics['accuracy'],
                    'precision': metrics['precision'],
                    'recall': metrics['recall'],
                    'f1_score': metrics['f1_score'],
                    'roc_auc': metrics['roc_auc']
                })
        
        # Sort by ROC AUC
        comparison_data.sort(key=lambda x: x['roc_auc'], reverse=True)
        
        return {
            'ranking': comparison_data,
            'best_model': comparison_data[0]['model'] if comparison_data else None,
            'performance_summary': {
                'avg_accuracy': np.mean([m['accuracy'] for m in comparison_data]),
                'avg_roc_auc': np.mean([m['roc_auc'] for m in comparison_data]),
                'std_roc_auc': np.std([m['roc_auc'] for m in comparison_data])
            }
        }
    
    def _generate_training_visualizations(
        self, 
        training_results: Dict[str, Any], 
        X_test: np.ndarray, 
        y_test: np.ndarray
    ):
        """Generate training visualizations."""
        try:
            plots_path = Path(settings.DATA_PATH) / "exports" / "plots"
            plots_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Model performance comparison
            self._plot_model_comparison(training_results, plots_path, timestamp)
            
            # Feature importance plot
            self._plot_feature_importance(training_results, plots_path, timestamp)
            
            # ROC curves
            self._plot_roc_curves(training_results, X_test, y_test, plots_path, timestamp)
            
            logger.info(f"Training visualizations saved to {plots_path}")
            
        except Exception as e:
            logger.warning(f"Could not generate visualizations: {str(e)}")
    
    def _plot_model_comparison(self, training_results: Dict[str, Any], plots_path: Path, timestamp: str):
        """Plot model performance comparison."""
        try:
            models_performance = training_results['models_performance']
            
            metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
            model_names = []
            metric_values = {metric: [] for metric in metrics}
            
            for model_name, performance in models_performance.items():
                if 'test_metrics' in performance:
                    model_names.append(model_name)
                    for metric in metrics:
                        metric_values[metric].append(performance['test_metrics'][metric])
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            axes = axes.flatten()
            
            for i, metric in enumerate(metrics):
                axes[i].bar(model_names, metric_values[metric])
                axes[i].set_title(f'{metric.replace("_", " ").title()}')
                axes[i].set_ylabel(metric)
                axes[i].tick_params(axis='x', rotation=45)
            
            # Remove empty subplot
            axes[5].remove()
            
            plt.tight_layout()
            plt.savefig(plots_path / f"model_comparison_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Could not create model comparison plot: {str(e)}")
    
    def _plot_feature_importance(self, training_results: Dict[str, Any], plots_path: Path, timestamp: str):
        """Plot feature importance for best model."""
        try:
            best_model_name = training_results.get('best_model')
            if not best_model_name:
                return
            
            best_model_performance = training_results['models_performance'].get(best_model_name, {})
            feature_importance = best_model_performance.get('feature_importance', {})
            
            if not feature_importance:
                return
            
            # Get top 10 features
            top_features = dict(list(feature_importance.items())[:10])
            
            plt.figure(figsize=(10, 6))
            features = list(top_features.keys())
            importance = list(top_features.values())
            
            plt.barh(features, importance)
            plt.xlabel('Feature Importance')
            plt.title(f'Top 10 Feature Importance - {best_model_name.title()}')
            plt.gca().invert_yaxis()
            
            plt.tight_layout()
            plt.savefig(plots_path / f"feature_importance_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Could not create feature importance plot: {str(e)}")
    
    def _plot_roc_curves(
        self, 
        training_results: Dict[str, Any], 
        X_test: np.ndarray, 
        y_test: np.ndarray, 
        plots_path: Path, 
        timestamp: str
    ):
        """Plot ROC curves for all models."""
        try:
            plt.figure(figsize=(10, 8))
            
            models_performance = training_results['models_performance']
            
            for model_name, performance in models_performance.items():
                if 'test_metrics' in performance and model_name in self.models:
                    model_info = self.models[model_name]
                    model = model_info['model']
                    scaler = model_info['scaler']
                    
                    # Make predictions
                    X_test_scaled = scaler.transform(X_test)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                    
                    # Calculate ROC curve
                    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
                    auc_score = roc_auc_score(y_test, y_pred_proba)
                    
                    plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})')
            
            plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curves Comparison')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            plt.savefig(plots_path / f"roc_curves_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Could not create ROC curves plot: {str(e)}")
    
    def _save_model(
        self, 
        model_name: str, 
        model, 
        scaler, 
        feature_names: List[str], 
        performance: Dict[str, Any]
    ):
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
                'version': settings.MODEL_VERSION,
                'performance': performance
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
            results_filename = f"comprehensive_training_results_{timestamp}.json"
            results_path = self.models_path / results_filename
            
            with open(results_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Add to training history
            self.training_history.append({
                'timestamp': timestamp,
                'best_model': results.get('best_model'),
                'best_score': results.get('best_score'),
                'results_file': str(results_path)
            })
            
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
    
    def get_training_history(self) -> List[Dict[str, Any]]:
        """Get training history."""
        return self.training_history
    
    def get_model_performance_summary(self) -> Dict[str, Any]:
        """Get summary of all model performances."""
        summary = {
            'total_models': len(self.models),
            'model_list': list(self.models.keys()),
            'latest_training': None,
            'best_performance': 0,
            'best_model': None
        }
        
        if self.training_history:
            latest = self.training_history[-1]
            summary['latest_training'] = latest['timestamp']
            summary['best_performance'] = latest['best_score']
            summary['best_model'] = latest['best_model']
        
        return summary
