# Employee Turnover Analytics Platform

A comprehensive production-grade application for predicting and analyzing employee turnover using machine learning. Built with FastAPI, Next.js, and modern ML techniques.

## 🚀 Features

### Core Analytics
- **Data Quality Check**: Comprehensive validation and missing value analysis
- **Exploratory Data Analysis (EDA)**: Correlation matrices, distribution plots, and statistical insights
- **Clustering Analysis**: KMeans clustering of departing employees based on satisfaction and evaluation
- **Class Imbalance Handling**: SMOTE technique for balanced model training
- **Model Training**: Multiple ML models with 5-fold cross-validation
- **Performance Evaluation**: ROC/AUC curves, confusion matrices, and comprehensive metrics
- **Retention Strategies**: Risk-based recommendations for employee retention

### Production Features
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Modern Frontend**: Next.js with TypeScript and Tailwind CSS
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based user authentication and authorization
- **Real-time Dashboard**: Interactive charts and analytics
- **Docker Support**: Containerized deployment
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 ML Models

The platform implements three machine learning models:

1. **Logistic Regression**: Baseline model for binary classification
2. **Random Forest**: Ensemble method for improved accuracy
3. **Gradient Boosting**: Advanced boosting algorithm

### Model Evaluation Metrics
- **Accuracy**: Overall prediction correctness
- **Precision**: True positive rate among predicted positives
- **Recall**: True positive rate among actual positives (prioritized for HR use case)
- **F1-Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under the receiver operating characteristic curve

## 🎯 Risk Zones

Employees are categorized into four risk zones based on turnover probability:

- **🟢 Safe Zone (Green)**: < 20% turnover probability
- **🟡 Low Risk Zone (Yellow)**: 20-60% turnover probability
- **🟠 Medium Risk Zone (Orange)**: 60-90% turnover probability
- **🔴 High Risk Zone (Red)**: > 90% turnover probability

## 🛠️ Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee_turn_over
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
employee_turn_over/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── ml_models.py    # ML model implementations
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and API client
│   │   └── types/        # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── notebooks/             # Jupyter notebooks for analysis
├── data/                 # Data files
├── models/              # Trained ML models
├── tests/               # Test suites
├── docs/                # Documentation
├── docker-compose.yml   # Docker orchestration
└── README.md
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/employee_turnover
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 📊 Data Schema

### Employee Data
- `satisfaction_level`: Employee satisfaction (0-1)
- `last_evaluation`: Last performance evaluation (0-1)
- `number_project`: Number of projects worked on
- `average_monthly_hours`: Average monthly working hours
- `time_spend_company`: Years spent in company
- `work_accident`: Work accident history (0/1)
- `left`: Turnover status (0/1)
- `promotion_last_5years`: Promotions in last 5 years
- `department`: Department name
- `salary`: Salary level (low/medium/high)

## 🔐 Authentication

The platform uses JWT-based authentication:

1. **Register**: Create a new user account
2. **Login**: Authenticate with username/password
3. **Access Token**: JWT token for API requests
4. **Authorization**: Role-based access control

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

## 📈 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard summary
- `GET /api/v1/analytics/risk-distribution` - Risk zone distribution
- `GET /api/v1/analytics/turnover-by-department` - Department analysis
- `GET /api/v1/analytics/clustering-analysis` - Clustering results

### Predictions
- `POST /api/v1/predictions/predict` - Predict turnover
- `GET /api/v1/predictions/high-risk-employees` - High risk employees
- `GET /api/v1/predictions/model-performance` - Model metrics

### Admin
- `POST /api/v1/admin/upload-employees` - Upload employee data
- `POST /api/v1/admin/train-models` - Train ML models
- `GET /api/v1/admin/users` - User management

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Build and deploy with Docker**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up reverse proxy** (nginx/traefik) for SSL termination
4. **Configure monitoring** and logging
5. **Set up database backups**

### Cloud Deployment Options
- **AWS**: ECS, RDS, CloudFront
- **Google Cloud**: Cloud Run, Cloud SQL, Cloud CDN
- **Azure**: Container Instances, SQL Database, CDN
- **DigitalOcean**: App Platform, Managed Databases

## 📊 Monitoring & Logging

### Health Checks
- Backend: `GET /health`
- Frontend: Built-in Next.js health checks
- Database: Connection monitoring

### Logging
- Application logs via Python logging
- Access logs via uvicorn
- Error tracking and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## 🔮 Future Enhancements

- [ ] Real-time notifications for high-risk employees
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Employee sentiment analysis
- [ ] Integration with HR systems
- [ ] Mobile application
- [ ] Advanced reporting and exports
- [ ] Multi-tenant support
- [ ] Advanced analytics and forecasting
