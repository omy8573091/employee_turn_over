import logging
import logging.config
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration for the application"""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}',
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": f"logs/error_{datetime.now().strftime('%Y%m%d')}.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": f"logs/access_{datetime.now().strftime('%Y%m%d')}.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "app": {
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["access_file"],
                "propagate": False
            },
            "sqlalchemy": {
                "level": "WARNING",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "fastapi": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(logging_config)
    
    # Get logger
    logger = logging.getLogger("app")
    logger.info("Logging configuration initialized")
    
    return logger

class RequestLogger:
    """Custom logger for request/response logging"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.requests")
    
    def log_request(self, request_id: str, method: str, path: str, client_ip: str):
        """Log incoming request"""
        self.logger.info(
            f"Request {request_id}: {method} {path} from {client_ip}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "client_ip": client_ip,
                "event_type": "request"
            }
        )
    
    def log_response(self, request_id: str, status_code: int, process_time: float):
        """Log response"""
        self.logger.info(
            f"Response {request_id}: {status_code} in {process_time:.3f}s",
            extra={
                "request_id": request_id,
                "status_code": status_code,
                "process_time": process_time,
                "event_type": "response"
            }
        )
    
    def log_error(self, request_id: str, error: str, process_time: float):
        """Log error"""
        self.logger.error(
            f"Error {request_id}: {error} in {process_time:.3f}s",
            extra={
                "request_id": request_id,
                "error": error,
                "process_time": process_time,
                "event_type": "error"
            }
        )

class MLModelLogger:
    """Custom logger for ML model operations"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.ml_models")
    
    def log_model_training(self, model_name: str, accuracy: float, f1_score: float, auc: float):
        """Log model training results"""
        self.logger.info(
            f"Model {model_name} trained - Accuracy: {accuracy:.3f}, F1: {f1_score:.3f}, AUC: {auc:.3f}",
            extra={
                "model_name": model_name,
                "accuracy": accuracy,
                "f1_score": f1_score,
                "auc": auc,
                "event_type": "model_training"
            }
        )
    
    def log_prediction(self, employee_id: int, probability: float, risk_zone: str, model_used: str):
        """Log prediction made"""
        self.logger.info(
            f"Prediction for employee {employee_id}: {probability:.3f} ({risk_zone}) using {model_used}",
            extra={
                "employee_id": employee_id,
                "probability": probability,
                "risk_zone": risk_zone,
                "model_used": model_used,
                "event_type": "prediction"
            }
        )
    
    def log_model_error(self, model_name: str, error: str):
        """Log model error"""
        self.logger.error(
            f"Model {model_name} error: {error}",
            extra={
                "model_name": model_name,
                "error": error,
                "event_type": "model_error"
            }
        )

class DatabaseLogger:
    """Custom logger for database operations"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.database")
    
    def log_query(self, query: str, execution_time: float):
        """Log database query"""
        self.logger.debug(
            f"Query executed in {execution_time:.3f}s: {query[:100]}...",
            extra={
                "query": query,
                "execution_time": execution_time,
                "event_type": "database_query"
            }
        )
    
    def log_connection_error(self, error: str):
        """Log database connection error"""
        self.logger.error(
            f"Database connection error: {error}",
            extra={
                "error": error,
                "event_type": "database_error"
            }
        )

# Initialize loggers
request_logger = RequestLogger()
ml_logger = MLModelLogger()
db_logger = DatabaseLogger()
