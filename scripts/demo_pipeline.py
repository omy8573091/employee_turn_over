#!/usr/bin/env python3
"""
Demo script to showcase the complete Employee Turnover Prediction Pipeline
"""
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.data_processing_service import DataProcessingService
from app.services.data_validation_service import DataValidationService
from app.services.ml_models_service import MLModelsService
from app.services.model_training_service import ModelTrainingService
from app.services.retention_strategies_service import RetentionStrategiesService
from app.core.config.settings import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmployeeTurnoverDemo:
    """Demo class to showcase the complete pipeline."""
    
    def __init__(self):
        self.data_service = DataProcessingService()
        self.validation_service = DataValidationService()
        self.ml_service = MLModelsService()
        self.training_service = ModelTrainingService()
        self.retention_service = RetentionStrategiesService()
        
    def run_complete_demo(self):
        """Run the complete demo pipeline."""
        print("🚀 EMPLOYEE TURNOVER PREDICTION PIPELINE DEMO")
        print("=" * 60)
        
        try:
            # Step 1: Setup sample data
            print("\n📊 Step 1: Setting up sample data...")
            sample_data_path = self._setup_sample_data()
            
            # Step 2: Data validation
            print("\n🔍 Step 2: Data quality validation...")
            validation_results = self._demo_data_validation(sample_data_path)
            
            # Step 3: Data processing
            print("\n⚙️ Step 3: Data processing and feature engineering...")
            processed_data_path = self._demo_data_processing(sample_data_path)
            
            # Step 4: Model training
            print("\n🤖 Step 4: Machine learning model training...")
            training_results = self._demo_model_training(processed_data_path)
            
            # Step 5: Predictions
            print("\n🔮 Step 5: Making predictions...")
            predictions = self._demo_predictions()
            
            # Step 6: Retention strategies
            print("\n💡 Step 6: Generating retention strategies...")
            retention_plans = self._demo_retention_strategies(predictions)
            
            # Step 7: Summary report
            print("\n📋 Step 7: Generating summary report...")
            self._generate_demo_report(validation_results, training_results, predictions, retention_plans)
            
            print("\n✅ Demo completed successfully!")
            print("Check the 'data/exports' directory for generated reports and visualizations.")
            
        except Exception as e:
            logger.error(f"Demo failed: {str(e)}")
            print(f"❌ Demo failed: {str(e)}")
    
    def _setup_sample_data(self) -> str:
        """Setup sample data for demo."""
        # Create sample data
        np.random.seed(42)
        n_employees = 500
        
        data = []
        departments = ['IT', 'HR', 'Sales', 'Marketing', 'Finance', 'Engineering']
        
        for i in range(n_employees):
            # Generate realistic employee data
            satisfaction = np.random.beta(2, 2)  # Beta distribution for satisfaction
            last_evaluation = np.random.beta(3, 2)  # Slightly higher for evaluations
            
            # Create correlation between satisfaction and turnover
            turnover_prob = 0.3 - (satisfaction * 0.4) + np.random.normal(0, 0.1)
            turnover_prob = np.clip(turnover_prob, 0.05, 0.8)
            
            employee_data = {
                'employee_id': f'DEMO_{i+1:04d}',
                'satisfaction_level': round(satisfaction, 3),
                'last_evaluation': round(last_evaluation, 3),
                'number_project': np.random.randint(2, 7),
                'average_montly_hours': np.random.randint(120, 280),
                'time_spend_company': np.random.randint(1, 8),
                'Work_accident': np.random.choice([0, 1], p=[0.9, 0.1]),
                'left': np.random.choice([0, 1], p=[1-turnover_prob, turnover_prob]),
                'promotion_last_5years': np.random.choice([0, 1], p=[0.8, 0.2]),
                'sales': np.random.choice(departments),
                'salary': np.random.choice(['low', 'medium', 'high'], p=[0.3, 0.5, 0.2])
            }
            data.append(employee_data)
        
        # Create DataFrame and save
        df = pd.DataFrame(data)
        sample_file = Path(settings.DATA_PATH) / "raw" / "demo_sample_data.csv"
        sample_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(sample_file, index=False)
        
        print(f"   Created sample dataset: {df.shape}")
        print(f"   Turnover rate: {df['left'].mean():.1%}")
        print(f"   Departments: {df['sales'].nunique()}")
        
        return str(sample_file)
    
    def _demo_data_validation(self, data_path: str) -> dict:
        """Demo data validation."""
        # Load data
        df = pd.read_csv(data_path)
        
        # Run validation
        validation_results = self.validation_service.validate_data_quality(df)
        
        print(f"   Data quality score: {validation_results['data_quality_score']:.2f}")
        print(f"   Validation passed: {'✅' if validation_results['passed_validation'] else '❌'}")
        print(f"   Issues found: {validation_results['validation_summary']['total_issues_found']}")
        
        # Save validation report
        report = self.validation_service.get_validation_report(validation_results)
        report_file = Path(settings.DATA_PATH) / "exports" / "validation_report.txt"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"   Validation report saved: {report_file}")
        
        return validation_results
    
    def _demo_data_processing(self, data_path: str) -> str:
        """Demo data processing pipeline."""
        # Run processing pipeline
        processing_results = self.data_service.process_data_pipeline(
            "demo_sample_data.csv", "demo_processed_data.csv"
        )
        
        print(f"   Processing steps completed: {len(processing_results['steps_completed'])}")
        print(f"   Feature columns: {len(processing_results['feature_columns'])}")
        print(f"   Data shape: {processing_results['data_shape']}")
        
        return processing_results['output_file']
    
    def _demo_model_training(self, processed_data_path: str) -> dict:
        """Demo model training."""
        # Load processed data
        df = pd.read_csv(processed_data_path)
        
        # Prepare ML data
        X, y, feature_columns = self.data_service.prepare_ml_data(df)
        
        # Train models
        training_results = self.training_service.train_comprehensive_models(X, y)
        
        print(f"   Models trained: {len(training_results['models_performance'])}")
        print(f"   Best model: {training_results['best_model']}")
        print(f"   Best score: {training_results['best_score']:.3f}")
        
        # Print model comparison
        print("   Model Performance Comparison:")
        for model_name, performance in training_results['models_performance'].items():
            if 'test_metrics' in performance:
                metrics = performance['test_metrics']
                print(f"     {model_name}: AUC={metrics['roc_auc']:.3f}, F1={metrics['f1_score']:.3f}")
        
        return training_results
    
    def _demo_predictions(self) -> list:
        """Demo predictions on sample employees."""
        # Create sample employees for prediction
        sample_employees = [
            {
                'employee_id': 'HIGH_RISK_001',
                'satisfaction_level': 0.2,
                'last_evaluation': 0.6,
                'number_project': 6,
                'average_monthly_hours': 280,
                'time_spend_company': 2,
                'work_accident': 0,
                'promotion_last_5years': 0,
                'department': 'Sales',
                'salary': 'low'
            },
            {
                'employee_id': 'LOW_RISK_001',
                'satisfaction_level': 0.8,
                'last_evaluation': 0.9,
                'number_project': 4,
                'average_monthly_hours': 200,
                'time_spend_company': 5,
                'work_accident': 0,
                'promotion_last_5years': 1,
                'department': 'IT',
                'salary': 'high'
            },
            {
                'employee_id': 'MEDIUM_RISK_001',
                'satisfaction_level': 0.5,
                'last_evaluation': 0.7,
                'number_project': 3,
                'average_monthly_hours': 220,
                'time_spend_company': 3,
                'work_accident': 0,
                'promotion_last_5years': 0,
                'department': 'Marketing',
                'salary': 'medium'
            }
        ]
        
        predictions = []
        
        print("   Making predictions for sample employees:")
        for employee in sample_employees:
            try:
                prediction = self.ml_service.predict_turnover(employee)
                predictions.append({
                    'employee': employee,
                    'prediction': prediction
                })
                
                print(f"     {employee['employee_id']}: {prediction['turnover_probability']:.3f} ({prediction['risk_zone']})")
                
            except Exception as e:
                print(f"     {employee['employee_id']}: Error - {str(e)}")
        
        return predictions
    
    def _demo_retention_strategies(self, predictions: list) -> list:
        """Demo retention strategy generation."""
        retention_plans = []
        
        print("   Generating retention strategies:")
        for pred_data in predictions:
            employee = pred_data['employee']
            prediction = pred_data['prediction']
            
            try:
                retention_plan = self.retention_service.generate_retention_strategies(
                    employee, 
                    prediction['risk_zone'], 
                    prediction['turnover_probability']
                )
                
                retention_plans.append(retention_plan)
                
                print(f"     {employee['employee_id']}: {len(retention_plan['strategies'])} strategies, "
                      f"Cost: ${retention_plan['total_estimated_cost']['total_estimated_cost']}, "
                      f"Success: {retention_plan['success_probability']:.1%}")
                
            except Exception as e:
                print(f"     {employee['employee_id']}: Error - {str(e)}")
        
        return retention_plans
    
    def _generate_demo_report(
        self, 
        validation_results: dict, 
        training_results: dict, 
        predictions: list, 
        retention_plans: list
    ):
        """Generate comprehensive demo report."""
        report = {
            'demo_timestamp': datetime.now().isoformat(),
            'pipeline_summary': {
                'data_quality_score': validation_results['data_quality_score'],
                'validation_passed': validation_results['passed_validation'],
                'models_trained': len(training_results['models_performance']),
                'best_model': training_results['best_model'],
                'best_score': training_results['best_score'],
                'predictions_made': len(predictions),
                'retention_plans_generated': len(retention_plans)
            },
            'model_performance': training_results['models_performance'],
            'predictions_summary': [
                {
                    'employee_id': pred['employee']['employee_id'],
                    'turnover_probability': pred['prediction']['turnover_probability'],
                    'risk_zone': pred['prediction']['risk_zone'],
                    'model_used': pred['prediction']['model_used']
                }
                for pred in predictions
            ],
            'retention_plans_summary': [
                {
                    'employee_id': plan['employee_id'],
                    'risk_zone': plan['risk_zone'],
                    'strategies_count': len(plan['strategies']),
                    'estimated_cost': plan['total_estimated_cost']['total_estimated_cost'],
                    'success_probability': plan['success_probability']
                }
                for plan in retention_plans
            ],
            'recommendations': validation_results['recommendations']
        }
        
        # Save report
        report_file = Path(settings.DATA_PATH) / "exports" / "demo_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   Demo report saved: {report_file}")
        
        # Print summary
        print("\n📊 DEMO SUMMARY:")
        print(f"   Data Quality Score: {validation_results['data_quality_score']:.2f}")
        print(f"   Best Model: {training_results['best_model']} (AUC: {training_results['best_score']:.3f})")
        print(f"   Predictions Made: {len(predictions)}")
        print(f"   Retention Plans: {len(retention_plans)}")
        
        # Risk distribution
        risk_distribution = {}
        for pred in predictions:
            risk_zone = pred['prediction']['risk_zone']
            risk_distribution[risk_zone] = risk_distribution.get(risk_zone, 0) + 1
        
        print(f"   Risk Distribution: {risk_distribution}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Employee Turnover Prediction Pipeline Demo")
    parser.add_argument("--quick", action="store_true", help="Run quick demo with smaller dataset")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize and run demo
    demo = EmployeeTurnoverDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()
