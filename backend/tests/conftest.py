"""
Pytest configuration and fixtures for testing.
"""
import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database.session import Base, get_db
from app.core.config.settings import Settings

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_settings():
    """Test settings fixture."""
    return Settings(
        DATABASE_URL=TEST_DATABASE_URL,
        SECRET_KEY="test-secret-key",
        DEBUG=True,
        LOG_LEVEL="DEBUG"
    )


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_employee_data():
    """Sample employee data for testing."""
    return {
        "employee_id": "EMP001",
        "satisfaction_level": 0.7,
        "last_evaluation": 0.8,
        "number_project": 4,
        "average_monthly_hours": 200,
        "time_spend_company": 3,
        "work_accident": 0,
        "left": 0,
        "promotion_last_5years": 0,
        "department": "IT",
        "salary": "medium"
    }


@pytest.fixture
def sample_prediction_data():
    """Sample prediction data for testing."""
    return {
        "satisfaction_level": 0.7,
        "last_evaluation": 0.8,
        "number_project": 4,
        "average_monthly_hours": 200,
        "time_spend_company": 3,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "IT",
        "salary": "medium",
        "model_name": "test_model"
    }


@pytest.fixture
def auth_headers():
    """Mock authentication headers for testing."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"test data")
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Cleanup
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
