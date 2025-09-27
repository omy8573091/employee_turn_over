# Data Directory Structure

This directory contains all data-related files for the Employee Turnover Prediction system.

## Directory Structure

- **raw/**: Original, unprocessed data files
  - Contains source data files (CSV, Excel, etc.)
  - Should not be modified after initial import
  
- **processed/**: Cleaned and preprocessed data
  - Contains data after cleaning, transformation, and feature engineering
  - Ready for model training and analysis
  
- **models/**: Trained ML models and artifacts
  - Serialized model files (.pkl, .joblib)
  - Model metadata and performance metrics
  - Model versioning information
  
- **exports/**: Generated reports and visualizations
  - Analysis reports
  - Charts and graphs
  - Export files for external use
  
- **logs/**: Data processing logs
  - ETL pipeline logs
  - Data validation logs
  - Error logs

## Data Pipeline

1. Raw data is placed in `raw/` directory
2. Data processing scripts clean and transform data into `processed/`
3. Models are trained and saved to `models/`
4. Results and reports are exported to `exports/`
5. All operations are logged in `logs/`

## File Naming Conventions

- Use descriptive names with timestamps
- Include version numbers for model files
- Use consistent date formats (YYYY-MM-DD)
- Include data source in filename when applicable
