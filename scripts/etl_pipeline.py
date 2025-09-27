#!/usr/bin/env python3
"""
ETL Pipeline for Employee Turnover Data Processing
"""
import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.data_processing_service import DataProcessingService
from app.services.ml_models_service import MLModelsService
from app.services.retention_strategies_service import RetentionStrategiesService
from app.core.config.settings import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Complete ETL pipeline for employee turnover data."""
    
    def __init__(self):
        self.data_service = DataProcessingService()
        self.ml_service = MLModelsService()
        self.retention_service = RetentionStrategiesService()
        
    def run_complete_pipeline(self, input_file: str, output_prefix: str = None) -> dict:
        """Run the complete ETL pipeline."""
        try:
            logger.info("Starting complete ETL pipeline")
            pipeline_start = datetime.now()
            
            if output_prefix is None:
                output_prefix = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Step 1: Extract and Transform Data
            logger.info("Step 1: Data Processing")
            processing_results = self.data_service.process_data_pipeline(
                input_file, f"{output_prefix}_cleaned.csv"
            )
            
            # Step 2: Load processed data for ML
            logger.info("Step 2: Loading processed data for ML")
            processed_file = processing_results["output_file"]
            df = pd.read_csv(processed_file)
            
            # Prepare ML data
            X, y, feature_columns = self.data_service.prepare_ml_data(df)
            
            # Step 3: Train ML Models
            logger.info("Step 3: Training ML Models")
            training_results = self.ml_service.train_models(X, y)
            
            # Step 4: Generate sample predictions and retention strategies
            logger.info("Step 4: Generating sample predictions")
            sample_predictions = self._generate_sample_predictions(df, feature_columns)
            
            # Step 5: Create data exports
            logger.info("Step 5: Creating data exports")
            exports = self._create_data_exports(df, sample_predictions, training_results)
            
            pipeline_end = datetime.now()
            pipeline_duration = (pipeline_end - pipeline_start).total_seconds()
            
            pipeline_summary = {
                "pipeline_start": pipeline_start.isoformat(),
                "pipeline_end": pipeline_end.isoformat(),
                "pipeline_duration_seconds": pipeline_duration,
                "input_file": input_file,
                "output_prefix": output_prefix,
                "processing_results": processing_results,
                "training_results": training_results,
                "sample_predictions_count": len(sample_predictions),
                "exports_created": exports,
                "status": "success"
            }
            
            # Save pipeline summary
            self._save_pipeline_summary(pipeline_summary, output_prefix)
            
            logger.info(f"ETL pipeline completed successfully in {pipeline_duration:.2f} seconds")
            return pipeline_summary
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "pipeline_end": datetime.now().isoformat()
            }
    
    def _generate_sample_predictions(self, df: pd.DataFrame, feature_columns: list) -> list:
        """Generate sample predictions for demonstration."""
        sample_predictions = []
        
        # Take a sample of employees for prediction
        sample_size = min(50, len(df))
        sample_df = df.sample(n=sample_size, random_state=42)
        
        for idx, row in sample_df.iterrows():
            try:
                # Prepare employee data for prediction
                employee_data = {
                    "employee_id": f"EMP_{idx:04d}",
                    "satisfaction_level": row.get("satisfaction_level", 0.5),
                    "last_evaluation": row.get("last_evaluation", 0.5),
                    "number_project": row.get("number_project", 3),
                    "average_monthly_hours": row.get("average_monthly_hours", 200),
                    "time_spend_company": row.get("time_spend_company", 3),
                    "work_accident": row.get("work_accident", 0),
                    "promotion_last_5years": row.get("promotion_last_5years", 0),
                    "department": row.get("department", "IT"),
                    "salary": row.get("salary", "medium")
                }
                
                # Make prediction
                prediction = self.ml_service.predict_turnover(employee_data)
                
                # Generate retention strategies
                retention_plan = self.retention_service.generate_retention_strategies(
                    employee_data, 
                    prediction["risk_zone"], 
                    prediction["turnover_probability"]
                )
                
                sample_predictions.append({
                    "employee_data": employee_data,
                    "prediction": prediction,
                    "retention_plan": retention_plan
                })
                
            except Exception as e:
                logger.warning(f"Failed to generate prediction for employee {idx}: {str(e)}")
                continue
        
        return sample_predictions
    
    def _create_data_exports(self, df: pd.DataFrame, predictions: list, training_results: dict) -> dict:
        """Create various data exports."""
        exports = {}
        exports_path = Path(settings.DATA_PATH) / "exports"
        exports_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Export processed data
            processed_file = exports_path / f"processed_data_{timestamp}.csv"
            df.to_csv(processed_file, index=False)
            exports["processed_data"] = str(processed_file)
            
            # Export predictions summary
            predictions_summary = []
            for pred in predictions:
                predictions_summary.append({
                    "employee_id": pred["employee_data"]["employee_id"],
                    "turnover_probability": pred["prediction"]["turnover_probability"],
                    "risk_zone": pred["prediction"]["risk_zone"],
                    "model_used": pred["prediction"]["model_used"],
                    "retention_strategies_count": len(pred["retention_plan"]["strategies"]),
                    "estimated_cost": pred["retention_plan"]["total_estimated_cost"]["total_estimated_cost"]
                })
            
            predictions_df = pd.DataFrame(predictions_summary)
            predictions_file = exports_path / f"predictions_summary_{timestamp}.csv"
            predictions_df.to_csv(predictions_file, index=False)
            exports["predictions_summary"] = str(predictions_file)
            
            # Export risk distribution
            risk_distribution = predictions_df["risk_zone"].value_counts().to_dict()
            risk_file = exports_path / f"risk_distribution_{timestamp}.json"
            import json
            with open(risk_file, 'w') as f:
                json.dump(risk_distribution, f, indent=2)
            exports["risk_distribution"] = str(risk_file)
            
            # Export model performance
            model_performance = training_results.get("models_performance", {})
            performance_file = exports_path / f"model_performance_{timestamp}.json"
            with open(performance_file, 'w') as f:
                json.dump(model_performance, f, indent=2)
            exports["model_performance"] = str(performance_file)
            
            logger.info(f"Created {len(exports)} data exports")
            return exports
            
        except Exception as e:
            logger.error(f"Error creating data exports: {str(e)}")
            return {}
    
    def _save_pipeline_summary(self, summary: dict, output_prefix: str):
        """Save pipeline summary to file."""
        try:
            summary_file = Path(settings.DATA_PATH) / "logs" / f"pipeline_summary_{output_prefix}.json"
            import json
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"Pipeline summary saved: {summary_file}")
        except Exception as e:
            logger.error(f"Error saving pipeline summary: {str(e)}")
    
    def run_data_processing_only(self, input_file: str, output_file: str = None) -> dict:
        """Run only the data processing pipeline."""
        try:
            logger.info("Running data processing pipeline only")
            return self.data_service.process_data_pipeline(input_file, output_file)
        except Exception as e:
            logger.error(f"Data processing pipeline failed: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    def run_ml_training_only(self, processed_file: str) -> dict:
        """Run only the ML training pipeline."""
        try:
            logger.info("Running ML training pipeline only")
            df = pd.read_csv(processed_file)
            X, y, feature_columns = self.data_service.prepare_ml_data(df)
            return self.ml_service.train_models(X, y)
        except Exception as e:
            logger.error(f"ML training pipeline failed: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    def validate_data_quality(self, input_file: str) -> dict:
        """Validate data quality without processing."""
        try:
            logger.info("Validating data quality")
            df = self.data_service.load_raw_data(input_file)
            return self.data_service.validate_data_quality(df)
        except Exception as e:
            logger.error(f"Data quality validation failed: {str(e)}")
            return {"status": "failed", "error": str(e)}


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description="Employee Turnover ETL Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Input data file")
    parser.add_argument("--output", "-o", help="Output file prefix")
    parser.add_argument("--mode", "-m", choices=["complete", "data_only", "ml_only", "validate"], 
                       default="complete", help="Pipeline mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize pipeline
    pipeline = ETLPipeline()
    
    try:
        if args.mode == "complete":
            results = pipeline.run_complete_pipeline(args.input, args.output)
        elif args.mode == "data_only":
            results = pipeline.run_data_processing_only(args.input, args.output)
        elif args.mode == "ml_only":
            results = pipeline.run_ml_training_only(args.input)
        elif args.mode == "validate":
            results = pipeline.validate_data_quality(args.input)
        
        # Print results summary
        print("\n" + "="*60)
        print("ETL PIPELINE RESULTS")
        print("="*60)
        print(f"Status: {results.get('status', 'unknown')}")
        
        if results.get("status") == "success":
            print(f"Duration: {results.get('pipeline_duration_seconds', 0):.2f} seconds")
            print(f"Input file: {results.get('input_file', 'N/A')}")
            
            if "processing_results" in results:
                print(f"Data shape: {results['processing_results'].get('data_shape', 'N/A')}")
            
            if "training_results" in results:
                best_model = results["training_results"].get("best_model", "N/A")
                best_score = results["training_results"].get("best_score", 0)
                print(f"Best model: {best_model} (AUC: {best_score:.3f})")
            
            if "exports_created" in results:
                print(f"Exports created: {len(results['exports_created'])}")
        else:
            print(f"Error: {results.get('error', 'Unknown error')}")
        
        print("="*60)
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        print(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
