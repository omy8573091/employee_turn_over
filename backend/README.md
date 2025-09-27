# Employee Turnover Prediction API

A production-ready FastAPI application for predicting employee turnover and providing retention strategies.

## Features

- **Employee Management**: CRUD operations for employee data
- **ML Predictions**: Turnover probability prediction using machine learning
- **Risk Assessment**: Categorize employees into risk zones (Low, Medium, High, Critical)
- **Retention Strategies**: Automated recommendations based on risk levels
- **Analytics**: Comprehensive statistics and reporting
- **RESTful API**: Well-documented API with OpenAPI/Swagger documentation
- **Authentication**: JWT-based authentication system
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Testing**: Comprehensive test suite with unit and integration tests
- **Docker**: Containerized deployment ready

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
backend/
├── app/
│   ├── api/                    # API layer
│   │   ├── v1/                # API version 1
│   │   │   └── endpoints/     # API endpoints
│   │   ├── deps.py            # Dependency injection
│   │   └── exception_handlers.py
│   ├── core/                  # Core functionality
│   │   ├── config/           # Configuration management
│   │   ├── database/         # Database configuration
│   │   └── security/         # Security utilities
│   ├── models/               # Database models
│   ├── repositories/         # Data access layer
│   ├── services/             # Business logic layer
│   ├── utils/                # Utility functions
│   ├── middleware/           # Custom middleware
│   └── exceptions/           # Custom exceptions
├── migrations/               # Database migrations
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test fixtures
└── requirements.txt         # Dependencies
```

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee_turn_over/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.production.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb employee_turnover
   
   # Run migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   python -m app.main
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/v1/openapi.json`

## Configuration

The application uses environment variables for configuration. Key settings:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

See `env.production.example` for all available configuration options.

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=app tests/
```

## Database Migrations

The application uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t employee-turnover-api .

# Run the container
docker run -p 8000:8000 --env-file .env employee-turnover-api
```

## API Endpoints

### Employees
- `GET /api/v1/employees/` - List employees
- `POST /api/v1/employees/` - Create employee
- `GET /api/v1/employees/{id}` - Get employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Predictions
- `POST /api/v1/employees/{id}/predict` - Predict turnover
- `GET /api/v1/employees/{id}/predictions` - Get predictions
- `GET /api/v1/predictions/` - List all predictions

### Analytics
- `GET /api/v1/analytics/statistics` - Get statistics
- `GET /api/v1/analytics/risk-distribution` - Risk distribution

### Retention
- `GET /api/v1/employees/{id}/retention-strategies` - Get strategies

## Data Models

### Employee
- Basic employee information
- Performance metrics
- Employment history

### Prediction
- ML model predictions
- Risk zone classification
- Prediction metadata

### Retention Strategy
- Recommended actions
- Implementation status
- Assignment tracking

## Machine Learning

The application includes a machine learning pipeline for turnover prediction:

1. **Feature Engineering**: Transform employee data into ML features
2. **Model Training**: Train models on historical data
3. **Prediction**: Generate turnover probabilities
4. **Risk Classification**: Categorize employees by risk level

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation
- SQL injection prevention

## Monitoring

- Structured logging
- Health check endpoints
- Performance metrics
- Error tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
